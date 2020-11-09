# coding: utf8
"""
Dataclass module for storing Property info
"""
from dataclasses import dataclass


@dataclass
class Property:
    """Property class used to store information about extracted property features and description"""
    text_description: str
    features: dict

    def to_dict(self):
        """Returns JSON serializable dictionary from Property object"""
        features = {
            noun_group: [
                s.lower_ for s in spans
            ] for (noun_group, spans) in self.features.items()
        }
        return {
            "text_description": self.text_description,
            "features": features
        }
