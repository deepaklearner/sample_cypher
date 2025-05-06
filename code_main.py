import os
import logging
import time
import gc
import tracemalloc
import psutil
import argparse
from datetime import datetime
import pandas as pd
import yaml

from sc.data_ingestion.data_ingestion import IAMDataIngestion
from src.graph_creation.create_graph import IAMGraphCreation
from sc.utils.utils import read_creds, initialize_logger


class IAMDataExecutor:
    """Executing Engine for loading data into Graph"""

    def __init__(self, configstream):
        self.db_credentials_file = configstream["db_credentials_file"]
        self.sql_yaml_file = configstream["sql_yaml_file"]
        self.delta_load_file = configstream["delta_load_file"]
        self.report_file_location = configstream["report_file_location"]
        self.database_config = read_creds(configstream)

    def write_report_to_csv(self, configstream, report_directory, warning_df, error_df):
        warning_file = configstream['warning_report_file_name']
        error_file = configstream['error_report_file_name']
        file_type = configstream['report_file_type']

        if not report_directory:
            raise ValueError("Report output file location is not configured")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        warning_path = os.path.join(report_directory, f"{warning_file}_{timestamp}.{file_type}")
        error_path = os.path.join(report_directory, f"{error_file}_{timestamp}.{file_type}")

        if len(warning_df) > 0:
            warning_df.to_csv(warning_path, index=False)
        if len(error_df) > 0:
            error_df.to_csv(error_path, index=False)

    def fetch_batched_data_for_feature_template(self, feature_name, feature_stream, source, chunksize, offset, load_type):
        sql_query_param = feature_stream["sql_query_param"]
        iam_ingestion = IAMDataIngestion(self.database_config, self.sql_yaml_file, self.delta_load_file, load_type, source)

        try:
            while True:
                if source == "edw":
                    df_batched = iam_ingestion.fetch_Batchdata_from_edw(feature_name, sql_query_param, chunksize, offset)

                    if len(df_batched):
                        memory_usage = df_batched.memory_usage(deep=True).sum() / (1024 ** 2)
                        logging.info(f"Data Retrieved for {feature_name} [BatchSize: {offset}-{offset+chunksize}, Records: {len(df_batched)}]")

                        if feature_stream["mode"] == "run_with_no_template":
                            self.create_data_for_graph_non_template(feature_name, feature_stream, df_batched)
                        else:
                            self.create_data_for_graph_template(feature_name, feature_stream, df_batched)

                        offset += chunksize
                    else:
                        logging.info(f"No records fetched for {feature_name} [BatchSize: {offset}-{offset+chunksize}]")
                        break
        except Exception as e:
            logging.error(f"Error in Batch Processing: {e}")
        finally:
            iam_ingestion.close_connections()

        return True

    def create_graph_for_entitlements(self, feature_name, feature_stream, chunksize, load_type, offset):
        logging.info("Running entitlements graph creation")
        sql_entitlements = feature_stream["sql_edw_entitlements_query_param"]
        sql_eservice = feature_stream["sql_edw_eservice_query_param"]

        iam_ingestion = IAMDataIngestion(self.database_config, self.sql_yaml_file, self.delta_load_file, load_type, source="edw")
        graph_creator = IAMGraphCreation(self.database_config)

        try:
            batch_counter = 1
            warning_df = pd.DataFrame()
            error_df = pd.DataFrame()

            while True:
                logging.info(f"Processing entitlements batch {batch_counter}")
                ent_raw = iam_ingestion.fetch_Batchdata_from_entitlement_master(feature_name, sql_entitlements, chunksize, offset)

                if len(ent_raw):
                    keys = tuple(ent_raw[['entitlementName', 'targetSystem']].drop_duplicates().itertuples(index=False, name=None))
                    placeholders = ','.join(['%s'] * len(keys))

                    eservice_df = iam_ingestion.fetch_data_from_eservice_data(feature_name, sql_eservice, placeholders, keys)
                    merged_df = ent_raw.merge(eservice_df, on=['entitlementName', 'targetSystem'], how='left')

                    owner_columns = ['owner', 'owner2', 'owner3']
                    all_owners = pd.unique(merged_df[owner_columns].values.ravel())
                    all_owners = set(filter(None, all_owners))

                    owner_status = graph_creator.validate_owners(all_owners)
                    inactive_df = owner_status[owner_status['Reason'] != 'Active']
                    missing_owners = all_owners - set(owner_status['OwnerID'])
                    missing_df = pd.DataFrame({'OwnerID': list(missing_owners), 'Reason': 'Missing in Graph DB'})

                    warning_df = pd.concat([warning_df, inactive_df], ignore_index=True)
                    error_df = pd.concat([error_df, missing_df], ignore_index=True)

                    graph_creator.create_graph_for_Entitlement(merged_df, feature_name)
                    offset += chunksize
                    batch_counter += 1
                else:
                    logging.info(f"No entitlements found in batch {offset}")
                    break

            self.write_report_to_csv(feature_stream, self.report_file_location, warning_df, error_df)

        except Exception as e:
            logging.error(f"Error creating entitlements graph: {e}")
        finally:
            iam_ingestion.close_connections()

        return True


