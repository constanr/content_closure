from scripts import infer
import math
from scipy.stats import spearmanr, pearsonr

def evaluate(dataset):
    e = infer.Embeddings.load("vecs.npy")
    with open(dataset, encoding="utf-8") as dataset_file:
        test = list(dataset_file)
    gold_similarities = []
    test_similarities = []
    count = 0
    total_count = 0
    for line in test:
        total_count += 1
        line = line.strip().lower()
        tokens = line.split()
        try:
            sim = e.similarity(tokens[0], tokens[1])
            #print(tokens, sim)
            test_similarities.append(sim)
            gold_similarities.append(tokens[2])
            count += 1
        except ValueError as error:
            pass
    spearman = spearmanr(gold_similarities, test_similarities)
    print("Evaluated with "+str(count)+"/"+str(total_count)+" examples.")
    print("Correlation: %.4f pvalue: %.3e" % (spearman.correlation, spearman.pvalue))

def evaluate_analogies(dataset, language):
    e = infer.Embeddings.load("vecs.npy")
    with open(dataset, encoding="utf-8") as dataset_file:
        test = list(dataset_file)
    count = 0
    total_count = 0
    found_count = 0
    hits = 0
    name = ""
    results = {}
    for line in test:
        if line.startswith(":"):
            if name:
                results[name] = hits/count
                found_count += count
                print(name+"\t"+results[name])
                hits = 0
                count = 0
            name = line.strip(":").split()[0]
            continue
        tokens = line.lower().strip().split()
        total_count += 1
        try:
            if language == "english":
                if not name:
                    name = tokens[0]
                elif tokens[0] != name:
                    if count == 0:
                        results[name] = 0.0
                    else:
                        results[name] = hits/count
                    found_count += count
                    print(name+"\t"+str(results[name]))
                    hits = 0
                    count = 0
                    name = tokens[0]
                words = e.analogy(tokens[1], tokens[2], tokens[3])
                count += 1
                for i in range(4):
                    if words[i][1] == tokens[4]:
                        #print("Correct!")
                        #print(tokens[1], "is to", tokens[2], "as", tokens[3], "is to", tokens[4])
                        hits += 1
                        #print(hits/count)
                    if words[i][1] in tokens[1:4]:
                        continue
                    else:
                        break
            elif language == "spanish":
                words = e.analogy(tokens[0], tokens[1], tokens[2])
                count += 1
                for i in range(4):
                    if words[i][1] == tokens[3]:
                        # print("Correct!")
                        # print(tokens[1], "is to", tokens[2], "as", tokens[3], "is to", tokens[4])
                        hits += 1
                        #print(hits / count)
                    if words[i][1] in tokens[0:3]:
                        continue
                    else:
                        break

        except ValueError as error:
            pass

    results[name] = hits / count
    print(name + "\t" + str(results[name]))
    found_count += count
    print("Evaluated with "+str(found_count)+"/"+str(total_count)+" examples.")
    print(results)

