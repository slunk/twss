#Peter Enns
from corpus import brown, erotic, common
from collections import defaultdict
import util
import math
import nltk

def compute_features(s):
    feats = []
    chunked = nltk.tokenize.word_tokenize(s)
    tagged = nltk.pos_tag(chunked)
    generic = list(common.generify(tagged))

    #"Noun Euphamism" Features

    #Has sexy noun
    feats.append(0.0)
    for w in chunked:
        if w.lower() in common.SN:
            feats[-1] = 1.0
            break

    #Has body part
    feats.append(0.0)
    for w in chunked:
        if w.lower() in common.BP:
            feats[-1] = 1.0
            break

    #TODO: NS(s) = 10^-7

    #Average NS(s) for all nouns in s not in union of SN and BP
    feats.append(ave_ns(tagged))

    #"Structural Element" features

    #Verb that never occurs in Se
    feats.append(0.0)
    for v in [w for w, t in tagged if t[0] == 'V']:
        if v not in sexy_verbs:
            feats[-1] = 1.0
            break

    #Verb phrase that never occurs in Se
    feats.append(0.0)
    for v in util.get_vps(generic):
        if str([w for w, t in v]) not in se_vp_set:
            feats[-1] = 1.0
            break

    #Average VS over all verb phrases in s
    feats.append(ave_vs(generic))

    #Average AS for all adjs in s
    feats.append(ave_as(tagged))

    #Is there an adjective in s that never occurs in Se U Sb with a noun in SN
    feats.append(0.0)
    for a in [w for w, t in tagged if t[0] == 'J']:
        if a not in sexy_adjs:
            feats[-1] = 1.0
            break

    #Basic Structure

    #Punctuation tokens
    feats.append(sum([1 for w, t in tagged if t != '.' and t != ':' and t !=',']))

    #Non-punctuation tokens (Note: this must stay directly after the punctuation tokens feature)
    feats.append(len(chunked) - feats[-1])

    #TODO: Number of times each pronoun and each (~~approximately) POS appears in s
    feats.append(sum([1 for w, t in tagged if t[0] == 'D'])) #determiners
    feats.append(sum([1 for w, t in tagged if t[0] == 'N'])) #nouns
    feats.append(sum([1 for w, t in tagged if t[0] == 'P'])) #pronouns
    feats.append(sum([1 for w, t in tagged if t[0] == 'V'])) #verbs
    feats.append(sum([1 for w, t in tagged if t[0] == 'J'])) #adjectives
    feats.append(sum([1 for w, t in tagged if t[0] == 'I'])) #prepositions
    
    #Subject
#    nouns = [w for w, t in tagged if t[0] == 'N' or t == 'PRP']
#    if len(nouns) > 0:
#        subj = nouns[0]
#    else:
#        subj = ""
#    feats.append(subj)

    return dict((n, f) for n, f in enumerate(feats))


#Noun sexiness
print "NS prep"
ns_adj_counts = defaultdict(lambda: util.Counter(0.0))
adj_vocab = set([])

for s in erotic.tagged_sents():
    nouns = [w for w, t in s if t[0] == 'N']
    adjs = [w for w, t in s if t[0] == 'J']
    for n in nouns:
        for a in adjs:
            ns_adj_counts[n].inc(a)
            adj_vocab.add(a)

for s in brown.tagged_sents():
    nouns = [w for w, t in s if t[0] == 'N']
    adjs = [w for w, t in s if t[0] == 'J']
    for n in nouns:
        for a in adjs:
            ns_adj_counts[n].inc(a)
            adj_vocab.add(a)

num_adjs = len(adj_vocab)
adj_id_dict = {}
for n, a in enumerate(adj_vocab):
    adj_id_dict[a] = n

def adj_count_vec(n):
    ret = defaultdict(lambda: 0.0)
    for k, v in ns_adj_counts[n].iteritems():
        ret[adj_id_dict[k]] = v
    return ret
#    return [ns_adj_counts[n][a] for a in adj_vocab]

