import re
import os

def getFiles(dirPath):
    """
    Returns all files in a directory.
    """
    liste = []
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            liste.append(os.path.join(root, file))
    return liste

class Token:
    """
    A token is a word with a lemma and a part-of-speech tag.
    """
    def __init__(self, text, lemma, pos):
        self.text = text
        self.lemma = lemma
        self.pos = pos

    def toString(self):
        return self.text + " " + self.lemma + " " + self.pos 

class Satz:
    """
    A sentence is a list of tokens.
    """
    def __init__(self):
        self.tokens = []

    # nicht unbedingt nötig, aber nice to have:
    def toString(self):
        temp = ""
        for t in self.tokens:
            temp = temp + t.toString()
        return temp

class Artikel:
    """
    An article has a title and a list of sentences.
    """
    def __init__(self, titel):
        self.titel = titel
        self.saetze = []

class Subcorpus:
    """
    Represents a subcorpus (a file in the wp corpus) that can consist of multiple articles.
    """

    def __init__(self, filename):
        self.artikel = []
        infile = open(filename, "r", encoding='utf-8')
        lines = infile.readlines()
        infile.close()

        satz = Satz()
        a = Artikel("")

        satzCounter = 0
        artikelCounter = 0

        reg = re.compile(r'title="(.*)"')
        for line in lines:
            if line.startswith('<doc'):
                title = re.findall(reg, line)[0]
                a = Artikel(title)
            elif line.startswith('</doc'):
                self.artikel.append(a)
                artikelCounter = artikelCounter + 1
            elif line.startswith('<s'):
                satzCounter = satzCounter + 1
            elif line.startswith('</s'):
                a.saetze.append(satz)
                satz = Satz()
            else:
                rec = line.strip().split("\t")
                t = Token(rec[0], rec[1], rec[2])
                satz.tokens.append(t)


if __name__ == "__main__":
    c = Subcorpus("wiki_00")

    for a in c.artikel:
        print("Titel: ", a.titel)
        print("Anzahl Sätze: ", len(a.saetze))
        print("Erster Satz: ")

        for t in a.saetze[0].tokens:
            print(t.text + " ", end="")
        print("")

        print("-----------------")


     