s = '''
nit yqmg mqrqn bxw mtjtm nq rqni fiklvbxu mqrqnl xwg dvmnzxu lqjnyxmt xatwnl, rzn nit uxnntm xmt zlzxuuk mtjtmmtg nq xl rqnl. nitmt vl wq bqwltwlzl qw yivbi exbivwtl pzxuvjk xl mqrqnl rzn nitmt vl atwtmxu xamttetwn xeqwa tsftmnl, xwg nit fzruvb, nixn mqrqnl ntwg nq gq lqet qm xuu qj nit jquuqyvwa: xbbtfn tutbnmqwvb fmqamxeevwa, fmqbtll gxnx qm fiklvbxu ftmbtfnvqwl tutbnmqwvbxuuk, qftmxnt xznqwqeqzluk nq lqet gtamtt, eqdt xmqzwg, qftmxnt fiklvbxu fxmnl qj vnltuj qm fiklvbxu fmqbtlltl, ltwlt xwg exwvfzuxnt nitvm twdvmqwetwn, xwg tsivrvn vwntuuvatwn rtixdvqm - tlftbvxuuk rtixdvqm yivbi evevbl izexwl qm qnitm xwvexul. juxa vl lzrlnvnzntfxllvldtmktxlkkqzaqnvn. buqltuk mtuxntg nq nit bqwbtfn qj x mqrqn vl nit jvtug qj lkwnitnvb rvquqak, yivbi lnzgvtl twnvnvtl yiqlt wxnzmt vl eqmt bqefxmxrut nq rtvwal nixw nq exbivwtl.
'''
print [x for x in s.split(' ') if len(x) == 1]
print [x for x in s.split(' ') if len(x) == 2]
m = {
    'a': 'g',
    'b': 'c',
    'd': 'v',
    'e': 'm',
    'f': 'p',
    'x': 'a',
    'r': 'b',
    's': 'x',
    'z': 'u',
    'g': 'd',
    'y': 'w',
    'j': 'f',

    'u': 'l',
    'k': 'y',

    'w': 'n',
    'q': 'o',

    'v': 'i',
    'l': 's',

    'n': 't',
    'i': 'h',
    't': 'e',
    'm': 'r'


}
ss = ''

for x in s:
    if x in m.keys():
        ss += m[x]
    else:
        ss += x
print ss

flag = 'lzrlnvnzntfxllvldtmktxlkkqzaqnvn'
for f in flag:
    if f not in m.keys():
        print f
