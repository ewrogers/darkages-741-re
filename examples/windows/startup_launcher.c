#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0600

#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <bcrypt.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#if defined(_MSC_VER)
#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "ws2_32.lib")
#endif

#define TARGET_SIZE 3112960ULL
#define MAX_PATCH_SIZE 10U

typedef struct memory_patch {
    const wchar_t *name;
    uintptr_t rva;
    size_t size;
    unsigned char expected[MAX_PATCH_SIZE];
    unsigned char replacement[MAX_PATCH_SIZE];
} memory_patch;

static const unsigned char target_sha256[32] = {
    0x05, 0x4a, 0x5d, 0x6a, 0xdc, 0x56, 0x09, 0x9c,
    0x6b, 0xfd, 0x9d, 0x2a, 0x58, 0x67, 0x5a, 0xff,
    0x62, 0xdc, 0x78, 0x8b, 0x63, 0x20, 0x9a, 0x3d,
    0x90, 0x64, 0x92, 0xf5, 0xb8, 0x9e, 0x96, 0xc6
};

static const memory_patch skip_intro_patch = {
    L"skip intro videos",
    (uintptr_t)0x000aca85,
    2U,
    {0x6a, 0x01},
    {0x6a, 0x02}
};

static const memory_patch allow_multiple_clients_patch = {
    L"allow multiple clients",
    (uintptr_t)0x0017a7d9,
    2U,
    {0x75, 0x07},
    {0xeb, 0x07}
};

static const memory_patch command_line_endpoint_patch = {
    L"enable command-line endpoint",
    (uintptr_t)0x00032253,
    5U,
    {0xe8, 0x28, 0x11, 0x00, 0x00},
    {0xe8, 0xb8, 0x0d, 0x00, 0x00}
};

static const memory_patch disable_official_fallback_patch = {
    L"disable official endpoint fallback",
    (uintptr_t)0x001655f4,
    10U,
    {0xc7, 0x85, 0x94, 0xfb, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00},
    {0xe9, 0x06, 0x13, 0x00, 0x00, 0x90, 0x90, 0x90, 0x90, 0x90}
};

static void print_win32_error(const wchar_t *operation)
{
    fwprintf(stderr, L"%ls failed with Win32 error %lu\n",
             operation, (unsigned long)GetLastError());
}

static int parse_tcp_port(const wchar_t *text, uint16_t *port)
{
    wchar_t *end = NULL;
    unsigned long value;

    if (text == NULL || *text == L'\0') {
        return 0;
    }

    errno = 0;
    value = wcstoul(text, &end, 10);
    if (errno == ERANGE || end == text || *end != L'\0' ||
        value == 0 || value > 65535UL) {
        return 0;
    }

    *port = (uint16_t)value;
    return 1;
}

static int resolve_ipv4(
    const wchar_t *host,
    wchar_t output[INET_ADDRSTRLEN])
{
    WSADATA wsa_data;
    ADDRINFOW hints;
    PADDRINFOW addresses = NULL;
    PADDRINFOW current;
    int result;
    int ok = 0;

    result = WSAStartup(MAKEWORD(2, 2), &wsa_data);
    if (result != 0) {
        fwprintf(stderr, L"WSAStartup failed with Winsock error %d\n", result);
        return 0;
    }

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    result = GetAddrInfoW(host, NULL, &hints, &addresses);
    if (result != 0) {
        fwprintf(stderr,
                 L"Unable to resolve %ls to IPv4: Winsock error %d\n",
                 host, result);
        goto cleanup;
    }

    for (current = addresses; current != NULL; current = current->ai_next) {
        SOCKADDR_IN *address;

        if (current->ai_family != AF_INET ||
            current->ai_addrlen < sizeof(SOCKADDR_IN)) {
            continue;
        }

        address = (SOCKADDR_IN *)current->ai_addr;
        if (InetNtopW(
                AF_INET,
                &address->sin_addr,
                output,
                INET_ADDRSTRLEN) != NULL) {
            ok = 1;
            break;
        }
    }

    if (!ok) {
        fwprintf(stderr, L"No IPv4 address was found for %ls\n", host);
    }

cleanup:
    if (addresses != NULL) {
        FreeAddrInfoW(addresses);
    }
    WSACleanup();
    return ok;
}

