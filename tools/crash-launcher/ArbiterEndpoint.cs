using System;

namespace DarkAgesCrashLauncher {
    internal static class ArbiterEndpoint {
        internal const int Entry = 0x190;
        // Preserve the stock initializer's installation identity, return value,
        // flags and callee-saved registers. Only replace its resulting IPv4/port.
        internal static readonly byte[] Wrapper = {
            0x56, 0x8B, 0xF1,                         // push esi; mov esi,ecx
            0xE8, 0, 0, 0, 0,                       // call net_configure_default_endpoint
            0xC7, 0x86, 0x95, 0x02, 0, 0, 0x7F, 0, 0, 1, // [esi+295] = 127.0.0.1
            0x66, 0xC7, 0x86, 0x34, 0x04, 0, 0, 0x32, 0x0A, // word [esi+434] = 2610
            0x5E, 0xC3                              // pop esi; ret
        };
        internal static readonly Patch[] Patches = {
            new Patch("arbiter-endpoint", 0x32253, new byte[] {0xE8,0x28,0x11,0,0}, Entry, null),
            new Patch("disable-endpoint-fallback", 0x1655F4,
                new byte[] {0xC7,0x85,0x94,0xFB,0xFF,0xFF,0,0,0,0}, -1,
                new byte[] {0xE9,0x06,0x13,0,0,0x90,0x90,0x90,0x90,0x90})
        };
        private static byte[] Relative(long target, long next) {
            return BitConverter.GetBytes(checked((int)(target - next)));
        }
        internal static void Extend(Plan plan, uint module, uint allocation) {
            byte[] stub = new byte[Entry + Wrapper.Length];
            if ((long)allocation + stub.Length > (long)uint.MaxValue + 1) throw new OverflowException();
            for (int i = 0; i < stub.Length; i++) stub[i] = 0x90;
            Array.Copy(plan.Stub, stub, plan.Stub.Length);
            Array.Copy(Wrapper, 0, stub, Entry, Wrapper.Length);
            Array.Copy(Relative((long)module + 0x33380, (long)allocation + Entry + 8), 0, stub, Entry + 4, 4);
            plan.Stub = stub;
            byte[] call = new byte[] {0xE8,0,0,0,0};
            Array.Copy(Relative((long)allocation + Entry, (long)module + Patches[0].Rva + 5), 0, call, 1, 4);
            plan.Hooks.Add(Patches[0].Name, call);
            plan.Hooks.Add(Patches[1].Name, (byte[])Patches[1].Fixed.Clone());
        }
    }
}
