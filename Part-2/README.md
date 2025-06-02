1.1 I have 8.8 million entitlements.
I want to search their status in Neo4j.

Suppose if I read in batches of 25k then use a cypher as below:
"""MATCH (u:User)
WHERE (u.employeeNumber IN $empids)
RETURN u.employeeNumber, u.status

where empids is list"""

or use unwind to get the status 

Which approach will be faster?

1.2 I have a pandas dataframe. and in it has multiple columns. I want to create a list of column name "entitlementName"

2.1 give me ideas to organize this code to make it easy to maintain 

2.3 i want to create a separate python file with name "entitlements_data_transformation.py and class name as IAMDataTransformation