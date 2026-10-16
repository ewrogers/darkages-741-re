using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;

namespace DarkAgesCrashLauncher {
    internal sealed class Patch {
        internal readonly string Name;
        internal readonly uint Rva;
        internal readonly byte[] Original, Fixed;
        internal readonly int Entry;
        internal Patch(string name, uint rva, byte[] original, int entry, byte[] fixedBytes) {
            Name = name; Rva = rva; Original = original; Entry = entry; Fixed = fixedBytes;
        }
    }
    internal sealed class Relocation {
        internal readonly int Offset;
        internal readonly bool Relative;
        internal readonly uint Rva;
        internal Relocation(int offset, bool relative, uint rva) {
            Offset = offset; Relative = relative; Rva = rva;
        }
    }
    internal sealed class Plan {
        internal byte[] Stub;
        internal readonly Dictionary<string, byte[]> Hooks = new Dictionary<string, byte[]>();
    }
    internal sealed class Options {
        internal string Client = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Darkages.exe");
        internal string Only;
        internal bool Vanilla, VerifyOnly, Pause, Help, SelfTest, Arbiter;
        internal readonly List<string> Arguments = new List<string>();

        internal static Options Parse(string[] args) {
            Options o = new Options();
            for (int i = 0; i < args.Length; i++) {
                string a = args[i];
                if (a == "--") {
                    for (i++; i < args.Length; i++) o.Arguments.Add(args[i]);
                    break;
                }
                if (a == "--client" || a == "--only") {
                    if (++i == args.Length) throw new ArgumentException("Missing value for " + a);
                    if (a == "--client") o.Client = args[i]; else o.Only = args[i];
                } else if (a == "--vanilla") o.Vanilla = true;
                else if (a == "--verify-only") o.VerifyOnly = true;
                else if (a == "--pause") o.Pause = true;
                else if (a == "--arbiter") o.Arbiter = true;
                else if (a == "--self-test") o.SelfTest = true;
                else if (a == "--help" || a == "/?") o.Help = true;
                else throw new ArgumentException("Unknown option: " + a + ". Use --help.");
            }
            if (o.Vanilla && o.Only != null) throw new ArgumentException("--vanilla cannot be combined with --only.");
            if (o.VerifyOnly && o.Pause) throw new ArgumentException("Choose --verify-only or --pause.");
            return o;
        }
        internal List<Patch> Selected() {
            List<Patch> result = new List<Patch>();
            if (Vanilla) return result;
            HashSet<string> names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            if (Only != null) {
                foreach (string token in Only.Split(',')) {
                    string name = token.Trim();
                    if (name == "status-elements") { names.Add("status-attack"); names.Add("status-defense"); }
                    else if (name == "field-map-palette" || name == "ground-item-null" ||
                             name == "balloon-palette" || name == "empty-pixmap" || name == "alpha-tail") names.Add(name);
                    else throw new ArgumentException("Unknown patch group: " + name);
                }
            }
            foreach (Patch p in PatchData.Patches) if (Only == null || names.Contains(p.Name)) result.Add(p);
            return result;
        }
    }

    internal sealed class LaunchResult {
        internal uint Pid, ModuleBase, StubBase;
        internal bool Resumed;
    }

