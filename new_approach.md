Problem: I have vendor records in pandas dataframe. 
I have different condition for different columns to raise warning, and to reject the record. 
There has to be different logic for warning and rejection for new records and existing records in database.

I want to write a code which is easy to maintain and add more conditions for warning and rejection later.

also i want to store the warning and rejection messsges.
Also i want to create separate dataframe having good records processed with warnings and rejected records.

The key columns are 
new record rejection columns: CM_PERS_ID, START_DATE, END_DATE, MANAGER_ID, FIRST_NAME, LAST_NAME, CX_PV_SOURCE

new records warning columns check: ManagerEmail, 
Existing records warning check: FIRST_NAME, LAST_NAME, CX_PV_SOURCE, ManagerEmail

existing records rejection columns: START_DATE, END_DATE, MANAGER_ID

### Breakdown of the Columns:
- **New Record Rejection Conditions**:
  - `MANAGER_ID`: should exist in neo4j db.
  - `FIRST_NAME`: should not be "DNE"
  - `LAST_NAME`: should not be "DNE"
  - `START_DATE`: Should not be "DNE"
  - `END_DATE`: Should not be "DNE"
  - `CXPVSOURCE`: should not be "DNE"

- **Existing Record Rejection Conditions**:
  - `MANAGER_ID`: should exist in neo4j db.
  - `START_DATE`: Should not be "DNE"
  - `END_DATE`: Should not be "DNE"
  
- **New Record Warning Conditions**:
  - `ManagerEmail`: Should exist in neo4j db.
  
- **Existing Record Warning Conditions**:
  - `ManagerEmail`: should exist in neo4j db.
  - `FIRST_NAME`, `LAST_NAME`: should not be "DNE"
  - `CXPVSOURCE`: Must not be empty.

rename the process_df as df, rejected_df as rejected_data_vendors, warned_data_vendors
i dont need warnings_list separately.
Append Reject_Warn_Reason separated with comma. Also, mention if its a new record or existing record.

v1.4 I want all the columns which are in df along with new column Reject_Warn_Reason in rejected_data_vendors and warned_data_vendors.

v1.5
First check for rejection, if the record not rejected then check for warning. 
If record is rejected and no need to check for warning.

v1.6 All the rejected records need to be removed from df in the end.
v1.7 should i initialize Reject_Warn_Reason column?
Suggest me approach.

