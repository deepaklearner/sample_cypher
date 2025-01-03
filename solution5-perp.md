Here's the modified Python code based on your requirements:

```python
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

    # Identify existing and new records
    existing_records = df[df['CM_PERS_ID'].isin(get_existing_employee_ids(neo4j_driver))]
    new_records = df[~df['CM_PERS_ID'].isin(get_existing_employee_ids(neo4j_driver))]

    # Process existing records
    existing_reject_condition = (
        (existing_records['MANAGER_ID'] == 'DNE') |
        (existing_records['START_DATE'] == 'DNE') |
        (existing_records['END_DATE'] == 'DNE')
    )
    existing_missing_data = existing_records[existing_reject_condition].copy()
    existing_missing_data['FailureReason'] = 'Update rejected: MANAGER_ID, START_DATE, or END_DATE is invalid'

    # Process new records
    new_reject_condition = (new_records[columns_to_check] == 'DNE').any(axis=1)
    new_missing_data = new_records[new_reject_condition].copy()
    new_missing_data['FailureReason'] = new_records[columns_to_check].apply(
        lambda row: 'New record rejected: ' + ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    # Combine rejected records
    missing_data_vendors = pd.concat([existing_missing_data, new_missing_data], ignore_index=True)

    # Keep only valid records in df
    df = pd.concat([
        existing_records[~existing_reject_condition],
        new_records[~new_reject_condition]
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
    invalid_manager_mask = missing_data_vendors['ManagerEmail'].isna()
    invalid_manager_records = missing_data_vendors[invalid_manager_mask].copy()
    invalid_manager_records['FailureReason'] += ' and MANAGER_ID not found in Neo4j'
    
    # Update missing_data_vendors with invalid manager records
    missing_data_vendors.update(invalid_manager_records)

    # Reset the index of the DataFrame to avoid indexing errors
    df = df.reset_index(drop=True)

    # Update missing_data_vendors set
    missing_data_vendors_set = total_emps - set(df['CM_PERS_ID'])

    return df, missing_data_vendors, missing_data_vendors_set

def get_existing_employee_ids(neo4j_driver):
    """
    Function to get existing employee IDs from Neo4j
    """
    cypher_query = """
    MATCH (u:User)
    RETURN u.employeeNumber AS employee_id
    """
    with neo4j_driver.session() as session:
        result = session.run(cypher_query)
        return [record['employee_id'] for record in result]
```

This modified code addresses all the requirements you specified:

1. It separates the processing for new and existing records based on the `CM_PERS_ID` (employeeNumber property in User node).
2. For new records, it checks all specified columns for 'DNE' values and rejects if any are found.
3. For existing records (updates), it only checks MANAGER_ID, START_DATE, and END_DATE for 'DNE' values.
4. It uses different failure reasons for new and update scenarios.
5. The Neo4j query uses UNWIND for better performance.
6. The FailureReason messages are different for new and update scenarios.

Note that I added a new function `get_existing_employee_ids()` to fetch existing employee IDs from Neo4j. This is necessary to determine which records are new and which are updates. You may need to adjust this function based on your exact Neo4j schema.

Also, the code now uses `isna()` instead of comparing to 'NOT_FOUND' to check for invalid manager IDs, as the `manager_email_dict` will not contain entries for manager IDs not found in Neo4j.