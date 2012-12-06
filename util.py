import math

def cossim(a, b):
    dot = sum(map(lambda(x): x[0] * x[1], zip(a, b)))
    alen = math.sqrt(sum(map(lambda(x): math.pow(x, 2), a)))
    blen = math.sqrt(sum(map(lambda(x): math.pow(x, 2), b)))
    return dot / (alen * blen)
