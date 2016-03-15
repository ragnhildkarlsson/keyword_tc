from keyword_handler import dice_keyword_generator


from evaluation import  evaluater
from keyword_handler import keyword_setup_handler
from experiment.prepare_resources import *
import specification_handler
from text_categorizer import text_categorizer
from result_handler import  result_analyser
from dataset_handler import test_data_filters
import json


__INDEX_DIRECTORY_CACHE = "index"
__KEYWORD_DIRECTORY_CACHE = "keywords"
__FREQ_DIST_CACHE = "freq_dists"
__TF_IDF_DIRECTORY_CACHE = "tf_idf"
__GOLD_STANDARD_CATEGORIZATION_CACHE = "gold_standard"
__CATEGORIZATIONS_CACHE = "categorizations"
__CATEGORY_HIEARACHY_SPECIFICATION = "category_hiearachy"
__EVALUATION_SCALE = 0.1


__KEYWORD_SEEDS_DIRECTORY_SPECIFICATION = "keyword_seeds"


def print_to_json(directory):
    file_path ="data/temp/temp.json"
    with open(file_path, 'w') as temp_file:
        json.dump(directory, temp_file, sort_keys=True,indent=4)

def prepare_experiment_resources(experiment_spec):
    prepare_index(experiment_spec,__INDEX_DIRECTORY_CACHE)
    prepare_keywords(experiment_spec,__KEYWORD_DIRECTORY_CACHE,__INDEX_DIRECTORY_CACHE)
    prepare_tf_idf_vectors(experiment_spec,__TF_IDF_DIRECTORY_CACHE,__INDEX_DIRECTORY_CACHE)
    prepare_freq_dists(experiment_spec,__FREQ_DIST_CACHE)
    prepare_gold_standard_categorization(experiment_spec,__GOLD_STANDARD_CATEGORIZATION_CACHE)

def do_categorization(experiment_spec):
    experiment_id = experiment_spec["id"]
    if cache.in_cache(__CATEGORIZATIONS_CACHE,experiment_id):
        print("categorization stored in cache for exeperiment "+ experiment_id)
        print_to_json(cache.load(__CATEGORIZATIONS_CACHE,experiment_id))
        return

    categorization_method_name = experiment_spec["catgorization_method"]
    keyword_setup_id = experiment_spec["keywords"]["setup_id"]
    keyword_id = keyword_setup_id_generator.get_keyword_setup_id(keyword_setup_id,experiment_spec["training_dataset"])
    keywords = cache.load(__KEYWORD_DIRECTORY_CACHE, keyword_id)


    if categorization_method_name == "grep":
        keywords = keyword_setup_handler.get_no_reference_word_in_context_words_setup(keywords)
        reference_words = keywords["reference_words"]
        context_words = keywords["context_words"]
        freq_dist_map_id = document_vectorization.get_freq_dist_map_id(experiment_spec)
        freq_dists = cache.load(__FREQ_DIST_CACHE,freq_dist_map_id)
        categorization = text_categorizer.get_categorization(categorization_method_name,freq_dists,reference_words,context_words)
        cache.write(__CATEGORIZATIONS_CACHE,experiment_id,categorization)
        pprint.pprint(categorization)

        return

    if categorization_method_name == "cosinus":
        keywords = keyword_setup_handler.get_all_reference_word_in_context_word_setup(keywords)
        reference_words = keywords["reference_words"]
        context_words = keywords["context_words"]
        tf_idf_map_id = document_vectorization.get_tf_idf_map_id(experiment_spec)
        tf_idf_map = cache.load(__TF_IDF_DIRECTORY_CACHE,tf_idf_map_id)
        categorization = text_categorizer.get_cosinus_categorization(tf_idf_map,reference_words ,context_words )
        pprint.pprint(categorization)
        cache.write(__CATEGORIZATIONS_CACHE,experiment_id,categorization)
        return

    raise NotImplemented()


