1.1 I have a pandas dataframe "df" and User node in neo4j.

The columns I have in df are:
employeeNumber, userType

We need to perform below for dataframe "df" records:
a. Filter all records where userType = "Employee"
b. Get the data for filtered data from Neo4j and check if User node has label "Active" and compare with column employmentStatus in df
c. If User node has label 