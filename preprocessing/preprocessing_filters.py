import nltk
from nltk.corpus import stopwords

__NLTK_ENGLISH_STOP_WORDS = set(stopwords.words('english'))

def to_lowercase(terms):
    lower_case_terms = [t.lower() for t in terms]
    return lower_case_terms

def only_aplha(terms):
    only_alpha_terms = [t for t in terms if t.isalpha()]
    return only_alpha_terms

def filter_nltk_english_stopwords(terms):
    no_stopwords = [t for t in terms if t not in __NLTK_ENGLISH_STOP_WORDS]
    return no_stopwords



def __get_filter(filter_name):
    filters = {'to_lowercase' : to_lowercase,
               'only_alpha' : only_aplha,
               'filter_nltk_english_stopwords':filter_nltk_english_stopwords
               }
    if filter_name not in filters:
        raise NotImplemented("Not implemented filter: "+filter_name)
    return(filters[filter_name])

def get_filter_id(filter_name):
    filters = {'to_lowercase' : 0,
               'only_alpha' : 1,
               'filter_nltk_english_stopwords':2
               }
    if filter_name not in filters:
        raise NotImplemented("Not implemented filter: "+filter_name)
    return(filters[filter_name])


def apply_filters_to_document(document, filter_names):
    filters = [__get_filter(filter_name) for filter_name in filter_names]
    document_terms = nltk.word_tokenize(document)
    for filter in filters:
        document_terms = filter(document_terms)
    return document_terms