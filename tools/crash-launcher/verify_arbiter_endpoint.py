#!/usr/bin/env python3
"""Execute the loopback wrapper against a mocked initializer (requires Unicorn)."""
import re, struct
from pathlib import Path
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import *
s=Path(__file__).with_name("ArbiterEndpoint.cs").read_text()
s=s.split("internal static readonly byte[] Wrapper = {",1)[1].split("};",1)[0]
s=re.sub(r"//[^\n]*", "", s)
raw=bytes(int(x.strip(),0) for x in s.split(",") if x.strip())
for module,stub in [(0x400000,0x1e0000),(0x12000000,0x30000000)]:
 entry=stub+0x190; native=module+0x33380; data=0x50000000; stack=0x60000000; done=0x70000000
 code=bytearray(raw);struct.pack_into("<i",code,4,native-(entry+8))
 uc=Uc(UC_ARCH_X86,UC_MODE_32)
 for base in [stub,native&~0xfff,data,stack,done]:uc.mem_map(base,0x1000)
 uc.mem_write(entry,bytes(code));uc.mem_write(stack+0x800,struct.pack("<I",done))
 regs={UC_X86_REG_EAX:0x11,UC_X86_REG_EBX:0x22,UC_X86_REG_ECX:data,UC_X86_REG_EDX:0x44,UC_X86_REG_ESI:0x55,UC_X86_REG_EDI:0x66,UC_X86_REG_EBP:0x77,UC_X86_REG_ESP:stack+0x800}
 for reg,val in regs.items():uc.reg_write(reg,val)
 calls=[]
 def hook(uc,addr,size,user):
  if addr==native:
   assert uc.reg_read(UC_X86_REG_ECX)==data
   calls.append(addr)
   uc.mem_write(data+0x424,struct.pack("<II",0x11223344,0x5678))
   uc.mem_write(data+0x295,b"\x34\x58\x37\x5e")
   uc.mem_write(data+0x434,struct.pack("<H",2601))
   for reg,val in [(UC_X86_REG_EAX,0x1234),(UC_X86_REG_ECX,0x8888),(UC_X86_REG_EDX,0x9999),(UC_X86_REG_EFLAGS,0x247)]:uc.reg_write(reg,val)
   sp=uc.reg_read(UC_X86_REG_ESP);ret=struct.unpack("<I",uc.mem_read(sp,4))[0];uc.reg_write(UC_X86_REG_ESP,sp+4);uc.reg_write(UC_X86_REG_EIP,ret)
 uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(entry,done,count=100)
 assert len(calls)==1
 assert bytes(uc.mem_read(data+0x295,4))==b"\x7f\0\0\1"
 assert struct.unpack("<H",uc.mem_read(data+0x434,2))[0]==2610
 assert struct.unpack("<II",uc.mem_read(data+0x424,8))==(0x11223344,0x5678)
 for reg in [UC_X86_REG_EBX,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EBP]:assert uc.reg_read(reg)==regs[reg]
 assert uc.reg_read(UC_X86_REG_EAX)==0x1234 and uc.reg_read(UC_X86_REG_ECX)==0x8888 and uc.reg_read(UC_X86_REG_EDX)==0x9999
 assert uc.reg_read(UC_X86_REG_ESP)==stack+0x804 and uc.reg_read(UC_X86_REG_EFLAGS)==0x247
print("PASS: 29-byte endpoint wrapper at two bases; stock initializer called once, IDs/return/registers/flags/stack preserved; loopback:2610 selected.")
