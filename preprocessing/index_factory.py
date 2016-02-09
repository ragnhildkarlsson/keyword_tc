import nltk
from preprocessing import n_gram_handler
from preprocessing import TrainingDatasetHandler
from preprocessing import preprocessing_filters


def __get_index_type_id(index_type):
    index_types = {"word":1, "bigram":2, "trigram":3 }
    if not index_type in index_types:
        raise NotImplemented("Not implemented index type: " + index_type)
    return index_types[index_type]


def get_index_id(index_specification):
    dataset_id = index_specification["dataset_id"]
    filter_names = index_specification["filters"]
    index_type = index_specification["index_type"]
    filters_id = [preprocessing_filters.get_filter_id(filter_name) for filter_name in filter_names]
    filters_id.sort()
    filters_id = [str(filter_id) for filter_id in filters_id]
    filters_id = "".join(filters_id)
    index_id = dataset_id + "_f_" + filters_id + "_it_" + str(__get_index_type_id(index_type))
    return index_id



"""
Returns a index matching the given specification
Specification format:

{
    "dataset_id":"datatset_id",
    "filters":["filter1","filter2",...]
	"index_type: "word"/"bigram"/"trigram"
}

Index format

{   "id": index_id
    "dataset_id: dataset_id,
    "filters":["filter1","filter2",...]
    "index_format":"word"/"bigram"/"trigram"
    "index":{term:[(document_id, frequency)...] ...}
}

"""

def create_index(index_specification):
    dataset_id = index_specification["dataset_id"]
    index_type = index_specification["index_type"]
    filter_names = index_specification["filters"]

    index = {}

    # Save meta info about index
    index["id"] = get_index_id(index_specification)
    for key in index_specification:
        index[key] = index_specification[key]

    # Create traing data handler and assign index help methods according to index type

    training_dataset_handler = TrainingDatasetHandler(dataset_id)

    filters = [preprocessing_filters.get_filter(filter_name) for filter_name in filter_names]

    to_index_term = n_gram_handler.get_to_index_term_function(index_type)
    to_freq_dist = n_gram_handler.get_to_freq_dist_function(index_type)

    #create index
    index["index"] = {}
    for document_data in training_dataset_handler:
        document_id = document_data[0]
        document = document_data[1]
        document_terms = nltk.word_tokenize(document)
        for filter in filters:
            document_terms = filter(document_terms)
        freq_dist = to_freq_dist(document_terms)
        for document_term in freq_dist:
            index_term = to_index_term(document_term)
            if not index_term in index["index"]:
                index["index"][index_term] = []
            posting = (document_id, freq_dist[document_term])
            index["index"][index_term].append(posting)

    return index