    internal sealed class Log : IDisposable {
        private StreamWriter writer;
        internal readonly string PathName;
        internal Log() {
            try {
                string dir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                                          "DarkAgesCrashLauncher", "logs");
                Directory.CreateDirectory(dir);
                PathName = Path.Combine(dir, DateTime.UtcNow.ToString("yyyyMMddTHHmmssfff") + "-" +
                                            Process.GetCurrentProcess().Id + ".log");
                writer = new StreamWriter(new FileStream(PathName, FileMode.CreateNew, FileAccess.Write, FileShare.Read),
                                          new UTF8Encoding(false));
                writer.AutoFlush = true;
            } catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }
        internal void Write(string message) {
            Console.WriteLine(message);
            if (writer != null) {
                try { writer.WriteLine(DateTime.UtcNow.ToString("O") + " " + message); }
                catch (IOException) { writer.Dispose(); writer = null; }
            }
        }
        public void Dispose() { if (writer != null) writer.Dispose(); }
    }

    internal static class Program {
#if LAUNCHER_TESTS
        internal static Action<string, uint> TestCheckpoint;
#endif
        [Conditional("LAUNCHER_TESTS")]
        private static void Checkpoint(string stage, uint pid) {
#if LAUNCHER_TESTS
            if (TestCheckpoint != null) TestCheckpoint(stage, pid);
#endif
        }
        private static void Require(bool success, string operation) {
            if (!success) throw new Win32Exception(Marshal.GetLastWin32Error(), operation);
        }
        internal static IntPtr Pointer(long address) {
            if (address < 0 || address > uint.MaxValue) throw new OverflowException("Not an x86 address.");
            return new IntPtr(unchecked((int)(uint)address));
        }
        private static uint Address(IntPtr value) { return unchecked((uint)value.ToInt32()); }
        private static UIntPtr Size(int value) { return new UIntPtr(checked((uint)value)); }

        internal static string Quote(string value) {
            StringBuilder text = new StringBuilder("\"");
            int slashes = 0;
            foreach (char c in value) {
                if (c == '\\') { slashes++; continue; }
                text.Append('\\', c == '"' ? slashes * 2 + 1 : slashes);
                text.Append(c); slashes = 0;
            }
            text.Append('\\', slashes * 2); text.Append('"');
            return text.ToString();
        }
        private static byte[] Relative(long target, long next) { return BitConverter.GetBytes(checked((int)(target - next))); }
        private static void Copy(byte[] output, int offset, byte[] data) { Buffer.BlockCopy(data, 0, output, offset, data.Length); }

        internal static Plan BuildPlan(uint module, uint allocation) {
            if ((long)module + PatchData.ImageSize > (long)uint.MaxValue + 1 ||
                (long)allocation + PatchData.Stub.Length > (long)uint.MaxValue + 1)
                throw new OverflowException("Image or allocation does not fit the x86 address space.");
            Plan plan = new Plan(); plan.Stub = (byte[])PatchData.Stub.Clone();
            foreach (Relocation r in PatchData.Relocations) {
                long target = (long)module + r.Rva;
                Copy(plan.Stub, r.Offset, r.Relative ? Relative(target, (long)allocation + r.Offset + 4)
                                                    : BitConverter.GetBytes(checked((uint)target)));
            }
            foreach (Patch p in PatchData.Patches) {
                byte[] bytes;
                if (p.Fixed != null) bytes = (byte[])p.Fixed.Clone();
                else {
                    bytes = new byte[p.Original.Length]; bytes[0] = 0xE9;
                    Copy(bytes, 1, Relative((long)allocation + p.Entry, (long)module + p.Rva + 5));
                    for (int i = 5; i < bytes.Length; i++) bytes[i] = 0x90;
                }
                plan.Hooks.Add(p.Name, bytes);
            }
            return plan;
        }

        private static byte[] Read(IntPtr process, long address, int count) {
            byte[] bytes = new byte[count]; UIntPtr got;
            Require(Native.ReadProcessMemory(process, Pointer(address), bytes, Size(count), out got), "ReadProcessMemory");
            if (got.ToUInt64() != (ulong)count) throw new IOException("Short remote read.");
            return bytes;
        }
        private static void Write(IntPtr process, long address, byte[] bytes) {
            UIntPtr written;
            Require(Native.WriteProcessMemory(process, Pointer(address), bytes, Size(bytes.Length), out written), "WriteProcessMemory");
            if (written.ToUInt64() != (ulong)bytes.Length) throw new IOException("Short remote write.");
        }
        private static void Equal(byte[] expected, byte[] actual, string label) {
            if (expected.Length != actual.Length) throw new IOException("Length mismatch: " + label);
            for (int i = 0; i < expected.Length; i++) if (expected[i] != actual[i])
                throw new IOException("Byte mismatch: " + label + ", offset " + i);
        }
        private static string Hash(FileStream file) {
            file.Position = 0;
            using (SHA256 sha = SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(file)).Replace("-", "").ToLowerInvariant();
        }
        private static byte[] FileBytes(FileStream file, long offset, int count) {
            file.Position = offset; byte[] bytes = new byte[count]; int read = 0;
            while (read < count) {
                int n = file.Read(bytes, read, count - read);
                if (n == 0) throw new IOException("Unexpected executable end."); read += n;
            }
            return bytes;
        }
        private static uint ValidateDisk(FileStream file) {
            if (file.Length != PatchData.FileSize || Hash(file) != PatchData.Sha256)
                throw new IOException("Client fingerprint mismatch; no process was created.");
            byte[] dos = FileBytes(file, 0, 64);
            if (dos[0] != 'M' || dos[1] != 'Z') throw new IOException("Missing DOS header.");
            uint pe = BitConverter.ToUInt32(dos, 0x3C);
            byte[] header = FileBytes(file, pe, 0x60);
            if (BitConverter.ToUInt32(header, 0) != 0x4550 || BitConverter.ToUInt16(header, 4) != 0x14C ||
                BitConverter.ToUInt16(header, 24) != 0x10B || BitConverter.ToUInt32(header, 80) != PatchData.ImageSize)
                throw new IOException("Unexpected x86 PE headers.");
            return pe;
        }
        private static uint FindModule(IntPtr process, FileStream file, uint pe) {
            IntPtr ntdll = Native.GetModuleHandleW("ntdll.dll");
            if (ntdll == IntPtr.Zero) throw new IOException("ntdll is unavailable.");
            IntPtr address = Native.GetProcAddress(ntdll, "NtQueryInformationProcess");
            if (address == IntPtr.Zero) throw new IOException("NtQueryInformationProcess is unavailable.");
            Native.QueryBasicInfo query = (Native.QueryBasicInfo)Marshal.GetDelegateForFunctionPointer(address, typeof(Native.QueryBasicInfo));
            Native.BasicInfo32 info; int returned;
            int status = query(process, 0, out info, Marshal.SizeOf(typeof(Native.BasicInfo32)), out returned);
            if (status < 0 || returned != 24 || info.peb == 0)
                throw new IOException("Unsupported x86 process-basic-information response.");
            // x86 PEB ImageBaseAddress is at +8. Validate the result, never assume 0x400000.
            uint module = BitConverter.ToUInt32(Read(process, (long)info.peb + 8, 4), 0);
            if (module == 0 || (module & 0xFFFF) != 0 || (long)module + PatchData.ImageSize > (long)uint.MaxValue + 1)
                throw new IOException("Invalid loaded image base.");
            Equal(FileBytes(file, 0, 64), Read(process, module, 64), "remote DOS header");
            Equal(FileBytes(file, pe, 0x100), Read(process, (long)module + pe, 0x100), "remote PE header");
            return module;
        }
        private static void VerifyProtection(IntPtr process, long address, uint expected) {
            Native.MemoryInfo32 info;
            UIntPtr got = Native.VirtualQueryEx(process, Pointer(address), out info, Size(Marshal.SizeOf(typeof(Native.MemoryInfo32))));
            if (got.ToUInt64() != 28 || info.state != 0x1000 || info.protect != expected)
                throw new IOException("Unexpected page protection at " + address.ToString("X8"));
        }
        private static uint Allocate(IntPtr process, uint module, bool arbiter, out Plan plan) {
            // First let Windows select an address. Then try nearby 64-KiB-aligned hints.
            for (int i = 0; i <= 128; i++) {
                long hint = 0;
                if (i != 0) hint = (long)module + ((i + 1) / 2) * 0x01000000L * (i % 2 == 1 ? 1 : -1);
                if (hint < 0 || hint + 4096 > (long)uint.MaxValue + 1) continue;
                int length = arbiter ? ArbiterEndpoint.Entry + ArbiterEndpoint.Wrapper.Length : PatchData.Stub.Length;
                IntPtr allocation = Native.VirtualAllocEx(process, Pointer(hint), Size(length), Native.MemCommitReserve, Native.ReadWrite);
                if (allocation == IntPtr.Zero) continue;
                uint value = Address(allocation);
                try {
                    plan = BuildPlan(module, value);
                    if (arbiter) ArbiterEndpoint.Extend(plan, module, value);
                    return value;
                }
                catch (OverflowException) {
                    Require(Native.VirtualFreeEx(process, allocation, UIntPtr.Zero, Native.MemRelease), "VirtualFreeEx unreachable allocation");
                }
            }
            throw new IOException("Cannot allocate a stub within signed rel32 reach.");
        }
        private static void WriteHook(IntPtr process, long address, byte[] original, byte[] replacement) {
            Equal(original, Read(process, address, original.Length), "original hook before write");
            uint previous;
            Require(Native.VirtualProtectEx(process, Pointer(address), Size(replacement.Length), Native.ExecuteReadWrite, out previous),
                    "VirtualProtectEx hook writable");
            try {
                Write(process, address, replacement);
                Equal(replacement, Read(process, address, replacement.Length), "hook readback");
            } finally {
                uint ignored;
                Require(Native.VirtualProtectEx(process, Pointer(address), Size(replacement.Length), previous, out ignored),
                        "VirtualProtectEx hook restoration");
            }
            VerifyProtection(process, address, previous);
        }
        private static void TerminateAndWait(IntPtr process, uint code) {
            if (Native.WaitForSingleObject(process, 0) != 0) {
                Require(Native.TerminateProcess(process, code), "TerminateProcess suspended child");
                if (Native.WaitForSingleObject(process, 5000) != 0) throw new IOException("Child termination was not confirmed.");
            }
        }

        internal static LaunchResult Launch(Options options, Log log) {
            if (IntPtr.Size != 4) throw new IOException("Use the x86 launcher build.");
            string client = Path.GetFullPath(options.Client);
            List<Patch> patches = options.Selected();
            if (options.Arbiter) patches.AddRange(ArbiterEndpoint.Patches);
            string command = Quote(client);
            foreach (string argument in options.Arguments) command += " " + Quote(argument);
            if (command.Length >= 32767) throw new ArgumentException("Client command line is too long.");
            Native.ProcessInfo child = new Native.ProcessInfo();
            bool resumed = false, terminated = false;
            // Read-only lease denies writes/deletion during hash, CreateProcess, and installation.
            using (FileStream file = new FileStream(client, FileMode.Open, FileAccess.Read, FileShare.Read)) {
                uint pe = ValidateDisk(file);
                log.Write("Client SHA-256 verified: " + PatchData.Sha256);
                Native.StartupInfo startup = new Native.StartupInfo(); startup.cb = (uint)Marshal.SizeOf(typeof(Native.StartupInfo));
                try {
                    Require(Native.CreateProcessW(client, new StringBuilder(command), IntPtr.Zero, IntPtr.Zero, false,
                        Native.CreateSuspended, IntPtr.Zero, Path.GetDirectoryName(client), ref startup, out child), "CreateProcessW suspended");
                    log.Write("Suspended child PID=" + child.pid);
                    Checkpoint("child-created", child.pid);
                    uint module = FindModule(child.process, file, pe);
                    log.Write("Module base=0x" + module.ToString("X8"));
                    // Check all canonical sites before making any allocation or write.
                    foreach (Patch p in PatchData.Patches)
                        Equal(p.Original, Read(child.process, (long)module + p.Rva, p.Original.Length), p.Name + " original bytes");
                    if (options.Arbiter) {
                        foreach (Patch p in ArbiterEndpoint.Patches)
                            Equal(p.Original, Read(child.process, (long)module + p.Rva, p.Original.Length), p.Name + " original bytes");
                        log.Write("Arbiter redirect: preserve stock initialization, then select 127.0.0.1:2610; official fallback disabled.");
                    }
                    Checkpoint("originals-verified", child.pid);
                    uint stub = 0; Plan plan = null;
                    if (patches.Count != 0) {
                        stub = Allocate(child.process, module, options.Arbiter, out plan);
                        log.Write("Stub base=0x" + stub.ToString("X8") + " size=0x" + plan.Stub.Length.ToString("X"));
                        Checkpoint("allocated", child.pid);
                        Write(child.process, stub, plan.Stub);
                        Equal(plan.Stub, Read(child.process, stub, plan.Stub.Length), "stub readback");
                        uint previous;
                        Require(Native.VirtualProtectEx(child.process, Pointer(stub), Size(plan.Stub.Length), Native.ExecuteRead, out previous),
                                "VirtualProtectEx stub executable/read-only");
                        VerifyProtection(child.process, stub, Native.ExecuteRead);
                        Checkpoint("stub-verified", child.pid);
                        int index = 0;
                        foreach (Patch p in patches) {
                            WriteHook(child.process, (long)module + p.Rva, p.Original, plan.Hooks[p.Name]);
                            log.Write("Verified " + p.Name + " at RVA=0x" + p.Rva.ToString("X8"));
                            if (++index == 1) Checkpoint("first-hook", child.pid);
                        }
                        Checkpoint("hooks-verified", child.pid);
                        Require(Native.FlushInstructionCache(child.process, Pointer(stub), Size(plan.Stub.Length)), "FlushInstructionCache stub");
                        foreach (Patch p in patches) {
                            Require(Native.FlushInstructionCache(child.process, Pointer((long)module + p.Rva), Size(p.Original.Length)), "FlushInstructionCache hook");
                            Equal(plan.Hooks[p.Name], Read(child.process, (long)module + p.Rva, p.Original.Length), p.Name + " final readback");
                        }
                        Checkpoint("cache-flushed", child.pid);
                    }
                    if (Hash(file) != PatchData.Sha256) throw new IOException("Executable changed during installation.");
                    LaunchResult result = new LaunchResult(); result.Pid = child.pid; result.ModuleBase = module; result.StubBase = stub;
                    if (options.VerifyOnly) {
                        TerminateAndWait(child.process, 0); terminated = true;
                        log.Write("PASS: " + patches.Count + " hooks verified; child terminated without resuming; disk hash unchanged.");
                        return result;
                    }
                    if (options.Pause) {
                        log.Write("Installation complete. Attach the debugger to PID " + child.pid + ". Press Enter to resume, or EOF to cancel.");
                        if (Console.ReadLine() == null) throw new OperationCanceledException("Launch cancelled while suspended.");
                    }
                    Checkpoint("before-resume", child.pid);
                    uint count = Native.ResumeThread(child.thread);
                    if (count != 1) throw new IOException("ResumeThread expected suspend count 1, got " + count + ". Child will be terminated.");
                    resumed = true; result.Resumed = true;
                    log.Write("RUNNING PID=" + child.pid + " patches=" + patches.Count + "; disk hash unchanged.");
                    return result;
                } finally {
                    if (child.process != IntPtr.Zero && !resumed && !terminated) {
                        try { TerminateAndWait(child.process, 0xDA741003); log.Write("Aborted child terminated before resume: PID=" + child.pid); }
                        catch (Exception e) { log.Write("ERROR: could not confirm termination of suspended PID=" + child.pid + ": " + e.Message); }
                    }
                    if (child.thread != IntPtr.Zero) Native.CloseHandle(child.thread);
                    if (child.process != IntPtr.Zero) Native.CloseHandle(child.process);
                }
            }
        }

        internal static void SelfTest() {
            if (PatchData.Patches.Length != 7 || PatchData.Stub.Length != 0x184 || PatchData.Relocations.Length != 15)
                throw new Exception("Unexpected generated patch inventory.");
            uint[,] bases = { { 0x400000, 0x1000000 }, { 0x12000000, 0x30000000 } };
            for (int n = 0; n < 2; n++) {
                uint module = bases[n, 0], allocation = bases[n, 1]; Plan p = BuildPlan(module, allocation);
                foreach (Relocation r in PatchData.Relocations) {
                    long actual = r.Relative ? (long)allocation + r.Offset + 4 + BitConverter.ToInt32(p.Stub, r.Offset)
                                             : BitConverter.ToUInt32(p.Stub, r.Offset);
                    if (actual != (long)module + r.Rva) throw new Exception("Relocation test failed.");
                }
                foreach (Patch patch in PatchData.Patches) {
                    byte[] hook = p.Hooks[patch.Name];
                    if (hook.Length != patch.Original.Length || (patch.Rva & 0xFFF) + hook.Length > 4096)
                        throw new Exception("Hook boundary test failed.");
                    long target = (long)module + patch.Rva + 5 + BitConverter.ToInt32(hook, 1);
                    long expected = patch.Fixed == null ? (long)allocation + patch.Entry : (long)module + 0x72720;
                    if (target != expected) throw new Exception("Hook target test failed.");
                }
                ArbiterEndpoint.Extend(p, module, allocation);
                byte[] endpoint = p.Hooks["arbiter-endpoint"];
                if (endpoint[0] != 0xE8 || (long)module + 0x32258 + BitConverter.ToInt32(endpoint, 1) != (long)allocation + ArbiterEndpoint.Entry ||
                    (long)allocation + ArbiterEndpoint.Entry + 8 + BitConverter.ToInt32(p.Stub, ArbiterEndpoint.Entry + 4) != (long)module + 0x33380)
                    throw new Exception("Arbiter endpoint call relocation failed.");
            }
            if (Options.Parse(new string[] { "--only", "status-elements" }).Selected().Count != 2 ||
                Options.Parse(new string[] { "--vanilla" }).Selected().Count != 0 ||
                Options.Parse(new string[0]).Selected().Count != 7 || Quote("") != "\"\"" || Quote("two words") != "\"two words\"")
                throw new Exception("Option or quoting test failed.");
            Console.WriteLine("PASS: generated inventory, relocations at two bases, hook targets, patch selection, quoting.");
        }

        private static void Usage() {
            Console.WriteLine("Dark Ages 7.41 crash-fix test launcher (x86)");
            Console.WriteLine("CrashFixLauncher.exe [--client PATH] [--arbiter] [--verify-only | --pause] [--only GROUPS | --vanilla] [-- client arguments]");
            Console.WriteLine("Default: Darkages.exe beside the launcher, all six repairs (seven hooks), in-memory only.");
            Console.WriteLine("--verify-only  Install/read back patches in a suspended child, terminate it without running game code.");
            Console.WriteLine("--pause        Wait for Enter after installation so a debugger can attach.");
            Console.WriteLine("--arbiter      Preserve stock initialization, redirect to 127.0.0.1:2610, disable official fallback (memory only).");
            Console.WriteLine("--only         Comma-separated: field-map-palette,ground-item-null,status-elements,balloon-palette,empty-pixmap,alpha-tail");
            Console.WriteLine("--vanilla      Disable crash repairs for an A/B control; --arbiter still applies endpoint routing.");
            Console.WriteLine("--self-test    Test byte-plan construction without launching the game.");
        }
        internal static int Main(string[] args) {
            try {
                Options options = Options.Parse(args);
                if (options.Help) { Usage(); return 0; }
                if (options.SelfTest) { SelfTest(); return 0; }
                using (Log log = new Log()) {
                    if (log.PathName != null) log.Write("Log: " + log.PathName);
                    try { Launch(options, log); return 0; }
                    catch (Exception e) { log.Write("FAILED: " + e.Message); return 1; }
                }
            } catch (Exception e) { Console.Error.WriteLine("FAILED: " + e.Message); return 2; }
        }
    }
}
