
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

b. owner1, owner2, owner3. They can we employeeNumber or aetnaresourceid (always starts with 'A') (both are properties of User node)

c. The constraints for Entitlement nodes are "entitlementName" and "targetSystem".

d. "Entitlement" node has below properties:
entitlementID,
entitlementName,
description,
riskLevel,
priviledgedAccess,
entitlementType,
targetSystem

e. Validate owner1, owner2 and owner3 if they exist in graph db or doesnt have "Active" label for the User node else create a error report. I dont want to validate for each owner if it exist in neo4j or not. I want to do in efficient manner. Suggest one?

f. For the valid ones, Create relationship "HAS_OWNER" to "User" node, based on owner1, owner2, owner3 

g. We are reading the data in batches of 50k. 

Give me ideas for efficient design.

2.1 In below cyphe query, I want to check if Entitlement with same owners set is present or not.
   If there is a change in owners or its not present, then create else dont create. 

   Also, if there is a change in any of the owners for an entitlement, move that owner node as below:
   (Entitlement)-[:PREVIOUS]->(User) and create new relationship with new owner.

    UNWIND $records AS record
    MERGE (e:Entitlement {entitlementName: record.entitlementName, targetSystem: record.targetSystem})
    SET e.entitlementID = record.entitlementID,
        e.description = record.description,
        e.riskLevel = record.riskLevel,
        e.priviledgedAccess = record.priviledgedAccess,
        e.entitlementType = record.entitlementType

    WITH e, record.validOwners AS owners
    UNWIND owners AS ownerId
    MATCH (u:User {employeeNumber: ownerId})
    MERGE (e)-[:HAS_OWNER]->(u)

not sure, if comparing owner set is right. because its also possible there is just change in one owner, then we will create just one owner and move the older to PREVIOUS

update record.validOwners as [row.owner1, row.owner2, row.owner3]

Questions:
What should we do if the Entitlement node already exists? Overwrite or skip?