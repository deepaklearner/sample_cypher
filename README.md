1.1 I have a pandas dataframe "df" and User node in neo4j.

The columns I have in df are:
employeeNumber, userType, employmentStatus, recordType, hireDate

We need to perform below for dataframe "df" records:
a. Filter all records in df, where userType = "Employee"
b. If User node has label "Contractor" in neo4j, check if recordType is "Conversion" in df
c. Check if employmentStatus in ['A', 'L'] in df and in also label in Neo4j in ['Active', 'OnLeave'] and compare.
i just want to check employmentStatus in ['A','L'] and Neo4J label in ['Active', 'OnLeave']

i need just employeeNumber and Reason for mismatched records

k. If any of the records doesnt match, take those records out and write in log.
l. filter the mismatched ones from original df

1.2
can we do dataframe operations instead of iterrows()

1.3 find the valid record by negating the employNumber present in mismatch_df compared to original df

1.4 
i changed to inner join and removed """labels_df.set_index('employeeNumber', inplace=True)
labels_df = labels_df.reindex(employee_df['employeeNumber']).fillna({'labels': [[]]})
labels_df.reset_index(inplace=True)"""

i dont want to track "User node not found in Neo4j"

1.5 full code

2.1 