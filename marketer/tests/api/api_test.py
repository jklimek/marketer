import json
import pytest
from marketer.api.api import app


@pytest.fixture
def app_client():
    return app.test_client()


@pytest.fixture()
def wrong_indexes_json():
    return {
        "textss": [
            "Text1"
        ],
        "nouns_groupss": {
            "bathroom": [
                "bathroom",
                "bath"
            ]
        }
    }


@pytest.fixture()
def wrong_data_json():
    return {
        "texts": [
            "Text1"
        ],
        "nouns_groups": [
            [
                "bathroom",
                "bath"
            ]
        ]
    }


@pytest.fixture()
def good_extraction_example_json():
    return {
        "texts": [
            "Bathroom is beautiful"
        ],
        "nouns_groups": {
            "bathroom": [
                "bathroom"
            ]
        }
    }


@pytest.fixture()
def empty_extraction_example_json():
    return {
        "texts": [
            "Bathroom is a must"
        ],
        "nouns_groups": {
            "bathroom": [
                "bathroom"
            ]
        }
    }


def test_non_existent_route(app_client):
    response = app_client.get("/test_api_endpoint", content_type="html/text")
    assert response.status_code == 404


# Extract section

def test_extract_route_without_data(app_client):
    response = app_client.post("/extract")
    assert response.status_code == 400


def test_extract_route_with_wrong_indexes_data(app_client, wrong_indexes_json):
    response = app_client.post("/extract", json=wrong_indexes_json)
    assert response.status_code == 400
    assert response.is_json is True
    assert response.json["error"] in ["Please provide texts", "Please provide nouns_groups"]


def test_extract_route_with_wrong_data(app_client, wrong_data_json):
    response = app_client.post("/extract", json=wrong_data_json)
    assert response.status_code == 400
    assert response.is_json is True
    assert response.json["error"] in ["Please provide data in correct format"]


def test_extract_route_with_good_data(app_client, good_extraction_example_json):
    response = app_client.post("/extract", json=good_extraction_example_json)
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json[0]["features"] == {"bathroom": ["beautiful"]}


def test_extract_route_with_empty_data(app_client, empty_extraction_example_json):
    response = app_client.post("/extract", json=empty_extraction_example_json)
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json[0]["features"] == {}


# Compare section

@pytest.fixture()
def good_comparison_example_json():
    return {
        "texts": [
            "Bathroom is beautiful",
            "Bathroom is pretty"
        ],
        "nouns_groups": {
            "bathroom": [
                "bathroom"
            ]
        }
    }


@pytest.fixture()
def far_comparison_example_json():
    return {
        "texts": [
            "Bathroom is beautiful",
            "Bathroom is ugly"
        ],
        "nouns_groups": {
            "bathroom": [
                "bathroom"
            ]
        }
    }


@pytest.fixture()
def empty_comparison_example_json():
    return {
        "texts": [
            "Bathroom is beautiful",
            "Bathroom is pretty"
        ],
        "nouns_groups": {}
    }


def test_compare_route_without_data(app_client):
    response = app_client.post("/compare")
    assert response.status_code == 400


def test_compare_route_with_wrong_indexes_data(app_client, wrong_indexes_json):
    response = app_client.post("/compare", json=wrong_indexes_json)
    assert response.status_code == 400
    assert response.is_json is True
    assert response.json["error"] in ["Please provide texts", "Please provide nouns_groups"]


def test_compare_route_with_wrong_data(app_client, wrong_data_json):
    response = app_client.post("/compare", json=wrong_data_json)
    assert response.status_code == 400
    assert response.is_json is True
    assert response.json["error"] in ["Please provide data in correct format"]


def test_compare_route_with_good_data(app_client, good_comparison_example_json):
    response = app_client.post("/compare", json=good_comparison_example_json)
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json["features_averaged_cosine_similarities"][0][1] > 0.5
    assert response.json["features_averaged_euclidean_similarities"][0][1] > 0.1


def test_compare_route_with_far_data(app_client, far_comparison_example_json):
    response = app_client.post("/compare", json=far_comparison_example_json)
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json["features_averaged_cosine_similarities"][0][1] < 0.5
    assert response.json["features_averaged_euclidean_similarities"][0][1] < 0.2


def test_compare_route_with_empty_data(app_client, empty_comparison_example_json):
    response = app_client.post("/compare", json=empty_comparison_example_json)
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json["features_averaged_cosine_similarities"][0][1] == 0
    assert response.json["features_averaged_euclidean_similarities"][0][1] == 0
