Certainly! Here's the full updated code incorporating all the modifications we've discussed:

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
    update_reject_columns = ['START_DATE', 'END_DATE', 'MANAGER_ID']
    update_warn_columns = ['FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE']

    # Get the set of all employee IDs
    total_emps = set(df['CM_PERS_ID'])

    # Get existing employee IDs from Neo4j
    existing_ids = get_existing_employee_ids(neo4j_driver, total_emps)

    # Identify existing and new records
    existing_records = df[df['CM_PERS_ID'].isin(existing_ids)]
    new_records = df[~df['CM_PERS_ID'].isin(existing_ids)]

    # Process existing records (updates)
    existing_reject_condition = (existing_records[update_reject_columns] == 'DNE').any(axis=1)
    existing_warn_condition = (existing_records[update_warn_columns] == 'DNE').any(axis=1)
    
    existing_rejected = existing_records[existing_reject_condition].copy()
    existing_rejected['FailureReason'] = existing_rejected[update_reject_columns].apply(
        lambda row: 'Update rejected: ' + ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    existing_warned = existing_records[existing_warn_condition & ~existing_reject_condition].copy()
    existing_warned['FailureReason'] = existing_warned[update_warn_columns].apply(
        lambda row: 'Update warning: ' + ', '.join([f"{col} is having invalid data" for col, val in row.items() if val == 'DNE']),
        axis=1
    )

    # Process new records
    new_reject_condition = (new_records[columns_to_check] == 'DNE').any(axis=1)
    new_rejected = new_records[new_reject_condition].copy()

    def generate_failure_reason(row):
        invalid_columns = [col for col, val in row.items() if val == 'DNE']
        grouped_columns = []
        if 'START_DATE' in invalid_columns and 'END_DATE' in invalid_columns:
            grouped_columns.append('START_DATE and END_DATE')
            invalid_columns = [col for col in invalid_columns if col not in ['START_DATE', 'END_DATE']]
        grouped_columns.extend(invalid_columns)
        return 'New record rejected: ' + ', '.join(grouped_columns) + ' having invalid data; Unable to process the record'

    new_rejected['FailureReason'] = new_rejected[columns_to_check].apply(generate_failure_reason, axis=1)

    # Combine rejected and warned records
    missing_data_vendors = pd.concat([existing_rejected, existing_warned, new_rejected], ignore_index=True)

    # Keep only valid records in df
    df = pd.concat([
        existing_records[~existing_reject_condition & ~existing_warn_condition],
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

def get_existing_employee_ids(neo4j_driver, ids):
    cypher_query = """
    UNWIND $ids AS id
    MATCH (u:User {employeeNumber: id})
    RETURN u.employeeNumber AS employee_id
    """
    with neo4j_driver.session() as session:
        result = session.run(cypher_query, ids=list(ids))
        return set(record['employee_id'] for record in result)
```

This code incorporates all the requirements and modifications we've discussed:

1. It separates processing for new and existing records.
2. For new records, it checks all specified columns for 'DNE' values and rejects if any are found, grouping 'START_DATE' and 'END_DATE' if both are invalid.
3. For existing records (updates), it:
   - Rejects if MANAGER_ID, START_DATE, or END_DATE have 'DNE' values.
   - Warns (adds to missing_data_vendors) but doesn't reject if FIRST_NAME, LAST_NAME, or CX_PV_SOURCE have 'DNE' values.
4. It uses different failure reasons for new and update scenarios.
5. The Neo4j query uses UNWIND for better performance.
6. It efficiently determines existing records by querying Neo4j with all IDs at once.

This code should handle all the scenarios we've discussed, including the specific formatting of the FailureReason for new records with multiple invalid columns.