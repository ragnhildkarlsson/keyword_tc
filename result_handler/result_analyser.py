import csv
import math
import numpy as np
import os
from operator import itemgetter
import json
from cache import cache
from keyword_handler import keyword_setup_id_generator

from keyword_handler import posting_list_handler
__RESULTDIRECTORY = "data/results"


def print_evaluation_to_csv(experiment_id, evaluation, evaluation_levels):
    recall_field = "recall"
    precission_field = "precission"
    eval_level_field = "eval_level"
    category_field = "category"
    fieldnames = [category_field, eval_level_field, precission_field, recall_field]
    result_file_name = experiment_id +"_"+ "eval.csv"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)

    with open(result_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for eval_level_index in evaluation:
            for category in evaluation[eval_level_index]:
                precission = evaluation[eval_level_index][category][precission_field]
                recall = evaluation[eval_level_index][category][recall_field]
                eval_level = evaluation_levels[eval_level_index]
                writer.writerow({category_field:category,
                                 eval_level_field:eval_level,
                                 precission_field:precission,
                                 recall_field:recall})


def print_precision_recall_matrix_csv(experiment_id, matrix, evaluation_levels):
    first_column_field = "precission/recall"
    recall_fields = [str(eval_level) for eval_level in evaluation_levels]
    field_names = [first_column_field]
    field_names.extend(recall_fields)
    result_file_name = experiment_id +"_"+ "p_r_matrix.csv"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)

    with open(result_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row_index in matrix:
            row = {first_column_field:evaluation_levels[row_index]}
            for recall_field_index in range(len(recall_fields)):
                recall_field = recall_fields[recall_field_index]
                row[recall_field]= matrix[row_index][recall_field_index]
            writer.writerow(row)

def calculate_precision_recall_matrix(evaluation, evaluation_levels):
    matrix = {}
    for precision_level_index in range(len(evaluation_levels)):
        precision_level = evaluation_levels[precision_level_index]
        matrix[precision_level_index]={}
        for recall_level_index in range(len(evaluation_levels)):
            recall_level = evaluation_levels[recall_level_index]
            categories_at_p_level = [c for c in evaluation[precision_level_index] if evaluation[precision_level_index][c]["precission"] >= precision_level]
            categories_at_p_r_level = [c for c in categories_at_p_level if evaluation[precision_level_index][c]["recall"] >= recall_level]
            matrix[precision_level_index][recall_level_index] = len(categories_at_p_r_level)
    return matrix

def print_general_recall_at_precissions_levels(experiment_id, result,eval_levels):
    first_column_field= "evaluation_levels"
    second_column_field = "general_recall"
    fieldnames = [first_column_field,second_column_field]
    result_file_name = experiment_id +"_"+ "general_recal_at_p_levels.csv"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)

    with open(result_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for eval_level_index in result:
            eval_level = eval_levels[eval_level_index]
            writer.writerow({first_column_field:eval_level,
                             second_column_field: result[eval_level_index]
                            })



def calculate_general_recall_at_precissions_levels(evaluation, evaluation_levels):
    result = {}
    for precision_level_index in range(len(evaluation_levels)):
        precision_level = evaluation_levels[precision_level_index]
        categories_at_p_level = [c for c in evaluation[precision_level_index] if evaluation[precision_level_index][c]["precission"] >= precision_level]
        all_cateogories = evaluation[precision_level_index]
        total_n_correct_classified = 0
        for c in categories_at_p_level:
            total_n_correct_classified += evaluation[precision_level_index][c]["n_correct_ranked_documents"]
        total_n_deccissions = 0
        for c in all_cateogories:
            total_n_deccissions += evaluation[precision_level_index][c]["n_documents_in_category"]

        general_recall = total_n_correct_classified/total_n_deccissions
        result[precision_level_index]= general_recall
    return result

def print_p_r_match_to_csv(experiment_id, p_r_matches):
    category_field = "category"
    best_pr_match_field = "p_r_match"
    field_names = [category_field,best_pr_match_field]
    result_file_name = experiment_id +"_"+ "p_r_match.csv"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)

    with open(result_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for category in p_r_matches:
            row = {category_field:category,best_pr_match_field:p_r_matches[category]}
            writer.writerow(row)


def print_n_documents_with_seed(experiment_id, min_n_docs, max_n_docs):
    category_field = "category"
    min_field = "min"
    max_field = "max"
    field_names = [category_field,min_field,max_field]
    result_file_name = experiment_id +"_"+ "n_docs_SEED.csv"
    result_file_path = os.path.join(__RESULTDIRECTORY,result_file_name)
    with open(result_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for category in min_n_docs:
            row = {category_field:category,min_field: min_n_docs[category], max_field:max_n_docs[category]}
            writer.writerow(row)


def calculate_p_r_match_for_categories(evaluation, evaluation_levels):
    p_r_matches = {}
    categories = [c for c in evaluation[0]]
    for category in categories:
        best_pr_match = 0
        for eval_level_index in range(len(evaluation_levels)):
            evaluaton_level = evaluation_levels[eval_level_index]
            precission = evaluation[eval_level_index][category]["precission"]
            recall = evaluation[eval_level_index][category]["recall"]
            if precission>= evaluaton_level and recall >= evaluaton_level and eval_level_index >= best_pr_match:
                best_pr_match = evaluation_levels[eval_level_index]

        p_r_matches[category]= best_pr_match

    return p_r_matches


def get_n_documents_with_given_seed(seed_words, posting_lists_id, index_directory, indices_id):
    min_n_docs ={}
    max_n_docs = {}
    if not cache.in_cache("posting_lists",posting_lists_id):
        posting_lists = posting_list_handler.get_seed_words_posting_lists(seed_words,index_directory,indices_id)
        cache.write("posting_lists",posting_lists_id,posting_lists)

    posting_lists = cache.load("posting_lists", posting_lists_id)

    for category in seed_words:
        n_docs_per_refererence_group = []
        for reference_group_id in posting_lists[category]:
            n_docs_per_refererence_group.append(len(posting_lists[category][reference_group_id]))
        min_n_docs[category] = min(n_docs_per_refererence_group)
        max_n_docs[category] = max(n_docs_per_refererence_group)

    return min_n_docs, max_n_docs
