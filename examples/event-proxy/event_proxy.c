#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "detour_backend.h"
#include "proxy_protocol.h"

#if !defined(_M_IX86)
#error This example must be built for 32-bit x86.
#endif

#ifndef PIPE_REJECT_REMOTE_CLIENTS
#define PIPE_REJECT_REMOTE_CLIENTS 0x00000008
#endif

#define PROXY_COMMAND_CAPACITY 64u
#define PROXY_TELEMETRY_CAPACITY 128u
#define PROXY_COMMANDS_PER_TICK 32u

#define RVA_EVENT_DISPATCH 0x000647C0u
#define RVA_EVENT_DISPATCHER_TICK 0x00064180u
#define RVA_INPUT_GET_EVENT_MANAGER 0x00027380u
#define RVA_INPUT_POST_POINTER_MOVE 0x00066C80u
#define RVA_INPUT_POST_LEFT_DOWN 0x00066D10u
#define RVA_INPUT_POST_LEFT_UP 0x00066D50u
#define RVA_INPUT_POST_RIGHT_DOWN 0x00066D80u
#define RVA_INPUT_POST_RIGHT_UP 0x00066DC0u
#define RVA_INPUT_POST_MOUSE_WHEEL 0x00066DF0u
#define RVA_INPUT_POST_KEY_DOWN 0x00066E20u
#define RVA_INPUT_POST_KEY_UP 0x00066E60u
#define RVA_INPUT_POST_CHARACTER 0x00066E90u
#define RVA_INPUT_POST_IME_OPEN_STATUS 0x00066EB0u
#define RVA_INPUT_POST_COMMITTED_TEXT 0x00066ED0u
#define RVA_INPUT_POST_IME_START 0x00066EF0u
#define RVA_INPUT_POST_IME_END 0x00066F30u
#define RVA_INPUT_POST_IME_CANDIDATE_CLOSE 0x00066F80u
#define RVA_NET_POST_SERVER_PACKET 0x00067060u
#define RVA_NET_SOCKET_POINTER 0x0033D958u
#define RVA_NET_SUBMIT_CLIENT_PACKET 0x00163E00u

#define EVENT_SIZE 0xA8u
#define EVENT_TYPE_OFFSET 0x0Cu
#define EVENT_VALUE0_OFFSET 0x10u
#define EVENT_VALUE1_OFFSET 0x14u
#define EVENT_VALUE2_OFFSET 0x18u
#define EVENT_TEXT_OFFSET 0x1Cu
#define EVENT_VALUE3_OFFSET 0x20u
#define EVENT_KEY_RAW_OFFSET 0xA4u
#define EVENT_NETWORK_BODY_OFFSET 0x14u
#define EVENT_NETWORK_LENGTH_OFFSET 0x18u

typedef uint8_t (__thiscall *event_dispatch_fn)(void *self, void *event);
typedef void (__thiscall *event_dispatcher_tick_fn)(void *self);
typedef uint32_t (__thiscall *net_submit_client_packet_fn)(
    void *self,
    const uint8_t *body,
    int16_t length);

typedef void *(__cdecl *input_get_event_manager_fn)(void);
typedef void *(__thiscall *input_post_pointer_move_fn)(
    void *self,
    int32_t x,
    int32_t y,
    uint32_t message_time);
typedef void *(__thiscall *input_post_button_fn)(
    void *self,
    uint32_t message_time);
typedef void *(__thiscall *input_post_mouse_wheel_fn)(
    void *self,
    int32_t wheel_delta,
    uint32_t message_time);
typedef void *(__thiscall *input_post_key_fn)(
    void *self,
    uint8_t scan_code,
    uint32_t composition_active,
    uint32_t message_time,
    uint32_t virtual_key);
typedef void *(__thiscall *input_post_character_fn)(
    void *self,
    uint8_t character,
    uint32_t message_time);
typedef void *(__thiscall *input_post_committed_text_fn)(
    void *self,
    const char *text,
    uint32_t message_time);
typedef void *(__thiscall *input_post_ime_status_fn)(
    void *self,
    uint32_t value,
    uint32_t message_time);
typedef void *(__thiscall *input_post_ime_marker_fn)(
    void *self,
    uint32_t message_time);
typedef void (__thiscall *net_post_server_packet_fn)(
    void *self,
    const uint8_t *body,
    int32_t length);

typedef struct proxy_command_queue {
    CRITICAL_SECTION lock;
    uint32_t head;
    uint32_t tail;
    proxy_wire_message items[PROXY_COMMAND_CAPACITY];
} proxy_command_queue;

