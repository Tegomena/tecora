import tecora.wp as wp
import sys

if __name__ == "__main__":

    subcorpora = wp.getFiles(sys.argv[1])

       # Iteration über alle Dateien:
    for subcorpus in subcorpora:
        print("Subcorpus: " + subcorpus)
        # Erstellen des Subcorpus-Objekts, Einlesen der Datei:
        sub = wp.Subcorpus(subcorpus)
        # Iteration über die Artikel im Subcorpus:
        for a in sub.artikel:
            print("Artikel: " + a.titel)

    print("Done.")