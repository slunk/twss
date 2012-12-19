#Peter Enns
import math
from collections import defaultdict

class Counter():
    def __init__(self, default):
        self._def = default
        self._dict = defaultdict(lambda: default)
        self._total = 0

    def inc(self, item):
        self._dict[item] += 1.0
        self._total += 1.0

    def __getitem__(self, item):
        return self._dict[item]

    def N(self):
        return self._total + self._total * self._def

    def iteritems(self):
        return self._dict.iteritems()

def vps(s):
    return list(get_vps(s))

def get_vps(s):
    for n, (w, t) in enumerate(s):
        if t[0] == 'V':
            first, last = n, n
            while first >= 0 and s[first][1][0] != 'N' and s[first][0] not in ['I', 'you', 'it', 'me']:
#                if first != n and s[first][1][0] == 'V':
#                    first = n
#                    break
                first -= 1
            while last < len(s) and s[last][1][0] != 'N' and s[last][0] not in ['I', 'you', 'it', 'me']:
#                if last != n and s[last][1][0] == 'V':
#                    first = n
#                    break
                last += 1
            if first < 0:
                first = n
            if last == len(s):
                last = n
            yield s[first:last + 1]

def words_of_type(s, t):
    return [w for w, tag in s if t[0] == tag[0]]

def adjs(s):
    return words_of_type(s, 'J')

def nouns(s):
    return words_of_type(s, 'N')

#def modifying_adjs_helper(s, n):
#    i = n - 1
#    while i >= 0 and s[i][1][0] == 'J':
#        yield s[i][0]
#        i -= 1
#    i = n + 1
#    while i < len(s) and s[i][1][0] == 'J':
#        yield s[i][0]
#        i += 1

def cossim(a, b):
    dot = 0.0
    for k, v in a.iteritems():
        dot += v * b[k]
    alen_squared = 0.0
    for v in a.values():
        alen_squared += math.pow(v, 2)
    if alen_squared == 0:
        return 0.0
    blen_squared = 0.0
    for v in b.values():
        blen_squared += math.pow(v, 2)
    if blen_squared == 0:
        return 0.0
    return dot / (math.sqrt(alen_squared) * math.sqrt(blen_squared))

#def cossim(a, b):
#    dot = sum(map(lambda(x): x[0] * x[1], zip(a, b)))
#    alen = math.sqrt(sum(map(lambda(x): math.pow(x, 2), a)))
#    blen = math.sqrt(sum(map(lambda(x): math.pow(x, 2), b)))
#    if alen > 0.0 and blen > 0.0:
#        return dot / (alen * blen)
#    return 0.0

def str_to_i(s):
    sum = 0
    for n, c in enumerate(s):
        sum += math.pow(10, n) * ord(c)
    return int(sum)
