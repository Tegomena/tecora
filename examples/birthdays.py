"""
Extract birth and death dates from an annotated corpus in WP format.

Scans sentences for the birth marker (*) and death marker (†), parses the
surrounding tokens to recover day, month, year, and place, then writes one
row per detected person to birthdays.csv in the output directory.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import tecora.wp as wp


class Person:
    """Holds extracted birth and death metadata for one person."""

    def __init__(self):
        self.name = "NONE"
        self.birth_month = "NONE"
        self.birth_monthday = 0
        self.birth_year = 0
        self.birth_place = "NONE"
        self.death_month = "NONE"
        self.death_monthday = 0
        self.death_year = 0
        self.death_place = "NONE"


def extract_day(person: Person, sentence: wp.Sentence, sign: str) -> Person:
    """Parse birth or death information from a sentence and update *person*.

    Looks for a token that exactly matches *sign* (``*`` for birth, ``†`` for
    death) and then reads the tokens that follow it to extract day, month,
    year, and place.  Handles three common patterns found in Wikipedia:

    * ``( * 1899 )``                  — year only
    * ``( * 31. Oktober 1974 )``      — day, month, year
    * ``( * 31. Oktober 1974 in … )`` — day, month, year, place
    """
    MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"]
    
    tokens = sentence.tokens
    n = len(tokens)

    for i in range(n - 1):
        if tokens[i].text == sign and i + 5 <= n - 1:

            # ( * 1899 )
            if i - 1 >= 0 and i + 2 <= n - 1:
                if tokens[i - 1].text == "(" and tokens[i + 2].text == ")":
                    try:
                        year = int(tokens[i + 1].text)
                        if sign == "*":
                            person.birth_year = year
                        else:
                            person.death_year = year
                    except ValueError:
                        pass
                    return person

            # ( * 31. Oktober 1974 in Boppard )  or  ( * 1899 in Somewhere )
            monthday_str = tokens[i + 1].text.replace(".", "")
            try:
                monthday = int(monthday_str)
                if sign == "*":
                    person.birth_monthday = monthday
                else:
                    person.death_monthday = monthday

                if person.birth_monthday > 31:
                    person.birth_year = person.birth_monthday
                    person.birth_monthday = 0

                if person.death_monthday > 31:
                    person.death_year = person.death_monthday
                    person.death_monthday = 0
            except ValueError:
                pass

            if tokens[i + 2].text in MONTHS:
                if sign == "*":
                    person.birth_month = tokens[i + 2].text
                else:
                    person.death_month = tokens[i + 2].text

            try:
                year = int(tokens[i + 3].text)
                if sign == "*":
                    person.birth_year = year
                else:
                    person.death_year = year
            except ValueError:
                pass

            if tokens[i + 4].text == "in" or tokens[i + 1].text == "in":
                addition = 2 if tokens[i + 1].text == "in" else 5
                place_parts = []
                while i + addition <= n - 1:
                    t = tokens[i + addition].text
                    if t == ")" or t == ";":
                        break
                    place_parts.append(t)
                    addition += 1
                place = " ".join(place_parts).strip()
                if sign == "*":
                    person.birth_place = place
                else:
                    person.death_place = place

    return person


def main():
    """Entry point: parse arguments, iterate the corpus, write birthdays.csv."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--basedir", default="/data/wp-2022/annotated/", help="Path to the corpus")
    parser.add_argument("--outdir", default="/data/wp-2022/snpOutput/", help="Path to the output dir")
    args = parser.parse_args()

    print("Basedir:", args.basedir)

    
    outputfile = os.path.join(args.outdir, "birthdays.csv")
    print("Outfile:", outputfile)

    files = wp.getFiles(args.basedir)
    counter = 0

    with open(outputfile, "w", encoding="utf-8") as f:
        f.write("File\tName\tBirth_Day\tBirth_Month\tBirth_Year\tBirth_Place\tDeath_Day\tDeath_Month\tDeath_Year\tDeath_Place\n")
        for file in files:
            counter += 1
            print(counter, file)
            sc = wp.Subcorpus(file)

            for article in sc.articles:
                sentences = article.sentences
                for i, sentence in enumerate(sentences):
                    for token in sentence.tokens:
                        if "*" in token.text:
                            counter += 1
                            person = Person()
                            person = extract_day(person, sentence, "*")

                            if i <= len(sentences) - 2:
                                person = extract_day(person, sentences[i + 1], "†")

                            person.name = article.title.split("/")[-1]
                                                        
                            line = (                                
                                f"{file}/{article.title}\t"
                                f"{person.name}\t"
                                f"{person.birth_monthday}\t"
                                f"{person.birth_month}\t"
                                f"{person.birth_year}\t"
                                f"{person.birth_place}\t"
                                f"{person.death_monthday}\t"
                                f"{person.death_month}\t"
                                f"{person.death_year}\t"
                                f"{person.death_place}\n"
                            )
                            f.write(line)

    print("Found:", counter)
    print("Written to:", outputfile)
    print("Done.")

if __name__ == "__main__":
    main()
