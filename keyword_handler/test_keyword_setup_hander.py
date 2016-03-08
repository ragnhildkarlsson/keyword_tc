from unittest import TestCase
from keyword_handler import keyword_setup_handler

class Test_keyword_setup_hander(TestCase):

    def test_get_no_reference_words_in_context_words(self):
        r= "reference_words"
        c="context_words"
        group_0 = "0"

        test_setup ={r:{"cats":{ group_0 :["cat","cats"]}},c:{"cats":{group_0:["cat","mjao"]}}}
        expected = {r:{"cats":{ group_0 :["cat","cats"]}},c:{"cats":{group_0:["mjao"]}}}
        res = keyword_setup_handler.get_no_reference_word_in_context_words_setup(test_setup)
        expected[c]["cats"][group_0].sort()
        expected[r]["cats"][group_0].sort()
        res[r]["cats"][group_0].sort()
        res[c]["cats"][group_0].sort()
        self.assertEqual(expected, res)

    def test_get_all_reference_words_in_context_words(self):
        r= "reference_words"
        c="context_words"
        group_0 = "0"

        test_setup ={r:{"cats":{ group_0 :["cat","cats"]}},c:{"cats":{group_0:["mjao"]}}}
        expected = {r:{"cats":{ group_0 :["cat","cats"]}},c:{"cats":{group_0:["cat","cats","mjao"]}}}
        expected[c]["cats"][group_0].sort()
        expected[r]["cats"][group_0].sort()
        res = keyword_setup_handler.get_all_reference_word_in_context_word_setup(test_setup)
        res[r]["cats"][group_0].sort()
        res[c]["cats"][group_0].sort()

        self.assertEqual(expected[c], res[c])
