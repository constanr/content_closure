import nltk

def normalized():
    with open("eswiki.txt", "r", encoding="utf-8", errors="surrogatepass") as r, open("eswiki_normalized.txt", "w", encoding="utf-8", errors="surrogatepass") as w:
        for line in r:
            w.write(" ".join(nltk.wordpunct_tokenize(line.lower()))+"\n")
