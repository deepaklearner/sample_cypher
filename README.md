import argparse import yam_ import os import logging import time
from sc.report _object _handler import ReportObjectHandler from src.main_graph_query_executor import MainGraphQueryExecutor from sc.utils.utils import read creds, initialize_ logger import gc import tracemalloc import psutil
from datetime import datetime import pandas as pd
# ReportProcessor : Executing Engine for creating report
class ReportProcessor:
This class containd methods to fetch report_id properties from graph db def
_init_ (self, configstream) -› None:
self.db_crendentials_file = configstream["db_crendentials_file"]
self.database_config = read_creds (configstream)
def fetch_and _create_graph_reportself, report_id):
logging. info"running fetch_and_create _graph_report")
report_object_handler = ReportObjectHandler(self.database_config)
query_executor = MainGraphQueryExecutor(self.database_config)
try:
with report_object_handler:
logging. info(f'Fetching report query for report_id: (report_id}')
report_object_data = report_object_handler.fetch_report_object_by_id(report_id)
report_query = str(report_object_data. loc[0, 'reportQuery'])
logging. info('deepak report_query string*)
logging. info(report_query)
with query_executor:
logging. info(f'Creating report for report_id: {report_id}')
report_df = query_executor.execute_report_query(report_query)
logging. info(report_df)
logging. info(f'Updating report object for report_id: (report_id}') report_object_handler.update_report_object()
except Exception as e: logging-error(
f"Error in Processing Batch - {offset} -Debug ‹Classs: IAM_data_executor | Method: create_graph_for_oneID() › | {e}"
finally:
return True
# Helper Fucntions
def configure_local_logging(feature_name):
Configure Local Logging
Args: None
Returns: None
### Setup Logging
feature_log = f"{args. log_location}/features/feature-{feature_name}. log*
error_log = f"(args. log_location)/errors/error.log"
initialize_logger (feature_log, error_10g, return
"a")
def get_memory_usage():
process = psutil. Process(os getpid())
memory_info = process.memory_info()
return memory_info.rss
# Resident Set Size (in bytes)

def
get_feature_stream(feature_name, configstream):
if Feature_name not in ["ConstraintCreation", "PRE_PROCESSING"]:
with open (configstream["report_feature_config"], "r") as stream datal:
try:
return yaml. safe_load(stream _datal) [feature_name]
except yaml. YAMLError as e:
print(e)
def get_config_stream(configuration_file="./config/config-yaml"):
with open (configuration file, "f") as stream data:
try:
return yaml. safe_load(stream_data)
except yaml. YAMLError as e:
print(e)
# Entrypoint for Script to run
if
name
== "
main_":
time_now = datetime.now()
# Activate Logging and metrics
tracemalloc. start()
# Argument Calls
parser = argparse.ArgumentParser(description="Process data for specific feature.")
parser .add_argument
"-- feature_name",
" _F",
type-str,
help-"Specify the feature_name: Refer (config/feature yaml) to get the exact feature",
parser. add_argument (
"--report_id",
"ーエゼ。
"-1", "-L", type str,
help="Specify the report_id: 1",
parser .add_argument("--log_location", type=str, help="Specify the log location") angs - parser-parse_args()
# Initializing variables
feature_name = args. feature_name
configure_local_logging(feature_name)
report_id = int(args.report_id)
configuration_file = "./config/config-yaml"
logging.info(f"Report {report_id} processing Started for {feature_name}")
# Reading Configuration file and getting data for passed features
configstream = get_config_ stream(configuration_file)
feature_stream = get_ feature_stream(feature_name, configstream)
Creating object for ReportProcessor Class and executing features based on parameters passed
-#
report_processor = ReportProcessor (configstream)
try:
if feature_name == "GraphDBReport":
status = report_processor. fetch_and_create_graph_report(report_id)
if status:
logging-infof"Batch Data load completed for {feature_name)")

logging.infol
f"Computation Memory used for {feature_name} run: fget_memory_usage ()/1024/1024} megabytes"
except Exception as e:
logging.error (f'Feature failed- {feature.
_name}, {e}")
finally:
ge. collecto time.sleep(5)
logging. info
f"Overall time taken by the feature - {feature
_name; is {datetime.now()-time_now}*
tracemalloc. stop()