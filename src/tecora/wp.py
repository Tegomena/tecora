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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.text == other.text and self.lemma == other.lemma and self.pos == other.pos

class Sentence:
    """
    A sentence is a list of tokens.
    """
    def __init__(self) -> None:
        self.tokens: list[Token] = []

    def findPhrase(self, phrase: list[str], use: str = "text", case: bool = False) -> int | None:
        """
        Returns the index of the first token of the phrase if found in exact
        order, or None if not found. use="text" matches against token text,
        use="lemma" matches against token lemma. If case is True, both the
        token values and the phrase are uppercased before comparison.
        """
        if use not in ("text", "lemma"):
            raise ValueError("use must be 'text' or 'lemma'")
        if not phrase:
            return None
        values = [getattr(t, use) for t in self.tokens]
        if case:
            values = [v.upper() for v in values]
            phrase = [p.upper() for p in phrase]
        n = len(phrase)
        for i in range(len(values) - n + 1):
            if values[i:i + n] == phrase:
                return i
        return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sentence):
            return NotImplemented
        return self.tokens == other.tokens

    def __str__(self) -> str:
        temp = ""
        for t in self.tokens:
            temp = temp + str(t)
        return temp

class Article:
    """
    An article has a title and a list of sentences.
    """
    def __init__(self, title: str) -> None:
        self.title = title
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


     