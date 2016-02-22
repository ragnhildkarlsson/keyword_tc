import json
import os

from .dice_keyword_generator import get_dice_keywords


def get_keyword_generator_algorithm(algorithm_name):
    keyword_generator_algorithms = {
        "dice":get_dice_keywords
    }

    if not algorithm_name in keyword_generator_algorithms:
        raise NotImplemented("Keyword generator algorithm not implemented: " + algorithm_name)

    return keyword_generator_algorithms[algorithm_name]


def check_for_constructed_keyword_setup(keyword_id):
    file_path = os.path.join("data/keyword_setups", keyword_id + ".json")
    with open(file_path) as keyword_setup_file:
        keyword_setup = json.load(keyword_setup_file)
    return  keyword_setup

def print_keyword_setup_to_json(keyword_id, keyword_setup):
    print("prints keywords" + keyword_id)
    file_path = os.path.join("data/keyword_setups", keyword_id + ".json")
    with open(file_path, 'w') as keyword_setup_file:
        json.dump(keyword_setup, keyword_setup_file, sort_keys=True,indent=4)

"""

Returns a map of keywords matching the given specification

Expected format keyword_specification:
{
"training_dataset":{
    "id":"training_dataset_id",
    "filters":["to_lowercase", "only_alpha", "filter_nltk_english_stopwords"]
    "index_directory":
    "index_id"
},
"reference_words":{
    "category":{
        "reference_word_group_id":["r1","r2","r3"],
        "reference_word_group_id":["r1","r2","r3"]
    }
},
"keyword_generate_algorithm" :"keyword_generate_algorithm",
"parameters:{"parameter":"parameter_value"}
"reference_word_filter"{"filter_1":{"parameters":"parameter":"parameter value"},"filter_2":{}}
}

Returns given reference words together with generated kewywords at format:

{"reference_words":{
    "id_reference_word_group_i" : ["r1","r2","r3"],
    "id_reference_word_group_j" : ["r_i"]
    }

"context_words"{
    "id_reference_word_group_i":["c1","c2","ci"],
    "id_reference_word_group_i":["c1","c2","ci"]
    }
}
"""

def get_keywords(keyword_specification, keyword_setup_id):
    keyword_algorithm = get_keyword_generator_algorithm(keyword_specification["keyword_generate_algorithm"])
    keywords =  keyword_algorithm(keyword_specification)
    print_keyword_setup_to_json(keyword_setup_id, keywords)
    return keywords
