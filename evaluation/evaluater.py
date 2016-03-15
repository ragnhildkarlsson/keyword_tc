import numpy as np
from operator import itemgetter
from cache import cache
from keyword_handler import posting_list_handler


def get_evaluation_levels(evaluation_scale):
    evaluation_levels = list(np.arange(0,1, evaluation_scale))
    evaluation_levels.append(1.0)
    evaluation_levels.pop(0)
    return evaluation_levels

def get_gold_standard_documents_for_category(category, gold_standard_categorization, category_hierarchy):
    documents_in_category = set(gold_standard_categorization[category])
    if category in category_hierarchy:
        for sub_category in category_hierarchy[category]:
            documents_in_category.update(set(gold_standard_categorization[sub_category]))
    return documents_in_category

def get_ranked_to_category(category, categorization, category_hiearachy):
    documents_ranked_to_main_category = list(categorization[category])
    if category == "water_sports":
        pass
    allready_ranked = {}
    for document_tuple in categorization[category]:
        allready_ranked[document_tuple[0]] = document_tuple[1]

    if category in category_hiearachy:
        for sub_category in category_hiearachy[category]:
            documents_in_sub_category = list(categorization[sub_category])
            for document_in_sub_category in documents_in_sub_category:
                if document_in_sub_category[0] in allready_ranked:
                    if document_in_sub_category[1] > allready_ranked[document_in_sub_category[0]]:
                        documents_ranked_to_main_category = [doc for doc in documents_ranked_to_main_category if not doc[0]==document_in_sub_category[0]]
                        documents_ranked_to_main_category.append(document_in_sub_category)
                else:
                    documents_ranked_to_main_category.append(document_in_sub_category)
                    allready_ranked[document_in_sub_category[0]] = document_in_sub_category[1]


    documents_ranked_to_main_category.sort(key=itemgetter(1), reverse=True)

    return documents_ranked_to_main_category

def get_n_correct_ranked_documents(ranked_to_category,documents_in_category):
    n_correct_ranked_docs = 0
    for document in ranked_to_category:
        if document[0] in documents_in_category:
            n_correct_ranked_docs +=1
    return n_correct_ranked_docs

def get_precission(ranked_to_category, documents_in_category):
    n_correct_ranked_docs = get_n_correct_ranked_documents(ranked_to_category,documents_in_category)
    n_documents_in_selection = len(ranked_to_category)
    if n_documents_in_selection == 0:
        return 0
    else:
        return n_correct_ranked_docs/n_documents_in_selection

def get_precission_selection_indices(ranked_to_category, documents_in_category, precission_levels):
    precission_selction_map = {}
    selection_index_precission_tuples = []

    # Calculate precission for different selections
    all_possible_selections = range(len(ranked_to_category)+1)

    for selection_index in all_possible_selections:
        selected_ranked_documents = ranked_to_category[:selection_index]
        precission_in_selection = get_precission(selected_ranked_documents, documents_in_category)
        selection_index_precission_tuples.append((selection_index,precission_in_selection))

    #find optimal selections
    for precission_level_index in range(len(precission_levels)):
        precission_level = precission_levels[precission_level_index]
        # Find selections that maintain precission level
        higer_precission_selections = [selection for selection in selection_index_precission_tuples if (selection[1] - precission_level) >= 0]
        # Sort on selection index deccending
        higer_precission_selections.sort(key=itemgetter(0),reverse = True)
        # Return a selection
        if not higer_precission_selections:
            precission_selction_map[precission_level_index] = 0
        else:
            best_selection = higer_precission_selections[0]
            precission_selction_map[precission_level_index] = best_selection[0]
    return precission_selction_map


def get_evaluation(test_categories,categorization, gold_standard_categorization,
                   category_hierarchy, evaluation_scale,
                   ):
    evaluation = {}
    evaluation_levels = get_evaluation_levels(evaluation_scale)
    selection_indices_map = {}
    documents_in_category_map = {}
    ranked_to_category_map = {}
    for category in test_categories:
        ranked_to_category_map[category] = get_ranked_to_category(category,categorization, category_hierarchy)
        documents_in_category_map[category]= get_gold_standard_documents_for_category(category,gold_standard_categorization,category_hierarchy)
        selection_indices_map[category] = get_precission_selection_indices(ranked_to_category_map[category],
                                                                           documents_in_category_map[category],
                                                                           evaluation_levels)
    # Caluclate evaluation

    for evaluation_level_index in range(len(evaluation_levels)):
        evaluation[evaluation_level_index] = {}
        for category in test_categories:
            evaluation[evaluation_level_index][category] = {}
            ranked_to_category = ranked_to_category_map[category]
            documents_in_category = documents_in_category_map[category]
            selection_index = selection_indices_map[category][evaluation_level_index]
            selected_ranked_documents = ranked_to_category[:selection_index]

            n_docs_in_category = len(documents_in_category)

            # evaluate precission and recall in selection
            n_correct_ranked_docs = get_n_correct_ranked_documents(selected_ranked_documents,documents_in_category)
            precission_in_selection = get_precission(selected_ranked_documents, documents_in_category)
            recall_in_selection = n_correct_ranked_docs/n_docs_in_category
            evaluation[evaluation_level_index][category]["precission"] =  precission_in_selection
            evaluation[evaluation_level_index][category]["recall"] = recall_in_selection
            evaluation[evaluation_level_index][category]["n_documents_in_category"] = n_docs_in_category
            evaluation[evaluation_level_index][category]["n_correct_ranked_documents"] = n_correct_ranked_docs

    return evaluation

