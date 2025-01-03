'''
Modify below python code.

I want to label the incoming records whether its to update the existing data in neo4j or to insert new data in neo4j. Based on CM_PERS_ID employeeNumber property in User node.

1. For new record scenario, check ['START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE'] columns if having DNE value.
2. For update record, check FIRST_NAME, LAST_NAME and CX_PV_SOURCE, if they are having 'DNE', dont reject them. But if columns MANAGER_ID, START_DATE, END_DATE having DNE then reject them.
3. Change the value in FailureReason different for new record scenario and for update scenario.

4. Use UNWIND and return only those employeeNumber from neo4j, which are not present as i know very less number of records will be having issue. in this manner i think we can reduce data transfer over network.

5. Also add different message in FailureReason for update and new record scenario.

6. Also, optimize the solution to check if the record for update scenario or new record by returning only employee_numbers which dont exist in neo4j. This i think will reduce data transfer over network as i know very few records are having issue.
'''

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

    # Check which employee numbers don't exist in Neo4j
    with neo4j_driver.session() as session:
        result = session.run("""
        UNWIND $emp_ids AS emp_id
        OPTIONAL MATCH (u:User {employeeNumber: emp_id})
        WITH emp_id, u
        WHERE u IS NULL
        RETURN emp_id AS non_existing_emp_id
        """, emp_ids=list(total_emps))
        new_emp_ids = set(record['non_existing_emp_id'] for record in result)

    # Separate new and existing records
    new_records = df[df['CM_PERS_ID'].isin(new_emp_ids)]
    existing_records = df[~df['CM_PERS_ID'].isin(new_emp_ids)]

    # Process new records
    new_reject_condition = (new_records[columns_to_check] == 'DNE').any(axis=1)
    new_missing_data = new_records[new_reject_condition].copy()
    new_missing_data['FailureReason'] = new_records[columns_to_check].apply(
        lambda row: 'New record: ' + ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    # Process existing records
    update_columns = ['MANAGER_ID', 'START_DATE', 'END_DATE']
    existing_reject_condition = (existing_records[update_columns] == 'DNE').any(axis=1)
    existing_missing_data = existing_records[existing_reject_condition].copy()
    existing_missing_data['FailureReason'] = existing_records[update_columns].apply(
        lambda row: 'Update record: ' + ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    # Combine missing data
    missing_data_vendors = pd.concat([new_missing_data, existing_missing_data], ignore_index=True)

    # Keep only valid records in df
    df = pd.concat([
        new_records[~new_reject_condition],
        existing_records[~existing_reject_condition]
    ], ignore_index=True)

    # Extract unique manager IDs for Neo4j validation (only for rejected records)
    invalid_manager_ids = missing_data_vendors['MANAGER_ID'].unique().tolist()

    # Single Cypher query to validate manager IDs and fetch manager's email for invalid records
    cypher_query = """
    UNWIND $manager_ids AS manager_id
    MATCH (u:User {employeeNumber: manager_id})-[:HAS_ATTRIBUTE]->(we:WorkEmail)
    RETURN u.employeeNumber AS manager_id, we.email AS manager_email
    """

    # Validate manager IDs in Neo4j and fetch manager emails for invalid records
    with neo4j_driver.session() as session:
        result = session.run(cypher_query, manager_ids=invalid_manager_ids)
        manager_email_dict = {record['manager_id']: record['manager_email'] for record in result}

    # Add manager email to invalid records only
    missing_data_vendors['ManagerEmail'] = missing_data_vendors['MANAGER_ID'].map(manager_email_dict)

    # Identify records with invalid manager IDs (i.e., manager ID not found in Neo4j)
    invalid_manager_mask = missing_data_vendors['ManagerEmail'].isnull()
    invalid_manager_records = missing_data_vendors[invalid_manager_mask].copy()
    invalid_manager_records['FailureReason'] += ' and MANAGER_ID not found in Neo4j'
    
    # Update missing_data_vendors with invalid manager records
    missing_data_vendors.update(invalid_manager_records)

    # Update missing_data_vendors set
    missing_data_vendors_set = set(missing_data_vendors['CM_PERS_ID'])

    return df, missing_data_vendors, missing_data_vendors_set
