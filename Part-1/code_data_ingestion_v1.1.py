import pymysql
import logging
import yaml
import pandas as pd
import time


class IAMDataIngestion:
    """
    This class contains all data ingestion scenarios from upstream sources.
    """

    def __init__(self, database_configs, sql_yaml_file, delta_load_file, load_type, source):
        self.sql_yaml_file = sql_yaml_file
        self.delta_load_file = delta_load_file
        self.source = source
        self.load_type = load_type
        self.database_configs = database_configs

        try:
            self.connect_to_edw()
            logging.info("EDW connection opened successfully!")
            self.sql_qrys = self.load_local_sql_query_yaml()
        except Exception as e:
            logging.error(f"Exception occurred at get source database connection: {str(e)}")

    def connect_to_edw(self):
        """
        Establish a new connection to EDW.
        """
        ssl_options = {
            'ssl': {
                'ssl_version': self.database_configs['EDW']["TLSVersions"]
            }
        }

        self.edw_connection = pymysql.connect(
            user=self.database_configs['EDW']['Username'],
            password=self.database_configs['EDW']['Password'],
            host=self.database_configs['EDW']['Hostname'],
            database=self.database_configs['EDW']['Database'],
            **ssl_options
        )

    def reconnect(self):
        """
        Attempt to reconnect to EDW.
        """
        try:
            logging.warning("Reconnecting to EDW...")
            self.connect_to_edw()
            logging.info("Reconnected to EDW successfully.")
        except Exception as e:
            logging.error(f"Reconnection to EDW failed: {str(e)}")
            raise

    def is_connection_alive(self):
        """
        Check if the EDW connection is alive.
        """
        try:
            self.edw_connection.ping(reconnect=False)
            return True
        except:
            return False

    def query_with_retry(self, query, params=None):
        """
        Execute SQL query with retry logic (hardcoded max_retries = 3).
        """
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                if not self.is_connection_alive():
                    self.reconnect()

                return pd.read_sql(query, con=self.edw_connection, params=params)

            except (pymysql.err.OperationalError, pymysql.err.InterfaceError) as e:
                attempt += 1
                logging.warning(f"Retry {attempt}/{max_retries}: {str(e)}")
                time.sleep(2 ** attempt)  # exponential backoff
                self.reconnect()
            except Exception as e:
                logging.error(f"Unrecoverable error during query: {str(e)}")
                break

        logging.error(f"All {max_retries} attempts failed for query")
        return pd.DataFrame()

    def load_local_sql_query_yaml(self):
        """
        Load SQL queries from YAML.
        """
        try:
            with open(self.sql_yaml_file, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.error(f"Failed to load SQL YAML: {str(e)}")
            return {}

    def load_delta_times_yaml(self):
        """
        Load delta time configuration.
        """
        try:
            with open(self.delta_load_file, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.error(f"Failed to load delta YAML: {str(e)}")
            return {}

    def close_connections(self):
        """
        Close all DB connections.
        """
        try:
            if self.source.lower() == 'glide' and hasattr(self, 'glide_connection'):
                self.glide_connection.close()
                logging.info("GLIDE connection closed.")
            elif hasattr(self, 'edw_connection') and self.edw_connection.open:
                self.edw_connection.close()
                logging.info("EDW connection closed.")
        except Exception as e:
            logging.error(f"Error closing {self.source} connection: {str(e)}")

    def fetch_data_from_edw(self, feature_name, sql_query_param):
        """
        Fetch full data from EDW.
        """
        try:
            if self.load_type == "full":
                query = self.sql_qrys['edw_query'][sql_query_param]
                return self.query_with_retry(query)
        except Exception as e:
            logging.error(f"Error in fetch_data_from_edw({feature_name}): {str(e)}")

    def fetch_Batchdata_from_entitlement_master(self, feature_name, sql_query_param, chunksize, offset):
        """
        Fetch batched data from Entitlement Master.
        """
        try:
            query = self.sql_qrys['edw_query'][sql_query_param]
            query = f"{query} LIMIT {chunksize} OFFSET {offset}"
            return self.query_with_retry(query)
        except Exception as e:
            logging.error(f"Error in fetch_Batchdata_from_entitlement_master({feature_name}): {str(e)}")

    def fetch_data_from_eservice_data(self, feature_name, sql_query_param, placeholders, keys):
        """
        Fetch data from E-Service.
        """
        try:
            query = self.sql_qrys['edw_query'][sql_query_param].format(placeholders=placeholders)
            return self.query_with_retry(query, params=keys)
        except Exception as e:
            logging.error(f"Error in fetch_data_from_eservice_data({feature_name}): {str(e)}")