static int hash_target_file(
    const wchar_t *path,
    unsigned char digest[32],
    uint64_t *file_size)
{
    HANDLE file = INVALID_HANDLE_VALUE;
    BCRYPT_ALG_HANDLE algorithm = NULL;
    BCRYPT_HASH_HANDLE hash = NULL;
    unsigned char *hash_object = NULL;
    unsigned char buffer[64 * 1024];
    LARGE_INTEGER size;
    DWORD object_size = 0;
    DWORD hash_size = 0;
    DWORD result_size = 0;
    DWORD bytes_read = 0;
    NTSTATUS status;
    int ok = 0;

    file = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL,
                       OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE) {
        print_win32_error(L"CreateFileW");
        goto cleanup;
    }

    if (!GetFileSizeEx(file, &size)) {
        print_win32_error(L"GetFileSizeEx");
        goto cleanup;
    }
    *file_size = (uint64_t)size.QuadPart;

    status = BCryptOpenAlgorithmProvider(
        &algorithm, BCRYPT_SHA256_ALGORITHM, NULL, 0);
    if (status < 0) {
        fwprintf(stderr, L"BCryptOpenAlgorithmProvider failed: 0x%08lx\n",
                 (unsigned long)status);
        goto cleanup;
    }

    status = BCryptGetProperty(
        algorithm, BCRYPT_OBJECT_LENGTH,
        (PUCHAR)&object_size, sizeof(object_size), &result_size, 0);
    if (status < 0) {
        fwprintf(stderr, L"BCryptGetProperty(object length) failed: 0x%08lx\n",
                 (unsigned long)status);
        goto cleanup;
    }

    status = BCryptGetProperty(
        algorithm, BCRYPT_HASH_LENGTH,
        (PUCHAR)&hash_size, sizeof(hash_size), &result_size, 0);
    if (status < 0 || hash_size != 32) {
        fwprintf(stderr, L"unexpected SHA-256 hash length\n");
        goto cleanup;
    }

    hash_object = (unsigned char *)HeapAlloc(
        GetProcessHeap(), 0, object_size);
    if (hash_object == NULL) {
        fwprintf(stderr, L"unable to allocate the hash object\n");
        goto cleanup;
    }

    status = BCryptCreateHash(
        algorithm, &hash, hash_object, object_size, NULL, 0, 0);
    if (status < 0) {
        fwprintf(stderr, L"BCryptCreateHash failed: 0x%08lx\n",
                 (unsigned long)status);
        goto cleanup;
    }

    for (;;) {
        if (!ReadFile(file, buffer, sizeof(buffer), &bytes_read, NULL)) {
            print_win32_error(L"ReadFile");
            goto cleanup;
        }
        if (bytes_read == 0) {
            break;
        }

        status = BCryptHashData(hash, buffer, bytes_read, 0);
        if (status < 0) {
            fwprintf(stderr, L"BCryptHashData failed: 0x%08lx\n",
                     (unsigned long)status);
            goto cleanup;
        }
    }

    status = BCryptFinishHash(hash, digest, 32, 0);
    if (status < 0) {
        fwprintf(stderr, L"BCryptFinishHash failed: 0x%08lx\n",
                 (unsigned long)status);
        goto cleanup;
    }

    ok = 1;

cleanup:
    if (hash != NULL) {
        BCryptDestroyHash(hash);
    }
    if (hash_object != NULL) {
        HeapFree(GetProcessHeap(), 0, hash_object);
    }
    if (algorithm != NULL) {
        BCryptCloseAlgorithmProvider(algorithm, 0);
    }
    if (file != INVALID_HANDLE_VALUE) {
        CloseHandle(file);
    }
    return ok;
}

static int verify_target(const wchar_t *path)
{
    unsigned char digest[32];
    uint64_t file_size = 0;

    if (!hash_target_file(path, digest, &file_size)) {
        return 0;
    }
    if (file_size != TARGET_SIZE) {
        fwprintf(stderr,
                 L"target size mismatch: expected %llu, found %llu\n",
                 (unsigned long long)TARGET_SIZE,
                 (unsigned long long)file_size);
        return 0;
    }
    if (memcmp(digest, target_sha256, sizeof(target_sha256)) != 0) {
        fwprintf(stderr, L"target SHA-256 does not match Darkages.exe 741\n");
        return 0;
    }

    return 1;
}

