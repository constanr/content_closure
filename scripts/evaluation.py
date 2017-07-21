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
    print("Trained with "+str(count)+"/"+str(total_count)+" examples.")
    print("Correlation: %.4f pvalue: %.3e" % (spearman.correlation, spearman.pvalue))