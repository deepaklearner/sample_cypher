import yaml
import logging
import psutil
import os
from retrieve_azure_creds import read_secrets_from_keyvault

def read_yaml_file(file_path: str) -> dict:
    data = None
    try:
        with open(file_path, 'r') as stream:
            data = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        logging.error(str(e))
    return data

def read_creds(configstream):
    # Read Credentials
    try:
        secret_reader = read_secrets_from_keyvault(configstream)
        data = secret_reader.read_secret_from_keyvault()
        return data
    except Exception as e:
        print("Exception occurred at get credentials: ", e)

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss  # Resident Set Size (in bytes)

def get_config_stream(configuration_file):
    return read_yaml_file(configuration_file)

def initialize_main_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    azure_sdk_logger = logging.getLogger('azure')
    azure_sdk_logger.setLevel(logging.WARNING)

    return logger
