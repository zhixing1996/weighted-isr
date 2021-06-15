import copy
import configparser

def load_config(file_name, share_dict = None):
    if share_dict is None:
        share_dict = {}
    if isinstance(file_name, dict):
        return copy.deepcopy(file_name)
    if isinstance(file_name, str):
        if file_name in share_dict:
            return load_config(share_dict[file_name])
        config = configparser.ConfigParser()
        config.read(file_name)
        return config
    raise TypeError("Not sypported config {}".format(type(file_name)))

class BaseConfig(object):
    def __init__(self, file_name, share_dict=None):
        self.config = load_config(file_name, share_dict)

    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value
