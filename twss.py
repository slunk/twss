import sys
import getopt
from processSentence import *
from svmutil import *
import pickle
import random
import deviantFeature

def twss(sentence,vocabList,model):
    #print "you said: '"+sentence+"'\n"
    # these should be moved to file
    responses = ['Whatever ...','Okay','Yawn','What makes you think I care?','Yada yada','Uhuh','Yeah, yeah','figures',"I'm hungry",'give me a break','so ...']
    #x  = processSentence(sentence, vocabList)
    x = feature.compute_features(sentence)
    #print [x]
    p_label, p_acc, p_val = svm_predict([1], [x], model, '-b 1 -q')
    print p_label, p_acc, p_val
    if p_label[0] == 1:
        return "That's what she said!\n"
    else:
        return random.choice(responses) +'\n'   

def twss_lite(sentence,vocabList,model):
    x = processSentence(sentence, vocabList)
    p_label, p_acc, p_val = svm_predict([1], [x], model, '-b 1 -q')
    return p_label[0]


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def test(filename, label, model):
    f = open('data/' + filename)
    sentences = pickle.load(f)
    hits = 0.0
    misses = 0.0
    for n in range(len(sentences) - 100, len(sentences)):
        x = deviantFeature.compute_features(sentences[n])
        p_label, p_acc, p_val = svm_predict([1], [x], model, '-b 1 -q')
        if p_label[0] == label:
#            input("That's what she said!")
            hits += 1.0
        else:
            misses += 1.0
    f.close()
    return hits, misses
        
# based on Guido's post: http://www.artima.com/weblogs/viewpost.jsp?thread=4829
# might be out of date for 2.7 ...
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        input = open('data/vocab.pk')
        vocabList = pickle.load(input)
        input.close()
        model = svm_load_model("data/svm_model.pk")
        if not args:
            raise Usage('python twss.py "<your sentence>"')
        print "testing on training data"
        hit1, miss1 = test('fml.txt.pk', -1, model)
        hit2, miss2 = test('tfln.onesent.txt.pk', -1, model)
        hit3, miss3 = test('twssstories.txt.pk', 1, model)
        hit4, miss4 = test('usaquotes.txt.pk', -1, model)
        print "precision: %f" %(hit3 / (miss1 + miss2 + hit3 + miss4))
        print "recall: %f" %(hit3 / (hit3 + miss3))
        print twss(args[0],vocabList,model)
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
