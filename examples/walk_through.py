import tecora.wp as wp
import sys

if __name__ == "__main__":

    subcorpora = wp.getFiles(sys.argv[1])

    # Iterate over all files:
    for subcorpus in subcorpora:
        print("Subcorpus: " + subcorpus)
        # Create the Subcorpus object, read the file:
        sub = wp.Subcorpus(subcorpus)
        # Iterate over the articles in the subcorpus:
        for a in sub.articles:
            for s in a.sentences:
                for t in s.tokens:
                    print(t)
                
    print("Done.")