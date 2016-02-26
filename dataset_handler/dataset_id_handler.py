from preprocessing import preprocessing_filters

def get_training_data_id(training_data_spec):
    training_dataset_id = training_data_spec["id"]
    training_data_filter_names = training_data_spec["filters"]
    filters_id = [preprocessing_filters.get_filter_id(filter_name) for filter_name in training_data_filter_names]
    filters_id.sort()
    filters_id = [str(filter_id) for filter_id in filters_id]
    filters_id = "".join(filters_id)
    return  training_dataset_id +"_"+ filters_id

def get_dataset_combination_id(experiment_spec):
    training_data_id = get_training_data_id(experiment_spec["training_dataset"])
    test_data_id = experiment_spec["test_dataset"]["id"]
    return training_data_id +"_"+ test_data_id

def get_test_data_id(experiment_spec):
    test_data_id = experiment_spec["test_dataset"]["id"]
    return test_data_id