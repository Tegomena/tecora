import os
import tempfile
import textwrap

import pytest

from tecora.wp import Article, Article, Sentence, Subcorpus, Token, getFiles


class TestToken:
    def test_attributes(self):
        t = Token("läuft", "laufen", "VERB")
        assert t.text == "läuft"
        assert t.lemma == "laufen"
        assert t.pos == "VERB"

    def test_str(self):
        t = Token("läuft", "laufen", "VERB")
        assert str(t) == "läuft laufen VERB"


class TestSentence:
    def test_empty(self):
        s = Sentence()
        assert s.tokens == []

    def test_str_empty(self):
        assert str(Sentence()) == ""

    def test_str_with_tokens(self):
        s = Sentence()
        s.tokens.append(Token("Das", "das", "DET"))
        s.tokens.append(Token("Haus", "Haus", "NOUN"))
        assert str(s) == "Das das DETHaus Haus NOUN"

    @pytest.fixture
    def sentence(self):
        s = Sentence()
        s.tokens.append(Token("Das", "das", "DET"))
        s.tokens.append(Token("alte", "alt", "ADJ"))
        s.tokens.append(Token("Haus", "Haus", "NOUN"))
        s.tokens.append(Token("steht", "stehen", "VERB"))
        return s

    def test_findPhrase_found_by_text(self, sentence):
        assert sentence.findPhrase(["alte", "Haus"]) == 1

    def test_findPhrase_found_at_start(self, sentence):
        assert sentence.findPhrase(["Das", "alte"]) == 0

    def test_findPhrase_single_token(self, sentence):
        assert sentence.findPhrase(["steht"]) == 3

    def test_findPhrase_not_found(self, sentence):
        assert sentence.findPhrase(["altes", "Haus"]) is None

    def test_findPhrase_wrong_order(self, sentence):
        assert sentence.findPhrase(["Haus", "alte"]) is None

    def test_findPhrase_by_lemma(self, sentence):
        assert sentence.findPhrase(["alt", "Haus"], use="lemma") == 1

    def test_findPhrase_lemma_not_found(self, sentence):
        assert sentence.findPhrase(["alte", "Haus"], use="lemma") is None

    def test_findPhrase_case_insensitive(self, sentence):
        assert sentence.findPhrase(["ALTE", "HAUS"], case=True) == 1

    def test_findPhrase_case_insensitive_phrase_lowercased(self, sentence):
        assert sentence.findPhrase(["das", "alte"], case=True) == 0

    def test_findPhrase_empty_phrase(self, sentence):
        assert sentence.findPhrase([]) is None

    def test_findPhrase_invalid_use(self, sentence):
        with pytest.raises(ValueError):
            sentence.findPhrase(["Haus"], use="pos")


class TestArticle:
    def test_title(self):
        a = Article("Berlin")
        assert a.title == "Berlin"

    def test_empty_sentences(self):
        a = Article("Berlin")
        assert a.sentences == []


class TestGetFiles:
    def test_returns_files(self, tmp_path):
        (tmp_path / "a.txt").write_text("x")
        (tmp_path / "b.txt").write_text("y")
        result = getFiles(str(tmp_path))
        assert len(result) == 2
        assert all(os.path.isfile(f) for f in result)

    def test_nested_files(self, tmp_path):
        subdir = tmp_path / "sub"
        subdir.mkdir()
        (subdir / "c.txt").write_text("z")
        result = getFiles(str(tmp_path))
        assert any("c.txt" in f for f in result)

    def test_empty_dir(self, tmp_path):
        assert getFiles(str(tmp_path)) == []


SAMPLE_WP = textwrap.dedent("""\
    <doc id="1" title="Berlin">
    <s id="1">
    Berlin\tBerlin\tPROPN\t_\t_
    ist\tsein\tAUX\t_\t_
    </s>
    <s id="2">
    Die\tdie\tDET\t_\t_
    Stadt\tStadt\tNOUN\t_\t_
    </s>
    </doc>
    <doc id="2" title="Hamburg">
    <s id="1">
    Hamburg\tHamburg\tPROPN\t_\t_
    </s>
    </doc>
""")


@pytest.fixture
def wp_file(tmp_path):
    p = tmp_path / "wiki_00"
    p.write_text(SAMPLE_WP, encoding="utf-8")
    return str(p)


class TestSubcorpus:
    def test_article_count(self, wp_file):
        sc = Subcorpus(wp_file)
        assert len(sc.articles) == 2

    def test_article_titles(self, wp_file):
        sc = Subcorpus(wp_file)
        titles = [a.title for a in sc.articles]
        assert titles == ["Berlin", "Hamburg"]

    def test_sentence_count(self, wp_file):
        sc = Subcorpus(wp_file)
        assert len(sc.articles[0].sentences) == 2
        assert len(sc.articles[1].sentences) == 1

    def test_token_text(self, wp_file):
        sc = Subcorpus(wp_file)
        first_sentence = sc.articles[0].sentences[0]
        assert first_sentence.tokens[0].text == "Berlin"
        assert first_sentence.tokens[1].text == "ist"

    def test_token_lemma_and_pos(self, wp_file):
        sc = Subcorpus(wp_file)
        t = sc.articles[0].sentences[0].tokens[0]
        assert t.lemma == "Berlin"
        assert t.pos == "PROPN"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            Subcorpus("/nonexistent/path/wiki_00")
