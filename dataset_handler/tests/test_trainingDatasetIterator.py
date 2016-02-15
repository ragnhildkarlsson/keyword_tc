from unittest import TestCase

from dataset_handler.training_dataset_handler import TrainingDatasetIterator


class TestTrainingDatasetIterator(TestCase):

    def test_next(self):
        test_data_file = "test_case_example_data/first_100_plots.txt"
        encoding = "ISO-8859-1"
        subset_indices = set()
        subset_indices.add(0)
        subset_indices.add(7)
        subset_indices.add(22)
        subset_indices.add(100)
        test_iterator = TrainingDatasetIterator(test_data_file, encoding, subset_indices)
        expected = list(subset_indices)
        expected.sort()
        res_doc_inidices = list(map(lambda doc_data: doc_data[0], test_iterator))
        self.assertEqual(res_doc_inidices,expected)



