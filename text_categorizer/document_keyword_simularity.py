from operator import itemgetter
import math


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
    for category in ranked_documents:
        ranked_documents[category].sort(key=itemgetter(1), reverse=True)

    return ranked_documents