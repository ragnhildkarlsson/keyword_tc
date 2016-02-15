import pprint
from unittest import TestCase

import specification_handler
from indexing import index_factory


class TestCreate_index(TestCase):

    # def test_create_index_trigram(self):
    #     test_specification = specification_handler.get_specification("experiments","test_experiment_first_100_plots_basic")
    #     test_specification = test_specification["training_dataset"]
    #     dataset_id = test_specification["id"]
    #     index_type = "word"
    #     filters = test_specification["filters"]
    #     index_specification = {"dataset_id":dataset_id,"filters":filters, "index_type":index_type}
    #     index = index_factory.create_index(index_specification)
    #     # print for debug
    #     pprint.pprint(index)

    def test_get_index_id(self):
        test_specification = specification_handler.get_specification("experiments","test_experiment_first_100_plots_basic")
        test_specification = test_specification["training_dataset"]
        dataset_id = test_specification["id"]
        index_type = "trigram"
        filters = test_specification["filters"]
        index_specification = {"dataset_id":dataset_id,"filters":filters, "index_type":index_type}
        index_id = index_factory.get_index_id(index_specification)
        expected_id = dataset_id + "_f_012" + "_it_3"
        self.assertEqual(index_id,expected_id)