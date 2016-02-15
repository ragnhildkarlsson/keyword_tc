import nltk


def string_to_index_term(words_string):
    return words_string.replace(" ","_")

def word_to_index_term(word):
    return word

def bigram_to_index_term(bigram):
    return bigram[0]+'_'+bigram[1]

def trigram_to_index_term(trigram):
    return trigram[0]+ '_' + trigram[1] + '_' + trigram[2]

def get_to_index_term_function(index_type):
    to_index_term_functions = {"word":word_to_index_term,
                               "bigram":bigram_to_index_term,
                               "trigram":trigram_to_index_term
                              }
    if not index_type in to_index_term_functions:
        raise NotImplemented("Not implemented index type: " + index_type)
    return to_index_term_functions[index_type]


def get_word_freq_dist(document_terms):
    return nltk.FreqDist(document_terms)

def get_bigram_freq_dist(document_terms):
    return nltk.FreqDist(nltk.bigrams(document_terms))

def get_trigram_freq_dist(document_terms):
    return nltk.FreqDist(nltk.trigrams(document_terms))


def get_to_freq_dist_function(index_type):
    to_freq_dist_functions = {"word":get_word_freq_dist,
                               "bigram":get_bigram_freq_dist,
                               "trigram":get_trigram_freq_dist
                              }

    if not index_type in to_freq_dist_functions:
        raise NotImplemented("Not implemented index type: " + index_type)
    return to_freq_dist_functions[index_type]

