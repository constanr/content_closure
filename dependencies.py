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
from scripts import vocab, extract_deps
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

def count_words(corpus, threshold):
    print("Counting words...")
    corpus_words = re.findall(r"[\w']+", corpus.lower())
    return vocab.count(corpus_words, threshold)

#delete this
def parse_dependencies(corpus):
    dependency_parser = StanfordDependencyParser(path_to_jar=stanford_parser, path_to_models_jar=parser_models)
    for sentence in corpus.split('.'):
        print(sentence)
        result = dependency_parser.raw_parse(sentence)
        for dep in result:
            print(list(dep.triples()))
            #parsed_Sentence = [parse.tree() for parse in dependency_parser.raw_parse(sentence)]
            #print(parsed_Sentence)

#delete this
def text_to_conll(corpus):
    conll_corpus = ''
    index = 1
    words = re.findall(r"[\w']+|[.,!?;]", corpus)
    for word in words:
        conll_corpus += str(index)+'\t'+word+'\n'
        index += 1
        if word == '.':
            conll_corpus += '\n'
            index = 1
    return conll_corpus

def create_vocabularies(corpus, threshold):
    print("Creating vocabularies...")
    word_count = count_words(corpus, threshold)
    with open('CorpusSample.conll', encoding="utf-8") as conll_file:
        conll_dependencies = conll_file.readlines()
    contexts = extract_deps.extract_contexts(conll_dependencies, word_count, threshold)
    print('CONTEXTS: ', contexts[len(contexts) - 1])
    dep_context = ''
    for context in contexts:
        dep_context += '\t'.join(context)+'\n'
    print('contexts: ', dep_context)
    with open('dep.contexts', 'w', encoding="utf-8") as context_file:
        context_file.write(dep_context)
    call(["word2vecf/count_and_filter", "-train", "dep.contexts", "-cvocab", "cv", "-wvocab", "wv", "-min-count", "10"])

def train_embeddings():
    call(["word2vecf/word2vecf", "-train", "dep.contexts", "-wvocab", "wv", "-cvocab", "cv", "-output", "dim200vecs", "-size", "200", "-negative", "15",
          "-threads", "10", "-dumpcv", "dim200context-vecs"])

if __name__ == '__main__':
    #corpus_path = 'CorpusSample.txt'
    corpus_path = 'WestburyLab.Wikipedia.Corpus.txt'
    threshold = 10
    corpus = load_corpus(corpus_path)
    corpus_conll = load_corpus(corpus)
    print
    with open('WikipediaCorpus.conll', 'w', encoding="utf-8") as corpus_file:
        corpus_file.write(corpus_conll)
    #create_vocabularies(corpus, threshold)
    #train_embeddings()

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