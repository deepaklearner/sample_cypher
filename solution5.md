Modify below python code.

I want to label the incoming records whether its to update the existing data in neo4j or to insert new data in neo4j. Based on CM_PERS_ID employeeNumber property in User node.

1. For new record scenario, check ['START_DATE', 'END_DATE', 'MANAGER_ID', 'FIRST_NAME', 'LAST_NAME', 'CX_PV_SOURCE'] columns if having DNE value.
2. For update record, check FIRST_NAME, LAST_NAME and CX_PV_SOURCE, if they are having 'DNE', dont reject them. But if columns MANAGER_ID, START_DATE, END_DATE having DNE then reject them.
3. Change the value in FailureReason different for new record scenario and for update scenario.

4. Use UNWIND and return only those employeeNumber from neo4j, which are not present as i know very less number of records will be having issue. in this manner i think we can reduce data transfer over network.

5. Also add different message in FailureReason for update and new record scenario.

6. Also, optimize the solution to check if the record for update scenario or new record by returning only employee_numbers which dont exist in neo4j. This i think will reduce data transfer over network as i know very few records are having issue.