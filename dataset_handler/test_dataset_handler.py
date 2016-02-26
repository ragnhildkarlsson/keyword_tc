import os
from indexing import n_gram_handler
import specification_handler
import dataset_handler


class TestDatasetHandler:
    """
    This class is responsible for create easy access to a training dataset,
    """

    SPECIFACATION_SUBDIRECTORY = "test_data"
    NO_CATEGORY_FOLDER_NAME = "no_category"

    def __init__(self, dataset_id):
        self.dataset_id = dataset_id
        data_spec = specification_handler.get_specification(self.SPECIFACATION_SUBDIRECTORY, dataset_id)
        self.data_path = data_spec["directory_path"]
        self.encoding = data_spec["encoding"]


    def __get_category_path(self, category):
        category_path = os.path.join(self.data_path, category)
        return category_path

    """
        Return the name of all categories in the test set
    """

    def __get_all_category_directory_names(self):
        subdirectories = dataset_handler.get_all_subdirectory_names(self.data_path)
        subdirectories = [sd for sd in subdirectories if not sd == self.NO_CATEGORY_FOLDER_NAME]
        return subdirectories

    """
        Return a map with the categories name mapped to a set with document id
    """

    def get_gold_standard_categorization(self):
        gold_standard_categorization = {}
        categories = self.__get_all_category_directory_names()
        for category in categories:
            category_path = self.__get_category_path(category)
            all_documents_in_category = dataset_handler.get_names_of_files_in_directory(category_path)
            category_index_term = n_gram_handler.string_to_index_term(category)
            gold_standard_categorization[category_index_term] = all_documents_in_category
        return gold_standard_categorization

    """
        Return the document specified by the category and document id
    """

    def get_document_in_test_set(self, category, document_id):
        category_path = self.__get_category_path(category)
        document_path = os.path.join(category_path, document_id)
        return dataset_handler.get_document_as_string(document_path, self.encoding)


    """
    Returns a map with each file id mapped to the text in that file
    """

    def get_all_test_documents(self):
        all_test_documents = {}
        sub_directories = dataset_handler.get_all_subdirectory_names(self.data_path)
        for sub_directory in sub_directories:
            sub_directory_path = os.path.join(self.data_path, sub_directory)
            files_indices = dataset_handler.get_names_of_files_in_directory(sub_directory_path)
            for file_id in files_indices:
                file_path = os.path.join(sub_directory_path, file_id)
                all_test_documents[file_id] = dataset_handler.get_document_as_string(file_path,self.encoding)
        return all_test_documents