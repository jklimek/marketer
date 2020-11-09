import pytest
from marketer.comparator.comparator import Comparator
from marketer.extractor.extractor import Extractor


@pytest.fixture
def extractor_object():
    return Extractor(pytest.nlp)


@pytest.fixture
def comparator_object():
    return Comparator()


@pytest.fixture()
def nouns_groups():
    return {
        "bathroom": [
            "bathroom"
        ]
    }


@pytest.fixture()
def good_comparison_texts():
    return [
        "Bathroom is beautiful",
        "Bathroom is pretty"
    ]


@pytest.fixture()
def far_comparison_texts():
    return [
        "Bathroom is beautiful",
        "Bathroom is ugly"
    ]


def test_positive_comparison(comparator_object, extractor_object, nouns_groups, good_comparison_texts):
    similarity_matrices = comparator_object.compare(good_comparison_texts, nouns_groups, extractor_object)
    assert similarity_matrices["features_averaged_cosine_similarities"][0][1] > 0.5
    assert similarity_matrices["features_averaged_euclidean_similarities"][0][1] > 0.1


def test_far_comparison(comparator_object, extractor_object, nouns_groups, far_comparison_texts):
    similarity_matrices = comparator_object.compare(far_comparison_texts, nouns_groups, extractor_object)
    assert similarity_matrices["features_averaged_cosine_similarities"][0][1] < 0.5
    assert similarity_matrices["features_averaged_euclidean_similarities"][0][1] < 0.2
