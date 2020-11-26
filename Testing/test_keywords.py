import pytest
from BackEnd.functions.textprocessing import TextProcessor
import os


@pytest.fixture
def get_processor():
    return TextProcessor()


@pytest.fixture
def text_from_files():
    test_genre = "Vaccine"
    text = ""
    for_path = os.path.join("Testing_Data", test_genre, "For")
    for filename in os.listdir(for_path):
        source_text = open(os.path.join(for_path, filename), "r", encoding="utf-8")
        lines = source_text.readlines()
        text += lines[2]

    for_path = os.path.join("Testing_Data", test_genre, "Against")
    for filename in os.listdir(for_path):
        source_text = open(os.path.join(for_path, filename), "r", encoding="utf-8")
        lines = source_text.readlines()
        text += lines[2]

    return text


@pytest.mark.parametrize("keyword_count", [
    -1, 0, 5, 10, 50
])


# check correct number of key words are returned
def test_text_rank_keywords_number_of_results(get_processor, text_from_files, keyword_count):
    keywords_with_scores = get_processor.calculate_keywords_with_text_rank(text_from_files, keyword_count)
    keywords = [k for k, v in keywords_with_scores]
    if keyword_count < 1:
        assert len(keywords) == 0
    else:
        assert len(keywords) == keyword_count


# check all values of keywords are positive
def test_text_rank_keywords_values(get_processor, text_from_files):
    keywords_with_scores = get_processor.calculate_keywords_with_text_rank(text_from_files, 1_000)
    assert all(score >= 0 for key, score in keywords_with_scores)


# check all keywords are more than one character
def test_text_rank_keywords_length(get_processor, text_from_files):
    keywords_with_scores = get_processor.calculate_keywords_with_text_rank(text_from_files, 1_000)
    assert all(len(key) > 1 for key, score in keywords_with_scores)

# check vaccine is in the keywords returned from all documents to do with keywords