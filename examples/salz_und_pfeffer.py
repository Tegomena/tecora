import argparse
import os
import tecora.wp as wp


def process(input_dir: str, output_dir: str, strings: list[str], property: str) -> None:
    out_filename = os.path.join(output_dir, "results.txt")
    true_counter = 0
    false_counter = 0
    with open(out_filename, "w", encoding="utf-8") as outfile:
        for filename in wp.getFiles(input_dir):
            print(filename)
            subcorpus = wp.Subcorpus(filename)
            for article in subcorpus.articles:
                for sentence in article.sentences:
                    if sentence.findPhrase(strings, use=property) is not None:
                        text = " ".join(t.text for t in sentence.tokens)
                        outfile.write(text + "\n")
                        true_counter += 1
                    else:
                        false_counter += 1
    print("Searched for: ", strings)
    print("Sentences with the phrase: ", true_counter)
    print("Sentences without the phrase: ", false_counter)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Input directory")
    parser.add_argument("output_dir", help="Output directory")
    
    parser.add_argument("strings", nargs="+", help="List of strings")
    parser.add_argument("--property", choices=["text", "lemma", "pos"], default="text", help="Token property to match against")
    
    args = parser.parse_args()


    process(args.input_dir, args.output_dir, args.strings, args.property)

    print("Done.")