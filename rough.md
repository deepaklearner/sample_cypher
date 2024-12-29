import yaml import
05
ghp_M2WD4vqUaRf1Fbpj9sL5zPAQhRb51A3wt6kx, 2 weeks ago • u
import logging import
Psuti
from
• retrieve_azure_creds import read_secrets_from_keyvault
def read yaml
_file(file_path: str) -› dict:
data = None
try:
with open(file_path, 'r') as stream:
data=yaml. safe_load (stream)
except yaml. YAMLError as e:
logging. error (str(e))
return data
def
read
_creds (configstream):
Read Credentials
try:
secret_reader=read
secrets_from_keyvault (configstream)
data-secret_reader read_secret_from _keyvault()
return data except Exception
as e:
print("Exception occurrec at get credentials: ", e)
def get_memory_usage():
process = psutil. Process(os -getpid())
memory_info = process.memory_info()
return memory_info.rss
# Resident Set Size (in bytes)
def get_config_ stream(configuration file):
return read_yaml_file(configuration file)
def initialize_main_logger):
logger - logging- getLogger() logger. setLevel (logging.INFO)
#iff create console handler and set level to info
handler = logging-StreamHandler()
handler .setLevel(logging.INFO)
formatter = logging. Formatter( %(asctime)s [%(levelname)s]
handler.setFormatter (formatter)
- %(message)s')
logger .addHandler(handler)
azure_sdk_logger = logging-getLogger ('azure')
azure_
sdk
logger. setLevel (logging-WARNING)
return logger