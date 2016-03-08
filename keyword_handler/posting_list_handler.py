from cache import cache
from indexing import n_gram_handler
from indexing import index_operations


"""
Returns a map with the merged posting lists for each word group in seed word spec
"""

def get_seed_words_posting_lists(seed_words_spec, index_directory, indices_id):
    # Return a map of postings for each reference_word_group_id
    posting_lists={}
    # set up structure of posting list map
    for category in seed_words_spec:
        posting_lists[category] = {}

    for index_id in indices_id:
        index = cache.load(index_directory, index_id)
        print("merging postining_list for index:")
        print(index["index_type"])
        index = index["index"]
        for category in seed_words_spec:
            reference_word_groups = seed_words_spec[category]
            for id_reference_word_group in reference_word_groups:
                if not id_reference_word_group in posting_lists[category]:
                    posting_lists[category][id_reference_word_group] = []
                for reference_word in reference_word_groups[id_reference_word_group]:
                    reference_term = n_gram_handler.string_to_index_term(reference_word)
                    if reference_term in index:
                        merged_postings = index_operations.get_merged_posting_lists(posting_lists[category][id_reference_word_group], index[reference_term])
                        posting_lists[category][id_reference_word_group] = merged_postings
    return posting_lists