import pickle

filename = 'data/SN'
f = open(filename)
SN = set(f.readlines())
f.close()

filename = 'data/BP'
f = open(filename)
BP = set(f.readlines())
f.close()

filename = 'data/estagged.pk'
f = open(filename)
data = pickle.load(f)
f.close()

generic_data = []
for s in data:
    temp = []
    for w, t in s:
        if t == 'CD' or t == 'NNP':
            temp.append((t, t))
        elif t == 'NN' or t == 'NNS':
            if w in SN:
                temp.append(('SN', t))
            elif w not in BP:
                temp.append((t, t))
        else:
            temp.append((w, t))
    generic_data.append(temp)

def words():
    return [w for s in data for w in s]

def sents():
    return [map(lambda(x): x[0], s) for s in data]

def tagged_sents():
    return data

def gen_tagged_sents():
    return generic_data