def do_evaluation(experiment_spec,evaluation_scale):
    experiment_id = experiment_spec["id"]
    test_dataset_id = dataset_id_handler.get_test_data_id(experiment_spec)
    categorization = cache.load(__CATEGORIZATIONS_CACHE,experiment_id)
    gold_standard_categorization = cache.load(__GOLD_STANDARD_CATEGORIZATION_CACHE,test_dataset_id)
    category_hiearchy = specification_handler.get_specification(__CATEGORY_HIEARACHY_SPECIFICATION,test_dataset_id)

    all_categories = list(gold_standard_categorization.keys())
    test_data_filter_spec = experiment_spec["test_dataset"]["test_category_filters"]
    test_categories = test_data_filters.get_test_categories(test_data_filter_spec,all_categories)
    print(test_categories)
    print(len(test_categories))

    evaluation = evaluater.get_evaluation(test_categories,categorization,gold_standard_categorization,category_hiearchy,evaluation_scale)
    print_to_json(evaluation)
    evaluation_levels = evaluater.get_evaluation_levels(evaluation_scale)
    result_analyser.print_evaluation_to_csv(experiment_id,evaluation,evaluation_levels)
    pr_matrix = result_analyser.calculate_precision_recall_matrix(evaluation,evaluation_levels)
    result_analyser.print_precision_recall_matrix_csv(experiment_id,pr_matrix,evaluation_levels)
    best_pr_matches = result_analyser.calculate_p_r_match_for_categories(evaluation,evaluation_levels)
    result_analyser.print_p_r_match_to_csv(experiment_id,best_pr_matches)
    general_recall = result_analyser.calculate_general_recall_at_precissions_levels(evaluation,evaluation_levels)
    result_analyser.print_general_recall_at_precissions_levels(experiment_id,general_recall,evaluation_levels)


    #Load seed words
    keyword_spec = experiment_spec["keywords"]
    keyword_seed_id =keyword_spec["seed_id"]
    seed_words = specification_handler.get_specification(__KEYWORD_SEEDS_DIRECTORY_SPECIFICATION, keyword_seed_id)
    seed_words = seed_words_to_index_terms(seed_words)
    index_indices = get_all_index_indices(experiment_spec["training_dataset"])
    posting_lists_id = keyword_setup_id_generator.get_no_filtered_keywords_id(keyword_seed_id,experiment_spec["training_dataset"])
    min_doc_seed, max_doc_seed = result_analyser.get_n_documents_with_given_seed(seed_words,posting_lists_id,__INDEX_DIRECTORY_CACHE,index_indices)
    result_analyser.print_n_documents_with_seed(experiment_id,min_doc_seed, max_doc_seed)


def run_experiment(experiment_id,evaluation_scale):
    experiment_directory = "experiments"
    experiment_spec = specification_handler.get_specification(experiment_directory,experiment_id)
    prepare_experiment_resources(experiment_spec)
    do_categorization(experiment_spec)
    do_evaluation(experiment_spec,evaluation_scale)



#run_experiment("lk_original_220000", __EVALUATION_SCALE)
#run_experiment("dice_2_iter_paradigmatic_1",__EVALUATION_SCALE)
#run_experiment("lk_original_seed_no_context_2_cosinus",__EVALUATION_SCALE)

#run_experiment("lk_original_220000_testdata2",__EVALUATION_SCALE)
run_experiment("lk_original_seed_no_context_2_cosinus_testdata2",__EVALUATION_SCALE)





#run_experiment("lk_original_220000_grep", __EVALUATION_SCALE)
#run_experiment("dice_2_iter_paradigmatic_1_grep",__EVALUATION_SCALE)

#run_experiment("imdb_manual_choice_dice_itertion_inflection_paradigmatic_grep",__EVALUATION_SCALE)
#run_experiment("imdb_manual_choice_dice_itertion_inflection_paradigmatic",__EVALUATION_SCALE)

#run_experiment("dice_2_iter_paradigmatic_1_grep",__EVALUATION_SCALE)


# # run_experiment("test_experiment_first_100_plots_basic")
# run_experiment("lk_inflection_max_usability",__EVALUATION_SCALE)

#run_experiment("lk_original_220000_no_keyword_filters",__EVALUATION_SCALE)

#run_experiment("imdb_220000_ref_manual_inflections_context_dice_inflections",__EVALUATION_SCALE)
#run_experiment("imdb_second_dice_iter_inflection_no_sub_groups",__EVALUATION_SCALE)
# run_experiment("imdb_29_feb_dice_iteration_manual_choice",__EVALUATION_SCALE)
#run_experiment("imdb_manual_choice_dice_itertion_inflection_paradigmatic",__EVALUATION_SCALE)