typedef struct proxy_telemetry_queue {
    CRITICAL_SECTION lock;
    uint32_t head;
    uint32_t tail;
    proxy_telemetry_payload items[PROXY_TELEMETRY_CAPACITY];
} proxy_telemetry_queue;

static uintptr_t g_module_base;
static volatile LONG g_running;
static volatile LONG g_started;
static HANDLE g_worker_thread;
static DWORD g_injection_tls = TLS_OUT_OF_INDEXES;

static proxy_command_queue g_command_queue;
static proxy_telemetry_queue g_telemetry_queue;

static volatile LONG g_event_rules[0x15];
static volatile LONG g_client_opcode_rules[0x100];
static volatile LONG g_server_opcode_rules[0x100];

static event_dispatch_fn g_original_event_dispatch;
static event_dispatcher_tick_fn g_original_event_dispatcher_tick;
static net_submit_client_packet_fn g_original_net_submit_client_packet;

static input_get_event_manager_fn g_input_get_event_manager;
static input_post_pointer_move_fn g_input_post_pointer_move;
static input_post_button_fn g_input_post_left_down;
static input_post_button_fn g_input_post_left_up;
static input_post_button_fn g_input_post_right_down;
static input_post_button_fn g_input_post_right_up;
static input_post_mouse_wheel_fn g_input_post_mouse_wheel;
static input_post_key_fn g_input_post_key_down;
static input_post_key_fn g_input_post_key_up;
static input_post_character_fn g_input_post_character;
static input_post_ime_status_fn g_input_post_ime_open_status;
static input_post_committed_text_fn g_input_post_committed_text;
static input_post_ime_marker_fn g_input_post_ime_start;
static input_post_ime_marker_fn g_input_post_ime_end;
static input_post_ime_marker_fn g_input_post_ime_candidate_close;
static net_submit_client_packet_fn g_net_submit_client_packet;
static net_post_server_packet_fn g_net_post_server_packet;
static void **g_net_socket_pointer;

static void *proxy_at_rva(uint32_t rva)
{
    return (void *)(g_module_base + (uintptr_t)rva);
}

static uint32_t proxy_read_u32(const uint8_t *p)
{
    uint32_t value;
    memcpy(&value, p, sizeof(value));
    return value;
}

static void *proxy_read_pointer(const uint8_t *p)
{
    void *value;
    memcpy(&value, p, sizeof(value));
    return value;
}

static size_t proxy_bounded_strlen(const char *text, size_t capacity)
{
    size_t length = 0;
    while (length < capacity && text[length] != '\0') {
        ++length;
    }
    return length;
}

static uint32_t proxy_tls_flags(void)
{
    if (g_injection_tls == TLS_OUT_OF_INDEXES) {
        return 0;
    }
    return (uint32_t)(uintptr_t)TlsGetValue(g_injection_tls);
}

static void proxy_set_tls_flags(uint32_t flags)
{
    if (g_injection_tls != TLS_OUT_OF_INDEXES) {
        TlsSetValue(g_injection_tls, (void *)(uintptr_t)flags);
    }
}

static enum proxy_rule_action proxy_rule_read(volatile LONG *rule)
{
    return (enum proxy_rule_action)InterlockedCompareExchange(rule, 0, 0);
}

static enum proxy_rule_action proxy_rule_merge(
    enum proxy_rule_action first,
    enum proxy_rule_action second)
{
    return first > second ? first : second;
}

static void proxy_reset_rules(void)
{
    uint32_t i;
    for (i = 0; i < 0x15; ++i) {
        InterlockedExchange(&g_event_rules[i], PROXY_RULE_ALLOW);
    }
    for (i = 0; i < 0x100; ++i) {
        InterlockedExchange(&g_client_opcode_rules[i], PROXY_RULE_ALLOW);
        InterlockedExchange(&g_server_opcode_rules[i], PROXY_RULE_ALLOW);
    }
}

static int proxy_set_rule(const proxy_rule_payload *rule)
{
    volatile LONG *slot = NULL;

    if (rule->action > PROXY_RULE_BLOCK) {
        return 0;
    }

    if (rule->domain == PROXY_RULE_EVENT_TYPE && rule->selector < 0x15) {
        slot = &g_event_rules[rule->selector];
    } else if (rule->domain == PROXY_RULE_CLIENT_OPCODE) {
        slot = &g_client_opcode_rules[rule->selector];
    } else if (rule->domain == PROXY_RULE_SERVER_OPCODE) {
        slot = &g_server_opcode_rules[rule->selector];
    }

    if (slot == NULL) {
        return 0;
    }

    InterlockedExchange(slot, rule->action);
    return 1;
}

