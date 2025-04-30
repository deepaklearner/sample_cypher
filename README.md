
1.1 
Create a ETL process in python to read data from mysql db and load into neo4j graph db.
Give me ideas for efficient design. Also, let me know for any cross questions, I should ask for further clarification.

I documented the draft as:

1. Read data from mysql table edwmaster.entitlement_master. 
Columns: 
entitle_name as entitlementName,
entitle_desc as description,
risk_rating as riskLevel,
priv as priviledgedAccess,
resource_type as entitlementType,
entitle_source as targetSystem,
owner1, owner2, owner3 
FROM edwmaster.entitlement_master

Note: owner1, owner2, owner3 can be employeeNumber or AID

2. Create a node in neo4j with label "Entitlement" with below properties:
entitlementID,
entitlementName,
description,
riskLevel,
priviledgedAccess,
entitlementType,
targetSystem

3. The constraints for Entitlement nodes are "entitlementName" and "targetSystem"
4. Create relationship "HAS_OWNER" to "User" node, based on owner1, owner2, owner3 


Questions:
1. What if owner1, owner2, owner3, any one is missing? what if all are missing?
2. What if owner is inactive?
3. When to send email? only for failure?
4**. How to process delta?
