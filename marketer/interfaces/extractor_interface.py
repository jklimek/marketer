# coding: utf8
"""
Extractor interface
"""


class ExtractorInterface:
    """Extractor interface"""

    def extract(self, texts, nouns_group):
        """Extract features for nouns groups from texts"""
