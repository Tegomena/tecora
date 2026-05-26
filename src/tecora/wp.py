import re
import os

def getFiles(dirPath: str) -> list[str]:
    """
    Returns all files in a directory.
    """
    liste: list[str] = []
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            liste.append(os.path.join(root, file))
    return liste

class Token:
    """
    A token is a word with a lemma and a part-of-speech tag.
    """
    def __init__(self, text: str, lemma: str, pos: str) -> None:
        self.text = text
        self.lemma = lemma
        self.pos = pos

    def __str__(self) -> str:
        return self.text + " " + self.lemma + " " + self.pos

class Sentence:
    """
    A sentence is a list of tokens.
    """
    def __init__(self) -> None:
        self.tokens: list[Token] = []

    # nicht unbedingt nötig, aber nice to have:
    def __str__(self) -> str:
        temp = ""
        for t in self.tokens:
            temp = temp + str(t)
        return temp

class Article:
    """
    An article has a title and a list of sentences.
    """
    def __init__(self, titel: str) -> None:
        self.titel = titel
        self.sentences: list[Sentence] = []

class Subcorpus:
    """
    Represents a subcorpus (a file in the wp corpus) that can consist of multiple articles.
    """

    def __init__(self, filename: str) -> None:
        self.articles: list[Article] = []
        infile = open(filename, "r", encoding='utf-8')
        lines = infile.readlines()
        infile.close()

        satz = Sentence()
        a = Article("")

        satzCounter = 0
        artikelCounter = 0

        reg = re.compile(r'title="(.*)"')
        for line in lines:
            if line.startswith('<doc'):
                title = re.findall(reg, line)[0]
                a = Article(title)
            elif line.startswith('</doc'):
                self.articles.append(a)
                artikelCounter = artikelCounter + 1
            elif line.startswith('<s'):
                satzCounter = satzCounter + 1
            elif line.startswith('</s'):
                a.sentences.append(satz)
                satz = Sentence()
            else:
                rec = line.strip().split("\t")
                t = Token(rec[0], rec[1], rec[2])
                satz.tokens.append(t)


if __name__ == "__main__":
    """
    An example of how to use the Subcorpus class to read a file and print the articles, sentences and tokens. Change PATH_TO_A_WP_FILE to the path of a file in the wp corpus on your computer.
    """
    
    PATH_TO_A_WP_FILE = "D:/wp-2022/AA/wiki_00"
    c = Subcorpus(PATH_TO_A_WP_FILE)

    for a in c.articles:
        print("Titel: ", a.titel)
        print("Anzahl Sätze: ", len(a.sentences))
        print("Erster Satz: ")

        for t in a.sentences[0].tokens:
            print(t.text + " ", end="")
        print("")

        print("-----------------")


     