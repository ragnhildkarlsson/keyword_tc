from text_categorizer import document_keyword_simularity


def get_cosinus_categorization(tf_idf_vectors, reference_words, context_words):
    categorization =  document_keyword_simularity.get_cosinus_ranked_documents(tf_idf_vectors,reference_words,context_words)
    return categorization

def get_grep_categorization(freq_dists, index_types,reference_words,context_words):
    categorization = document_keyword_simularity.get_grep_ranked_documents(freq_dists,index_types,reference_words,context_words)
    return categorization

def get_categorization(categorization_method_name, test_document_representation, reference_words, context_words):
    if categorization_method_name == "cosinus":
        return document_keyword_simularity.get_cosinus_ranked_documents(test_document_representation,reference_words,context_words)
    if categorization_method_name == "grep":
        return document_keyword_simularity.get_grep_ranked_documents(test_document_representation,reference_words,context_words)