static int get_suspended_image_base(
    HANDLE process,
    HANDLE thread,
    uintptr_t *image_base)
{
    DWORD peb_address;
    DWORD image_base_32;
    SIZE_T bytes_read = 0;

#if defined(_WIN64)
    BOOL is_wow64 = FALSE;
    WOW64_CONTEXT context;

    if (!IsWow64Process(process, &is_wow64)) {
        print_win32_error(L"IsWow64Process");
        return 0;
    }
    if (!is_wow64) {
        fwprintf(stderr, L"the target process is not 32-bit x86\n");
        return 0;
    }

    memset(&context, 0, sizeof(context));
    context.ContextFlags = WOW64_CONTEXT_INTEGER;
    if (!Wow64GetThreadContext(thread, &context)) {
        print_win32_error(L"Wow64GetThreadContext");
        return 0;
    }
    peb_address = context.Ebx;
#else
    CONTEXT context;

    memset(&context, 0, sizeof(context));
    context.ContextFlags = CONTEXT_INTEGER;
    if (!GetThreadContext(thread, &context)) {
        print_win32_error(L"GetThreadContext");
        return 0;
    }
    peb_address = context.Ebx;
#endif

    if (!ReadProcessMemory(
            process,
            (LPCVOID)(uintptr_t)(peb_address + 8U),
            &image_base_32,
            sizeof(image_base_32),
            &bytes_read) ||
        bytes_read != sizeof(image_base_32)) {
        print_win32_error(L"ReadProcessMemory(PEB.ImageBaseAddress)");
        return 0;
    }

    *image_base = (uintptr_t)image_base_32;
    return 1;
}

static int apply_memory_patch(
    HANDLE process,
    uintptr_t image_base,
    const memory_patch *patch)
{
    unsigned char actual[MAX_PATCH_SIZE];
    uintptr_t address = image_base + patch->rva;
    SIZE_T transferred = 0;
    DWORD old_protection = 0;
    DWORD unused_protection = 0;
    DWORD failure = ERROR_SUCCESS;
    size_t index;

    if (patch->size == 0 || patch->size > MAX_PATCH_SIZE) {
        fwprintf(stderr, L"Invalid patch size for %ls\n", patch->name);
        return 0;
    }

    if (!ReadProcessMemory(
            process, (LPCVOID)address,
            actual, patch->size, &transferred) ||
        transferred != patch->size) {
        print_win32_error(L"ReadProcessMemory(patch verification)");
        return 0;
    }

    if (memcmp(actual, patch->expected, patch->size) != 0) {
        fwprintf(stderr,
                 L"%ls verification failed at %p: found",
                 patch->name,
                 (void *)address);
        for (index = 0; index < patch->size; ++index) {
            fwprintf(stderr, L" %02x", (unsigned int)actual[index]);
        }
        fputwc(L'\n', stderr);
        return 0;
    }

    if (!VirtualProtectEx(
            process, (LPVOID)address, patch->size,
            PAGE_EXECUTE_READWRITE, &old_protection)) {
        print_win32_error(L"VirtualProtectEx(enable write)");
        return 0;
    }

    transferred = 0;
    if (!WriteProcessMemory(
            process, (LPVOID)address,
            patch->replacement, patch->size, &transferred) ||
        transferred != patch->size) {
        failure = GetLastError();
    } else if (!FlushInstructionCache(
                   process, (LPCVOID)address, patch->size)) {
        failure = GetLastError();
    }

    if (!VirtualProtectEx(
            process, (LPVOID)address, patch->size,
            old_protection, &unused_protection) &&
        failure == ERROR_SUCCESS) {
        failure = GetLastError();
    }

    if (failure != ERROR_SUCCESS) {
        SetLastError(failure);
        print_win32_error(L"apply memory patch");
        return 0;
    }

    transferred = 0;
    if (!ReadProcessMemory(
            process, (LPCVOID)address,
            actual, patch->size, &transferred) ||
        transferred != patch->size ||
        memcmp(actual, patch->replacement, patch->size) != 0) {
        fwprintf(stderr, L"%ls write verification failed at %p\n",
                 patch->name, (void *)address);
        return 0;
    }

    wprintf(L"Applied %ls at %p\n", patch->name, (void *)address);
    return 1;
}

static wchar_t *duplicate_wide_string(const wchar_t *value)
{
    size_t count = wcslen(value) + 1;
    wchar_t *copy = (wchar_t *)malloc(count * sizeof(wchar_t));

    if (copy != NULL) {
        memcpy(copy, value, count * sizeof(wchar_t));
    }
    return copy;
}

