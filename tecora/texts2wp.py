import argparse
from pathlib import Path
import os
import spacy
from spacy.tokens import Doc

def writeFile(doc: Doc, outputfile: str, counter: int, title: str) -> None:
    """Write a spaCy Doc to a vertically formatted file with sentence and token annotations."""
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


def annotate_file(file_path: Path, model: str = "de_core_news_sm") -> Doc:
    """Load a spaCy model, read a text file, and return the annotated Doc."""
    nlp = spacy.load(model)
    text = file_path.read_text(encoding="utf-8")
    return nlp(text)


def get_all_files(directory: str) -> list[Path]:
    """Recursively return all files under the given directory."""
    return [p for p in Path(directory).rglob("*") if p.is_file()]

def annotate_folder(inputdir, outputdir, spacymodel: str):
    """Annotate all files in inputdir with spaCy and write the results to outputdir, preserving the directory structure."""
    files = get_all_files(inputdir)

    counter = 0
    for f in files:
        counter += 1
        print(f)
        outputfile = str(f).replace(inputdir, outputdir )        
        doc = annotate_file(f, spacymodel)
        writeFile(doc, outputfile, counter, os.path.basename(f))  
        print(outputfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputdir", help="Input directory")
    parser.add_argument("outputdir", help="Output directory")
    parser.add_argument("spacymodel", help="The Spacy model to use")
    args = parser.parse_args()

    annotate_folder(args.inputdir, args.outputdir, args.spacymodel)

    print("Done.")
