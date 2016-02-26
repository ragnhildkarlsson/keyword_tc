from keyword_handler import dice_keyword_generator


from evaluation import  evaluater
from experiment.prepare_resources import *
import specification_handler
from text_categorizer import text_categorizer
from result_handler import  result_analyser
import json


__INDEX_DIRECTORY_CACHE = "index"
__KEYWORD_DIRECTORY_CACHE = "keywords"
__TF_IDF_DIRECTORY_CACHE = "tf_idf"
__GOLD_STANDARD_CATEGORIZATION_CACHE = "gold_standard"
__CATEGORIZATIONS_CACHE = "categorizations"
__CATEGORY_HIEARACHY_SPECIFICATION = "category_hiearachy"
__EVALUATION_SCALE = 0.1


def print_to_json(directory):
    file_path ="data/temp/temp.json"
    with open(file_path, 'w') as temp_file:
        json.dump(directory, temp_file, sort_keys=True,indent=4)

def prepare_experiment_resources(experiment_spec):
    prepare_index(experiment_spec,__INDEX_DIRECTORY_CACHE)
    prepare_keywords(experiment_spec,__KEYWORD_DIRECTORY_CACHE,__INDEX_DIRECTORY_CACHE)
    prepare_tf_idf_vectors(experiment_spec,__TF_IDF_DIRECTORY_CACHE,__INDEX_DIRECTORY_CACHE,)
    prepare_gold_standard_categorization(experiment_spec,__GOLD_STANDARD_CATEGORIZATION_CACHE)

def do_categorization(experiment_spec):
    experiment_id = experiment_spec["id"]
    if cache.in_cache(__CATEGORIZATIONS_CACHE,experiment_id):
        print("categorization calculated for exeperiment "+ experiment_id)
        print_to_json(cache.load(__CATEGORIZATIONS_CACHE,experiment_id))
        return
    tf_idf_map_id = document_vectorization.get_tf_idf_map_id(experiment_spec)
    tf_idf_map = cache.load(__TF_IDF_DIRECTORY_CACHE,tf_idf_map_id)
    keyword_setup_id = experiment_spec["keywords"]["setup_id"]
    keyword_id = keyword_setup_id_generator.get_keyword_setup_id(keyword_setup_id,experiment_spec["training_dataset"])
    keywords = cache.load(__KEYWORD_DIRECTORY_CACHE, keyword_id)
    categorization = text_categorizer.get_categorization(tf_idf_map,keywords["reference_words"],keywords["context_words"])
    pprint.pprint(categorization)
    cache.write(__CATEGORIZATIONS_CACHE,experiment_id,categorization)

def do_evaluation(experiment_spec,evaluation_scale):
    experiment_id = experiment_spec["id"]
    test_dataset_id = dataset_id_handler.get_test_data_id(experiment_spec)
    categorization = cache.load(__CATEGORIZATIONS_CACHE,experiment_id)
    gold_standard_categorization = cache.load(__GOLD_STANDARD_CATEGORIZATION_CACHE,test_dataset_id)
    category_hiearchy = specification_handler.get_specification(__CATEGORY_HIEARACHY_SPECIFICATION,test_dataset_id)
    result = evaluater.get_evaluation(categorization,gold_standard_categorization,category_hiearchy,evaluation_scale)
    print_to_json(result)
    evaluation_levels = evaluater.get_evaluation_levels(evaluation_scale)
    result_analyser.print_evaluation_to_csv(experiment_id, result, evaluation_levels)
    result_analyser.print_analysis_result(experiment_id,result,evaluation_levels)



def run_experiment(experiment_id,evaluation_scale):
    experiment_directory = "experiments"
    experiment_spec = specification_handler.get_specification(experiment_directory,experiment_id)
    prepare_experiment_resources(experiment_spec)
    do_categorization(experiment_spec)
    do_evaluation(experiment_spec,evaluation_scale)

# def fix_olympic_games_1():
#     fix_file = "lk_original_imdb_imdb_220000_012"
#     # fix_file =  "lk_inflection_max_usability_imdb_220000_012"
#     result = dice_keyword_generator.fix_olympic_games_1(fix_file)
#     print_to_json(result)
#
# def fix_olympic_games_2():
#     # fix_file = "lk_original_imdb_imdb_220000_012"
#     fix_file =  "lk_inflection_imdb_imdb_220000_012"
#     result = dice_keyword_generator.fix_olympic_games_2(fix_file)
#     print_to_json(result)



# run_experiment("lk_original_220000", __EVALUATION_SCALE)
# # run_experiment("test_experiment_first_100_plots_basic")
# run_experiment("lk_inflection_max_usability",__EVALUATION_SCALE)

run_experiment("lk_original_220000_no_keyword_filters",__EVALUATION_SCALE)
#run_experiment("imdb_220000_ref_manual_inflections_context_dice_inflections",__EVALUATION_SCALE)