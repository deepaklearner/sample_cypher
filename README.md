
1.2
Create a ETL process in python to read data from mysql db and load into neo4j graph db in Entitlement node for entitlement data.

a. The columns we are reading from mysql are: 
entitle_name as entitlementName,
entitle_desc as description,
risk_rating as riskLevel,
priv as priviledgedAccess,
resource_type as entitlementType,
entitle_source as targetSystem,
owner1, owner2, owner3 
FROM edwmaster.entitlement_master

b. owner1, owner2, owner3 are employeeNumber 

c. The constraints for Entitlement nodes are "entitlementName" and "targetSystem".

d. "Entitlement" node has below properties:
entitlementID,
entitlementName,
description,
riskLevel,
priviledgedAccess,
entitlementType,
targetSystem

e. Validate owner1, owner2 and owner3 if they exist in graph db or has disabled label for the User node else create a error report.

f. For the valid ones, Create relationship "HAS_OWNER" to "User" node, based on owner1, owner2, owner3 

g. We are reading the data in batches of 50k.

Give me ideas for efficient design. Also, let me know for any cross questions, I should ask for further clarification.


1.3 i am thinking should i validate each owner or should i do in a batch?

Questions:
What should we do if the Entitlement node already exists? Overwrite or skip?