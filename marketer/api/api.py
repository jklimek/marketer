# coding: utf8
"""
Main REST api file
"""
import json
import spacy
from flask_cors import CORS
from flask import Flask, abort
from flask import request
from marketer.comparator.comparator import Comparator
from marketer.extractor.extractor import Extractor

# Initialize spacy nlp object
nlp = spacy.load("en_core_web_md", disable=["ner"])

# Create extractor object with dep injection of nlp object
extractor_object = Extractor(nlp)

# Create comparator object
comparator_object = Comparator()

# Create Flask app
app = Flask(__name__)
# Enable CORS
CORS(app)


def make_json_response(data):
    response = app.make_response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    return response


def check_input_data(input_data):
    if not request.data:
        abort(400)
    if "nouns_groups" not in request.json:
        error = {"error": "Please provide nouns_groups"}
        response = make_json_response(error)
        response.status_code = 400
        return response
    if "texts" not in request.json:
        error = {"error": "Please provide texts"}
        response = make_json_response(error)
        response.status_code = 400
        return response

    def check_input_data_correctness(input_data):
        if not isinstance(input_data["texts"], list):
            return False
        if not isinstance(input_data["nouns_groups"], dict):
            return False
        if not all(isinstance(t, str) for t in input_data["texts"]):
            return False
        return True

    if not check_input_data_correctness(request.json):
        error = {"error": "Please provide data in correct format"}
        response = make_json_response(error)
        response.status_code = 400
        return response
    return False

@app.route('/extract', methods=['POST'])
def extract_route():
    """REST route for extracting features from given texts and nouns_groups"""
    error_response = check_input_data(request.json)
    if error_response:
        return error_response
    nouns_groups = request.json["nouns_groups"]
    texts = request.json["texts"]

    # Extract
    properties = extractor_object.extract(texts, nouns_groups)

    # Prepare JSON serializable result from list of properties
    result = [property_obj.to_dict() for property_obj in properties]
    response = app.make_response(json.dumps(result))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route('/compare', methods=['POST'])
def compare_route():
    """REST route for comparing properties from given texts and nouns_groups"""
    error_response = check_input_data(request.json)
    if error_response:
        return error_response
    nouns_groups = request.json["nouns_groups"]
    texts = request.json["texts"]

    # Compare
    similarity_matrices = comparator_object.compare(texts, nouns_groups, extractor_object)

    # Prepare JSON serializable result from dict of NumPy arrays
    result = {metric_name: matrix.tolist() for (metric_name, matrix) in similarity_matrices.items()}
    response = app.make_response(json.dumps(result))
    response.headers['Content-Type'] = "application/json"
    return response


if __name__ == '__main__':
    app.run(port=5006)