static int proxy_command_push(const proxy_wire_message *message)
{
    uint32_t count;

    EnterCriticalSection(&g_command_queue.lock);
    count = g_command_queue.tail - g_command_queue.head;
    if (count >= PROXY_COMMAND_CAPACITY) {
        LeaveCriticalSection(&g_command_queue.lock);
        return 0;
    }

    g_command_queue.items[g_command_queue.tail % PROXY_COMMAND_CAPACITY] = *message;
    ++g_command_queue.tail;
    LeaveCriticalSection(&g_command_queue.lock);
    return 1;
}

static int proxy_command_pop(proxy_wire_message *message)
{
    if (!TryEnterCriticalSection(&g_command_queue.lock)) {
        return 0;
    }
    if (g_command_queue.head == g_command_queue.tail) {
        LeaveCriticalSection(&g_command_queue.lock);
        return 0;
    }

    *message = g_command_queue.items[g_command_queue.head % PROXY_COMMAND_CAPACITY];
    ++g_command_queue.head;
    LeaveCriticalSection(&g_command_queue.lock);
    return 1;
}

static int proxy_telemetry_push(const proxy_telemetry_payload *telemetry)
{
    uint32_t count;

    if (!TryEnterCriticalSection(&g_telemetry_queue.lock)) {
        return 0;
    }
    count = g_telemetry_queue.tail - g_telemetry_queue.head;
    if (count >= PROXY_TELEMETRY_CAPACITY) {
        LeaveCriticalSection(&g_telemetry_queue.lock);
        return 0;
    }

    g_telemetry_queue.items[g_telemetry_queue.tail % PROXY_TELEMETRY_CAPACITY] = *telemetry;
    ++g_telemetry_queue.tail;
    LeaveCriticalSection(&g_telemetry_queue.lock);
    return 1;
}

static int proxy_telemetry_pop(proxy_telemetry_payload *telemetry)
{
    EnterCriticalSection(&g_telemetry_queue.lock);
    if (g_telemetry_queue.head == g_telemetry_queue.tail) {
        LeaveCriticalSection(&g_telemetry_queue.lock);
        return 0;
    }

    *telemetry = g_telemetry_queue.items[
        g_telemetry_queue.head % PROXY_TELEMETRY_CAPACITY];
    ++g_telemetry_queue.head;
    LeaveCriticalSection(&g_telemetry_queue.lock);
    return 1;
}

static void proxy_publish(
    uint8_t domain,
    uint8_t selector,
    enum proxy_rule_action action,
    uint32_t value0,
    uint32_t value1,
    uint32_t value2,
    uint32_t value3,
    const uint8_t *captured,
    uint32_t original_size)
{
    proxy_telemetry_payload telemetry;
    uint32_t capture_size = original_size;

    memset(&telemetry, 0, sizeof(telemetry));
    telemetry.domain = domain;
    telemetry.selector = selector;
    telemetry.action = (uint8_t)action;
    telemetry.source = (proxy_tls_flags() != 0)
        ? PROXY_SOURCE_INJECTED
        : PROXY_SOURCE_CLIENT;
    telemetry.value0 = value0;
    telemetry.value1 = value1;
    telemetry.value2 = value2;
    telemetry.value3 = value3;
    telemetry.original_size = (uint16_t)(original_size > 0xFFFFu
        ? 0xFFFFu
        : original_size);

    if (capture_size > PROXY_CAPTURE_CAPACITY) {
        capture_size = PROXY_CAPTURE_CAPACITY;
    }
    if (captured != NULL && capture_size != 0) {
        memcpy(telemetry.captured, captured, capture_size);
        telemetry.captured_size = (uint16_t)capture_size;
    }

    proxy_telemetry_push(&telemetry);
}

