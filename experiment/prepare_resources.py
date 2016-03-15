import pprint

from cache import cache
from indexing import index_factory
from indexing import n_gram_handler
from keyword_handler import keyword_factory
from keyword_handler import keyword_setup_id_generator
from dataset_handler import dataset_id_handler
from dataset_handler.test_dataset_handler import TestDatasetHandler

from preprocessing import preprocessing_filters
from text_categorizer import document_vectorization
import specification_handler


__KEYWORD_SEEDS_DIRECTORY_SPECIFICATION = "keyword_seeds"


def __get_all_index_specs(training_data_spec):
    index_specs = {}
    index_types = ["word", "bigram", "trigram"]
    for index_type in index_types:
        index_spec_base = {}
        index_spec_base["dataset_id"] = training_data_spec["id"]
        index_spec_base["filters"] = training_data_spec["filters"]
        index_spec_base["index_type"] = index_type
        index_id = index_factory.get_index_id(index_spec_base)
        index_specs[index_id] = index_spec_base

    return index_specs

def __get_index_id_index_type(training_data_spec):
    index_specs = __get_all_index_specs(training_data_spec)
    result = {}
    for index_id in index_specs:
        result[index_id] = index_specs[index_id]["index_type"]
    return result


def get_all_index_indices(training_data_spec):
    index_indices= list(__get_all_index_specs(training_data_spec).keys())
    return index_indices


def prepare_index(experiment_spec, index_cache_directory):
    # Check that all indxes are created or init creation
    training_data_spec = experiment_spec["training_dataset"]
    index_specs = __get_all_index_specs(training_data_spec)
    for index_id in index_specs:
        index_spec = index_specs[index_id]
        if not cache.in_cache(index_cache_directory, index_id):
            index = index_factory.create_index(index_spec)
            cache.write(index_cache_directory, index_id, index)
            print("Created index " + index_id)
        else:
            print("Index present in cache " + index_id)

def seed_words_to_index_terms(given_seed_words):
    for category in given_seed_words:
        for group_id in given_seed_words[category]:
            given_seed_words[category][group_id] = [n_gram_handler.string_to_index_term(given_word) for given_word in given_seed_words[category][group_id]]
    return given_seed_words

def prepare_keywords(experiment_spec,keyword_cache_directory, index_cache_directory):
    keyword_spec = experiment_spec["keywords"]
    #if manual keywords
    keyword_method = keyword_spec["keyword_generate_algorithm"]
    if keyword_method == "manual":
        keywords = specification_handler.get_specification("keyword_setups",keyword_spec["setup_id"])
        keyword_setup_id = keyword_spec["setup_id"]
        keyword_id = keyword_setup_id_generator.get_keyword_setup_id(keyword_setup_id,experiment_spec["training_dataset"])
        cache.write(keyword_cache_directory,keyword_id,keywords)
        print("Manual keyword now stored in cache")
        return
    keyword_setup_id = keyword_spec["setup_id"]
    keyword_seed_id =keyword_spec["seed_id"]
    keyword_id = keyword_setup_id_generator.get_keyword_setup_id(keyword_setup_id,experiment_spec["training_dataset"])
    if cache.in_cache(keyword_cache_directory, keyword_id):
       print("Keyword stored in cache: "+keyword_id)
       keywords = cache.load(keyword_cache_directory,keyword_id)
       keyword_factory.print_keyword_setup_to_json(keyword_id,keywords)
       # keywords = keyword_factory.check_for_constructed_keyword_setup(keyword_id)
       # print(keywords)
       return

    crete_new_keywords_spec = {}

    training_data_spec = experiment_spec["training_dataset"]
    crete_new_keywords_spec["seed_id"] = keyword_spec["seed_id"]
    crete_new_keywords_spec["training_dataset"] = training_data_spec
    crete_new_keywords_spec["training_dataset"]["index_directory"] = index_cache_directory
    crete_new_keywords_spec["training_dataset"]["index_id"]= get_all_index_indices(training_data_spec)


    given_reference_words = specification_handler.get_specification(__KEYWORD_SEEDS_DIRECTORY_SPECIFICATION, keyword_seed_id)
    given_reference_words = seed_words_to_index_terms(given_reference_words)

    crete_new_keywords_spec["given_reference_words"] = given_reference_words
    crete_new_keywords_spec["keyword_generate_algorithm"] = keyword_spec["keyword_generate_algorithm"]
    crete_new_keywords_spec["parameters"] = keyword_spec["parameters"]
    crete_new_keywords_spec["reference_word_filter"] = keyword_spec["reference_word_filter"]
    keywords = keyword_factory.get_keywords(crete_new_keywords_spec,keyword_id)
    cache.write(keyword_cache_directory,keyword_id, keywords)

def prepare_tf_idf_vectors(experiment_spec,tf_idf_cache_dirctory,index_cache_directory):
    # Create test data handler

    tf_idf_vector_map_id = document_vectorization.get_tf_idf_map_id(experiment_spec)
    if cache.in_cache(tf_idf_cache_dirctory, tf_idf_vector_map_id):
        print( "TF_IDF_VECTORS stored in cache: " + tf_idf_vector_map_id)
        return
    test_data_id = dataset_id_handler.get_test_data_id(experiment_spec)
    preprocessing_filter_names =  experiment_spec["training_dataset"]["filters"]
    test_docuement_term_map = document_vectorization.get_test_document_term_map(test_data_id,preprocessing_filter_names)
    print("test data preprocessed")
    index_id_index_type_map = __get_index_id_index_type(experiment_spec["training_dataset"])
    index_types = ["word", "bigram", "trigram"]
    max_freq_map = index_factory.create_max_freq_term_by_index_types(test_docuement_term_map, index_types)
    print("max_freq_map_calculated")
    tf_idf_vector_map = document_vectorization.get_docs_id_tf_idf_map(test_docuement_term_map, index_id_index_type_map, index_cache_directory,max_freq_map)
    pprint.pprint(tf_idf_vector_map)
    cache.write(tf_idf_cache_dirctory, tf_idf_vector_map_id, tf_idf_vector_map)


def prepare_freq_dists(experiment_spec, freq_dists_cache_directory):
    freq_dist_map_id = document_vectorization.get_freq_dist_map_id(experiment_spec)
    if cache.in_cache(freq_dists_cache_directory, freq_dist_map_id):
        print( "FREQDISTS stored in cache: " + freq_dist_map_id)
        return
    test_data_id = dataset_id_handler.get_test_data_id(experiment_spec)
    preprocessing_filter_names =  experiment_spec["training_dataset"]["filters"]
    test_document_term_map = document_vectorization.get_test_document_term_map(test_data_id,preprocessing_filter_names)
    index_types = ["word", "bigram", "trigram"]
    freq_dist_map = document_vectorization.get_freq_dists_map(test_document_term_map,index_types)
    pprint.pprint(freq_dist_map)
    cache.write(freq_dists_cache_directory,freq_dist_map_id,freq_dist_map)


def prepare_gold_standard_categorization(experiment_spec, gold_standard_categorization_directory):
    test_data_id = dataset_id_handler.get_test_data_id(experiment_spec)
    if cache.in_cache(gold_standard_categorization_directory,test_data_id):
        print("Gold standard categorization in cache: "+ test_data_id)
        return
    test_dataset_handler = TestDatasetHandler(experiment_spec["test_dataset"]["id"])
    gold_standard_categorization = test_dataset_handler.get_gold_standard_categorization()
    pprint.pprint(gold_standard_categorization)
    cache.write(gold_standard_categorization_directory,test_data_id,gold_standard_categorization)
