from operator import itemgetter
import nltk

from cache import cache
from indexing import n_gram_handler
from indexing import index_operations
from preprocessing import preprocessing_filters
from dataset_handler.training_dataset_handler import TrainingDatasetHandler
from keyword_handler import keyword_filters
from keyword_handler import keyword_setup_id_generator


__RAW_KEYWORD_CACHE = "keywords_no_filter"
__RAW_KEYWORD_BY_INDEX_CACHE = "raw_keywords_by_index"

"""
Returns a map with the merged posting lists for each reference word group in reference word spec
"""


def __get_reference_word_posting_lists(reference_words_spec, index_directory, indices_id):
    # Return a map of postings for each reference_word_group_id
    posting_lists={}
    # set up structure of posting list map
    for category in reference_words_spec:
        posting_lists[category] = {}

    for index_id in indices_id:
        index = cache.load(index_directory, index_id)
        index = index["index"]
        for category in reference_words_spec:
            reference_word_groups = reference_words_spec[category]
            for id_reference_word_group in reference_word_groups:
                if not id_reference_word_group in posting_lists[category]:
                    posting_lists[category][id_reference_word_group] = []
                for reference_word in reference_word_groups[id_reference_word_group]:
                    reference_term = n_gram_handler.string_to_index_term(reference_word)
                    if reference_term in index:
                        merged_postings = index_operations.get_merged_posting_lists(posting_lists[category][id_reference_word_group], index[reference_term])
                        posting_lists[category][id_reference_word_group] = merged_postings
    return posting_lists

"""
    Calculate the dice-coefficients between the given index_terms and the concept                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           represented by the given
    posting list
    Dice(w1,w1) = D(w1,w2) / (D(w1) + D(w2))
     where
      D(wi,wj) = Number of document with both wi and wj,
      D(wk) = Number of document with wk
"""

def __calculate_dice_coefficient(posting_list, index_term, index_map):
    term_posting_list = index_map[index_term]
    intersection = index_operations.intersection_search(posting_list, term_posting_list)
    dice_coefficient = len(intersection)/(len(term_posting_list) + len(posting_list))
    return dice_coefficient

"""
    Return a list with all terms in the given index that have a positive dice coefficient to the
    concept represented by the given posting list.
    The list is a list of tupples at the format (term,dice_coefficient)
     sorted in deccending order on dice_coefficients
"""

def __get_all_dice_neighbours(posting_list, index, trainingdata_handler, document_filters):
    dice_neighbours = {}
    index_type = index["index_type"]
    index_map = index["index"]
    to_index_term = n_gram_handler.get_to_index_term_function(index_type)
    to_freq_dist = n_gram_handler.get_to_freq_dist_function(index_type)
    for post in posting_list:
        document_file_id = str(post[0])
        document =  trainingdata_handler.get_training_data_file_string(document_file_id)
        document_terms = preprocessing_filters.apply_filters_to_document(document,document_filters)
        freq_dist = to_freq_dist(document_terms)
        documents_index_terms = [to_index_term(t) for t in freq_dist]
        for index_term in documents_index_terms:
            if index_term not in dice_neighbours and index_term in index_map:
                dice_coefficient = __calculate_dice_coefficient(posting_list,index_term,index_map)
                if dice_coefficient > 0:
                    dice_neighbours[index_term] = dice_coefficient

    dice_neighbours = list(dice_neighbours.items())
    dice_neighbours.sort(key=itemgetter(1), reverse=True)
    return dice_neighbours


def __calculate_top_n_dice_neighbours_for_index(temporary_keyword_cache_id,
                                                n, index_id, index_directory,
                                                posting_lists, trainingdata_handler,
                                                training_data_filters):
    top_dice_neighbours = {}
    for category in posting_lists:
        top_dice_neighbours[category] = {}
        for id_reference_word_group in posting_lists[category]:
            top_dice_neighbours[category][id_reference_word_group] = []
    index = cache.load(index_directory, index_id)
    print("Index id "+ index_id)
    n_categories_left = len(posting_lists)
    for category in posting_lists:
        posting_lists_category = posting_lists[category]
        #TODO remove
        print("Calculate keyword for category "+category)
        print("Number of categories left "+ str(n_categories_left))
        n_categories_left = n_categories_left -1
        for id_reference_word_group in posting_lists_category:
            posting_list_reference_word_group = posting_lists_category[id_reference_word_group]
            all_dice_neighbours = __get_all_dice_neighbours(posting_list_reference_word_group, index, trainingdata_handler, training_data_filters)
            top_dice_neighbours[category][id_reference_word_group] = all_dice_neighbours[:n]
    cache.write(__RAW_KEYWORD_BY_INDEX_CACHE,temporary_keyword_cache_id, top_dice_neighbours)


"""
Return the n closest dice neighbours to the refererence_word_groups for a category
"""

