# coding: utf8
"""
Comparator module responsible for comparing properties
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

from marketer.interfaces.comparator_interface import ComparatorInterface


class Comparator(ComparatorInterface):
    """
    Comparator class
    """

    def compare(self, texts, nouns_groups, extractor_object):
        """
        Compare properties by their extracted features and return pairwise similarities matrices
        """
        # Extract
        properties = extractor_object.extract(texts, nouns_groups)

        texts = [p.text_description for p in properties]
        default_matrix = np.diagflat([1 for _ in range(len(properties))])
        nouns_groups_vectors = self.__prepare_noun_groups_vectors(properties, nouns_groups)

        if nouns_groups_vectors:
            cosine_similarity_matrix = self.__calculate_cosine_similarity(nouns_groups_vectors)
            euclidean_similarity_matrix = self.__calculate_euclidean_similarity(nouns_groups_vectors)
        else:
            cosine_similarity_matrix = default_matrix
            euclidean_similarity_matrix = default_matrix

        text_sim = self.__calculate_tf_idf_text_similarity(texts)

        return {
            "features_averaged_cosine_similarities": cosine_similarity_matrix,
            "features_averaged_euclidean_similarities": euclidean_similarity_matrix,
            "text_descriptions_similarities": text_sim
        }

    def __calculate_tf_idf_text_similarity(self, texts):
        """Calculate text tf-idf similarity matrix for texts list"""

        tf_idf_vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
        tfidf_pairwise_matrix = tf_idf_vectorizer.fit_transform(texts)
        result = (tfidf_pairwise_matrix * tfidf_pairwise_matrix.T).toarray()

        return result

    def __calculate_euclidean_similarity(self, nouns_groups_vectors):
        """Calculate averaged euclidean similarities for noun groups vectors"""

        features_vectors_list = [euclidean_distances(v) for _, v in nouns_groups_vectors.items()]

        # Lambda function for inversing euclidean distance resulting with euclidean similarity
        inverse_distance_f = np.vectorize(lambda i: 1.0 / (1.0 + i))
        euclidean_similarities_list = [inverse_distance_f(a) for a in features_vectors_list]

        # Here we could implement and use average with weights for noun groups
        # (i.e. "bathroom": 0.9, "garden": 0.5 ... )
        result = self.__average_list_of_matrices(euclidean_similarities_list)

        return result

    def __calculate_cosine_similarity(self, nouns_groups_vectors):
        """Calculate averaged cosine similarities for noun groups vectors"""
        features_vectors_list = [cosine_similarity(v) for _, v in nouns_groups_vectors.items()]

        # Here we could implement and use average with weights for noun groups
        # (i.e. "bathroom": 0.9, "garden": 0.5 ... )
        result = self.__average_list_of_matrices(features_vectors_list)

        return result

    @staticmethod
    def __prepare_noun_groups_vectors(properties, nouns_groups):
        """Prepare"""
        prop_features_list = [p.features for p in properties]
        ng_vectors = {noun_group: [] for noun_group in nouns_groups}
        for noun_group in nouns_groups:
            for props in prop_features_list:
                # Prepare ones vector for non existen features for given property
                vector = np.ones((300,), dtype="f")
                if noun_group in props:
                    # Calculate mean of all detected spans vectors
                    vector = np.mean([p.vector for p in props[noun_group]], axis=0)
                ng_vectors[noun_group].append(vector)

        return ng_vectors

    @staticmethod
    def __average_list_of_matrices(m_list):
        """Simple linear average of list of matrices"""
        return np.array(m_list).sum(axis=0) / len(m_list)