static wchar_t *get_full_path(const wchar_t *path)
{
    DWORD count = GetFullPathNameW(path, 0, NULL, NULL);
    wchar_t *full_path;

    if (count == 0) {
        return NULL;
    }

    full_path = (wchar_t *)calloc((size_t)count, sizeof(wchar_t));
    if (full_path == NULL) {
        return NULL;
    }

    if (GetFullPathNameW(path, count, full_path, NULL) == 0) {
        free(full_path);
        return NULL;
    }
    return full_path;
}

static wchar_t *get_parent_directory(const wchar_t *full_path)
{
    wchar_t *directory = duplicate_wide_string(full_path);
    wchar_t *backslash;
    wchar_t *slash;
    wchar_t *separator;

    if (directory == NULL) {
        return NULL;
    }

    backslash = wcsrchr(directory, L'\\');
    slash = wcsrchr(directory, L'/');
    separator = backslash;
    if (separator == NULL || (slash != NULL && slash > separator)) {
        separator = slash;
    }

    if (separator == NULL) {
        free(directory);
        return NULL;
    }

    if (separator == directory + 2 && directory[1] == L':') {
        separator[1] = L'\0';
    } else {
        *separator = L'\0';
    }
    return directory;
}

static wchar_t *make_command_line(
    const wchar_t *full_path,
    const wchar_t *server_ipv4,
    uint16_t server_port)
{
    wchar_t port_text[6];
    size_t path_length = wcslen(full_path);
    size_t server_length = 0;
    size_t port_length = 0;
    size_t count = path_length + 3;
    wchar_t *command_line;
    wchar_t *cursor;

    if (server_ipv4 != NULL) {
        if (swprintf(
                port_text,
                sizeof(port_text) / sizeof(port_text[0]),
                L"%u",
                (unsigned int)server_port) < 0) {
            return NULL;
        }
        server_length = wcslen(server_ipv4);
        port_length = wcslen(port_text);
        count += server_length + port_length + 2;
    }

    command_line = (wchar_t *)calloc(count, sizeof(wchar_t));

    if (command_line == NULL) {
        return NULL;
    }

    cursor = command_line;
    *cursor++ = L'"';
    memcpy(cursor, full_path, path_length * sizeof(wchar_t));
    cursor += path_length;
    *cursor++ = L'"';

    if (server_ipv4 != NULL) {
        *cursor++ = L' ';
        memcpy(cursor, server_ipv4, server_length * sizeof(wchar_t));
        cursor += server_length;
        *cursor++ = L' ';
        memcpy(cursor, port_text, port_length * sizeof(wchar_t));
        cursor += port_length;
    }

    *cursor = L'\0';
    return command_line;
}

static void print_usage(const wchar_t *program)
{
    fwprintf(stderr,
             L"Usage: %ls [--multi] [--skip-intro] "
             L"[--server HOST --port PORT [--no-fallback]] "
             L"<Darkages.exe>\n"
             L"With no startup patch flags, multi-client and intro-skip "
             L"are both applied.\n",
             program);
}

