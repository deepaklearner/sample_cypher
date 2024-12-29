Based on this project below,

create a scalable and maintainable RestAPI project using FastAPI with below characteristics:

1. with good naming conventions with examples of how different teams can interact with the API through Unix-based commands to interact with neo4j iam data.
2. i want the different teams to access this api via unix. It can contain 20+ rest api end points. Create atleast 5 endpoints with some parameters. 
3. Also have a the feature for versioning.
4. Also, it should have pagination feature if required.
5. Reuse the existing files config.yaml, helper.py and retrieve_azure_creds.py

Project: """
Supervisor_hierachy/
├── config/
│   ├── config.yaml
├── src/
│   ├── __init__.py              
│   ├── utils/
│   │   ├── __init__.py   
│   │   ├── helper.py
│   │   ├── retrieve_azure_creds.py
├── generate_supervisor_hierachy.sh
├── generate_supervisor_hierachy.py
└── README.md

config.yaml

common_ProjConfig:
  venv_location: /opt/cvs/deepak/venv/bin/activate
  timeout_duration: 14400
  main_log_history_days: 30
  error_log_history_days: 30
  stat_log_history_days: 30
  dev_keyvaulturi: kv-corpneo4j0101
  uat_east_keyvaulturi: kv-corpne04j0601
  uat_central_keyvaulturi: kv-corpneo4j0602
  prod_east_keyvaulturi: kv-corpne04j0701
  prod_central_keyvaulturi: kv-corpne04j0702

configyaml:
  KeyvaultURI:
    dev_keyvaulturi: kv-corpne04j0101
    uat_east_keyvaulturi: kv-corpne4j0601
    uat_central_keyvaulturi: kv-corpne04j0602
    prod_east_keyvaulturi: kv-corpne04j0701
    prod_central_keyvaulturi: kv-corpne04j0702

  MailServer:
    MAIL_SERVER: Upstream-SMTP-MAIL-SERVER
    MAIL_PORT: Upstream-SMTP-MAIL-PORT
    MAIL_FROM: Upstream-SMTP-MAIL-FROM
    MAIL_SENDER_NAME: Upstream-SMTP-MAIL-SENDER-NAME
    MAIL_TO: Upstream-SMTP-MAIL-TO

  NE04J:
    Username: Upstream-NE04J-Username
    Password: Upstream-NE04J-Password
    Database: Upstream-NE04J-Database
    HostURI: Upstream-NE04J-HostURI
    ServiceAccount: Upstream-GLIDE-Username

  FileShare:
    filesharename: Upstream-Neo4j-FileShare-Name

supervisor_hierarchy_ProjConfig:
  log_location: /opt/cvs/deepak/logs/Ne4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervis
  batch_size: 5000
  supervisor_hierarchy_query: |
    call apoc.periodic.iterate("match (n:User) where n.managerid is not null AND ('Employee' IN labels(n) OR
    // Delete mismatching managerid relationships
    optional match (n)-[r:REPORTS_TO]->(m:User)
    WHERE
    (NOT TOUPPER(n.managerid) STARTS WITH 'A' AND n.managerid <> m.employeeNumber) OR
    (TOUPPER(n.managerid) STARTS WITH 'A' AND n.managerid <> m.aetnaresourceid)
    delete r
    // Determining managerid type
"""

helper.py
"""
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
"""

