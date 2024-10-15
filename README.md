
import logging
from retrieve_azure_creds import read import logging
_secrets_from_keyvault
### Util Functions
def initialize logger (feature_log, error_log, mode) :
@param output dir: output directory for log files @return:
TE IT IT
None
logger - logging getLogger ( logger. setLevel(logging. INFO)
### create console handler and set level to info handler - logging. StreamHandler ( handler. setLevel(logging.INFO)
formatter - logging. Formatter (*%(asctime)s [%(levelname)s] - %(message)s *) handler. setFormatter(formatter) logger.addHandler(handler)
handler = logging-FileHandler (
error_10g,
mode, encoding-None, delay='true' handler. setLevel logging. ERROR)
formatter = logging. Formatter ('%(asctime)s [%(levelname)s] - %(message)s*)
handler. setFormatter(formatter)
logger. addHandler(handler)
### logfname - log.
the log file name
handler = logging. FileHandler (feature_log,mode) # all.10g
# Set the logging level for Azure SDK to WARNING to skip INFO and DEBUG messages
azure_sdk_logger = logging getLogger ('azure")
azure
_sdk_logger. setLevel(logging-WARNING)
handler-setLevel(logging.DEBUG)
formatter - logging. Formatter(%(asctime)s [%(levelname)s] - %(message)s *) handler.setFormatter (formatter) logger.addHandler(handler)
return
def read_creds (configstream) :
Read Credentials
try:
secret_reader=read_secrets_from_keyvault(configstream)
data-secret_reader. read_ _secret_from_keyvault()
except Exception as e:
return data
print("Exception occurrec at get credentials: ", e)