def ave_ns(s):
    sum = 0.0
    total = 0.0
    for w, t in s:
        if t[0] == 'N' and w not in common.SN and w not in common.BP:
            max = 0.0
            for n in common.SN:
                temp = util.cossim(adj_count_vec(w), adj_count_vec(n))
                if temp > max:
                    max = temp
            sum += max
            total += 1.0
    if total > 0:
        return sum / total
    return 0.0

#Adjective Sexiness
print "AS prep"
adjs = [w for s in erotic.tagged_sents() for w, t in s if t[0] == 'J']
adj_fd = nltk.FreqDist(adjs)

def adj_sexiness(a):
    return 1.0 * adj_fd[a] / adj_fd.N()

def ave_as(s):
    sum = 0.0
    total = 0.0
    for w, t in s:
        if t[0] == 'J':
            sum += adj_sexiness(w)
            total += 1
    if total > 0.0:
        return sum / total
    return 0.0

brown_sexy_adjs = set([w for s in brown.tagged_sents() for w, t in s if len(common.SN.intersection(set([w for w, t in s]))) > 0 and t[0] == 'J'])
sexy_adjs = brown_sexy_adjs.union(set(adjs))

#Verb Sexiness
sexy_verbs = set([w for s in erotic.tagged_sents() for w, t in s if t[0] == 'V'])

#print "making lists"
#se_vp_words = [w for s in erotic.tagged_sents() for vp in util.get_vps(s) for w, t in [('<s>', '<s>')] + vp + [('</s>', '</s>')]]
#sb_vp_words = [w for s in brown.tagged_sents() for vp in util.get_vps(s) for w, t in [('<s>', '<s>')] + vp + [('</s>', '</s>')]]
#se_words = [w for s in erotic.tagged_sents() for w, t in [('<s>', '<s>')] + s + [('</s>', '</s>')]]
#
#class Placeholder:
#    def __init__(self, corpus):
#        vocabulary = set(corpus)
#        cfd = nltk.ConditionalFreqDist(nltk.bigrams(corpus))
#        self.cfd_laplace = nltk.ConditionalProbDist(cfd, nltk.LaplaceProbDist, bins=len(vocabulary))
#
#    def phrase_prob(self, phrase):
#        prob = 0.0
#        for w0, w1 in nltk.bigrams(phrase):
#            prob += self.cfd_laplace[w0].logprob(w1)
#        return prob
#
#print "calculating fdist 1"
#v_in_se = Placeholder(se_vp_words)
#print "calculating fdist 2"
#s_in_se = Placeholder(se_words)
#print "calculating fdist 3"
#v_in_s = Placeholder(se_vp_words + sb_vp_words)
#
#def vs(s, v):
#    return math.pow(2, v_in_se.phrase_prob(v) + s_in_se.phrase_prob(s) - v_in_s.phrase_prob(v))

def ave_vs(s):
    sum = 0.0
    total = 0.0
    words = str([w for w, t in s])
    for v in util.get_vps(s):
        sum += vs(words, str([w for w, t in v]))
        total += 1
    if total > 0.0:
        return sum / total
    return 0.0

se_vps = [str([w for w, t in vp]) for s in erotic.generic_tagged_sents() for vp in util.get_vps(s)]
sb_vps = [str([w for w, t in vp]) for s in brown.generic_tagged_sents() for vp in util.get_vps(s)]
se_sents = [str([w for w, t in s]) for s in erotic.generic_tagged_sents()]
se_vp_set = set(se_vps)

v_in_se = nltk.LaplaceProbDist(nltk.FreqDist(se_vps), len(set(se_vps)))
s_in_se = nltk.LaplaceProbDist(nltk.FreqDist(se_sents), len(set(se_sents)))
v_in_s = nltk.LaplaceProbDist(nltk.FreqDist(se_vps + sb_vps), len(set(se_vps + sb_vps)))

def vs(s, v):
    return (v_in_se.prob(v) * s_in_se.prob(s)) / v_in_s.prob(v)
