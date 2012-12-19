#Peter Enns
import pickle

filename = 'data/SN'
f = open(filename)
SN = set([s.strip() for s in f.readlines()])
f.close()

filename = 'data/BP'
f = open(filename)
BP = set([s.strip() for s in f.readlines()])
f.close()

def generify(s):
    for w, t in s:
        if t == 'CD' or t == 'NNP':
            yield (t, t)
        elif t[0] == 'N':
            if w.lower() in SN:
                yield ('SN', t)
            elif w.lower() not in BP:
                yield ('NN', t)
            else:
                yield (w, t)
        else:
            yield (w, t)
