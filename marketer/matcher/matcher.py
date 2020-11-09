# coding: utf8
"""
General Matcher module cosisting Matcher classes
"""
from spacy.matcher import Matcher as SpacyMatcher


class Matcher:
    """Matcher superclass with rules for inheriting SpacyMatcher with rules"""

    def __init__(self, vocab, rules):
        self.matcher = SpacyMatcher(vocab, validate=True)
        self.rules = rules


class MainMatcher(Matcher):
    """Main Matcher used for applying main syntactic rules"""

    def __init__(self, vocab, rules):
        super().__init__(vocab, rules)
        self.initialize_main_rules__()

    def initialize_main_rules__(self):
        """Initializes main set of rules by adding them to SpacyMatcher object"""
        for rule_main_name, rule_set in self.rules.items():
            self.matcher.add(rule_main_name, [rule_set[rule_main_name]])


class SubMatcher(Matcher):
    """Sub Matcher used for applying sub-rules"""

    def add_sub_rules_for_rule(self, rule_name):
        """Add sub-rule from rules set for a given rule name"""
        for sub_rule_name, sub_rule in self.rules[rule_name].items():
            if sub_rule_name != rule_name:
                self.matcher.add(sub_rule_name, [sub_rule])

    def remove_sub_rules_for_rule(self, rule_name):
        """Remove all sub-rules for given rule name"""
        for sub_rule_name in self.rules[rule_name]:
            if sub_rule_name != rule_name:
                self.matcher.remove(sub_rule_name)