static uint8_t __fastcall proxy_hook_event_dispatch(
    void *self,
    void *unused_edx,
    void *event)
{
    const uint8_t *bytes = (const uint8_t *)event;
    uint8_t type;
    uint32_t tls_flags;
    enum proxy_rule_action action;
    const uint8_t *capture = NULL;
    uint32_t capture_size = 0;
    uint32_t value0 = 0;
    uint32_t value1 = 0;
    uint32_t value2 = 0;
    uint32_t value3 = 0;
    uint8_t domain = PROXY_RULE_EVENT_TYPE;
    uint8_t selector;

    (void)unused_edx;

    if (event == NULL) {
        return g_original_event_dispatch(self, event);
    }

    type = bytes[EVENT_TYPE_OFFSET];
    selector = type;
    if (type >= 0x15) {
        return g_original_event_dispatch(self, event);
    }

    action = proxy_rule_read(&g_event_rules[type]);

    if (type <= 0x07) {
        value0 = proxy_read_u32(bytes + EVENT_VALUE0_OFFSET);
        value1 = proxy_read_u32(bytes + EVENT_VALUE1_OFFSET);
        value2 = bytes[EVENT_VALUE2_OFFSET];
        value3 = proxy_read_u32(bytes + EVENT_TEXT_OFFSET);
    } else if (type <= 0x0C) {
        value0 = bytes[EVENT_VALUE0_OFFSET];
        value1 = bytes[EVENT_VALUE0_OFFSET + 1];
        value2 = proxy_read_u32(bytes + EVENT_VALUE1_OFFSET);
        value3 = proxy_read_u32(bytes + EVENT_KEY_RAW_OFFSET);
        if (type == 0x0A || type == 0x0B) {
            capture = bytes + EVENT_TEXT_OFFSET;
            capture_size = (uint32_t)proxy_bounded_strlen(
                (const char *)capture,
                PROXY_TEXT_CAPACITY);
        }
    } else if (type <= 0x12) {
        value0 = proxy_read_u32(bytes + EVENT_VALUE0_OFFSET);
        value1 = proxy_read_u32(bytes + EVENT_VALUE1_OFFSET);
        value2 = proxy_read_u32(bytes + EVENT_VALUE2_OFFSET);
        value3 = proxy_read_u32(bytes + EVENT_VALUE3_OFFSET);
    } else if (type == 0x13) {
        const uint8_t *body = (const uint8_t *)proxy_read_pointer(
            bytes + EVENT_NETWORK_BODY_OFFSET);
        uint32_t length = proxy_read_u32(bytes + EVENT_NETWORK_LENGTH_OFFSET);
        value0 = length;
        capture = body;
        capture_size = body != NULL ? length : 0;
        if (body != NULL && length != 0) {
            selector = body[0];
            domain = PROXY_RULE_SERVER_OPCODE;
            action = proxy_rule_merge(
                action,
                proxy_rule_read(&g_server_opcode_rules[selector]));
        }
    }

    tls_flags = proxy_tls_flags();
    if (action != PROXY_RULE_ALLOW || tls_flags != 0) {
        proxy_publish(
            domain,
            selector,
            action,
            value0,
            value1,
            value2,
            value3,
            capture,
            capture_size);
    }

    if (action == PROXY_RULE_BLOCK &&
        (tls_flags & PROXY_FLAG_BYPASS_RULES) == 0) {
        /* Returning consumed preserves cleanup in event_dispatch_immediate. */
        return 1;
    }

    return g_original_event_dispatch(self, event);
}

static uint32_t __fastcall proxy_hook_net_submit_client_packet(
    void *self,
    void *unused_edx,
    const uint8_t *body,
    int16_t length)
{
    uint8_t opcode;
    uint32_t tls_flags;
    enum proxy_rule_action action;

    (void)unused_edx;

    if (body == NULL || length <= 0) {
        return g_original_net_submit_client_packet(self, body, length);
    }

    opcode = body[0];
    action = proxy_rule_read(&g_client_opcode_rules[opcode]);
    tls_flags = proxy_tls_flags();

    if (action != PROXY_RULE_ALLOW || tls_flags != 0) {
        proxy_publish(
            PROXY_RULE_CLIENT_OPCODE,
            opcode,
            action,
            (uint32_t)(uint16_t)length,
            0,
            0,
            0,
            body,
            (uint32_t)(uint16_t)length);
    }

    if (action == PROXY_RULE_BLOCK &&
        (tls_flags & PROXY_FLAG_BYPASS_RULES) == 0) {
        return 0;
    }

    return g_original_net_submit_client_packet(self, body, length);
}

static uint32_t proxy_message_time(uint32_t supplied)
{
    return supplied != 0 ? supplied : GetTickCount();
}

static void proxy_execute_pointer(
    const uint8_t *payload,
    uint32_t payload_size)
{
    const proxy_pointer_payload *pointer;
    void *manager;
    uint32_t time;

    if (payload_size != sizeof(*pointer)) {
        return;
    }
    pointer = (const proxy_pointer_payload *)payload;
    manager = g_input_get_event_manager();
    if (manager == NULL) {
        return;
    }

    time = proxy_message_time(pointer->message_time);
    switch (pointer->action) {
    case PROXY_POINTER_MOVE:
        g_input_post_pointer_move(manager, pointer->x, pointer->y, time);
        break;
    case PROXY_POINTER_LEFT_DOWN:
        g_input_post_left_down(manager, time);
        break;
    case PROXY_POINTER_LEFT_UP:
        g_input_post_left_up(manager, time);
        break;
    case PROXY_POINTER_RIGHT_DOWN:
        g_input_post_right_down(manager, time);
        break;
    case PROXY_POINTER_RIGHT_UP:
        g_input_post_right_up(manager, time);
        break;
    case PROXY_POINTER_WHEEL:
        g_input_post_mouse_wheel(manager, pointer->wheel_delta, time);
        break;
    default:
        break;
    }
}