int wmain(int argc, wchar_t **argv)
{
    int allow_multiple = 0;
    int skip_intro = 0;
    int disable_official_fallback = 0;
    int saw_patch_flag = 0;
    int index = 1;
    int exit_code = 1;
    const wchar_t *server_host = NULL;
    uint16_t server_port = 0;
    wchar_t server_ipv4[INET_ADDRSTRLEN];
    wchar_t *full_path = NULL;
    wchar_t *working_directory = NULL;
    wchar_t *command_line = NULL;
    STARTUPINFOW startup_info;
    PROCESS_INFORMATION process_info;
    uintptr_t image_base = 0;

    while (index < argc && wcsncmp(argv[index], L"--", 2) == 0) {
        if (wcscmp(argv[index], L"--multi") == 0) {
            allow_multiple = 1;
            saw_patch_flag = 1;
        } else if (wcscmp(argv[index], L"--skip-intro") == 0) {
            skip_intro = 1;
            saw_patch_flag = 1;
        } else if (wcscmp(argv[index], L"--no-fallback") == 0) {
            disable_official_fallback = 1;
        } else if (wcscmp(argv[index], L"--server") == 0) {
            if (index + 1 >= argc) {
                fwprintf(stderr, L"--server requires a hostname or IPv4 address\n");
                return 2;
            }
            server_host = argv[index + 1];
            index += 2;
            continue;
        } else if (wcscmp(argv[index], L"--port") == 0) {
            if (index + 1 >= argc ||
                !parse_tcp_port(argv[index + 1], &server_port)) {
                fwprintf(stderr, L"--port requires a value from 1 through 65535\n");
                return 2;
            }
            index += 2;
            continue;
        } else if (wcscmp(argv[index], L"--help") == 0) {
            print_usage(argv[0]);
            return 0;
        } else {
            fwprintf(stderr, L"Unknown option: %ls\n", argv[index]);
            print_usage(argv[0]);
            return 2;
        }
        ++index;
    }

    if (index + 1 != argc) {
        print_usage(argv[0]);
        return 2;
    }
    if ((server_host == NULL && server_port != 0) ||
        (server_host != NULL && server_port == 0)) {
        fwprintf(stderr, L"--server and --port must be supplied together\n");
        return 2;
    }
    if (disable_official_fallback && server_host == NULL) {
        fwprintf(stderr,
                 L"--no-fallback requires --server and --port\n");
        return 2;
    }
    if (!saw_patch_flag) {
        allow_multiple = 1;
        skip_intro = 1;
    }

    full_path = get_full_path(argv[index]);
    if (full_path == NULL) {
        print_win32_error(L"GetFullPathNameW");
        goto cleanup;
    }
    working_directory = get_parent_directory(full_path);
    if (working_directory == NULL) {
        fwprintf(stderr, L"unable to prepare the client path\n");
        goto cleanup;
    }

    if (!verify_target(full_path)) {
        goto cleanup;
    }

    server_ipv4[0] = L'\0';
    if (server_host != NULL) {
        if (!resolve_ipv4(server_host, server_ipv4)) {
            goto cleanup;
        }
        wprintf(L"Resolved endpoint %ls:%u to %ls:%u\n",
                server_host,
                (unsigned int)server_port,
                server_ipv4,
                (unsigned int)server_port);
    }

    command_line = make_command_line(
        full_path,
        server_host != NULL ? server_ipv4 : NULL,
        server_port);
    if (command_line == NULL) {
        fwprintf(stderr, L"unable to prepare the client command line\n");
        goto cleanup;
    }

    memset(&startup_info, 0, sizeof(startup_info));
    memset(&process_info, 0, sizeof(process_info));
    startup_info.cb = sizeof(startup_info);

    if (!CreateProcessW(
            full_path,
            command_line,
            NULL,
            NULL,
            FALSE,
            CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT,
            NULL,
            working_directory,
            &startup_info,
            &process_info)) {
        print_win32_error(L"CreateProcessW");
        goto cleanup;
    }

    if (!get_suspended_image_base(
            process_info.hProcess, process_info.hThread, &image_base)) {
        goto process_failure;
    }

    if (server_host != NULL &&
        !apply_memory_patch(
            process_info.hProcess,
            image_base,
            &command_line_endpoint_patch)) {
        goto process_failure;
    }
    if (disable_official_fallback &&
        !apply_memory_patch(
            process_info.hProcess,
            image_base,
            &disable_official_fallback_patch)) {
        goto process_failure;
    }
    if (skip_intro &&
        !apply_memory_patch(
            process_info.hProcess, image_base, &skip_intro_patch)) {
        goto process_failure;
    }
    if (allow_multiple &&
        !apply_memory_patch(
            process_info.hProcess,
            image_base,
            &allow_multiple_clients_patch)) {
        goto process_failure;
    }

    if (ResumeThread(process_info.hThread) == (DWORD)-1) {
        print_win32_error(L"ResumeThread");
        goto process_failure;
    }

    CloseHandle(process_info.hThread);
    CloseHandle(process_info.hProcess);
    process_info.hThread = NULL;
    process_info.hProcess = NULL;
    exit_code = 0;
    goto cleanup;

process_failure:
    TerminateProcess(process_info.hProcess, 1);
    WaitForSingleObject(process_info.hProcess, 5000);
    CloseHandle(process_info.hThread);
    CloseHandle(process_info.hProcess);
    process_info.hThread = NULL;
    process_info.hProcess = NULL;

cleanup:
    free(command_line);
    free(working_directory);
    free(full_path);
    return exit_code;
}
