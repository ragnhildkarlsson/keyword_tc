import csv
import math
import numpy as np
import os
from operator import itemgetter
import json
__RESULTDIRECTORY = "data/results"


def print_evaluation_to_csv(experiment_id, evaluation, evaluation_levels):
    recall_field = "recall"
    precission_field = "precission"
    eval_level_field = "eval_level"
    category_field = "category"
    fieldnames = [category_field, eval_level_field, precission_field, recall_field]
    for selection_type in evaluation:
        result_file_name = experiment_id +"_"+ selection_type + ".csv"
        eval_selection = evaluation[selection_type]
        result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)

        with open(result_file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for eval_level_index in eval_selection:
                categories = eval_selection[eval_level_index][precission_field]
                for category in categories:
                    precission = eval_selection[eval_level_index][precission_field][category]
                    recall = eval_selection[eval_level_index][recall_field][category]
                    eval_level = evaluation_levels[eval_level_index]
                    writer.writerow({category_field:category,
                                     eval_level_field:eval_level,
                                     precission_field:precission,
                                     recall_field:recall})


def print_analysis_result(experiment_id, evaluation, evaluation_levels):
    result_file_name = experiment_id +"_"+"analysis"+ ".json"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)
    analysis = calculate_result_analyse(evaluation,evaluation_levels)
    with open(result_file_path, 'w') as analysis_file:
        json.dump(analysis, analysis_file, sort_keys=True,indent=4)


def calculate_result_analyse(evaluation, evaluation_levels):
    precission_field = "precission"
    recall_field = "recall"

    median_precission_field = "median_p"
    median_recall_field = "median_r"
    average_precission_field = "average_p"
    average_recall_field = "average_r"
    std_precission_field = "std_p"
    std_recall_field = "std_r"
    n_no_correct_classified_field = "n_no_correct_classified"
    no_correct_classified_field = "no_correct_classified"
    top_classification_limit_field = "top_classification_limit"
    n_top_classified_field = "n_top_classified"
    top_classified_field = "top_classified"


    average_precission_field_nz = "average_p_nz"
    average_recall_field_nz = "average_r_nz"
    std_precission_field_nz = "std_p_nz"
    std_recall_field_nz = "std_r_nz"


    top_classification_limit = 0.9

    analysis = {}
    analysis[top_classification_limit_field]=top_classification_limit

    for selection_type in evaluation:
        analysis[selection_type] = {}
        for evaluation_level_index in range(len(evaluation_levels)):
            evaluation_level_string = str(evaluation_levels[evaluation_level_index])
            analysis[selection_type][evaluation_level_string] = {}
            categories_by_precission = list(evaluation[selection_type][evaluation_level_index][precission_field].items())
            categories_by_precission.sort(key = itemgetter(1),reverse=True)

            categories_by_recall = list(evaluation[selection_type][evaluation_level_index][recall_field].items())
            categories_by_recall.sort(key=itemgetter(1),reverse=True)

            mid_index = math.floor(len(categories_by_precission)/2)
            median_precission = categories_by_precission[mid_index][1]
            median_recall = categories_by_recall[mid_index][1]

            average_precission = np.mean([p[1] for p in categories_by_precission])
            average_recall = np.mean([r[1] for r in categories_by_recall])
            average_precission_nz = np.mean([p[1] for p in categories_by_precission if p[1]> 0])
            average_recall_nz = np.mean([r[1] for r in categories_by_recall if r[1] > 0])


            std_precission = np.std([p[1] for p in categories_by_precission])
            std_recall = np.std([r[1] for r in categories_by_recall])
            std_precission_nz = np.std([p[1] for p in categories_by_precission if p[1]>0])
            std_recall_nz = np.std([r[1] for r in categories_by_recall if r[1]>0])


            categories_no_correct_classified = [category[0] for category in categories_by_precission if category[1] == 0]
            categories_no_correct_classified.sort()
            n_categories_no_correct_classified = len(categories_no_correct_classified)

            categories_top_recall = [category[0] for category in categories_by_recall if category[1] >= top_classification_limit]
            categories_top_precission = [category[0] for category in categories_by_precission if category[1] >= top_classification_limit]
            categories_top_result = list(set(categories_top_precission).intersection(categories_top_recall))
            categories_top_result.sort()
            n_categories_top_result = len(categories_top_result)

            n_cateogories_zero_correct_1 = len([category for category in categories_by_precission if category[1] == 0])
            n_cateogories_zero_correct_2 = len([category for category in categories_by_recall if category[1] == 0])
            if not n_cateogories_zero_correct_1 == n_cateogories_zero_correct_2:
                raise Exception()


            # Fill in calculated values
            analysis[selection_type][evaluation_level_string][median_precission_field] = median_precission
            analysis[selection_type][evaluation_level_string][median_recall_field] = median_recall

            analysis[selection_type][evaluation_level_string][average_precission_field]=average_precission
            analysis[selection_type][evaluation_level_string][average_recall_field]=average_recall

            analysis[selection_type][evaluation_level_string][std_precission_field]=std_precission
            analysis[selection_type][evaluation_level_string][std_recall_field]=std_recall

            analysis[selection_type][evaluation_level_string][average_precission_field_nz]=average_precission_nz
            analysis[selection_type][evaluation_level_string][average_recall_field_nz]=average_recall_nz

            analysis[selection_type][evaluation_level_string][std_precission_field_nz]=std_precission_nz
            analysis[selection_type][evaluation_level_string][std_recall_field_nz]=std_recall_nz



            analysis[selection_type][evaluation_level_string][n_no_correct_classified_field] = n_categories_no_correct_classified
            analysis[selection_type][evaluation_level_string][no_correct_classified_field]= categories_no_correct_classified
            analysis[selection_type][evaluation_level_string][n_top_classified_field] =n_categories_top_result
            analysis[selection_type][evaluation_level_string][top_classified_field]= categories_top_result


    return analysis