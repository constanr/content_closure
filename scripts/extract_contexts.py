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

def read_conll(corpus, language):
    if language == "spanish":
        pos = 4
    elif language == "english":
        pos = 3
    else:
        print("Language "+language+" not identified.")
        return
    root = (0,'*root*','rroot', -1)
    tokens = [root]
    for line in corpus:
        line = line.lower()
        token = line.strip().split('\t')
        #print(token)
        if not token:
            if len(tokens) > 1: yield tokens
            tokens = [root]
        elif token[0]=="1":
            if len(tokens) > 1:
                yield tokens
            tokens = [root]
            tokens.append((int(token[0]), token[1], token[pos], int(token[6]), token[7]))
        elif len(token) == 10:
            #print(token)
            tokens.append((int(token[0]), token[1], token[pos], int(token[6]), token[7]))
    if len(tokens) > 1:
        yield tokens

def extract_contexts(corpus, vocab_file, threshold, linkers, content_words, language, output_file):
    vocab = set(read_vocabulary(vocab_file, threshold).keys())
    out = open(output_file, "w", encoding="utf-8")
    print("vocab:",len(vocab))
    #contexts = []
    for i, sent in enumerate(read_conll(corpus, language)):
        #print(i, sent)
        sent_contexts = {}
        if i%10000 == 0:
            print(i)#print(i, end='\r')
        for token in sent[1:]:
            word = token[1]
            par = sent[token[3]]
            rel = token[4]
            if word not in vocab: continue
            #if relation == 'adpmod': continue # this is the prep. we'll get there (or the PP is crappy)
            if token[2] in content_words and par[1] in vocab and par[2] in linkers:
                if not par[0] in sent_contexts.keys():
                    sent_contexts[par[0]] = [par[1], "_".join((rel, word))]
                    if not token[0] in sent_contexts.keys():
                        sent_contexts[token[0]] = [token[1], "I_".join((rel, par[1]))]
                    else:
                        sent_contexts[token[0]].append("I_".join((rel, par[1])))
                elif not token[0] in sent_contexts.keys():
                    sent_contexts[par[0]].append("_".join((rel, word)))
                    sent_contexts[token[0]] = [par[1], "I_".join((rel, par[1]))]
                else:
                    sent_contexts[par[0]].append("_".join((rel, word)))
                    sent_contexts[token[0]].append("I_".join((rel, par[1])))
                #print(par)
                while True:
                    if par[0] == 0 or par[0] == par[3]:
                        break
                    else:
                        if par[2] in linkers:
                            #if not par[0] in sent_contexts.keys():
                            #    sent_contexts[par[0]] = [par[1], word]
                            #else:
                            #    sent_contexts[par[0]].append(word)
                            if par[3] == sent[par[3]][0]:
                                break
                            par = sent[par[3]]
                            # print(par)
                        elif par[1] in vocab and par[2] in content_words:
                            if not par[0] in sent_contexts.keys():
                                sent_contexts[par[0]] = [par[1], "_".join(("cc", word))]
                                if not token[0] in sent_contexts.keys():
                                    sent_contexts[token[0]] = [token[1], "I_".join(("cc", par[1]))]
                                else:
                                    sent_contexts[token[0]].append("I_".join(("cc", par[1])))
                            elif not token[0] in sent_contexts.keys():
                                sent_contexts[par[0]].append("_".join(("cc", word)))
                                sent_contexts[token[0]] = [token[1], "I_".join(("cc", par[1]))]
                            else:
                                sent_contexts[par[0]].append("_".join(("cc", word)))
                                sent_contexts[token[0]].append("I_".join(("cc", par[1])))
                            break
                        else:
                            break
            elif par[1] in vocab:
                if not par[0] in sent_contexts.keys():
                    sent_contexts[par[0]] = [par[1], "_".join((rel, word))]
                    if not token[0] in sent_contexts.keys():
                        sent_contexts[token[0]] = [token[1], "I_".join((rel, par[1]))]
                    else:
                        sent_contexts[token[0]].append("I_".join((rel, par[1])))
                elif not token[0] in sent_contexts.keys():
                    sent_contexts[par[0]].append("_".join((rel, word)))
                    sent_contexts[token[0]] = [token[1], "I_".join((rel, par[1]))]
                else:
                    sent_contexts[par[0]].append("_".join((rel, word)))
                    sent_contexts[token[0]].append("I_".join((rel, par[1])))
            #print(sent_contexts)
        #contexts.append(list(sent_contexts.values()))
        for context in list(sent_contexts.values()):
            word = context[0]
            for cword in context[1:]:
                out.write(word + '\t' + cword + '\n')
    #print("SENTENCE CONTEXTS: ", len(contexts))
    out.close()

"""def bag_of_words_contexts(corpus, vocab_file, threshold):
    vocab = set(read_vocabulary(vocab_file, threshold).keys())
    print("vocab:",len(vocab))
    contexts = []
    for i, sent in enumerate(read_conll(corpus)):"""