from BeautifulSoup import BeautifulSoup
import random
import re
import nltk
import pickle
import urllib2

root = 'http://textfiles.com/sex/EROTICA'

def crawl(addr, pages, curdepth=0):
    try:
        html = urllib2.urlopen(addr)
        soup = BeautifulSoup(html)
        if curdepth == 2:
            html = urllib2.urlopen(addr)
            pages.append(html.read())
        for link in soup.findAll('a'):
            href = link.get('href')
            if curdepth < 2:
                crawl(addr + '/' + href, pages, curdepth=curdepth+1)
    except urllib2.HTTPError:
        print "404: %s not found" %(addr)

def clean(page):
    temp = re.sub('[\t\r]', '', page)
    temp = temp.split('\n')
    temp = [x for x in temp if x != '']
    temp = temp[1:-1]
    return ' '.join(temp).replace('  ', ' ')

def taggedSents(pages):
    print "tokenizing documents"
    sents = [s for d in pages for s in nltk.tokenize.sent_tokenize(d)]
    print "tokenizing sentences"
    random.shuffle(sents)
    sents = [s for s in sents if re.match(r'^[a-zA-Z\'-]+ [a-zA-Z ,\'-]+[.?!]$', s)]
    chunked = [nltk.tokenize.word_tokenize(s) for s in sents[:60000]]
    print "tagging words"
    tagged = [nltk.pos_tag(s) for s in chunked]
    return tagged

def main():
    pages = []
    print "crawling"
    crawl(root, pages)
    print "cleaning"
    tagged = taggedSents([clean(d) for d in pages[1:]])
    f = open('data/estagged.pk', 'wb')
    pickle.dump(tagged, f)
    f.close()


if __name__ == "__main__":
    main()