static void proxy_execute_key(const uint8_t *payload, uint32_t payload_size)
{
    const proxy_key_payload *key;
    void *manager;
    input_post_key_fn post;

    if (payload_size != sizeof(*key)) {
        return;
    }
    key = (const proxy_key_payload *)payload;
    if (key->action > PROXY_KEY_UP) {
        return;
    }

    manager = g_input_get_event_manager();
    if (manager == NULL) {
        return;
    }
    post = key->action == PROXY_KEY_DOWN
        ? g_input_post_key_down
        : g_input_post_key_up;
    post(
        manager,
        key->scan_code,
        key->composition_active,
        proxy_message_time(key->message_time),
        key->virtual_key);
}

static void proxy_execute_text(const uint8_t *payload, uint32_t payload_size)
{
    const proxy_text_payload *text;
    size_t prefix_size = offsetof(proxy_text_payload, bytes);
    char committed[PROXY_TEXT_CAPACITY + 1];
    void *manager;

    if (payload_size < prefix_size) {
        return;
    }
    text = (const proxy_text_payload *)payload;
    if (text->byte_length > PROXY_TEXT_CAPACITY ||
        payload_size != prefix_size + text->byte_length) {
        return;
    }

    manager = g_input_get_event_manager();
    if (manager == NULL) {
        return;
    }

    if (text->action == PROXY_TEXT_CHARACTER && text->byte_length == 1) {
        g_input_post_character(
            manager,
            text->bytes[0],
            proxy_message_time(text->message_time));
    } else if (text->action == PROXY_TEXT_COMMITTED &&
               text->byte_length != 0) {
        memcpy(committed, text->bytes, text->byte_length);
        committed[text->byte_length] = '\0';
        g_input_post_committed_text(
            manager,
            committed,
            proxy_message_time(text->message_time));
    }
}

static void proxy_execute_application(
    const uint8_t *payload,
    uint32_t payload_size)
{
    const proxy_application_payload *application;
    void *manager;
    uint32_t time;

    if (payload_size != sizeof(*application)) {
        return;
    }
    application = (const proxy_application_payload *)payload;
    manager = g_input_get_event_manager();
    if (manager == NULL) {
        return;
    }
    time = proxy_message_time(application->message_time);

    switch (application->action) {
    case PROXY_APPLICATION_IME_OPEN_STATUS:
        g_input_post_ime_open_status(manager, application->value, time);
        break;
    case PROXY_APPLICATION_IME_COMPOSITION_START:
        g_input_post_ime_start(manager, time);
        break;
    case PROXY_APPLICATION_IME_COMPOSITION_END:
        g_input_post_ime_end(manager, time);
        break;
    case PROXY_APPLICATION_IME_CANDIDATE_CLOSE:
        g_input_post_ime_candidate_close(manager, time);
        break;
    default:
        break;
    }
}

static void proxy_execute_client_packet(
    const uint8_t *body,
    uint32_t body_size)
{
    void *socket;

    if (body_size == 0 || body_size > PROXY_MAX_PAYLOAD ||
        body_size > 0x7FFFu || g_net_socket_pointer == NULL) {
        return;
    }
    socket = *g_net_socket_pointer;
    if (socket != NULL) {
        /* Call the detoured entry so injected packets remain subject to rules. */
        g_net_submit_client_packet(socket, body, (int16_t)body_size);
    }
}

static void proxy_execute_server_packet(
    const uint8_t *body,
    uint32_t body_size)
{
    void *socket;

    if (body_size == 0 || body_size > PROXY_MAX_PAYLOAD ||
        g_net_socket_pointer == NULL) {
        return;
    }
    socket = *g_net_socket_pointer;
    if (socket != NULL) {
        g_net_post_server_packet(socket, body, (int32_t)body_size);
    }
}

