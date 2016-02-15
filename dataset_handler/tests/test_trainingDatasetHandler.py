from dataset_handler.training_dataset_handler import TrainingDatasetHandler

from unittest import TestCase

class TestTrainingDatasetHandler(TestCase):

    def test___generate_subset_indices(self):
        seed = 5
        n_documents_in_set = 400
        n_documents_in_subset = 10
        set_1 = TrainingDatasetHandler.generate_subset_indices(n_documents_in_set,n_documents_in_subset,seed)
        set_2 = TrainingDatasetHandler.generate_subset_indices(n_documents_in_set,n_documents_in_subset,seed)

        self.assertEqual(set_1,set_2)
