import numpy as np
from evaluation import evaluater
from unittest import TestCase


class TestEvaluater(TestCase):

    def test_get_precission_selection_indices_1(self):
        ranked_to_category = [('a',1),('b',0.9),('c',0.8),('d',0.7),('e',0.6),('f',0.5)]
        documents_in_category=['a','b','f']
        precission_levels=[0.1, 0.5, 0.6, 1.0]
        expected = {0:6,1:6,2:3,3:2}
        res = evaluater.get_precission_selection_indices(ranked_to_category, documents_in_category, precission_levels)
        self.assertEqual(res, expected)

    def test_get_precission_selection_indices_2(self):
        ranked_to_category = [('a',1),('b',0.9),('c',0.8),('d',0.7),('e',0.6),('f',0.5)]
        documents_in_category=['f']
        precission_levels=[0.1,1.0]
        expected = {0:6,1:0}
        res = evaluater.get_precission_selection_indices(ranked_to_category, documents_in_category, precission_levels)
        self.assertEqual(res, expected)

    def test_get_precission_selection_indices_3(self):
        ranked_to_category = []
        documents_in_category=['f']
        precission_levels=[0.1,1.0]
        expected = {0:0,1:0}
        res = evaluater.get_precission_selection_indices(ranked_to_category, documents_in_category, precission_levels)
        self.assertEqual(res, expected)

