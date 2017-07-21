#dependencies = self.parser.parseToStanfordDependencies("Pick up the tire pallet.")
#tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]
#self.assertEqual(tupleResult, [('prt', 'Pick', 'up'),
#                               ('det', 'pallet', 'the'),
#                               ('nn', 'pallet', 'tire'),
#                               ('dobj', 'Pick', 'pallet')
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.parse.stanford import StanfordDependencyParser
import os
import re
from scripts import vocab, vecs2nps, extract_contexts, extract_deps, evaluation
from subprocess import call

java_path = "C:/Program Files/Java/jdk1.8.0_131/bin/java.exe"
os.environ['JAVAHOME'] = java_path

stanford_parser = 'C:\StanfordParser\stanford-parser-full-2016-10-31\stanford-parser.jar'
parser_models = 'C:\StanfordParser\stanford-parser-full-2016-10-31\stanford-parser-3.7.0-models.jar'

def load_corpus(path):
    print("Loading corpus...")
    with open(path, 'r', encoding="utf8") as corpus_file:
        corpus = corpus_file.read().replace('---END.OF.DOCUMENT---', '').replace('\n', '')
    return corpus

def count_words(conll_corpus, threshold):
    print("Counting words...")
    #corpus_words = re.findall(r"[\w']+", corpus.lower())
    corpus = []
    for line in conll_corpus:
        corpus.append(line.split('\t')[1])
    return vocab.count(corpus, threshold)

def create_vocabularies(conll_corpus, threshold):
    print("Creating vocabularies...")
    word_count = count_words(corpus, threshold)
    linkers = ["in"] #["in", "cc", "rp", "to"]
    content_words = ["nn"] #["nn", "nns", "nnp", "nnps", "jj", "jjr", "jjs"]
    contexts = extract_contexts.extract_contexts(conll_corpus, word_count, threshold, linkers, content_words)
    #contexts = extract_deps.extract_contexts(conll_dependencies, word_count, threshold)
    #print('CONTEXTS: ', contexts[len(contexts) - 1])
    dep_context = ''
    for sentence in contexts:
        for context in sentence:
            #print(context)
            dep_context += '\t'.join(context)+'\n'
    #print('contexts: ', dep_context)
    with open('dep.contexts', 'w', encoding="utf-8") as context_file:
        context_file.write(dep_context)
    call(["word2vecf/count_and_filter", "-train", "dep.contexts", "-cvocab", "cv", "-wvocab", "wv", "-min-count", "10"])

def train_embeddings(method, file):
    if method == "dependency":
        call(["word2vecf/word2vecf", "-train", "dep.contexts", "-wvocab", "wv", "-cvocab", "cv", "-output", "dim200vecs", "-size", "200", "-negative", "15",
              "-threads", "4", "-iters", "5", "-dumpcv", "dim200context-vecs"])
    elif method == "bow":
        call(["word2vecf/word2vec", "-train", file, "-output", "dim200vecs", "-size", "200", "-negative", "15", "-min-count", "10"
              "-threads", "4", "-iters", "5", "-dumpcv", "dim200context-vecs"])
    else:
        return
    vecs2nps.vecs2nps("dim200vecs", "vecs")

if __name__ == '__main__':
    #corpus_path = 'CorpusSample.txt'
    corpus_path = 'enwiki_dep.txt'
    threshold = 10
    """corpus = load_corpus(corpus_path)
    with open('WikipediaCorpus.conll', 'w', encoding="utf-8") as corpus_file:
            corpus_file.write(corpus_conll)"""
    with open(corpus_path, 'r', encoding="utf8") as corpus_file:
        corpus = corpus_file.readlines()
    create_vocabularies(corpus, threshold)
    #train_embeddings("bow", "enwiki.txt")
    train_embeddings("dependency", "enwiki_dep.txt")
    test_dataset1 = "wordsim353_sim_rel/wordsim_similarity_goldstandard.txt"
    test_dataset2 = "wordsim353_sim_rel/wordsim_relatedness_goldstandard.txt"
    test_dataset3 = "rg65"
    test_dataset4 = "public_datasets/men.txt"
    test_dataset5 = "public_datasets/rw.txt"
    evaluation.evaluate(test_dataset1)
    evaluation.evaluate(test_dataset2)
    evaluation.evaluate(test_dataset3)
    evaluation.evaluate(test_dataset4)
    evaluation.evaluate(test_dataset5)

#sentence = 'The government plan was a success.'

#sentence = texts[2]
#print(sentence)
"""
result = dependency_parser.raw_parse(sentence)
dep = result.__next__()
print(list(dep.triples()))
# GUI
for line in result:
       print(line)
       line.draw()

parsed_Sentence = [parse.tree() for parse in dependency_parser.raw_parse(sentence)]
print(parsed_Sentence)

# GUI
for line in parsed_Sentence:
        print(line)
        line.draw()"""