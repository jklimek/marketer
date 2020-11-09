# coding: utf8
"""
Extractor module responsible for extracting features for gieven properties
"""
import spacy

from marketer.interfaces.extractor_interface import ExtractorInterface
from marketer.property.property import Property
from marketer.matcher.matcher import MainMatcher, SubMatcher


class Extractor(ExtractorInterface):
    """Extractor class"""

    def __init__(self, nlp_object):
        self.nlp = nlp_object
        self.__set_rules()
        # Create main rules matcher
        self.main_matcher = MainMatcher(self.nlp.vocab, self.rules)
        # Create empty sub matcher
        self.sub_matcher = SubMatcher(self.nlp.vocab, self.rules)

    def __set_rules(self, rules=False):
        if rules:
            self.rules = rules
        else:
            self.rules = {
                "nv_vna": {
                    "nv_vna": [
                        # NOUN
                        {'POS': {'IN': ['NOUN']}},
                        # AND 1
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # NOUN
                        {'POS': 'NOUN', 'OP': '*'},
                        # AND 2
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # NOUN
                        {'POS': 'NOUN', 'OP': '*'},
                        # AND 3 max
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # NOUN
                        {'POS': 'NOUN', 'OP': '*'},
                        # IS (VERB)
                        {'POS': 'AUX'},
                        {'POS': 'AUX', 'OP': '*'},
                        # ADV? ADJ
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['VERB', 'ADJ']}, 'OP': '*'},
                        # AND 1
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # ADV? ADJ
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['VERB', 'ADJ']}}
                    ],
                    "object": [
                        {'POS': {'IN': ['NOUN']}, 'OP': '+'}
                    ],
                    "feature": [
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['VERB', 'ADJ']}}
                    ]
                },
                "an": {
                    "an": [
                        # ADV? ADJ 1
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['ADJ', 'VERB']}, 'DEP': 'amod', 'OP': '*'},
                        # AND
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # ADV? ADJ 2
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['ADJ', 'VERB']}, 'OP': '*'},
                        # AND
                        {'POS': {'IN': ['CCONJ', 'CONJ', 'PUNCT']}, 'OP': '*'},
                        # ADV? ADJ 3 max
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['ADJ', 'VERB']}},
                        # NOUN
                        {'POS': 'NOUN', 'DEP': 'compound', 'OP': '*'},
                        {'POS': {'IN': ['NOUN', 'PROPN']}},
                    ],
                    "object": [
                        {'POS': {'IN': ['NOUN', 'PROPN']}, 'OP': '*'},
                        {'POS': {'IN': ['NOUN', 'PROPN']}}
                    ],
                    "feature": [
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': {'IN': ['NOUN']}, 'DEP': 'npadvmod', 'OP': '*'},
                        {'POS': {'IN': ['ADJ', 'VERB']}},
                    ]
                },
                "xn": {
                    "xn": [
                        # NUM
                        {'POS': {'IN': ['NUM']}, 'DEP': {'IN': ['quantmod', 'nummod']}, 'OP': '*'},
                        {'POS': {'IN': ['SYM']}, 'DEP': 'punct', 'OP': '*'},
                        {'POS': {'IN': ['NUM']}, 'DEP': 'nummod'},
                        # NOUN
                        {'POS': 'NOUN', 'DEP': 'compound', 'OP': '*'},
                        {'POS': {'IN': ['NOUN', 'PROPN']}},
                    ],
                    "object": [
                        {'POS': {'IN': ['NOUN', 'PROPN']}, 'OP': '*'},
                        {'POS': {'IN': ['NOUN', 'PROPN']}}
                    ],
                    "feature": [
                        {'POS': {'IN': ['NUM']}, 'DEP': {'IN': ['quantmod', 'nummod']}, 'OP': '*'},
                        {'POS': {'IN': ['SYM']}, 'DEP': 'punct', 'OP': '*'},
                        {'POS': {'IN': ['NUM']}, 'DEP': 'nummod'}
                    ]
                },
                # "pn_n": {
                #     "pn_n": [
                #         {'POS': {'IN': ['NOUN', 'PROPN']}, 'DEP': 'compound', 'OP': '+'},
                #         {'POS': {'IN': ['NOUN']}, 'DEP': 'compound', 'OP': '!'}
                #     ],
                #     "object": [
                #         {'POS': {'IN': ['NOUN']}, 'DEP': 'compound', 'OP': '!'}
                #     ],
                #     "feature": [
                #         {'POS': {'IN': ['NOUN', 'PROPN']}, 'DEP': 'compound', 'OP': '+'},
                #     ]
                # },
            }

    def extract(self, texts, nouns_group):
        """Extract features for given noun groups and
        property texts and return list of Properties"""
        properties = []
        for doc in self.nlp.pipe(texts):
            matches = self.main_matcher.matcher(doc)
            filtered_matches = self.__filter_matched_spans(matches, doc)
            features = self.__get_features_for_matches(
                filtered_matches, self.sub_matcher, nouns_group
            )
            property_obj = Property(doc.text, features)
            properties.append(property_obj)
        return properties

    def __filter_matched_spans(self, matches, doc):
        # Dict comprehension with rule name as a key and filtered list of spans as a value
        return {
            self.nlp.vocab.strings[match_id]:
            # Applying filtering method on spans list comprehension
                spacy.util.filter_spans(
                    [doc[start:end] for match_id_i, start, end in matches if match_id_i == match_id]
                )
            for match_id, _, _ in matches
        }

    def __get_sub_matches_results_for_span(self, sub_matches, span):
        result = {}
        for match_id, start, end in sub_matches:
            match_name = self.nlp.vocab.strings[match_id]
            if match_name not in result:
                result[match_name] = []
            result[match_name].append(span[start:end])
        # Filter only longest spans
        result = {k: spacy.util.filter_spans(v) for k, v in result.items()}
        return result

    @staticmethod
    def __update_object_results_with_sub_matches(sub_matches_result, object_results, nouns_map_):
        for obj in sub_matches_result['object']:
            if obj.lemma_ in nouns_map_:
                obj_base_name = nouns_map_[obj.lemma_]
                if obj_base_name not in object_results:
                    object_results[obj_base_name] = []
                object_results[obj_base_name] += [
                    # List comprehension of deduplicated matched features
                    feature for feature in sub_matches_result['feature']
                    # Deduplicate on the fly - check if given feature
                    # already exists based on lemma
                    if feature.lower_ not in [ftr.lower_ for ftr in object_results[obj_base_name]]
                ]
        return object_results

    def __get_features_for_matches(self, matches_, matcher_, nouns_groups_):
        object_results = {}
        for rule_name, spans in matches_.items():
            # Add sub rules
            matcher_.add_sub_rules_for_rule(rule_name)
            for span in spans:
                # Apply sub rules for detected spans
                sub_matches = matcher_.matcher(span)
                sub_matches_result = self.__get_sub_matches_results_for_span(sub_matches, span)
                object_results = self.__update_object_results_with_sub_matches(
                    sub_matches_result, object_results, self.flip_dict_of_lists(nouns_groups_)
                )
            # Remove sub rules from submatcher
            matcher_.remove_sub_rules_for_rule(rule_name)
        return object_results

    @staticmethod
    def flip_dict_of_lists(dictionary_to_flip):
        flipped_dict = {}
        for key_, list_ in dictionary_to_flip.items():
            for el_ in list_:
                flipped_dict[el_] = key_
        return flipped_dict
