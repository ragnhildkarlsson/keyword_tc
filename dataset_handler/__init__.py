import os

def get_document_as_string(file_path, encoding):
    lines = []
    with open(file_path, encoding = encoding) as f:
        lines = f.readlines()
    document_string = ' '.join(lines)
    return document_string

def get_names_of_files_in_directory(folder):
    files =  next(os.walk(folder))[2]
    return files

def get_all_subdirectory_names(directory_path):
    subdirectories = []
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for dir in dirs:
            subdirectories.append(dir)
    return subdirectories