def __get_top_n_dice_neighbours(n, posting_lists, index_directory, indices_id, trainingdata_handler, training_data_filters, raw_keyword_id):
    # return a map of top n dice neighbours for each group of reference words

    #init top_dice_neighbours_structure
    top_dice_neighbours = {}
    for category in posting_lists:
        top_dice_neighbours[category] = {}
        for id_reference_word_group in posting_lists[category]:
            top_dice_neighbours[category][id_reference_word_group] = []

    for index_id in indices_id:
        temporary_keyword_cache_id = "temporary_cached_keywords"
        temporary_keyword_cache_id = temporary_keyword_cache_id + "_"+raw_keyword_id + "_"+index_id
        if not cache.in_cache(__RAW_KEYWORD_BY_INDEX_CACHE,temporary_keyword_cache_id):
            __calculate_top_n_dice_neighbours_for_index(temporary_keyword_cache_id,n,
                                                    index_id,index_directory,
                                                    posting_lists, trainingdata_handler,
                                                    training_data_filters)
        print("All keyword for index calculated "+ index_id)

    top_dice_neighbours_by_index = {}
    for index_id in indices_id:
        temporary_keyword_cache_id = "temporary_cached_keywords"
        temporary_keyword_cache_id = temporary_keyword_cache_id + "_"+raw_keyword_id + "_"+index_id
        top_dice_neighbours_by_index[index_id] = cache.load(__RAW_KEYWORD_BY_INDEX_CACHE,temporary_keyword_cache_id)


    for index_id in indices_id:
        present_top_dice_neighbours_by_index = top_dice_neighbours_by_index[index_id]
        for category in present_top_dice_neighbours_by_index:
            for id_reference_word_group in present_top_dice_neighbours_by_index[category]:
                top_dice_neighbours[category][id_reference_word_group] = top_dice_neighbours[category][id_reference_word_group] + present_top_dice_neighbours_by_index[category][id_reference_word_group]

    # sort dice neighbours after dice_coefficients and short to n neighbours
    for category in top_dice_neighbours:
        for id_reference_word_group in top_dice_neighbours[category]:
            top_dice_neighbours[category][id_reference_word_group].sort(key=itemgetter(1), reverse=True)
            top_dice_neighbours[category][id_reference_word_group] = top_dice_neighbours[category][id_reference_word_group][:n]
    return top_dice_neighbours


def __seperate_reference_and_context_words(top_dice_neighbours, weight_limit):
    new_reference_words = {}
    new_context_words = {}
    for category in top_dice_neighbours:
        new_reference_words[category] = {}
        new_context_words[category] = {}
        for id_reference_word_group in top_dice_neighbours[category]:
            top_dice_neighbours_group = top_dice_neighbours[category][id_reference_word_group]
            new_reference_words_group = [d for d in top_dice_neighbours_group if d[1]>= weight_limit]
            new_context_words_group = [d for d in top_dice_neighbours_group if d[1] < weight_limit]
            new_reference_words[category][id_reference_word_group] = new_reference_words_group
            new_context_words[category][id_reference_word_group] = new_context_words_group

    return new_reference_words, new_context_words


def __remove_dice_coefficients(key_words):
    keywords_without_score = {}
    for category in key_words:
        keywords_without_score[category]= {}
        for id_reference_wors_group in key_words[category]:
            keywords_with_score = key_words[category][id_reference_wors_group]
            keywords_without_score[category][id_reference_wors_group] = [k[0] for k in keywords_with_score]

    return keywords_without_score

def __merge_new_and_given_reference_words(given_reference_words, new_reference_words):
    merged_reference_words = {}

    for category in given_reference_words:
        merged_reference_words[category] = {}
        for id_reference_wors_group in given_reference_words[category]:
            given_reference_words_group = given_reference_words[category][id_reference_wors_group]
            new_reference_words_group = new_reference_words[category][id_reference_wors_group]
            merged_reference_words_set = set(given_reference_words_group + new_reference_words_group)
            merged_reference_words[category][id_reference_wors_group] = list(merged_reference_words_set)

    return  merged_reference_words


def __calculate_raw_dice_keywords(keyword_specification):
    # load paramters
    training_dataset_spec = keyword_specification["training_dataset"]
    index_directory = training_dataset_spec["index_directory"]
    indices_id = training_dataset_spec["index_id"]
    training_data_filters = training_dataset_spec["filters"]

    trainingdata_handler = TrainingDatasetHandler(training_dataset_spec["id"])

    given_reference_words = keyword_specification["given_reference_words"]
    weight_limit = float(keyword_specification["parameters"]["weight_limit"])
    max_number_of_key_words = int(keyword_specification["parameters"]["max_number_of_key_words"])


    keyword_seed_id = keyword_specification["seed_id"]
    raw_keywords_id = keyword_setup_id_generator.get_no_filtered_keywords_id(keyword_seed_id,training_dataset_spec)

    # Calculate keywords

    # calculate posting lists for reference word groups
    posting_lists = __get_reference_word_posting_lists(given_reference_words,index_directory,indices_id)
    print("Merged posting lists calculated")

    top_dice_neighbours = __get_top_n_dice_neighbours(max_number_of_key_words,
                                                     posting_lists,
                                                     index_directory,
                                                     indices_id,
                                                     trainingdata_handler,
                                                     training_data_filters,
                                                     raw_keywords_id)

    new_reference_words, new_context_words = __seperate_reference_and_context_words(top_dice_neighbours, weight_limit)

    return {"raw_reference_words": new_reference_words, "raw_context_words":new_context_words}

