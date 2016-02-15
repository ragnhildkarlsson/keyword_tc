from unittest import TestCase

from indexing import index_operations


class TestIndexOperations(TestCase):

    def test_get_merged_posting_lists(self):
        postinglist_1 = [("0",5),("1",1),("2",2)]
        postinglist_2 =[("1",1),("3",3)]
        expected_merged_list= [("0",5),("1",2),("2",2),("3",3)]
        merged_list = index_operations.get_merged_posting_lists(postinglist_1,postinglist_2)
        self.assertEqual(merged_list,expected_merged_list)

    def test_get_merged_posting_lists_empty(self):
        postinglist_1 = [(0,5),(1,1),(2,2)]
        postinglist_2 =[]
        expected_merged_list= [(0,5),(1,1),(2,2)]
        merged_list_1 = index_operations.get_merged_posting_lists(postinglist_1,postinglist_2)
        merged_list_2 = index_operations.get_merged_posting_lists(postinglist_2,postinglist_1)
        self.assertEqual(merged_list_1,expected_merged_list)
        self.assertEqual(merged_list_2,expected_merged_list)