static void proxy_execute_command(const proxy_wire_message *message)
{
    uint32_t previous_tls = proxy_tls_flags();
    uint32_t injected_tls = 0x80000000u |
        (message->header.flags & PROXY_FLAG_BYPASS_RULES);

    if (message->header.kind == PROXY_COMMAND_SET_RULE) {
        if (message->header.payload_size == sizeof(proxy_rule_payload)) {
            proxy_set_rule((const proxy_rule_payload *)message->payload);
        }
        return;
    }
    if (message->header.kind == PROXY_COMMAND_RESET_RULES) {
        proxy_reset_rules();
        return;
    }

    proxy_set_tls_flags(injected_tls);
    switch (message->header.kind) {
    case PROXY_COMMAND_POINTER:
        proxy_execute_pointer(message->payload, message->header.payload_size);
        break;
    case PROXY_COMMAND_KEY:
        proxy_execute_key(message->payload, message->header.payload_size);
        break;
    case PROXY_COMMAND_TEXT:
        proxy_execute_text(message->payload, message->header.payload_size);
        break;
    case PROXY_COMMAND_APPLICATION:
        proxy_execute_application(message->payload, message->header.payload_size);
        break;
    case PROXY_COMMAND_CLIENT_PACKET:
        proxy_execute_client_packet(message->payload, message->header.payload_size);
        break;
    case PROXY_COMMAND_SERVER_PACKET:
        proxy_execute_server_packet(message->payload, message->header.payload_size);
        break;
    default:
        break;
    }
    proxy_set_tls_flags(previous_tls);
}

static void proxy_drain_commands(void)
{
    proxy_wire_message message;
    uint32_t count = 0;

    while (count < PROXY_COMMANDS_PER_TICK && proxy_command_pop(&message)) {
        proxy_execute_command(&message);
        ++count;
    }
}

static void __fastcall proxy_hook_event_dispatcher_tick(
    void *self,
    void *unused_edx)
{
    (void)unused_edx;
    g_original_event_dispatcher_tick(self);
    proxy_drain_commands();
}

static int proxy_validate_wire_message(
    const proxy_wire_message *message,
    DWORD bytes_read)
{
    uint32_t expected;

    if (bytes_read < sizeof(proxy_message_header) ||
        message->header.magic != PROXY_PROTOCOL_MAGIC ||
        message->header.version != PROXY_PROTOCOL_VERSION ||
        message->header.payload_size > PROXY_MAX_PAYLOAD) {
        return 0;
    }

    expected = (uint32_t)sizeof(proxy_message_header) +
        message->header.payload_size;
    return bytes_read == expected;
}

static int proxy_send_telemetry(HANDLE pipe)
{
    proxy_wire_message message;
    proxy_telemetry_payload telemetry;
    DWORD bytes_written;
    DWORD message_size;

    if (!proxy_telemetry_pop(&telemetry)) {
        return 0;
    }

    memset(&message, 0, sizeof(message.header));
    message.header.magic = PROXY_PROTOCOL_MAGIC;
    message.header.version = PROXY_PROTOCOL_VERSION;
    message.header.kind = PROXY_MESSAGE_TELEMETRY;
    message.header.payload_size = sizeof(telemetry);
    memcpy(message.payload, &telemetry, sizeof(telemetry));
    message_size = (DWORD)sizeof(message.header) + sizeof(telemetry);

    WriteFile(pipe, &message, message_size, &bytes_written, NULL);
    return 1;
}

static DWORD WINAPI proxy_ipc_thread(void *unused)
{
    char pipe_name[96];
    HANDLE pipe;
    int connected;

    (void)unused;
    wsprintfA(
        pipe_name,
        "\\\\.\\pipe\\darkages-event-proxy-%lu",
        (unsigned long)GetCurrentProcessId());

    while (InterlockedCompareExchange(&g_running, 0, 0) != 0) {
        pipe = CreateNamedPipeA(
            pipe_name,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_NOWAIT |
                PIPE_REJECT_REMOTE_CLIENTS,
            1,
            65536,
            65536,
            0,
            NULL);
        if (pipe == INVALID_HANDLE_VALUE) {
            Sleep(100);
            continue;
        }

        connected = 0;
        while (InterlockedCompareExchange(&g_running, 0, 0) != 0) {
            if (!connected) {
                BOOL result = ConnectNamedPipe(pipe, NULL);
                DWORD error = result ? ERROR_SUCCESS : GetLastError();
                if (result || error == ERROR_PIPE_CONNECTED) {
                    connected = 1;
                } else if (error != ERROR_PIPE_LISTENING &&
                           error != ERROR_NO_DATA) {
                    break;
                }
            } else {
                proxy_wire_message message;
                DWORD bytes_read = 0;
                BOOL result = ReadFile(
                    pipe,
                    &message,
                    sizeof(message),
                    &bytes_read,
                    NULL);
                if (result && proxy_validate_wire_message(&message, bytes_read)) {
                    proxy_command_push(&message);
                } else if (!result) {
                    DWORD error = GetLastError();
                    if (error == ERROR_BROKEN_PIPE ||
                        error == ERROR_PIPE_NOT_CONNECTED ||
                        error == ERROR_MORE_DATA) {
                        break;
                    }
                }

                while (proxy_send_telemetry(pipe)) {
                    /* Drain without making a hook wait for the controller. */
                }
            }
            Sleep(2);
        }

        DisconnectNamedPipe(pipe);
        CloseHandle(pipe);
    }
    return 0;
}

