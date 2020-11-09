import spacy
import pytest


def pytest_configure():
    pytest.nlp = spacy.load("en_core_web_md", disable=["ner"])
