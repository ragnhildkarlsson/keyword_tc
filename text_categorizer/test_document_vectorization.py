import nltk
from unittest import TestCase
from text_categorizer import document_vectorization
import pprint


class Test_document_vectorization(TestCase):

    def test_get_freq_dists_map(self):
        test_documents = {1:"test document test dogs", 2: "test document test test cats"}
        test_document_terms =dict([(doc_id, nltk.word_tokenize(test_documents[doc_id])) for doc_id in test_documents])
        index_types = ["word","bigram","trigram"]
        res = document_vectorization.get_freq_dists_map(test_document_terms,index_types)
        expected_word_freq_doc_2 = {"test":3,"document":1,"cats":1}
        self.assertEqual(res[2]["word"], expected_word_freq_doc_2)
        expected = {1: {'bigram': {'document_test': 1, 'test_document': 1, 'test_dogs': 1},
                        'trigram': {'document_test_dogs': 1, 'test_document_test': 1},
                        'word': {'document': 1, 'dogs': 1, 'test': 2}},
                    2: {'bigram': {'document_test': 1,'test_cats': 1, 'test_document': 1, 'test_test': 1},
                        'trigram': {'document_test_test': 1,'test_document_test': 1,'test_test_cats': 1},
                        'word': {'cats': 1, 'document': 1, 'test': 3}}
                    }
        self.assertEqual(res,expected)