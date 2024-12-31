Modify below code to include a column rejection_reason with value as the column name having issue.
Give me a simple solution which is easy to understand and with minimal change in existing code.

def identify_vendor_reject_records(df):
    total_emps = set(df['CM_PERS_ID'])
    
    # Exclude records where certain fields contain 'DNE'
    df = df[
        ~(df['START_DATE'] == 'DNE') &
        ~(df['END_DATE'] == 'DNE') &
        ~(df['MANAGER_ID'] == 'DNE') &
        ~(df['FIRST_NAME'] == 'DNE') &
        ~(df['LAST_NAME'] == 'DNE') &
        ~(df['C_PV_SOURCE'] == 'DNE')
    ]
    
    logging.info(f"Filtered DataFrame: \n{df.to_string()}")
    
    configuration_file = '/opt/cvs/deepak/Neo4j_Inbound_dev/VENDOR/config/VENDOR_config.yaml'
    database_config = read_creds(configuration_file)
    
    manager_ids = df['MANAGER_ID'].unique().tolist()
    iam_graph_data_validator = IAMGraphDataValidator(database_config)
    
    with iam_graph_data_validator:
        valid_manager_ids = iam_graph_data_validator.check_user_existence_in_graphdb(manager_ids)
        df = df[df['MANAGER_ID'].isin(valid_manager_ids)]
    
    logging.info(f"Validated DataFrame: \n{df.to_string()}")
    
    missing_data_vendors = total_emps - set(df['CM_PERS_ID'])
    return df, missing_data_vendors
