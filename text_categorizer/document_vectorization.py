import math
from dataset_handler import dataset_id_handler
from indexing import index_operations
from indexing import n_gram_handler
from cache import cache


"""
    Returns a tf_idf_vector at the format of
    a map with a documents terms mapped to their tf_idf value if the term is present in the given index
"""

def get_tf_idf_vector(document_terms, index, max_frequence, n_documents):
    tf_idf_map = {}
    for term in document_terms:
        tf = 0
        idf = math.log(n_documents)
        if term in index and term not in tf_idf_map:
            posting_list = index[term]
            freq_term = sum([post[1] for post in posting_list])
            tf = 0.5 + 0.5*(freq_term/max_frequence)
            idf = math.log(1 + (n_documents/len(posting_list)))
        if term not in tf_idf_map:
            tf_idf_map[term] = tf * idf

    return tf_idf_map


def get_tf_idf_map_id(experiment_spec):
    id_data = dataset_id_handler.get_dataset_combination_id(experiment_spec)
    return "tf_idf" +"_" + id_data

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


def _calculate_tf_idf_vectors_per_index(document_tf_idf_vectors_map, document_terms_map, index_id, index_directory,max_frequency,):
    index = cache.load(index_directory,index_id)
    index_type = index["index_type"]
    to_frequency_distribution = n_gram_handler.get_to_freq_dist_function(index_type)
    to_index_term = n_gram_handler.get_to_index_term_function(index_type)
    n_documents_in_index = index["n_documents"]
    n_documents_left = len(document_terms_map)
    print("calculate if idf with index: "+ str(index_type))
    print("Number of documents to calculate vectors for "+ str(len(document_terms_map)))

    for document_id in document_terms_map:
        #TODO remove
        if(n_documents_left % 100) == 0 :
            print(n_documents_left)
        n_documents_left = n_documents_left -1
        document_terms = document_terms_map[document_id]
        frequncy_distribution = to_frequency_distribution(document_terms)
        document_terms = list(frequncy_distribution.keys())
        document_terms = [to_index_term(n_gram) for n_gram in document_terms]
        if not document_id in document_tf_idf_vectors_map:
            document_tf_idf_vectors_map[document_id] = get_tf_idf_vector(document_terms, index["index"],max_frequency,n_documents_in_index)
        else:
            document_tf_idf_vectors_map[document_id].update(get_tf_idf_vector(document_terms, index["index"],max_frequency,n_documents_in_index))

    return document_tf_idf_vectors_map


def get_docs_id_tf_idf_map(document_terms_map, indices_id, index_directory):
    document_tf_idf_vectors_map = {}

    max_frequency = __get_max_frequency(indices_id,index_directory)
    print("TF_IDF creater calculated max frequency word in index")
    for index_id in indices_id:
        document_tf_idf_vectors_map = _calculate_tf_idf_vectors_per_index(document_tf_idf_vectors_map,document_terms_map,index_id,index_directory, max_frequency)
        print("TF_IDF creater calculated tf_idf_vector for index:"+ index_id)

    return document_tf_idf_vectors_map
