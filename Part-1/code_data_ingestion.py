import pymysql
import logging
import yaml
import pandas as pd
import warnings
import time


class IAMDataIngestion:
    """
    This class contains all data ingestion scenarios from upstream sources.
    """

    def __init__(self, database_configs, sql_yaml_file, delta_load_file, load_type, source):
        """
        Initialize and get credentials from YAML files and set up DB connection.
        """
        self.sql_yaml_file = sql_yaml_file
        self.delta_load_file = delta_load_file
        self.source = source
        self.load_type = load_type
        self.database_configs = database_configs

        try:
            ssl_options = {
                'ssl': {
                    'ssl_version': database_configs['EDW']["TLSVersions"]
                }
            }

            self.edw_connection = pymysql.connect(
                user=database_configs['EDW']['Username'],
                password=database_configs['EDW']['Password'],
                host=database_configs['EDW']['Hostname'],
                database=database_configs['EDW']['Database'],
                **ssl_options
            )
            logging.info("EDW connection opened successfully!")
            self.sql_qrys = self.load_local_sql_query_yaml()

        except Exception as e:
            logging.error(f"Exception occurred at get source database connection: {str(e)}")

    def load_local_sql_query_yaml(self):
        """
        Read SQL query YAML file.
        """
        data = None
        try:
            with open(self.sql_yaml_file, 'r') as stream:
                data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.error(str(e))
        return data

    def load_delta_times_yaml(self):
        """
        Read delta time configuration.
        """
        data = None
        try:
            with open(self.delta_load_file, 'r') as stream:
                data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.error(str(e))
        return data

    def close_connections(self):
        """
        Close active DB connections.
        """
        try:
            if self.source.lower() == 'glide':
                self.glide_connection.close()
                logging.info("GLIDE connection closed successfully!")
            else:
                self.edw_connection.close()
                logging.info("EDW connection closed successfully!")
        except Exception as e:
            logging.error(f"There is an issue closing the {self.source} connection: {str(e)}")

    def fetch_data_from_edw(self, feature_name, sql_query_param):
        """
        Fetch full data for a feature from EDW.
        """
        try:
            if self.load_type == "full":
                query = self.sql_qrys['edw_query'][sql_query_param]
                return pd.read_sql(query, con=self.edw_connection)
        except Exception as e:
            logging.error("Error fetching data - Debug [Class: IAMDataIngestion | Method: fetch_data_from_edw()]")
            logging.error(f"Exception occurred at fetch_data_from_edw({feature_name}): {str(e)}")

    def fetch_Batchdata_from_entitlement_master(self, feature_name, sql_query_param, chunksize, offset):
        """
        Fetch batched data from Entitlement Master for a feature.
        """
        if not self.edw_connection:
            logging.error("No Database connection available")
            return

        try:
            query = self.sql_qrys['edw_query'][sql_query_param]
            query = f"{query} LIMIT {chunksize} OFFSET {offset}"
            return pd.read_sql(query, con=self.edw_connection)
        except Exception as e:
            logging.error(f"Error fetching data: {str(e)} - Debug [Class: IAMDataIngestion | Method: fetch_Batchdata_from_entitlement_master()]")

    def fetch_data_from_eservice_data(self, feature_name, sql_query_param, placeholders, keys):
        """
        Fetch data from E-Service based on placeholders and keys.
        """
        if not self.edw_connection:
            logging.error("No Database connection available")
            return

        try:
            query = self.sql_qrys['edw_query'][sql_query_param].format(placeholders=placeholders)
            return pd.read_sql(query, con=self.edw_connection, params=keys)
        except Exception as e:
            logging.error(f"Error fetching data: {str(e)} - Debug [Class: IAMDataIngestion | Method: fetch_data_from_eservice_data()]")
