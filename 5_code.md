import pandas as pd
import argparse
import datetime
import logging
import os
import tracemalloc
import csv

from src.db_operation.ne4j_operations import IAM_GraphOperations
from src.db_operation.glide_operations import IAM_DataExport

# Entrypoint for Script to run
# cd pipeline_routines/supervisor_hierarchy & sh generate_supervisor_hierarchy_report.sh

time_now = datetime.datetime.now()
tracemalloc.start()

parser = argparse.ArgumentParser(description="Generate supervisor hierarchy report")
parser.add_argument("log_location", type=str, help="Specify the log location")
args = parser.parse_args()

# Initializing variables
configuration_file = "/config/config.yaml"

# Reading configuration file and getting data for passed configs
logger = logging.getLogger("main_logger")
base_config_stream = get_config_stream(configuration_file)
database_configs = read_creds(configuration_file)

config_stream = base_config_stream["supervisor_hierarchy_report_ProjConfig"]
manager_level = config_stream["manager_level"]
report_directory = config_stream["report_directory"]
report_file_name = config_stream["report_file_name"]
report_file_type = config_stream["report_file_type"]
batch_size = config_stream["batch_size"]
chunk_size = config_stream["chunk_size"]
offset = config_stream["offset"]
fetch_manager_hierarchy_query = base_config_stream["fetch_manager_hierarchy_query"]

# Validate output file location configuration
if not report_directory:
    raise ValueError("Report output file location is not configured")

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
report_output_file_with_timestamp = os.path.join(
    report_directory, f"{report_file_name}_{timestamp}.{report_file_type}"")
)

iam_graph_operations = IAM_GraphOperations(database_configs)
iam_data_export_glide = IAM_DataExport(database_configs)

def run_query(query):
    with iam_graph_operations.driver.session() as session:
        result = session.run(query)
    return pd.DataFrame([record.values() for record in result], columns=result.keys())

with open(report_output_file_with_timestamp, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    header_written = False

    if iam_graph_operations:
        backup_success = iam_data_export_glide.backup_table_data(
            table_name="glide.glidesupervisorhierarchy",
            backup_table_name="glide.glidesupervisorhierarchy_backup"
        )
        
        if backup_success:
            iam_data_export_glide.del_7days_old_data(
                backup_table_name="glide.glidesupervisorhierarchy_backup",
                chunk_size=chunk_size
            )
            iam_data_export_glide.del_data_frm_table(
                table_name="glide.glidesupervisorhierarchy",
                chunk_size=chunk_size
            )
            flag_success = True
        else:
            logging.info("Backup failed, skipping deletion of old data")
            flag_success = False

    batch_counter = 1
    while flag_success:
        try:
            # Step 1: Fetch manager hierarchy
            fetch_manager_hierarchy_query_formatted = fetch_manager_hierarchy_query.format(
                batch_size=batch_size, offset=offset
            )
            manager_ids_df = run_query(fetch_manager_hierarchy_query_formatted)

            # Exit loop if no more records are found
            if not len(manager_ids_df):
                break

            # Extract EmployeeID column for rows where Manager Level == 0
            manager_ids_df_manager_level_0 = manager_ids_df[manager_ids_df['ManagerLevel'] == 0]
            if not manager_ids_df_manager_level_0.empty:
                logging.info(f"EmployeeIDs with ManagerLevel - 0: {manager_ids_df_manager_level_0['EmployeeID'].tolist()}")

            manager_ids_df = manager_ids_df[manager_ids_df['ManagerLevel'] != 0]
            filtered_df = manager_ids_df[manager_ids_df['ManagerLevel'] > manager_level]
            
            if not filtered_df.empty:
                logging.info(f"Employee IDs with ManagerLevel > {manager_level}: {filtered_df['EmployeeID'].tolist()}")
            
            # Step 2: Query manager details
            manager_ids = manager_ids_df['ManagerLevel'].explode().unique()
            manager_ids_list = manager_ids.tolist()
            managers_data_from_graph = iam_graph_operations.fetch_users_data_from_graph(manager_ids_list)
            
            missing_manager_ids = set(manager_ids_list) - set(managers_data_from_graph['ManagerID'])
            if missing_manager_ids:
                logging.info(f"Missing manager IDs in graph DB: {missing_manager_ids}")
            
            # Step 3: Merge manager details
            manager_dict = managers_data_from_graph.set_index('ManagerID').to_dict('index')
            
            def expand_manager_levels(row):
                levels = row['ManagerLevel']
                max_levels = manager_level
                expanded = levels + [None] * (max_levels - len(levels))
                return pd.Series(expanded, index=[f'L{i+1}ManagerID' for i in range(max_levels)])
            
            expanded_df = manager_ids_df.apply(expand_manager_levels, axis=1)
            result_df = pd.concat([manager_ids_df[['EmployeeID', 'ManagerLevel']], expanded_df], axis=1)
            
            for i in range(1, manager_level + 1):
                level_id = f'L{i}ManagerID'
                result_df[f'L{i}ManagerFirstName'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('ManagerFirstName'))
                result_df[f'L{i}ManagerLastName'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('ManagerLastName'))
                result_df[f'L{i}ManagerEmailAddress'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('ManagerEmailAddress'))
                result_df[f'L{i}ManagerJobCodeDescription'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('ManagerJobCodeDescription'))
                result_df[f'L{i}ManagerTelephoneNumber'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('ManagerTelephoneNumber'))
            
            column_order = ['EmployeeID', 'ManagerLevel']
            for i in range(1, manager_level + 1):
                column_order.extend([f'L{i}ManagerID', f'L{i}ManagerFirstName', f'L{i}ManagerLastName',
                                     f'L{i}ManagerEmailAddress', f'L{i}ManagerJobCodeDescription', f'L{i}ManagerTelephoneNumber'])
            
            result_df = result_df[column_order]
            iam_data_export_glide.write_data_to_supervisorhierarchy(result_df, chunk_size)
            
            offset += batch_size
            batch_counter += 1
        except Exception as e:
            flag_success = False
            logging.error(f"Error executing Cypher query batch at offset {offset} for batch {batch_counter}: {e}")
            break
    
    iam_data_export_glide.close_connections()
    
    if flag_success:
        logging.info(f"Supervisor hierarchy report job ran successfully with batch_size {batch_size}")
    else:
        logging.error("Supervisor hierarchy report creation job failed, please debug logs")

tracemalloc.stop()
