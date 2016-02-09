import hashlib
import json
import os

__SPECFICATION_DIRECTORY = "data/specifications"

def get_specification(directory, specification_id):
    specification_dir = os.path.join(__SPECFICATION_DIRECTORY, directory)
    file_path = os.path.join(specification_dir, specification_id + "." + 'json')
    with open(file_path) as spec_file:
        specification = json.load(spec_file)
    return  specification
