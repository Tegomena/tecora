import argparse
from pathlib import Path
import os
import spacy

def writeFile(doc, outputfile, counter, title):
    output = open(outputfile, "w", encoding="utf-8")
    output.write("<doc id=\"" + str(counter) + "\"" + " title=\"" + title +  "\">\n")
    for s in doc.sents:
        output.write("<s>\n")
        for t in s:    
            temp = t.text + "\t" + t.pos_ + "\t" + t.lemma_             
            if t.pos_ != "SPACE":
                output.write(temp + "\n")
        output.write("</s>\n")
    output.write("</doc>")    
    output.close()


def annotate_file(file_path: Path, model: str = "de_core_news_sm") -> spacy.tokens.Doc:
    nlp = spacy.load(model)
    text = file_path.read_text(encoding="utf-8")
    return nlp(text)


def get_all_files(directory: str) -> list[Path]:
    return [p for p in Path(directory).rglob("*") if p.is_file()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputdir", help="Input directory")
    parser.add_argument("outputdir", help="Output directory")
    parser.add_argument("spacymodel", help="The Spacy model to use")
    args = parser.parse_args()

    files = get_all_files(args.inputdir)

    counter = 0
    for f in files:
        counter += 1
        print(f)
        outputfile = str(f).replace(args.inputdir, args.outputdir )
        print(outputfile)
        doc = annotate_file(f, args.spacymodel)
        writeFile(doc, outputfile, counter, os.path.basename(f))        

    print("Done.")
