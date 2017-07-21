import sys
from collections import Counter

def count(corpus, threshold):
    wc = Counter()
    print("Corpus length: ",len(corpus))
    l = []
    for i,w in enumerate(corpus):
        #print(i,w)
        if i % 1000000 == 0:
            #if i > 10000000: break
            #print(sys.stderr,i,len(wc))
            wc.update(l)
            l = []
        l.append(w)
    wc.update(l)

    word_count = ""
    for w,c in sorted([(w,c) for w,c in wc.items() if c >= threshold and w != ''],key=lambda x:-x[1]):
        word_count += "\t".join([w.strip(),str(c)])
        word_count += "\n"
    return word_count