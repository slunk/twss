#Peter Enns
import common
from itertools import imap
from nltk.corpus import brown as nltk_brown

def sents():
    return nltk_brown.sents()

def tagged_sents():
    return nltk_brown.tagged_sents()

def generic_tagged_sents():
    return imap(lambda(x): list(generify(x)), nltk_brown.tagged_sents())

def generify(s):
    for w, t in common.generify(s):
        if t[0] == 'P':
            yield (w, 'PRP')
        else:
            yield (w, t)
