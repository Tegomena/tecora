# test_wp.py

Unit tests for `src/tecora/wp.py`, covering all public classes and the `getFiles` utility.

## Running the tests

```bash
uv run pytest tests/test_wp.py -v
```

## Test structure

### `TestToken`

Tests the `Token` class, which represents a single annotated word with text, lemma, and part-of-speech tag.

| Test | Description |
|---|---|
| `test_attributes` | Constructor stores `text`, `lemma`, and `pos` correctly |
| `test_str` | `__str__` returns the three fields separated by spaces |

---

### `TestSentence`

Tests the `Sentence` class, which holds an ordered list of `Token` objects.

| Test | Description |
|---|---|
| `test_empty` | Newly created sentence has an empty token list |
| `test_str_empty` | `__str__` on an empty sentence returns an empty string |
| `test_str_with_tokens` | `__str__` concatenates the string representations of all tokens |

---

### `TestArticle`

Tests the `Article` class, which groups sentences under a title.

| Test | Description |
|---|---|
| `test_title` | Constructor stores the title correctly |
| `test_empty_sentences` | Newly created article has an empty sentence list |

---

### `TestGetFiles`

Tests the `getFiles` function, which recursively lists all files under a directory.

| Test | Description |
|---|---|
| `test_returns_files` | Returns all files directly inside a directory |
| `test_nested_files` | Recurses into subdirectories |
| `test_empty_dir` | Returns an empty list for an empty directory |

---

### `TestSubcorpus`

Tests the `Subcorpus` class, which parses a Wikipedia corpus file in the WP tab-separated format.

A sample WP file (two articles, three sentences total) is written to a temporary file by the `wp_file` fixture and reused across all tests in this class.

**Sample file format:**

```
<doc id="1" title="Berlin">
<s id="1">
Berlin	Berlin	PROPN	_	_
ist	sein	AUX	_	_
</s>
</doc>
```

| Test | Description |
|---|---|
| `test_article_count` | Correct number of articles is parsed from the file |
| `test_article_titles` | Article titles are extracted from the `title=` attribute |
| `test_sentence_count` | Each article contains the correct number of sentences |
| `test_token_text` | Token surface forms are read from the first tab-separated column |
| `test_token_lemma_and_pos` | Lemma (column 2) and POS tag (column 3) are stored correctly |
| `test_file_not_found` | Passing a non-existent path raises `FileNotFoundError` |

## Dependencies

- [pytest](https://docs.pytest.org/) — test runner
- Python standard library only (`os`, `re`, `tempfile`, `textwrap`)

The `tecora` package must be on the Python path. This is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
```
