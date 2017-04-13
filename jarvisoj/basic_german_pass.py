s0 = '000000000000000000000000000000000000000000000000000101110000110001000000101000000001'
s1 = 'WELCOMETOCFF'
print len(s0)
print len(s1)
l = []
for i in range(12):
    l.append(s0[i*7: i*7+7])

print l
ll = [int(x, 2) for x in l]
flag = ''
for i in range(12):
    flag += chr(ll[i] ^ ord(s1[i]))
print flag
