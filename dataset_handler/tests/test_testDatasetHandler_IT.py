import pprint
from dataset_handler.test_dataset_handler import TestDatasetHandler
from unittest import TestCase


class TestTestDatasetHandler(TestCase):

    def test_get_all_test_documents(self):
        testing_dataset_handler = TestDatasetHandler("example_test_data_set")
        result = testing_dataset_handler.get_all_test_documents()
        expected_document_names = ["cat1","cat2","dog1","no_category1"]
        expected_document_names = set(expected_document_names)
        result = set(list(result.keys()))
        self.assertEqual(result,expected_document_names)

    def test_get_gold_standard_cateogorization(self):
        testing_dataset_handler = TestDatasetHandler("example_test_data_set")
        result = testing_dataset_handler.get_gold_standard_categorization()
        expected_cateogories = set(["cats", "dogs"])
        result_categories = set(result.keys())
        self.assertEqual(result_categories,expected_cateogories)

