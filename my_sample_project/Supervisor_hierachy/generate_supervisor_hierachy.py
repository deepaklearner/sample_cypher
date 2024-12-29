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
