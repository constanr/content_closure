def read_vocabulary(vocabulary_file, threshold):
   print("vocabulary words: ", len(vocabulary_file))
   v = {}
   for line in vocabulary_file.splitlines():
      line = line.lower()
      line = line.strip().split()
      if len(line) != 2: continue
      if int(line[1]) >= threshold:
         v[line[0]] = int(line[1])
   return v

def read_conll(corpus):
    root = (0,'*root*','rroot', -1)
    tokens = [root]
    for line in corpus:
        line = line.lower()
        token = line.strip().split('\t')
        #print(token)
        if not token:
            if len(tokens)>1: yield tokens
            tokens = [root]
        else:
            tokens.append((int(token[0]), token[1], token[4], int(token[6])))
    if len(tokens) > 1:
        yield tokens

def extract_contexts(corpus, vocab_file, threshold, linkers, content_words):
    vocab = set(read_vocabulary(vocab_file, threshold).keys())
    print("vocab:",len(vocab))
    contexts = []
    for i, sent in enumerate(read_conll(corpus)):
        #print(i, sent)
        sent_contexts = {}
        if i % 100000 == 0:
            print(i)
        for token in sent[1:]:
            word = token[1]
            par = sent[token[3]]
            if word not in vocab: continue
            #if relation == 'adpmod': continue # this is the prep. we'll get there (or the PP is crappy)
            if token[2] in content_words and par[1] in vocab and par[2] in linkers:
                if not par[0] in sent_contexts.keys():
                    sent_contexts[par[0]] = [par[1], word]
                else:
                    sent_contexts[par[0]].append(word)
                #print(par)
                while True:
                    if par[0] == 0:
                        break
                    else:
                        if par[2] in linkers:
                            """if not par[0] in sent_contexts.keys():
                                sent_contexts[par[0]] = [par[1], word]
                            else:
                                sent_contexts[par[0]].append(word)"""
                            par = sent[par[3]]
                            # print(par)
                        elif par[1] in vocab and par[2] in content_words:
                            if not par[0] in sent_contexts.keys():
                                sent_contexts[par[0]] = [par[1], word]
                            else:
                                sent_contexts[par[0]].append(word)
                            break
                        else:
                            break
            elif par[1] in vocab:
                if not par[0] in sent_contexts.keys():
                    sent_contexts[par[0]] = [par[1], word]
                else:
                    sent_contexts[par[0]].append(word)

        contexts.append(list(sent_contexts.values()))
        print("SENTENCE CONTEXTS: ")

    return contexts
"""def bag_of_words_contexts(corpus, vocab_file, threshold):
    vocab = set(read_vocabulary(vocab_file, threshold).keys())
    print("vocab:",len(vocab))
    contexts = []
    for i, sent in enumerate(read_conll(corpus)):"""