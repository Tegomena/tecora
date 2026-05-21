# tecora

A Python library for analyzing large text corpora using NLP annotation.

## Overview

tecora provides tools to annotate collections of plain-text files with [spaCy](https://spacy.io/) and work with the resulting annotated corpus. Text files are processed into a vertical XML format that stores token text, part-of-speech tags, and lemmas, which can then be read back into Python objects for further analysis.

## Workflow

1. **Annotate** a folder of plain-text files with `texts2wp.py` → produces vertically formatted XML files
2. **Analyze** the annotated output with the `wp` module → load corpus into `Subcorpus`, `Artikel`, `Satz`, and `Token` objects

## Output Format

Each annotated file follows this structure:

```xml
<doc id="1" title="filename.txt">
<s>
Token    POS    Lemma
...
</s>
</doc>
```

## Usage

### Annotating a corpus

```bash
python -m tecora.texts2wp <inputdir> <outputdir> <spacymodel>
```

| Argument | Description |
|---|---|
| `inputdir` | Directory containing plain-text input files (searched recursively) |
| `outputdir` | Directory where annotated output files will be written |
| `spacymodel` | spaCy model to use for annotation (e.g. `de_core_news_sm`) |

### Reading an annotated corpus

```python
from tecora.wp import Subcorpus

corpus = Subcorpus("path/to/annotated_file")

for article in corpus.artikel:
    print(article.titel)
    for sentence in article.saetze:
        for token in sentence.tokens:
            print(token.text, token.pos, token.lemma)
```

## Installation

Requires Python 3.13+.

```bash
pip install tecora
```

Install a spaCy language model, e.g. for German:

```bash
python -m spacy download de_core_news_sm
```

## Dependencies

- [spaCy](https://spacy.io/) >= 3.0
