import pprint
from keyword_handler import keyword_filters

from unittest import TestCase


class TestKeywordFiltering(TestCase):

    def test_seed_filtering(self):
        given_reference_words = {"cat":{
                                    1:["animal","mjao"],
                                    2:["cat",]
                                },
                                "dog:":{
                                    1:["dog"]
                                }
                            }

        new_reference_words =  {"cat":{
                                    1:[("animal",0.1),("cat",0.5)],
                                    2:[("kitten",0.4),("jaguar",0.4)]
                                },
                                "dog:":{
                                    1:[("dog",0.5),("animal",0.5),("hound",0.5)]
                                }
                            }

        expected_reference_words = {"cat":{
                                        1:[],
                                        2:[("kitten",0.4),("jaguar",0.4)]
                                    },
                                        "dog:":{
                                        1:[("hound",0.5)]
                                    }
                                    }
        result = keyword_filters.seed_filter(given_reference_words, new_reference_words)
        self.assertEqual(expected_reference_words,result)

    def test_multiple_expansion_filter(self):

        new_reference_words =  {"cat":{
                                    1:[("animal",0.1),("cat",0.5)],
                                    2:[("kitten",0.4),("jaguar",0.4)]
                                },
                                "dog:":{
                                    1:[("dog",0.5),("animal",0.5),("hound",0.5)]
                                }
                            }

        expected_reference_words = {"cat":{
                                        1:[("cat",0.5)],
                                        2:[("kitten",0.4),("jaguar",0.4)]
                                    },
                                        "dog:":{
                                        1:[("dog",0.5),("animal",0.5),("hound",0.5)]
                                    }
                                    }

        result = keyword_filters.multiple_expansion_filter(new_reference_words)
        self.assertEqual(expected_reference_words,result)


    def test___freqent_term_filtering(self):

        frequency_limit = 0.1
        n_document_in_index = 100
        index = {}
        index["animal"]= list(zip(list(range(11)), list(range(11))))
        index["cat"] = list(zip(list(range(10)), list(range(10))))
        index["dog"] = list(zip(list(range(5)), list(range(5))))



        new_reference_words =  {"cat":{
                                    1:[("animal","_"),("cat","_")],
                                },
                                "dog:":{
                                    1:[("dog","_"),("animal","_"),]
                                }
                                }

        expected_reference_words =  {"cat":{
                                        1:[("cat","_")],
                                    },
                                    "dog:":{
                                        1:[("dog","_"),]
                                    }
                                    }

        result = keyword_filters._test_frequent_term_filtering(new_reference_words, index, frequency_limit, n_document_in_index)

        self.assertEqual(expected_reference_words, result)

    def test_no_n_gram_with_seed(self):

        given_reference_words = {"cat":{
                                    1:["cat","animal"],
                                },
                                "dog:":{
                                    1:["dog"]
                                }
                                }

        new_reference_words =  {"cat":{
                                    1:[('no_cat', "_"), ('cat_no', "_"), ('no_cat_no', '_'), ('jaguar', '_'),('animal_mjaou', '_')],
                                },
                                "dog:":{
                                    1:[("dog","_"),("doggy_bag","_"),("hound","_"),("animal_cat","_"),('doggy','_')]
                                }
                                }

        expected_reference_words =  {"cat":{
                                        1:[("jaguar","_")],
                                    },
                                    "dog:":{
                                        1:[("doggy_bag","_"),("hound","_"),('animal_cat','_'),('doggy','_')]
                                    }
                                    }

        result = keyword_filters.no_n_gram_with_seed_filter(given_reference_words, new_reference_words)
        self.assertEqual(expected_reference_words, result)
