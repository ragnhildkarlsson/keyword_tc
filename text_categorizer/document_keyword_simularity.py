from operator import itemgetter
import math
from indexing import n_gram_handler


"""
Calculate simularity beetwen the given tf idf vector and a vecotr with all keyword set to 1
"""

def __get_cosinus_simularity(tf_idf_vector, key_words):
    sum_common_terms = 0
    sum_tf_idf_terms = 0
    for term in tf_idf_vector:
        if term in key_words:
            sum_common_terms += tf_idf_vector[term]
        sum_tf_idf_terms += math.pow(tf_idf_vector[term], 2)
    cosinus_similarity = sum_common_terms/(math.sqrt(sum_tf_idf_terms)+math.sqrt(len(key_words)))
    return cosinus_similarity


"""
 Return a map with the document ranked after cosinus simularity for each category based on the word in the documents
 and all the referene word groups and their corresponding context word.
 Caosinus simularity is calculated based on each seperate group, the document ranked to a category is sorted after
 simulrity to any sub group of keywords

"""

def get_cosinus_ranked_documents(tf_idf_map, reference_words, context_words):
    ranked_documents = {}
    for category in reference_words:
        ranked_documents[category] = []
        for document in tf_idf_map:
            for reference_word_group_id in reference_words[category]:
                reference_words_group = reference_words[category][reference_word_group_id]
                context_words_group = context_words[category][reference_word_group_id]
                referens_simularity = __get_cosinus_simularity(tf_idf_map[document],reference_words_group)
                context_simularity = 0
                if not referens_simularity == 0:
                    context_simularity = __get_cosinus_simularity(tf_idf_map[document], context_words_group)
                simularity = context_simularity*referens_simularity
                if(simularity != 0):
                    ranked_documents[category].append((document,simularity))

    #Sort ranked documents in ranked order
    ranked_documents = __sort_ranked_documents(ranked_documents)

    return ranked_documents



def __get_flat_keyword_map(keywords):
    flat_keyword_map =  {}
    for category in keywords:
        all_keywords = set()
        for word_group_id in keywords[category]:
            for word in keywords[category][ word_group_id]:
                all_keywords.add(word)
        flat_keyword_map[category] = all_keywords
    return flat_keyword_map

def __sort_ranked_documents(ranked_documents):
    for category in ranked_documents:
        ranked_documents[category].sort(key=itemgetter(1), reverse=True)
    return ranked_documents

def get_ranked_documents_by_keywords(test_document_freq_dists, flat_keywords):
    ranked_documents = {}
    for category in flat_keywords:
            ranked_documents[category] = {}

    for category in flat_keywords:
        for document_id in test_document_freq_dists:
            ranked_documents[category][document_id] = 0
            for index_type in test_document_freq_dists[document_id]:
                freq_dist = test_document_freq_dists[document_id][index_type]
                n_terms_in_document = sum([freq_dist[term] for term in freq_dist])
                for keyword in flat_keywords[category]:
                    if keyword in freq_dist:
                        ranked_documents[category][document_id] += (freq_dist[keyword]/n_terms_in_document)
    return ranked_documents

def __to_rank_list(ranking):
    for category in ranking:
        ranking[category] = list(ranking[category].items())
        ranking[category] = [ranked_doc for ranked_doc in ranking[category] if ranked_doc[1]>0]
    return ranking


def get_grep_ranked_documents(test_document_freq_dists, reference_words, context_words):

    flat_reference_words = __get_flat_keyword_map(reference_words)
    flat_context_words = __get_flat_keyword_map(context_words)
    reference_word_ranking = get_ranked_documents_by_keywords(test_document_freq_dists,flat_reference_words)
    context_word_ranking = get_ranked_documents_by_keywords(test_document_freq_dists, flat_context_words)
    #merge ranking
    for category in reference_word_ranking:
        for document_id in reference_word_ranking:
            if document_id in context_word_ranking[category]:
                reference_word_ranking[category][document_id] += context_word_ranking[category][document_id]

    ranked_documents = __to_rank_list(reference_word_ranking)
    ranked_documents = __sort_ranked_documents(ranked_documents)
    return ranked_documents
