from subprocess import call
from os import listdir
from os.path import isfile, join
def split(corpus_name):
    with open(corpus_name,"r") as corpus:
        lines = corpus.readlines()
    print(len(lines))
    delimiter = "---END.OF.DOCUMENT---"
    file_count = 1
    document_count = 1
    file_text = ""
    for line in lines:
        if delimiter in line:
            if document_count % 1000 == 0:
                print("Document ", document_count)
                with open("corpus/" + corpus_name.strip(".txt") + "-" + str(file_count).zfill(4) + ".txt", "w") as target:
                    target.write(file_text)
                file_count += 1
                file_text = ""
            document_count += 1
        else:
            file_text += line

    with open("corpus/" + corpus_name + "-" + str(file_count).zfill(3) + ".txt", "w") as target:
        target.write(file_text)

def dependencies(corpus_path):
    files = [f for f in listdir(corpus_path) if isfile(join(corpus_path, f))]
    files.sort()
    print(files)
    for file in files:
        print(" ".join(["java", "-mx1g", "-cp", "\"/usr/share/stanford-parser-full-2017-06-09/*:\"", "edu.stanford.nlp.trees.EnglishGrammaticalStructure",
            "-basic", "-keepPunct", "-conllx", "-sentFile", "corpus/"+file]))
        call(["java", "-mx1g", "-cp", "\"/usr/share/stanford-parser-full-2017-06-09/*:\"", "edu.stanford.nlp.trees.EnglishGrammaticalStructure",
            "-basic", "-keepPunct", "-conllx", "-sentFile", "corpus/"+file])

#split("WestburyLab.Wikipedia.Corpus.txt")
dependencies("corpus")