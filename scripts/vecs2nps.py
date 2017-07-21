import numpy as np
import sys

def vecs2nps(embeddings_path, vectors_path):
    with open(embeddings_path) as embeddings:
        fh = embeddings.readlines()

    size=list(map(int,fh[0].strip().split()))

    wvecs=np.zeros((size[0],size[1]),float)

    vocab=[]
    for i,line in enumerate(fh[1:]):
        line = line.strip().split()
        vocab.append(line[0])
        wvecs[i,] = np.array(list(map(float,line[1:])))

    np.save(vectors_path+".npy",wvecs)
    with open(vectors_path+".vocab","w") as outf:
       outf.write(" ".join(vocab))