retrieve_azire_creds.py
"""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
import socket
import re
import yaml

class ReadSecretsFromKeyVault:
    def __init__(self, configuration_file):
        self.config_file = configuration_file
        self.server_creds = yaml.safe_load(open(self.config_file, 'r'))
        self.keyvault_uri = self.server_creds["KeyvaultURI"]
        self.ne04j_config = self.server_creds["NE04"]
        
        # Request to get region information
        region = requests.get(
            "http://169.254.169.254/metadata/instance/compute/location?api-version=2021-02-01&format=text",
            headers={'Metadata': 'true'}
        ).text
        
        # Get hostname of the instance
        hostname = socket.gethostname()
        
        # Set vault URI based on hostname and region
        if re.search(r'dl\d', hostname):
            self.vault_uri = self.keyvault_uri["dev_keyvault_uri"]
        elif re.search(r'ul\d', hostname) and re.search(r'east', region):
            self.vault_uri = self.keyvault_uri["uat_east_keyvault_uri"]
        elif re.search(r'ul\d', hostname) and re.search(r'central', region):
            self.vault_uri = self.keyvault_uri["uat_central_keyvault_uri"]
        elif re.search(r'pl\d', hostname) and re.search(r'east', region):
            self.vault_uri = self.keyvault_uri["prod_east_keyvault_uri"]
        elif re.search(r'pl\d', hostname):
            self.vault_uri = self.keyvault_uri["prod_keyvault_uri"]
    
    def read_secret_from_keyvault(self):
        vault_url = f"https://{self.vault_uri}.vault.azure.net"
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=vault_url, credential=credential)
        
        # Read content from configuration file
        with open(self.config_file, 'r') as file:
            content = file.read()
        
        # Pattern to find the upstream values in the content
        pattern = r'(Upstream[0-9a-zA-Z-]+)'
        vars = re.findall(pattern, content)
        
        try:
            for var in vars:
                # Retrieve the secret value from Azure Key Vault
                secret_value = secret_client.get_secret(var).value
                content = content.replace(var, secret_value)
            
            # Parse updated content into YAML
            data = yaml.safe_load(content)
            return data
        
        except Exception as e:
            print(f"Error: {e}")
"""

generate_supervisor_hierachy.sh
"""
#!/bin/bash
# Script: generate_supervisor_hierarchy_report.sh
# Author: TCS IAM BuildTeam
# Version: 1.0
# Description: This script generates the supervisor hierarchy report.

# Init Process
if [ -z "$1" ]; then
  cd /opt/cvs/Neo4J_Inbound/pipeline_routines/supervisor_hierarchy  # Default Working Directory if no argument is passed
else
  cd "$1"
fi

start_time=$(date +"%Y-%m-%d %H:%M:%S")

project_configfile="/opt/cvs/Utils/config/pipeline_routines/supervisor_hierarchy/config.yaml"
activate_file=$(cat "$project_configfile" | grep -w "venv_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Check if activate file exists
if [ -f "$activate_file" ]; then
  # Activate the virtual environment
  source "$activate_file"
  echo "Virtual environment activated."
else
  echo "Error: Virtual environment not found or activate file does not exist."
  exit 1
fi

# Function written to handle Interrupt Signal
cleanup_function() {
  echo "Interrupt signal received, Stopping backend python process..."
  program_user=$(whoami)
  pkill -u "$program_user" python
  exit 1
}
trap cleanup_function SIGINT

# Initializing variables from supervisor_hierarchy_ProjConfig
main_log_history_days=$(cat "$project_configfile" | grep -w "main_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
error_log_history_days=$(cat "$project_configfile" | grep -w "error_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
stat_log_history_days=$(cat "$project_configfile" | grep -w "stat_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
log_location=$(awk '/supervisor_hierarchy_report_ProjConfig:/, /^$/' "$project_configfile" | grep -w "log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
error_log_location="$log_location/errors/"
stat_log_location="$log_location/stats/"
timeout_duration=$(cat "$project_configfile" | grep -w "timeout_duration" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Create necessary directories
mkdir -p "$log_location"
mkdir -p "$error_log_location"
mkdir -p "$stat_log_location"

# Remove old log files
find "$log_location" -maxdepth 1 -mtime +$main_log_history_days -type f -name "*.10g" -delete
find "$error_log_location" -maxdepth 1 -mtime +$error_log_history_days -type f -name "*.10g" -delete
find "$stat_log_location" -maxdepth 1 -mtime +$stat_log_history_days -type f -name "*.10g" -delete

# Generate report
log_file="$log_location/generate_supervisor_hierarchy_report_$(date +"%Y-%m-%d_%T").log"
echo "$(date +"%Y-%m-%d %T"): $1" >> "$log_file"

cd ../supervisor_hierarchy/
python -B generate_supervisor_hierarchy_report.py --log_location="$log_location" >> "$log_file" 2>&1

# Update Stats for Timeout feature
timedout_feature=$(cat "$log_file" | grep "Process Timed Out for" | rev | cut -d '=' -f1 | rev)

for i in $timedout_feature; do
  echo "$i"
  sed -i "/$i,/d" "$stat_log_location"
  echo "$i, Timeout" >> "$stat_log_location"
done

# Calculate the duration
end_time=$(date +"%Y-%m-%d %H:%M:%S")
start_seconds=$(date -d "$start_time" +%s)
end_seconds=$(date -d "$end_time" +%s)
duration=$((end_seconds - start_seconds))

# Displaying the captured times and duration
echo "Start Time: $start_time"
echo "End Time: $end_time"
echo "Generate supervisor hierarchy report job completed in $duration seconds. Please Debug stats & Logs for exact status!" >> "$log_file"
"""

