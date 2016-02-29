import os
import pickle


__BASE_CACHE_DIRECTORY = "data/cache"

def write(directory, resource_id, resource):
    cache_dir = os.path.join(__BASE_CACHE_DIRECTORY, directory)
    file_path = os.path.join(cache_dir, resource_id + "." + 'pickle')
    pickle.dump(resource, open(file_path, 'wb'))

def load(directory, resource_id):
    cache_dir = os.path.join(__BASE_CACHE_DIRECTORY, directory)
    file_path = os.path.join(cache_dir, resource_id + "." + 'pickle')
    resource = pickle.load( open(file_path, "rb" ) )
    return resource

def in_cache(directory, resource_id):
    cache_dir = os.path.join(__BASE_CACHE_DIRECTORY, directory)
    file_path = os.path.join(cache_dir, resource_id + "." + 'pickle')
    return os.path.isfile(file_path)
