def gen():
    for x in xrange(1000000000):
        if x % 3 == 0 or x % 5 == 0:
            yield x
acc = 0

for s in gen():
    acc += s

print acc
