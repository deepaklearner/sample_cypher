This code is not working for a scenario. I have a existing record in neo4j and I am its first name as DNE.
Its not included in final df.

def identify_vendor_reject_records(df, config_file):
    # Read database credentials
    database_config = read_creds(config_file)
    
    # Columns to check for 'DNE'
    new_record_reject_cols = ['START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE']
    update_record_reject_cols = ['START_DATE', 'END_DATE', 'MANAGER_ID']
    update_record_warning_cols = ['FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE']
    
    # Get the set of all employee IDs
    total_emps = set(df['CM_PERS_ID'])
    
    # Check if employee ID exists in graph DB
    iam_graph_data_operations = IAGraphDataOperations(database_config)
    with iam_graph_data_operations:
        existing_emps = iam_graph_data_operations.get_existing_emps(total_emps)
    
    # 1. Identify new and existing records
    new_records = df[~df['CM_PERS_ID'].isin(existing_emps)]
    existing_records = df[df['CM_PERS_ID'].isin(existing_emps)]
    
    # 2. Process new records
    new_record_reject_cond = (new_records[new_record_reject_cols] == 'DNE').any(axis=1)
    new_record_rejected = new_records[new_record_reject_cond].copy()
    new_record_rejected['Reject_Warn_Reason'] = new_record_rejected[new_record_reject_cols].apply(
        lambda row: generate_failure_reason(row, new_record_reject_cols, "New record Error. Record rejected"), axis=1
    )
    
    # 3. Process existing records (updates)
    existing_record_reject_cond = (existing_records[update_record_reject_cols] == 'DNE').any(axis=1)
    existing_record_warn_cond = (existing_records[update_record_warning_cols] == 'DNE').any(axis=1)
    
    existing_record_rejected = existing_records[existing_record_reject_cond].copy()
    existing_record_rejected['Reject_Warn_Reason'] = existing_record_rejected[update_record_reject_cols].apply(
        lambda row: generate_failure_reason(row, update_record_reject_cols, "Update record Error. Record rejected"), axis=1
    )
    
    existing_record_warned = existing_records[existing_record_warn_cond & ~existing_record_reject_cond].copy()
    existing_record_warned['Reject_Warn_Reason'] = existing_record_warned[update_record_warning_cols].apply(
        lambda row: generate_failure_reason(row, update_record_warning_cols, "Update record Warning. Record processed."), axis=1
    )
    
    # Combine rejected and warned records
    rejected_data_vendors = pd.concat([new_record_rejected, existing_record_rejected], ignore_index=True)
    warned_data_vendors = pd.concat([existing_record_warned], ignore_index=True)
    rejected_n_warned_data_vendors = pd.concat([new_record_rejected, existing_record_rejected, existing_record_warned], ignore_index=True)
    
    # Update the main DataFrame with accepted records
    df = pd.concat([
        existing_records[~existing_record_reject_cond & ~existing_record_warn_cond],
        new_records[~new_record_reject_cond]
    ], ignore_index=True)
    
    # 4. Find their manager emails
    manager_empids = rejected_n_warned_data_vendors['MANAGER_ID'].unique().tolist()
    manager_email_dict = iam_graph_data_operations.fetch_work_email(manager_empids)
    
    # Add manager emails to rejected and warned records
    rejected_n_warned_data_vendors['ManagerEmail'] = rejected_n_warned_data_vendors['MANAGER_ID'].map(manager_email_dict)
    rejected_data_vendors['ManagerEmail'] = rejected_data_vendors['MANAGER_ID'].map(manager_email_dict)
    warned_data_vendors['ManagerEmail'] = warned_data_vendors['MANAGER_ID'].map(manager_email_dict)
    
    # Identify records with invalid manager IDs
    invalid_manager_mask = rejected_n_warned_data_vendors['ManagerEmail'].isna()
    invalid_manager_records = rejected_n_warned_data_vendors[invalid_manager_mask].copy()
    invalid_manager_records['Reject_Warn_Reason'] += ' and MANAGER_ID not found in Neo4j'
    
    # Update rejected and warned data vendors with invalid manager records
    rejected_data_vendors.update(invalid_manager_records)
    warned_data_vendors.update(invalid_manager_records)
    
    # Fill NaN with 'DNE'
    rejected_data_vendors['ManagerEmail'] = rejected_data_vendors['ManagerEmail'].fillna('DNE')
    warned_data_vendors['ManagerEmail'] = warned_data_vendors['ManagerEmail'].fillna('DNE')
    
    # Reset the index of the DataFrame to avoid indexing errors
    df.reset_index(drop=True, inplace=True)
    
    # Log the final DataFrames
    logging.info(f"deepak df: \n{df.to_string()}")
    logging.info(f"deepak warned_data_vendors: \n{warned_data_vendors.to_string()}")
    logging.info(f"deepak rejected_data_vendors: \n{rejected_data_vendors.to_string()}")
    
    # Return the updated DataFrames
    return df, rejected_data_vendors, warned_data_vendors
