def identify_vendor_reject_records(df):
    """
    Function to identify valid records for vendors and missing data vendors.
    """

    # Extract manager IDs from the dataframe
    manager_ids = df['managerid'].tolist()

    # Load configuration file
    configuration_file = '../config/config.yaml'
    database_config = read_creds(configuration_file)

    # Initialize the IAM Graph Data Validator
    iam_graph_data_validator = IAMGraphDataValidator(database_config)

    # Check if manager IDs exist in the database
    with iam_graph_data_validator:
        manager_ids_exists_df = iam_graph_data_validator.check_user_existance(manager_ids)

    # Filter valid manager IDs
    valid_manager_ids_df = manager_ids_exists_df[manager_ids_exists_df['exists'] == True]

    # Filter dataframe for valid manager IDs
    df = df[df['managerid'].isin(valid_manager_ids_df['managerid'])]

    # Get the set of all employee IDs
    total_emps = set(df['CM_PERS_ID'])

    # Filter out records with missing or invalid data
    df = df[
        ~(df['START_DATE'] == 'DNE') &
        ~(df['END_DATE'] == 'DNE') &
        ~(df['MANAGER_ID'] == 'DNE') &
        ~(df['FIRST_NAME'] == 'DNE') &
        ~(df['LAST_NAME'] == 'DNE') &
        ~(df['CX_PV_SOURCE'] == 'DNE')
    ]

    # Identify missing data vendors
    missing_data_vendors = total_emps - set(df['CM_PERS_ID'])

    return df, missing_data_vendors
