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
    crete_new_keywords_spec["training_dataset"]["index_id"]= list(__get_all_index_specs(training_data_spec).keys())

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
    test_dataset_handler = TestDatasetHandler(test_data_id)
    test_documents = test_dataset_handler.get_all_test_documents()
    print("loaded test data")
    preprocessing_filter_names =  experiment_spec["training_dataset"]["filters"]
    for test_document_id in test_documents:
        test_document = test_documents[test_document_id]
        test_documents[test_document_id] = preprocessing_filters.apply_filters_to_document(test_document, preprocessing_filter_names)

    print("test data preprocessed")

    index_specs = __get_all_index_specs(experiment_spec["training_dataset"])
    index_indices = list(index_specs.keys())
    tf_idf_vector_map = document_vectorization.get_docs_id_tf_idf_map(test_documents, index_indices, index_cache_directory)
    pprint.pprint(tf_idf_vector_map)
    cache.write(tf_idf_cache_dirctory, tf_idf_vector_map_id, tf_idf_vector_map)


def prepare_gold_standard_categorization(experiment_spec, gold_standard_categorization_directory):
    test_data_id = dataset_id_handler.get_test_data_id(experiment_spec)
    if cache.in_cache(gold_standard_categorization_directory,test_data_id):
        print("Gold standard categorization in cache: "+ test_data_id)
        return
    test_dataset_handler = TestDatasetHandler(experiment_spec["test_dataset"]["id"])
    gold_standard_categorization = test_dataset_handler.get_gold_standard_categorization()
    pprint.pprint(gold_standard_categorization)
    cache.write(gold_standard_categorization_directory,test_data_id,gold_standard_categorization)
