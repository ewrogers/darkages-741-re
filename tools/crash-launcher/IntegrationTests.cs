using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;

namespace DarkAgesCrashLauncher {
    internal static class IntegrationTests {
        private static string Hash(string path) {
            using (SHA256 hash = SHA256.Create())
            using (FileStream file = File.OpenRead(path))
                return BitConverter.ToString(hash.ComputeHash(file));
        }
        private static void Dead(uint pid) {
            try {
                using (Process process = Process.GetProcessById(checked((int)pid))) {
                    if (!process.HasExited) throw new Exception("Child survived cleanup: " + pid);
                }
            } catch (ArgumentException) { }
        }
        private static int Main(string[] args) {
            try {
                if (args.Length != 1) throw new Exception("Pass the client executable path.");
                string before = Hash(args[0]);
                int passed = 0;
                using (Log log = new Log()) {
                    foreach (string group in new string[] { null, "field-map-palette", "ground-item-null", "status-elements", "balloon-palette", "empty-pixmap", "alpha-tail", "vanilla" }) {
                        Options options = new Options(); options.Client = args[0]; options.VerifyOnly = true;
                        if (group == "vanilla") options.Vanilla = true; else options.Only = group;
                        LaunchResult result = Program.Launch(options, log);
                        if (result.Resumed) throw new Exception("Verification resumed a child.");
                        Dead(result.Pid); ++passed;
                    }
                    foreach (string stage in new string[] { "child-created", "originals-verified", "allocated", "stub-verified", "first-hook", "hooks-verified", "cache-flushed", "before-resume" }) {
                        uint child = 0;
                        Program.TestCheckpoint = delegate(string actual, uint pid) {
                            child = pid;
                            if (actual == stage) throw new IOException("Deliberate integration fault at " + stage);
                        };
                        bool failed = false;
                        try { Options options = new Options(); options.Client = args[0]; options.Arbiter = true; Program.Launch(options, log); }
                        catch (IOException e) {
                            if (e.Message != "Deliberate integration fault at " + stage) throw;
                            failed = true;
                        } finally { Program.TestCheckpoint = null; }
                        if (!failed || child == 0) throw new Exception("Fault checkpoint not reached: " + stage);
                        Dead(child); ++passed;
                    }
                    foreach (bool vanilla in new bool[] {false, true}) {
                        Options options = new Options(); options.Client = args[0]; options.Arbiter = true;
                        options.Vanilla = vanilla; options.VerifyOnly = true;
                        LaunchResult result = Program.Launch(options, log);
                        if (result.Resumed) throw new Exception("Arbiter verification resumed a child.");
                        Dead(result.Pid); ++passed;
                    }
                    string invalid = Path.Combine(Path.GetTempPath(), "da741-invalid-" + Guid.NewGuid().ToString("N") + ".exe");
                    try {
                        File.WriteAllBytes(invalid, new byte[] { 0x4d, 0x5a });
                        bool created = false, rejected = false;
                        Program.TestCheckpoint = delegate(string stage, uint pid) { created = true; };
                        try { Options options = new Options(); options.Client = invalid; Program.Launch(options, log); }
                        catch (IOException) { rejected = true; }
                        finally { Program.TestCheckpoint = null; }
                        if (created || !rejected) throw new Exception("Invalid executable was not rejected before process creation.");
                        ++passed;
                    } finally { File.Delete(invalid); }
                }
                if (Hash(args[0]) != before) throw new Exception("Client disk hash changed.");
                Console.WriteLine("PASS: " + passed + " integration scenarios; all children terminated; client disk hash unchanged.");
                return 0;
            } catch (Exception e) { Console.Error.WriteLine("FAIL: " + e); return 1; }
        }
    }
}
