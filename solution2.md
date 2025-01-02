can we rename dne_mask as reject_condition. 

import pandas as pd
from neo4j import GraphDatabase

def identify_vendor_reject_records(df, neo4j_driver):
    """
    Function to identify valid records for vendors and missing data vendors,
    including Neo4j validation for manager IDs.
    """
    # Columns to check for 'DNE' values
    columns_to_check = ['START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE']

    # Get the set of all employee IDs
    total_emps = set(df['CM_PERS_ID'])

    # Create a boolean mask for reject conditions (i.e., 'DNE' values)
    reject_condition = (df[columns_to_check] == 'DNE').any(axis=1)

    # Capture rejected records with reasons
    missing_data_vendors = df[reject_condition].copy()
    missing_data_vendors['FailureReason'] = df[columns_to_check].apply(
        lambda row: ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    # Keep only valid records in df
    df = df[~reject_condition]

    # Extract unique manager IDs for Neo4j validation
    manager_ids = df['MANAGER_ID'].unique().tolist()

    # Cypher query to validate manager IDs
    cypher_query = """
    UNWIND $manager_ids AS manager_id
    MATCH (u:User {employeeNumber: manager_id})
    RETURN manager_id
    """

    # Validate manager IDs in Neo4j
    with neo4j_driver.session() as session:
        result = session.run(cypher_query, manager_ids=manager_ids)
        valid_manager_ids = [record['manager_id'] for record in result]

    # Identify records with invalid manager IDs
    invalid_manager_mask = ~df['MANAGER_ID'].isin(valid_manager_ids)
    invalid_manager_records = df[invalid_manager_mask].copy()
    invalid_manager_records['FailureReason'] = 'MANAGER_ID not found in Neo4j'
    
    # Add records with invalid manager IDs to missing_data_vendors
    missing_data_vendors = pd.concat([missing_data_vendors, invalid_manager_records], ignore_index=True)

    # Keep only records with valid manager IDs in df
    df = df[~invalid_manager_mask]

    # Update missing_data_vendors set
    missing_data_vendors_set = total_emps - set(df['CM_PERS_ID'])

    return df, missing_data_vendors, missing_data_vendors_set

# Usage example:
# neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# valid_df, missing_data_vendors_df, missing_data_vendors_set = identify_vendor_reject_records(df, neo4j_driver)
