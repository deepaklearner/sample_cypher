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

Suggest me approach.