def fix_olympic_games_1(keywords_id):
    if cache.in_cache("keywords", keywords_id):
        keywords = cache.load("keywords", keywords_id)
        keyword_types = ["reference_words","context_words"]
        for keyword_type in keyword_types:
            if "olympic games" in keywords[keyword_type]:
                print("Fix olympic game in keyword directory " + keywords_id)
                olympic_keywords = keywords[keyword_type].pop("olympic games")
                keywords[keyword_type]["olympic_games"] = olympic_keywords
            for category in keywords[keyword_type]:
                keywords[keyword_type][category]['0'] = [keyword for keyword in keywords[keyword_type][category]['0'] if not " " in keyword]
        cache.write("keywords", keywords_id, keywords)
    return keywords

def fix_olympic_games_2(keywords_no_filter_id):
    if cache.in_cache(__RAW_KEYWORD_CACHE, keywords_no_filter_id):
        keywords= cache.load(__RAW_KEYWORD_CACHE, keywords_no_filter_id)
        keyword_types = list(keywords.keys())
        for keyword_type in keyword_types:
            if "olympic games" in keywords[keyword_type]:
                print("Fix olympic game in keyword directory " + keywords_no_filter_id)
                olympic_keywords = keywords[keyword_type].pop("olympic games")
                keywords[keyword_type]["olympic_games"] = olympic_keywords
            for category in keywords[keyword_type]:
                keywords[keyword_type][category]['0'] = [keyword for keyword in keywords[keyword_type][category]['0'] if not " " in keyword]
        cache.write(__RAW_KEYWORD_CACHE, keywords_no_filter_id, keywords)
    return keywords



"""
    Returns a map that contains
    Dice reference words Dice context words and the given seed reference words at the format

    {"reference_words":{
        "category":{
	    "id_reference_word_group_i" : ["r1","r2","r3",..r_i],
	    "id_reference_word_group_j" : ["r_i, r_j"]
	    }

    "context_words"{
        category:{
	    "id_reference_word_group_i":["c1","c2","ci"],
	    "id_reference_word_group_i":["c1","c2","ci"]
        }
    }

    The given keyword specificatation specify the settings for the dice keyword calcualation and filtering

    Expected format keyword_specification:
    {
    "id":"id for the given keywords setup"
	"training_dataset":{
		"id":"training_dataset_id",
		"filters":["to_lowercase", "only_alpha", "filter_nltk_english_stopwords"]
		"index_directory":
		"index_id": [index_id_1,index_id_2]
	},
	"given_reference_words":{
		"category":{
			id_reference_word_group_i:["r1","r2","r3"],
			id_reference_word_group_j:["r1","r2","r3"]
		}
	},
	{
	"parameters:{"weight_limit":"the dice_coefficient limit for seperating refererence and context words",
	            "max_number_of_key_words":"the maximum amount of new key words per reference word group"}
	"reference_word_filter"{"filter_1":{"parameters":"parameter":"parameter value"},"filter_2":{}}
    }

    Returns given reference words and dice kewywords at format:

"""


def get_dice_keywords(keyword_specification):

    training_dataset_spec = keyword_specification["training_dataset"]
    given_reference_words = keyword_specification["given_reference_words"]

    #Try load Keyword from cache else calculate
    keyword_seed_id = keyword_specification["seed_id"]
    raw_keywords_id = keyword_setup_id_generator.get_no_filtered_keywords_id(keyword_seed_id,training_dataset_spec)

    if cache.in_cache(__RAW_KEYWORD_CACHE, raw_keywords_id):
        raw_keywords = cache.load(__RAW_KEYWORD_CACHE,raw_keywords_id)
    else:
        raw_keywords = __calculate_raw_dice_keywords(keyword_specification)
        cache.write(__RAW_KEYWORD_CACHE, raw_keywords_id, raw_keywords)

    raw_reference_words = raw_keywords["raw_reference_words"]
    raw_context_words = raw_keywords["raw_context_words"]

    # Apply filter and clean from scores
    index_directory = training_dataset_spec["index_directory"]
    indices_id = training_dataset_spec["index_id"]
    index_spec = {"index_directory": index_directory, "index_id": indices_id}

    reference_words_filter = keyword_specification["reference_word_filter"]
    new_reference_words = keyword_filters.apply_reference_word_filters(reference_words_filter,given_reference_words,raw_reference_words,index_spec)

    new_reference_words = __remove_dice_coefficients(new_reference_words)
    new_context_words = __remove_dice_coefficients(raw_context_words)

    reference_words = __merge_new_and_given_reference_words(given_reference_words,new_reference_words)


    return {"reference_words":reference_words,"context_words":new_context_words}
