using System;
using System.Runtime.InteropServices;
using System.Text;

namespace DarkAgesCrashLauncher {
    internal static class Native {
        internal const uint CreateSuspended = 0x4;
        internal const uint MemCommitReserve = 0x3000, MemRelease = 0x8000;
        internal const uint ReadWrite = 0x04, ExecuteRead = 0x20, ExecuteReadWrite = 0x40;

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
        internal struct StartupInfo {
            internal uint cb;
            internal string reserved, desktop, title;
            internal uint x, y, xSize, ySize, xChars, yChars, fill, flags;
            internal ushort show, reservedSize;
            internal IntPtr reservedData, stdIn, stdOut, stdErr;
        }
        [StructLayout(LayoutKind.Sequential)]
        internal struct ProcessInfo {
            internal IntPtr process, thread;
            internal uint pid, tid;
        }
        // This launcher and its child are x86, including on Windows ARM64.
        [StructLayout(LayoutKind.Sequential, Pack = 4)]
        internal struct BasicInfo32 {
            internal uint exitStatus, peb, affinity;
            internal int priority;
            internal uint pid, parentPid;
        }
        [StructLayout(LayoutKind.Sequential, Pack = 4)]
        internal struct MemoryInfo32 {
            internal uint address, allocationBase, allocationProtect, regionSize;
            internal uint state, protect, type;
        }
        [UnmanagedFunctionPointer(CallingConvention.Winapi)]
        internal delegate int QueryBasicInfo(IntPtr process, int informationClass,
            out BasicInfo32 information, int length, out int returnedLength);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool CreateProcessW(string application, StringBuilder commandLine,
            IntPtr processAttributes, IntPtr threadAttributes, [MarshalAs(UnmanagedType.Bool)] bool inheritHandles,
            uint flags, IntPtr environment, string directory, ref StartupInfo startup, out ProcessInfo process);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool ReadProcessMemory(IntPtr process, IntPtr address, byte[] data,
            UIntPtr size, out UIntPtr read);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool WriteProcessMemory(IntPtr process, IntPtr address, byte[] data,
            UIntPtr size, out UIntPtr written);
        [DllImport("kernel32.dll", SetLastError = true)]
        internal static extern IntPtr VirtualAllocEx(IntPtr process, IntPtr address, UIntPtr size, uint type, uint protect);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool VirtualFreeEx(IntPtr process, IntPtr address, UIntPtr size, uint type);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool VirtualProtectEx(IntPtr process, IntPtr address, UIntPtr size,
            uint protect, out uint previous);
        [DllImport("kernel32.dll", SetLastError = true)]
        internal static extern UIntPtr VirtualQueryEx(IntPtr process, IntPtr address,
            out MemoryInfo32 information, UIntPtr size);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool FlushInstructionCache(IntPtr process, IntPtr address, UIntPtr size);
        [DllImport("kernel32.dll", SetLastError = true)]
        internal static extern uint ResumeThread(IntPtr thread);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool TerminateProcess(IntPtr process, uint code);
        [DllImport("kernel32.dll", SetLastError = true)]
        internal static extern uint WaitForSingleObject(IntPtr handle, uint milliseconds);
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool CloseHandle(IntPtr handle);
        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        internal static extern IntPtr GetModuleHandleW(string name);
        [DllImport("kernel32.dll", CharSet = CharSet.Ansi, ExactSpelling = true, SetLastError = true)]
        internal static extern IntPtr GetProcAddress(IntPtr module, string name);
    }
}
