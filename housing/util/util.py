#In this file we will write any helper functions required by multiple modules

import yaml
from housing.exception import HousingException
import os, sys

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file  and returns the contents as dictionary.
    file_path: string
    """

    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e