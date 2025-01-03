I apologize for the misunderstanding. You're absolutely right, we should group all column names together for all scenarios. Let's modify the code to achieve this for both new and existing records. Here's the updated version of the `identify_vendor_reject_records` function:

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

    def generate_failure_reason(row, columns, prefix):
    invalid_columns = [col for col, val in row[columns].items() if val == 'DNE']
    if invalid_columns:
        if prefix.startswith("Update"):
            return f"{prefix}: {' and '.join(invalid_columns)} having invalid data; Record processed"
        else:
            return f"{prefix}: {' and '.join(invalid_columns)} having invalid data; Unable to process the record"
    return ""


    # Process existing records (updates)
    existing_reject_condition = (existing_records[update_reject_columns] == 'DNE').any(axis=1)
    existing_warn_condition = (existing_records[update_warn_columns] == 'DNE').any(axis=1)
    
    existing_rejected = existing_records[existing_reject_condition].copy()
    existing_rejected['FailureReason'] = existing_rejected.apply(
        lambda row: generate_failure_reason(row, update_reject_columns, "Update rejected"),
        axis=1
    )

    existing_warned = existing_records[existing_warn_condition & ~existing_reject_condition].copy()
    existing_warned['FailureReason'] = existing_warned.apply(
        lambda row: generate_failure_reason(row, update_warn_columns, "Update warning"),
        axis=1
    )

    # Process new records
    new_reject_condition = (new_records[columns_to_check] == 'DNE').any(axis=1)
    new_rejected = new_records[new_reject_condition].copy()
    new_rejected['FailureReason'] = new_rejected.apply(
        lambda row: generate_failure_reason(row, columns_to_check, "New record rejected"),
        axis=1
    )

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

# The get_existing_employee_ids function remains the same
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

This updated version:

1. Introduces a `generate_failure_reason` function that groups all invalid column names together for any scenario.
2. Uses this function for both new and existing records, ensuring consistent formatting across all cases.
3. For existing records, it still separates reject and warn conditions but uses the same formatting for the FailureReason.
4. For new records, it checks all columns and groups them together in the FailureReason if they have 'DNE' values.

This approach will result in FailureReason messages like:
- "New record rejected: START_DATE and END_DATE and MANAGER_ID having invalid data; Unable to process the record"
- "Update rejected: START_DATE and MANAGER_ID having invalid data; Unable to process the record"
- "Update warning: FIRST_NAME and LAST_NAME having invalid data; Unable to process the record"

This should meet your requirement of grouping column names together for all scenarios.