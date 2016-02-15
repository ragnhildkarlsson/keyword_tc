import os
import random
import re

import specification_handler

"""
This class is responsible for create easy access to a training dataset,
"""

class TrainingDatasetHandler:

    SPECIFACATION_SUBDIRECTORY = "training_data"
    DATA_FOLDER = "data"

    def __init__(self, dataset_id):
        self.__dataset_id = dataset_id
        data_spec = specification_handler.get_specification(self.SPECIFACATION_SUBDIRECTORY, dataset_id)
        self.file_path_all_data = data_spec['file_path']
        self.encoding = data_spec['encoding']
        self.n_documents_in_subset = data_spec['n_documents_in_subset']
        self.subset_indices = self.generate_subset_indices(data_spec['n_documents_in_set'],
                                                             self.n_documents_in_subset,
                                                             data_spec['seed'],
                                                             )
        self.dataset_files_directory = data_spec["directory_path"]

    @property
    def dataset_id(self):
        return  self.__dataset_id


    @staticmethod
    def generate_subset_indices(n_documents_in_set,
                                  n_documents_in_subset,
                                  seed):
        l = list(range(n_documents_in_set))
        random.seed(seed)
        random.shuffle(l)
        l =  l[:n_documents_in_subset]
        s = set(l)
        return s

    def get_training_data_file_lines(self, file_name):
        file_path = os.path.join(self.dataset_files_directory,file_name)
        with open(file_path,'r') as f:
            lines = f.readlines()
        return lines

    def get_training_data_file_string(self,file_name):
        lines = self.get_training_data_file_lines(file_name)
        document = ' '.join(lines)
        return document

    def __iter__(self):
        return TrainingDatasetIterator(self.file_path_all_data, self.encoding, self.subset_indices)

class TrainingDatasetIterator:
    """
    file_path:  to the data_file that is iterated
    encoding of the file
    subset_document_indices: a set with the document indices in the subset
    """
    def __init__(self, file_path, encoding, subset_document_indices):
        self.data_file = self.__open_train_data_file(file_path, encoding)
        self.subset_indices = subset_document_indices

    def __iter__(self):
        return  self


    def __open_train_data_file(self, file_path,encoding):
        data_file = open(file_path, encoding = encoding)
        return data_file


    def __is_delimeter_line(self, line):
        break_line_matcher = '^---.*'
        return re.match(break_line_matcher, line)

    def __get_document_id(self, line):
        doc_id_matcher = '-*(\d+)'
        doc_id = re.search(doc_id_matcher, line).group(1)
        return int(doc_id)

    """
    Returns a tuple with doc id and corresponding document as a string representing
    the next document in the data file with a document id that is present in subset_document_indices
    """
    def __next__(self):
        lines = []
        while True:
            line = self.data_file.readline()
            # Check for EOF
            if not line:
                self.data_file.close()
                raise StopIteration()
            if self.__is_delimeter_line(line):
                document_id = self.__get_document_id(line)
                if(document_id in self.subset_indices):
                    document = ' '.join(lines)
                    return (document_id, document)
                else:
                    lines = []
            else:
                lines.append(line)
