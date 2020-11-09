import pytest
from marketer.extractor.extractor import Extractor


@pytest.fixture
def extractor_object():
    return Extractor(pytest.nlp)


@pytest.fixture
def dict_to_flip():
    return {
        "bathroom": [
            "bathroom",
            "bath"
        ]
    }


def test_dict_flipper(extractor_object, dict_to_flip):
    flipped = extractor_object.flip_dict_of_lists(dict_to_flip)
    assert flipped == {"bathroom": "bathroom", "bath": "bathroom"}


@pytest.fixture
def good_result_texts_n_groups():
    return ["Bathroom is beautiful"], {"bathroom": ["bathroom"]}


@pytest.fixture
def empty_result_texts_n_groups():
    return ["Bathroom is a must"], {"bathroom": ["bathroom"]}


def test_positive_extraction(extractor_object, good_result_texts_n_groups):
    extracted_properties = extractor_object.extract(*good_result_texts_n_groups)
    extracted_properties_list = [property_obj.to_dict() for property_obj in extracted_properties]
    assert extracted_properties_list == [
        {
            "text_description": "Bathroom is beautiful",
            "features": {
                "bathroom": [
                    "beautiful"
                ]
            }
        }
    ]


def test_negative_extraction(extractor_object, empty_result_texts_n_groups):
    extracted_properties = extractor_object.extract(*empty_result_texts_n_groups)
    extracted_properties_list = [property_obj.to_dict() for property_obj in extracted_properties]
    assert extracted_properties_list == [
        {
            "text_description": "Bathroom is a must",
            "features": {}
        }
    ]
