ine_routines › supervisor_hierarchy ›
generate_ supervisor_ hierarchy_report.py › ...
You, 3 days ago | 2 authors (ghp_M2WD4vqUaRf1 Fbpj9sL5zPAQhRb5A3w6kx and one other)
import os import sys
currentdir = os. path.dirname(os.path.realpath(__file_))
parentdir = os. path. dirname(currentdir)
sys. path. append (parentdir) from ne04 import GraphDatabase, exceptions import logging import tracemalloc from datetime import datetime import argparse
from sc.utils.helper import read _creds, initialize main_logger, get_config_stream import csv
You, 6 days ago | 1 author (You) class IAM_GraphOperations:
This class contains methods to handle graph for IAM application
def init_(self, database_configs):

Get the credentials from yaml file
self.driver - None self.database_configs - database_configs
enter_(self):
try:
self.driver = GraphDatabase.driver
urieself.database_configs[ 'NE04] ' ]['HostURI'],
auth=(self database_configs[ 'NE04]' ]['Username '],
self database_configs['NE04J']['Password']),
database = self.database_configs[ 'NE04J" ]['Database'],
max_connection_pool_size=50,
# Adjust this value based on your needs
logging. info"Neo4j connection opened successfully")
except Exception as e:
logging.info(f"Error opening Neo4j connection: {str(e)}")
return self
def
exit__(self, exc_type, exc_value, traceback):
try:
if self.driver:
self. driver.close()
logging. info("Neo4j connection closed successfully")
except Exception as e:
logging. info(f"Error closing Neo4j connection: {str(e)}")
# Entrypoint for Script to run
# cd pipeline_routines/supervisor_hierarchy & sh generate_supervisor _hierarchy_report.sh .
if
main
time_now=datetime.now()
tracemalloc. start()
parser = argparse.ArgumentParser(description="Generate supervisor hierarchy report")
parser.add _argument("--log_location", type=str, help="Specify the log location") args - parser-parse_args)
# Initializing variables
configuration_file = './config/config-yaml'
You, 3 days ago • u
# Reading Configuration file and getting data for passed configs
logger = initialize_main_logger()
baseconfigstream - get_config_stream(configuration file)


database_configs = read_creds (configuration_file)
configstream - baseconfigstream[' supervisor_hierarchy_report_ProjConfig'] report directory - configstream[
report _directory']
report_file_name - configstreami
report_file_name ']
report_file_type - configstreami report_file_type'] batch_size - configstream[ 'batch_size'] offset - configstream 'offset']
query - baseconfigstream[' supervisor_hierarchy_report_query']
# Validate output file location configuration
if not report directory:
raise ValueError ("Report output file location is not configured")
timestamp - datetime.now()-strftime"%Y%m%d_%H%M%")
report_output_file_with_timestamp - os-path-join(report _directory, f"(report_file_name)_(timestamp)-(report_file_type}")
iam graph_operations - IAM_ GraphOperationsdatabase_configs)
Flag - False
with open (report_output_file with_timestamp,
"w", newline=*) as csfile:
writer - csv.writer(csvfile)
header written - False with iam graph_operations:
batch counter - 1
while True:
try:
formatted_query - query. format (batch_size-batch_size, offset-offset) result - iam graph _operations driver execute_query (formatted_query) records, summary, keys - result
# Exit loop if no more records are found
if not len(records):
break
logging. info(f"Processing batch (batch_counter) for supervisor hierachy report Generation")
# Write header only once
if not header written:
writer writerow(result.keys) # Write column headers header_written - True
# write data rows
for record in records:
writer writerow record)
# Increment offset for the next batch
offset += batch_size batch_counter += 1
except exceptions.Ne4jError as e:
flag - True
logging.info(f"Error executing Cypher query batch at offset (offset) for batch (batch_counter): (e)") break
if flag:
logging. ERROR('Supervisor hierarchy report creation unsuccessful, please debug logs') else:
logging. info(f'Supervisor hierarchy report created successfully with batch_size (batch_size}.') tracemalloc.stop()