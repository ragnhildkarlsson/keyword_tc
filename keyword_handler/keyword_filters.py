from cache import cache
from indexing.n_gram_handler import is_n_gram_part_in_term


def __frequent_term_filtering(new_reference_words, index, n_document_in_index, frequency_limit):
    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            reference_word_group = new_reference_words[category][reference_word_group_id]
            passed_filter = [r for r in reference_word_group if
                             r[0] not in index or (len(index[r[0]]) / n_document_in_index) <= frequency_limit]
            new_reference_words[category][reference_word_group_id] = passed_filter
    return new_reference_words


def _test_frequent_term_filtering(new_reference_words, index, n_document_in_index, frequency_limit):
    return __frequent_term_filtering(new_reference_words, index, n_document_in_index, frequency_limit)


""""
Reference word filters
removes the affected words from new_reference_words
"""

"""
Removes reference word that occure as seed to any category
:type new_reference_words: {"category":{reference word group id:[(new reference word, score)]}
"""


def seed_filter(given_reference_words, new_reference_words):
    all_seeds = set()
    for category in given_reference_words:
        for reference_word_group_id in given_reference_words[category]:
            for given_reference_word in given_reference_words[category][reference_word_group_id]:
                all_seeds.add(given_reference_word)

    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            reference_word_group = new_reference_words[category][reference_word_group_id]
            passed_filter = [r for r in reference_word_group if r[0] not in all_seeds]
            new_reference_words[category][reference_word_group_id] = passed_filter

    return new_reference_words


"""
Removes reference word that have higher score in an other reference word group
:type new_reference_words: {"category":{reference word group id:[(new reference word, score)]}
"""


def multiple_expansion_filter(new_reference_words):
    all_new_reference_words = {}
    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            for new_reference in new_reference_words[category][reference_word_group_id]:
                if new_reference[0] not in all_new_reference_words:
                    all_new_reference_words[new_reference[0]] = new_reference[1]
                elif new_reference[1] > all_new_reference_words[new_reference[0]]:
                    all_new_reference_words[new_reference[0]] = new_reference[1]

    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            reference_word_group = new_reference_words[category][reference_word_group_id]
            passed_filter = [r for r in reference_word_group if r[1] >= all_new_reference_words[r[0]]]
            new_reference_words[category][reference_word_group_id] = passed_filter
    return new_reference_words


"""
Removes reference word that have an higher doc frequency then the given frequency limit
:type new_reference_words: {"category":{reference word group id:[(new reference word, score)]}
"""


def freqent_term_filter(new_reference_words, index_directory, indices_id, frequence_limit):
    for index_id in indices_id:
        index = cache.load(index_directory, index_id)
        n_document_in_index = index["n_documents"]
        new_reference_words = __frequent_term_filtering(new_reference_words, index["index"], n_document_in_index,
                                                        frequence_limit)

    return new_reference_words


"""
Removes all reference word that is a n-gram and contains a given seed word from the same reference word group
:type new_reference_words: {"category":{reference word group id:[(new reference word, score)]}
"""


def no_n_gram_with_seed_filter(given_reference_words, new_reference_words):
    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            given_terms_for_group = given_reference_words[category][reference_word_group_id]
            new_reference_word_group = new_reference_words[category][reference_word_group_id]
            n_grams_with_seed = set()
            not_passed_filter = []
            for given_term in given_terms_for_group:
                not_passed_filter = not_passed_filter + [r for r in new_reference_word_group if
                                                         is_n_gram_part_in_term(r[0],
                                                                                given_term) or r in not_passed_filter]

            passed_filter = [r for r in new_reference_word_group if r not in not_passed_filter]
            new_reference_words[category][reference_word_group_id] = passed_filter

    return new_reference_words


"""
Removes all new reference words
:type new_reference_words: {"category":{reference word group id:[(new reference word, score)]}
"""


def no_new_reference_words(new_reference_words):
    for category in new_reference_words:
        for reference_word_group_id in new_reference_words[category]:
            new_reference_words[category][reference_word_group_id] = []
    return new_reference_words


def get_filter_id(filter):
    filters = {"seed_filtering": 0,
               "multiple_expansion_filter": 1,
               "frequent_term_filterin": 2,
               "no_n_gram_with_seed": 3,
               "no_new_reference_words": 4
               }

    if not filter in filters:
        raise NotImplemented("Keyword filter not implemented: " + filter)
    return filters[filter]


"""
    Return a map with the given reference_words together with the new reference wwords
    that pass the given filters, at the format:
    {
        "category":{
	    "id_reference_word_group_i" : ["r1","r2","r3",..r_i],
	    "id_reference_word_group_j" : ["r_i, r_j"]
	    }

	expect parameters at format:'

	index_spec:{
		"index_directory":
		"index_id": [index_id_1,index_id_2]
	},

    filter_spec:{
        "filter_1":{parameters:{"paramater":"parameter_value"},...
        }
    }

	given_refererence_words: {
		"category":{
			id_reference_word_group_i:["r1","r2","r3"],
			id_reference_word_group_j:["r1","r2","r3"]
		}

	new_refererence_words: {
		"category":{
			id_reference_word_group_i:[("r1",score),("r2",score),("r3",score)],
			id_reference_word_group_j:[("r1",score),("r2",score),("r3",score)]
		}
"""


def apply_reference_word_filters(filter_spec, given_reference_words, new_reference_words, index_spec, ):
    for filter in filter_spec:
        if filter == "seed_filter":
            new_reference_words = seed_filter(given_reference_words, new_reference_words)
        if filter == "multiple_expansion_filter":
            new_reference_words = multiple_expansion_filter(new_reference_words)
        if filter == "freqent_term_filter":
            parameters = filter_spec[filter]["parameters"]
            index_directory = index_spec["index_directory"]
            indices_id = index_spec["index_id"]
            frequency_limit = float(parameters["frequency_limit"])
            new_reference_words = freqent_term_filter(new_reference_words, index_directory, indices_id, frequency_limit)
        if filter == "no_n_gram_with_seed_filter":
            new_reference_words = no_n_gram_with_seed_filter(given_reference_words, new_reference_words)
        if filter == "no_new_reference_words":
            new_reference_words = no_new_reference_words(new_reference_words)

    return new_reference_words
