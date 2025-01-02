import pandas as pd
from neo4j import GraphDatabase

def identify_vendor_reject_records(df, neo4j_driver):
    """
    Function to identify valid records for vendors and missing data vendors,
    including Neo4j validation for manager IDs and fetching manager email only for invalid records.
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

    # Extract unique manager IDs for Neo4j validation (only for rejected records)
    invalid_manager_ids = missing_data_vendors['MANAGER_ID'].unique().tolist()

    # Single Cypher query to validate manager IDs and fetch manager's email for invalid records
    cypher_query = """
    UNWIND $manager_ids AS manager_id
    MATCH (u:User {employeeNumber: manager_id})-[:HAS_ATTRIBUTE]->(we:WorkEmail)
    OPTIONAL MATCH (u)-[:HAS_ATTRIBUTE]->(we2:WorkEmail)
    RETURN u.employeeNumber AS manager_id, coalesce(we.email, 'NOT_FOUND') AS manager_email
    """

    # Validate manager IDs in Neo4j and fetch manager emails for invalid records
    with neo4j_driver.session() as session:
        result = session.run(cypher_query, manager_ids=invalid_manager_ids)
        manager_email_dict = {record['manager_id']: record['manager_email'] for record in result}

    # Add manager email to invalid records only
    missing_data_vendors['ManagerEmail'] = missing_data_vendors['MANAGER_ID'].map(manager_email_dict)

    # Identify records with invalid manager IDs (i.e., manager ID not found in Neo4j)
    invalid_manager_mask = missing_data_vendors['ManagerEmail'] == 'NOT_FOUND'
    invalid_manager_records = missing_data_vendors[invalid_manager_mask].copy()
    invalid_manager_records['FailureReason'] = 'MANAGER_ID not found in Neo4j'
    
    # Add records with invalid manager IDs to missing_data_vendors
    missing_data_vendors = pd.concat([missing_data_vendors, invalid_manager_records], ignore_index=True)

    # Reset the index of the DataFrame to avoid indexing errors
    df = df.reset_index(drop=True)

    # Reset the index of the boolean mask to align with df
    invalid_manager_mask = invalid_manager_mask.reset_index(drop=True)

    # Now apply the boolean mask to filter out invalid manager records
    df = df[~invalid_manager_mask]

    # Update missing_data_vendors set
    missing_data_vendors_set = total_emps - set(df['CM_PERS_ID'])

    return df, missing_data_vendors, missing_data_vendors_set
