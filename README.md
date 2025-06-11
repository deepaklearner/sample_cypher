1.1 I have a pandas dataframe "df" and User node in neo4j.

The columns I have in df are:
employeeNumber, userType, employmentStatus, recordType

We need to perform below for dataframe "df" records:
a. Filter all records in df, where userType = "Employee"
b. If User node has label "Contractor" in neo4j, check if recordType is "Conversion" in df
c. Check if employmentStatus in ['A', 'L'] in df and in also label in Neo4j in ['Active', 'OnLeave'] and compare.
d. If any of the records doesnt match, take those records out and write in log.
e. filter the mismatched ones from original df