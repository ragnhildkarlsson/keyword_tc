import math
from dataset_handler import dataset_id_handler
from indexing import n_gram_handler
from cache import cache
from dataset_handler.test_dataset_handler import TestDatasetHandler
from preprocessing import preprocessing_filters

"""
    Returns a tf_idf_vector at the format of
    a map with a documents terms mapped to their tf_idf value if the term is present in the given index
"""

def __get_tf_idf_vector(freq_dist_document, index, max_frequency, n_documents):
    tf_idf_map = {}
    for term in freq_dist_document:
        tf = 0
        idf = math.log(n_documents)
        if term in index and term not in tf_idf_map:
            posting_list = index[term]
            tf = 0.5 + 0.5*(freq_dist_document[term]/max_frequency)
            idf = math.log(1 + (n_documents/len(posting_list)))
        if term not in tf_idf_map:
            tf_idf_map[term] = tf * idf

    return tf_idf_map


def get_tf_idf_map_id(experiment_spec):
    id_data = dataset_id_handler.get_dataset_combination_id(experiment_spec)
    return "tf_idf" +"_" + id_data

def get_freq_dist_map_id(experiment_spec):
    id_data = dataset_id_handler.get_dataset_combination_id(experiment_spec)
    return "freq_dist_map" +"_" + id_data



def __is_index_word_index(index_id, index_directory):
    index = cache.load(index_directory,index_id)
    return index["index_type"] == "word"

def __get_max_frequency(indices_id, index_directory):
    max_frequency = 0
    for index_id in indices_id:
        if __is_index_word_index(index_id,index_directory):
            index = cache.load(index_directory,index_id)
            max_frequency= index["max_frequency"]
    return max_frequency


def _calculate_tf_idf_vectors_per_index(document_tf_idf_vectors_map, freq_dists_map,
                                        index_id,index_directory,
                                        max_frequency_map):
    index = cache.load(index_directory,index_id)
    index_type = index["index_type"]
    n_documents_in_index = index["n_documents"]
    n_documents_left = len(freq_dists_map)
    print("calculate if idf with index: "+ str(index_type))
    print("Number of documents to calculate vectors for "+ str(len(freq_dists_map)))
    for document_id in freq_dists_map:
        #TODO remove
        if(n_documents_left % 100) == 0 :
            print(n_documents_left)
        n_documents_left = n_documents_left -1
        frequency_distribution = freq_dists_map[document_id][index_type]
        max_frequency = max_frequency_map[document_id][index_type]
        if not document_id in document_tf_idf_vectors_map:
            document_tf_idf_vectors_map[document_id] = __get_tf_idf_vector(frequency_distribution, index["index"], max_frequency, n_documents_in_index)
        else:
            document_tf_idf_vectors_map[document_id].update(__get_tf_idf_vector(frequency_distribution, index["index"], max_frequency, n_documents_in_index))
    return document_tf_idf_vectors_map


def get_docs_id_tf_idf_map(document_terms_map, index_id_type_map, index_directory, max_frequency_map):
    document_tf_idf_vectors_map = {}
    index_types = list(index_id_type_map.values())
    freq_dist_map = get_freq_dists_map(document_terms_map,index_types)
    print("TF_IDF creater calculated max frequency word in index")
    for index_id in index_id_type_map:
        index_type = index_id_type_map[index_id]
        document_tf_idf_vectors_map = _calculate_tf_idf_vectors_per_index(document_tf_idf_vectors_map,
                                                                          freq_dist_map,
                                                                          index_id,
                                                                          index_directory,
                                                                          max_frequency_map)

        print("TF_IDF creater calculated tf_idf_vector for index:"+ index_id)

    return document_tf_idf_vectors_map


def get_test_document_term_map(test_data_id, preprocessing_filter_names):
    test_dataset_handler = TestDatasetHandler(test_data_id)
    test_documents = test_dataset_handler.get_all_test_documents()
    print("loaded test data")
    for test_document_id in test_documents:
        test_document = test_documents[test_document_id]
        test_documents[test_document_id] = preprocessing_filters.apply_filters_to_document(test_document, preprocessing_filter_names)
    return test_documents


def get_freq_dists_map(document_terms_map, index_types):
    freq_dist_map = {}
    n_documents_left = len(document_terms_map)
    for document_id in document_terms_map:
        freq_dist_map[document_id]={}
        if(n_documents_left % 100) == 0 :
                print(n_documents_left)
        n_documents_left = n_documents_left -1
        document_terms = document_terms_map[document_id]
        for index_type in index_types:
            to_index_term = n_gram_handler.get_to_index_term_function(index_type)
            to_frequency_distribution = n_gram_handler.get_to_freq_dist_function(index_type)
            freq_dist_doc_terms = to_frequency_distribution(document_terms)
            freq_dist_terms = list(freq_dist_doc_terms.keys())
            freq_dist_index_terms = dict([(to_index_term(freq_dist_term),freq_dist_doc_terms[freq_dist_term]) for freq_dist_term in freq_dist_terms])
            freq_dist_map[document_id][index_type] = freq_dist_index_terms
    return freq_dist_map