# Utility functions
def configure_local_logging(feature_name, log_location):
    feature_log = f"{log_location}/features/feature-{feature_name}.log"
    error_log = f"{log_location}/errors/error.log"
    initialize_logger(feature_log, error_log)


def execute_neo4j_preprocessing(stream_data):
    try:
        with open(stream_data["neo4j_constraints_file"], "r") as f:
            constraints = yaml.safe_load(f)
        graph_creator = IAMGraphCreation(read_creds(stream_data))
        with graph_creator:
            graph_creator.execute_neo4j_preprocessing(constraints["neo4jconstraints"], stream_data)
    except Exception as e:
        logging.info("Error in Creating Neo4j Constraints: %s", e)


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_feature_stream(feature_name, configstream):
    if feature_name not in ["ConstraintCreation", "PRE_PROCESSING"]:
        with open(configstream["neo4j_feature_config"], "r") as f:
            return yaml.safe_load(f)[feature_name]


def get_config_stream(path="./config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# Entrypoint
if __name__ == "__main__":
    tracemalloc.start()
    time_now = datetime.now()

    parser = argparse.ArgumentParser(description="Process data for specific feature.")
    parser.add_argument("--feature_name", type=str, required=True)
    parser.add_argument("--load_type", type=str, required=True)
    parser.add_argument("--chunksize", type=int, required=True)
    parser.add_argument("--offset", type=int, required=True)
    parser.add_argument("--log_location", type=str, required=True)

    args = parser.parse_args()

    feature_name = args.feature_name
    load_type = args.load_type.lower()
    chunksize = args.chunksize
    offset = args.offset

    configure_local_logging(feature_name, args.log_location)

    logging.info(f"{load_type.capitalize()} Load Started for {feature_name}")
    configstream = get_config_stream()
    feature_stream = get_feature_stream(feature_name, configstream)

    data_processor = IAMDataExecutor(configstream)

    try:
        if feature_name == "Entitlements":
            data_processor.create_graph_for_entitlements(feature_name, feature_stream, chunksize, load_type, offset)
        else:
            data_processor.fetch_batched_data_for_feature_template(feature_name, feature_stream, "edw", chunksize, offset, load_type)

        logging.info(f"Memory used: {get_memory_usage() / 1024 / 1024:.2f} MB")

    except Exception as e:
        logging.error(f"Feature failed: {feature_name}, Error: {e}")

    finally:
        gc.collect()
        time.sleep(5)
        logging.info(f"Total execution time for {feature_name}: {datetime.now() - time_now}")
        tracemalloc.stop()
