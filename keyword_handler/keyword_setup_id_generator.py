from dataset_handler import dataset_id_handler

def get_no_filtered_keywords_id(keyword_seed_id, training_data_spec):
    training_data_id = dataset_id_handler.get_training_data_id(training_data_spec)
    no_filtered_keywords_id = keyword_seed_id + "_"+ training_data_id
    return no_filtered_keywords_id

def get_keyword_setup_id(keyword_setup_id, training_data_spec):
    training_data_id = dataset_id_handler.get_training_data_id(training_data_spec)
    return keyword_setup_id+ "_" +training_data_id