generate_supervisor_hierachy.py
"""
import os
import sys
from datetime import datetime
import logging
import tracemalloc
import argparse
import csv
from neo4j import GraphDatabase, exceptions
from src.utils.helper import read_creds, initialize_main_logger, get_config_stream

# Setting up paths
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

class IAM_GraphOperations:
    """This class contains methods to handle graph for IAM application."""
    
    def __init__(self, database_configs):
        # Get the credentials from the yaml file
        self.driver = None
        self.database_configs = database_configs

    def enter(self):
        try:
            self.driver = GraphDatabase.driver(
                self.database_configs['NE04']['HostURI'],
                auth=(
                    self.database_configs['NE04']['Username'],
                    self.database_configs['NE04']['Password']
                ),
                database=self.database_configs['NE04']['Database'],
                max_connection_pool_size=50  # Adjust this value based on your needs
            )
            logging.info("Neo4j connection opened successfully")
        except Exception as e:
            logging.info(f"Error opening Neo4j connection: {str(e)}")
        return self

    def exit(self, exc_type, exc_value, traceback):
        try:
            if self.driver:
                self.driver.close()
                logging.info("Neo4j connection closed successfully")
        except Exception as e:
            logging.info(f"Error closing Neo4j connection: {str(e)}")

# Entrypoint for Script to run
# cd pipeline_routines/supervisor_hierarchy & sh generate_supervisor_hierarchy_report.sh

if __name__ == "__main__":
    time_now = datetime.now()
    tracemalloc.start()
    
    parser = argparse.ArgumentParser(description="Generate supervisor hierarchy report")
    parser.add_argument("--log_location", type=str, help="Specify the log location")
    args = parser.parse_args()

    # Initializing variables
    configuration_file = './config/config-yaml'
    
    # Reading Configuration file and getting data for passed configs
    logger = initialize_main_logger()
    baseconfigstream = get_config_stream(configuration_file)
    
    database_configs = read_creds(configuration_file)
    configstream = baseconfigstream['supervisor_hierarchy_report_ProjConfig']
    
    report_directory = configstream['report_directory']
    report_file_name = configstream['report_file_name']
    report_file_type = configstream['report_file_type']
    batch_size = configstream['batch_size']
    offset = configstream['offset']
    query = baseconfigstream['supervisor_hierarchy_report_query']

    # Validate output file location configuration
    if not report_directory:
        raise ValueError("Report output file location is not configured")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%")
    report_output_file_with_timestamp = os.path.join(report_directory, f"{report_file_name}_{timestamp}_{report_file_type}")

    # Initialize graph operations
    iam_graph_operations = IAM_GraphOperations(database_configs)
    
    flag = False
    with open(report_output_file_with_timestamp, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_written = False
        
        with iam_graph_operations:
            batch_counter = 1
            while True:
                try:
                    formatted_query = query.format(batch_size=batch_size, offset=offset)
                    result = iam_graph_operations.driver.execute_query(formatted_query)
                    records, summary, keys = result
                    
                    # Exit loop if no more records are found
                    if not len(records):
                        break
                    
                    logging.info(f"Processing batch {batch_counter} for supervisor hierarchy report generation")
                    
                    # Write header only once
                    if not header_written:
                        writer.writerow(result.keys())  # Write column headers
                        header_written = True
                    
                    # Write data rows
                    for record in records:
                        writer.writerow(record)
                    
                    # Increment offset for the next batch
                    offset += batch_size
                    batch_counter += 1
                
                except exceptions.Neo4jError as e:
                    flag = True
                    logging.info(f"Error executing Cypher query batch at offset {offset} for batch {batch_counter}: {e}")
                    break
        
        if flag:
            logging.ERROR('Supervisor hierarchy report creation unsuccessful, please debug logs')
        else:
            logging.info(f'Supervisor hierarchy report created successfully with batch_size {batch_size}.')
    
    tracemalloc.stop()
"""


