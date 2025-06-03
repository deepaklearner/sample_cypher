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

2.4 I have two pandas dataframes:
entitlements_owners_in_graph
columns are: entitlementName, targetSystem, owners and owners_status
owners is a python list and owners_status a list of lists containing employeeNumber and their status.
[['A1010', Active],['A1818',Inactive]]

and
entitlements_owners_in_edw
entitlementName, targetSystem, owner1, owner2 and owner3

I need to find the delta_entitlement_owners, active_owners and missing_owners in graph db