static int proxy_match_bytes(uint32_t rva, const uint8_t *bytes, size_t size)
{
    return memcmp(proxy_at_rva(rva), bytes, size) == 0;
}

static int proxy_validate_target(void)
{
    static const uint8_t event_dispatch_prefix[] = {
        0x55, 0x8B, 0xEC, 0x6A, 0xFF, 0x68
    };
    static const uint8_t tick_prefix[] = {
        0x55, 0x8B, 0xEC, 0x6A, 0xFF, 0x68
    };
    static const uint8_t submit_prefix[] = {
        0x55, 0x8B, 0xEC, 0x83, 0xEC, 0x38
    };
    const IMAGE_DOS_HEADER *dos = (const IMAGE_DOS_HEADER *)g_module_base;
    const IMAGE_NT_HEADERS32 *nt;

    if (dos->e_magic != IMAGE_DOS_SIGNATURE) {
        return 0;
    }
    nt = (const IMAGE_NT_HEADERS32 *)(g_module_base + (uintptr_t)dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE ||
        nt->FileHeader.Machine != IMAGE_FILE_MACHINE_I386 ||
        nt->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR32_MAGIC) {
        return 0;
    }

    return proxy_match_bytes(
               RVA_EVENT_DISPATCH,
               event_dispatch_prefix,
               sizeof(event_dispatch_prefix)) &&
           proxy_match_bytes(
               RVA_EVENT_DISPATCHER_TICK,
               tick_prefix,
               sizeof(tick_prefix)) &&
           proxy_match_bytes(
               RVA_NET_SUBMIT_CLIENT_PACKET,
               submit_prefix,
               sizeof(submit_prefix));
}

static void proxy_resolve_client_functions(void)
{
    g_input_get_event_manager = (input_get_event_manager_fn)proxy_at_rva(
        RVA_INPUT_GET_EVENT_MANAGER);
    g_input_post_pointer_move = (input_post_pointer_move_fn)proxy_at_rva(
        RVA_INPUT_POST_POINTER_MOVE);
    g_input_post_left_down = (input_post_button_fn)proxy_at_rva(
        RVA_INPUT_POST_LEFT_DOWN);
    g_input_post_left_up = (input_post_button_fn)proxy_at_rva(
        RVA_INPUT_POST_LEFT_UP);
    g_input_post_right_down = (input_post_button_fn)proxy_at_rva(
        RVA_INPUT_POST_RIGHT_DOWN);
    g_input_post_right_up = (input_post_button_fn)proxy_at_rva(
        RVA_INPUT_POST_RIGHT_UP);
    g_input_post_mouse_wheel = (input_post_mouse_wheel_fn)proxy_at_rva(
        RVA_INPUT_POST_MOUSE_WHEEL);
    g_input_post_key_down = (input_post_key_fn)proxy_at_rva(
        RVA_INPUT_POST_KEY_DOWN);
    g_input_post_key_up = (input_post_key_fn)proxy_at_rva(
        RVA_INPUT_POST_KEY_UP);
    g_input_post_character = (input_post_character_fn)proxy_at_rva(
        RVA_INPUT_POST_CHARACTER);
    g_input_post_ime_open_status = (input_post_ime_status_fn)proxy_at_rva(
        RVA_INPUT_POST_IME_OPEN_STATUS);
    g_input_post_committed_text = (input_post_committed_text_fn)proxy_at_rva(
        RVA_INPUT_POST_COMMITTED_TEXT);
    g_input_post_ime_start = (input_post_ime_marker_fn)proxy_at_rva(
        RVA_INPUT_POST_IME_START);
    g_input_post_ime_end = (input_post_ime_marker_fn)proxy_at_rva(
        RVA_INPUT_POST_IME_END);
    g_input_post_ime_candidate_close = (input_post_ime_marker_fn)proxy_at_rva(
        RVA_INPUT_POST_IME_CANDIDATE_CLOSE);
    g_net_submit_client_packet = (net_submit_client_packet_fn)proxy_at_rva(
        RVA_NET_SUBMIT_CLIENT_PACKET);
    g_net_post_server_packet = (net_post_server_packet_fn)proxy_at_rva(
        RVA_NET_POST_SERVER_PACKET);
    g_net_socket_pointer = (void **)proxy_at_rva(RVA_NET_SOCKET_POINTER);
}

