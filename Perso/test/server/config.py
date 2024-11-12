import yaml
from utils import create_file_if_not_exists

DEFAULT_CONFIG = "version : 1.0\n"

create_file_if_not_exists("config.yaml", DEFAULT_CONFIG)

def load_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
