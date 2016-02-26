from text_categorizer import document_keyword_simularity


def get_categorization(tf_idf_vectors,reference_words, context_words):
    categorization =  document_keyword_simularity.get_cosinus_ranked_documents(tf_idf_vectors,reference_words,context_words)
    return categorization
