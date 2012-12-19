#Peter Enns
import common
from itertools import imap
import pickle

filename = 'data/estagged2.pk'
f = open(filename)
data = pickle.load(f)
f.close()

def words():

    return [w for s in data for w in s]

def sents():
    return [map(lambda(x): x[0], s) for s in data]

def tagged_sents():
    return data

def generic_tagged_sents():
    return imap(lambda(x): list(common.generify(x)), data)