static int proxy_install_hooks(void)
{
    void *event_target = proxy_at_rva(RVA_EVENT_DISPATCH);
    void *submit_target = proxy_at_rva(RVA_NET_SUBMIT_CLIENT_PACKET);
    void *tick_target = proxy_at_rva(RVA_EVENT_DISPATCHER_TICK);

    if (!proxy_detour_attach(
            event_target,
            proxy_hook_event_dispatch,
            (void **)&g_original_event_dispatch)) {
        return 0;
    }
    if (!proxy_detour_attach(
            submit_target,
            proxy_hook_net_submit_client_packet,
            (void **)&g_original_net_submit_client_packet)) {
        proxy_detour_detach(event_target, proxy_hook_event_dispatch);
        return 0;
    }
    if (!proxy_detour_attach(
            tick_target,
            proxy_hook_event_dispatcher_tick,
            (void **)&g_original_event_dispatcher_tick)) {
        proxy_detour_detach(submit_target, proxy_hook_net_submit_client_packet);
        proxy_detour_detach(event_target, proxy_hook_event_dispatch);
        return 0;
    }
    return 1;
}

static void proxy_remove_hooks(void)
{
    proxy_detour_detach(
        proxy_at_rva(RVA_EVENT_DISPATCHER_TICK),
        proxy_hook_event_dispatcher_tick);
    proxy_detour_detach(
        proxy_at_rva(RVA_NET_SUBMIT_CLIENT_PACKET),
        proxy_hook_net_submit_client_packet);
    proxy_detour_detach(
        proxy_at_rva(RVA_EVENT_DISPATCH),
        proxy_hook_event_dispatch);
}

static DWORD WINAPI proxy_worker(void *unused)
{
    DWORD ipc_thread_id;
    HANDLE ipc_thread;

    (void)unused;
    g_module_base = (uintptr_t)GetModuleHandleA(NULL);
    if (g_module_base == 0 || !proxy_validate_target()) {
        InterlockedExchange(&g_running, 0);
        return 1;
    }

    InitializeCriticalSection(&g_command_queue.lock);
    InitializeCriticalSection(&g_telemetry_queue.lock);
    g_injection_tls = TlsAlloc();
    proxy_reset_rules();
    proxy_resolve_client_functions();

    if (g_injection_tls == TLS_OUT_OF_INDEXES) {
        InterlockedExchange(&g_running, 0);
        DeleteCriticalSection(&g_telemetry_queue.lock);
        DeleteCriticalSection(&g_command_queue.lock);
        return 2;
    }
    if (!proxy_install_hooks()) {
        InterlockedExchange(&g_running, 0);
        TlsFree(g_injection_tls);
        g_injection_tls = TLS_OUT_OF_INDEXES;
        DeleteCriticalSection(&g_telemetry_queue.lock);
        DeleteCriticalSection(&g_command_queue.lock);
        return 3;
    }

    ipc_thread = CreateThread(
        NULL,
        0,
        proxy_ipc_thread,
        NULL,
        0,
        &ipc_thread_id);
    if (ipc_thread == NULL) {
        InterlockedExchange(&g_running, 0);
    } else {
        WaitForSingleObject(ipc_thread, INFINITE);
        CloseHandle(ipc_thread);
    }

    proxy_remove_hooks();
    if (g_injection_tls != TLS_OUT_OF_INDEXES) {
        TlsFree(g_injection_tls);
        g_injection_tls = TLS_OUT_OF_INDEXES;
    }
    DeleteCriticalSection(&g_telemetry_queue.lock);
    DeleteCriticalSection(&g_command_queue.lock);
    return 0;
}

__declspec(dllexport) BOOL WINAPI event_proxy_start(void)
{
    DWORD thread_id;

    if (InterlockedCompareExchange(&g_started, 1, 0) != 0) {
        return TRUE;
    }
    InterlockedExchange(&g_running, 1);
    g_worker_thread = CreateThread(
        NULL,
        0,
        proxy_worker,
        NULL,
        0,
        &thread_id);
    if (g_worker_thread == NULL) {
        InterlockedExchange(&g_running, 0);
        InterlockedExchange(&g_started, 0);
        return FALSE;
    }
    return TRUE;
}

__declspec(dllexport) void WINAPI event_proxy_stop(void)
{
    InterlockedExchange(&g_running, 0);
    if (g_worker_thread != NULL) {
        WaitForSingleObject(g_worker_thread, 5000);
        CloseHandle(g_worker_thread);
        g_worker_thread = NULL;
    }
    InterlockedExchange(&g_started, 0);
}

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, void *reserved)
{
    (void)reserved;

    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(instance);
        event_proxy_start();
    } else if (reason == DLL_PROCESS_DETACH) {
        InterlockedExchange(&g_running, 0);
    }
    return TRUE;
}
