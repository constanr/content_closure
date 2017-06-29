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
java_path = "C:/Program Files/Java/jdk1.8.0_131/bin/java.exe"
os.environ['JAVAHOME'] = java_path

stanford_parser = 'C:\StanfordParser\stanford-parser-full-2016-10-31\stanford-parser.jar'
parser_models = 'C:\StanfordParser\stanford-parser-full-2016-10-31\stanford-parser-3.7.0-models.jar'

def load_corpus(path):
    print("Loading corpus...")
    with open(path, 'r', encoding="utf8") as corpus_file:
        corpus = corpus_file.read().replace('---END.OF.DOCUMENT---', '').replace('\n', '')
    print(corpus)
    return corpus

def count_words(corpus, threshold):
    corpus_words = re.findall(r"[\w']+", corpus.lower())
    print(corpus_words)
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
    word_count = count_words(corpus, threshold)
    with open('CorpusSample.conll', encoding="utf-8") as conll_file:
        conll_dependencies = conll_file.readlines()
        print('conll: ', conll_dependencies[0])
    contexts = extract_deps.extract_contexts(conll_dependencies, word_count, threshold)
    print('contexts: ', contexts)

if __name__ == '__main__':
    corpus_path = 'CorpusSample.txt'
    threshold = 10
    corpus = load_corpus(corpus_path)
    contexts = create_vocabularies(corpus, threshold)

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