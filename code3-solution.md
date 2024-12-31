To modify the code to include a column 'rejection_reason' with the value as the column name having an issue, we can make the following changes:

```python
def identify_vendor_reject_records(df):
    total_emps = set(df['CM_PERS_ID'])
    
    # Create a new column for rejection reason
    df['rejection_reason'] = ''
    
    # Check for 'DNE' in specific columns and set rejection reason
    columns_to_check = ['START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', 'C_PV_SOURCE']
    for col in columns_to_check:
        df.loc[df[col] == 'DNE', 'rejection_reason'] = col
    
    # Filter out rows with rejection reasons
    df_rejected = df[df['rejection_reason'] != '']
    df = df[df['rejection_reason'] == '']
    
    logging.info(f"Filtered DataFrame: \n{df.to_string()}")
    
    configuration_file = '/opt/cvs/deepak/Neo4j_Inbound_dev/VENDOR/config/VENDOR_config.yaml'
    database_config = read_creds(configuration_file)
    
    manager_ids = df['MANAGER_ID'].unique().tolist()
    iam_graph_data_validator = IAMGraphDataValidator(database_config)
    
    with iam_graph_data_validator:
        valid_manager_ids = iam_graph_data_validator.check_user_existence_in_graphdb(manager_ids)
        df_invalid_managers = df[~df['MANAGER_ID'].isin(valid_manager_ids)]
        df_invalid_managers['rejection_reason'] = 'MANAGER_ID'
        df = df[df['MANAGER_ID'].isin(valid_manager_ids)]
    
    logging.info(f"Validated DataFrame: \n{df.to_string()}")
    
    # Combine all rejected records
    df_rejected = pd.concat([df_rejected, df_invalid_managers])
    
    missing_data_vendors = total_emps - set(df['CM_PERS_ID'])
    return df, missing_data_vendors, df_rejected
```

This solution makes minimal changes to the existing code while adding the requested functionality. Here's what changed:

1. We add a new column 'rejection_reason' to the DataFrame at the beginning.
2. Instead of filtering out rows with 'DNE' values, we set the 'rejection_reason' for these rows and separate them into a new DataFrame `df_rejected`.
3. We do the same for invalid manager IDs, adding them to `df_rejected` with the reason 'MANAGER_ID'.
4. The function now returns an additional DataFrame `df_rejected` containing all rejected records with their reasons.

This approach maintains the original logic while providing more detailed information about why certain records were rejected.

Based on the code modification described earlier, the 'rejection_reason' column value would be set to the name of the column that has an issue. Specifically:

1. For records where certain fields contain 'DNE', the 'rejection_reason' value would be the name of the column containing 'DNE'. This could be any of the following: 'START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', or 'C_PV_SOURCE'[1].

2. For records with invalid manager IDs (those not found in the graph database), the 'rejection_reason' value would be set to 'MANAGER_ID'[1].

The 'rejection_reason' column serves to identify which specific data field caused a record to be rejected, providing more detailed information about why certain records were excluded from the final dataset.

Citations:
[1] https://www.hopsworks.ai/post/common-error-messages-in-pandas
[2] https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
[3] https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
[4] https://builtin.com/data-science/pandas-show-all-columns
[5] https://stackoverflow.com/questions/51452562/pandas-dataframe-consistently-falling-column-values