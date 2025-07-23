import pytest
import warnings
from utils.ling import type_token_ratio, average_sentence_length, get_np_counts, get_np_ratios


@pytest.mark.parametrize("tokens,expected", [
    (["the", "cat", "sat", "on", "the", "mat"], 5 / 6), # 5 unique tokens out of 6 total
    (["a", "b", "c", "d"], 1.0), # All unique tokens
    (["word"] * 10, 0.1), # All tokens are the same
    (["unique"], 1.0), # Single unique token
    (["Word", "word", "WORD"], 1 / 3), # Case insensitive, all the same
])
def test_type_token_ratio(tokens, expected):
    assert type_token_ratio(tokens) == expected

# In future commit, separate warning functionality from the main logic
def test_type_token_ratio_empty():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = type_token_ratio([])
        assert result == 0.0
        assert any("Empty token list" in str(warn.message) for warn in w)


@pytest.mark.parametrize("sentences,expected", [
    ([["the", "cat", "sat"], ["on", "the", "mat"]], 3.0),  # Two sentences, both length 3
    ([["a", "b", "c", "d"], ["e", "f", "g"]], 3.5),  # Lengths 4 and 3, avg 3.5
    ([["one", "two", "three", "four"], ["a", "b", "c", "d", "e"]], 4.5),  # Lengths 4 and 5, avg 4.5
    ([["a", "b", "c"]], 3.0),  # Single sentence
])
def test_average_sentence_length(sentences, expected):
    assert average_sentence_length(sentences) == expected

def test_average_sentence_length_empty():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = average_sentence_length([])
        assert result == 0.0
        assert any("Empty sentences list" in str(warn.message) for warn in w)


@pytest.mark.parametrize("text,expected", [
    ("The dog barked.", 1),  # Single sentence with 1 NP
    ("My brother and his dog walked to the park.", 3),  # Multiple NPs
])
def test_get_np_counts(text, expected):
    assert get_np_counts(text) == expected


@pytest.mark.parametrize("text,expected", [
    ("The tall man saw a cat.", 2 / 5),
    ("", None)
])
def test_np_ratio_nonzero(sentence, expected):
    ratios = get_np_ratios(sentence)
    assert ratios[0] == expected