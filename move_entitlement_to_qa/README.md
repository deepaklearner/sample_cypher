1.1 
a. I have two databases mysql edw and neo4j.
b. I am syncing data from edw to neo4j db for entitlement owners.
c. below are the steps i am following:
    1. read all entitlements in neo4j in batch
    2. for batch 1, find the owners in neo4j
        UNWIND $entitlements AS ent
MATCH (e:Entitlement {
    entitlementName: ent.entitlementName,
    targetSystem: ent.targetSystem
})
OPTIONAL MATCH (e)-[:OWNER]->(u:User)
RETURN
    e.entitlementName AS entitlementName,
    e.targetSystem AS targetSystem,
    e.description AS description,
    e.riskLevel AS riskLevel,
    e.priviledgedAccess AS priviledgedAccess,
    e.entitlementType AS entitlementType,
    e.entitlementName + '|' + e.targetSystem AS concat_attr_entitlements1,
    e.entitlementName + '|' + e.targetSystem + '|' +
        coalesce(e.description, 'DNE') + '|' +
        coalesce(e.riskLevel, 'DNE') + '|' +
        coalesce(e.priviledgedAccess, 'DNE') + '|' +
        coalesce(e.entitlementType, 'DNE') AS concat_attr_entitlements2,
    collect(u.employeeNumber) AS owners;

    3. Then fetch the entitmenent owner from edw db
    SELECT
    entitle_name,
    platform AS entitle_source,
    MAX(CASE WHEN rank = 1 THEN owner END) AS owner1,
    MAX(CASE WHEN rank = 2 THEN owner END) AS owner2,
    MAX(CASE WHEN rank = 3 THEN owner END) AS owner3
FROM eservice_data
WHERE (entitle_name, platform) IN %s
GROUP BY entitle_name, platform;

4. Then calculate delta to obtain:
    inactive edw owners in neo4j,
    missing edw owners in neo4j,
    delta entitlement owner flag,
    all edw owners present in neo4j

5. At last, i am assigning and updating data in neo4j

UNWIND $records AS row
WITH row, [row.owner1, row.owner2, row.owner3] AS validOwners
MERGE (e:Entitlement {entitlementName: row.entitlementName, targetSystem: row.targetSystem})
SET e.entitlementID = row.entitlementID,
    e.description = row.description,
    e.riskLevel = row.riskLevel,
    e.priviledgedAccess = row.priviledgedAccess,
    e.entitlementType = row.entitlementType

WITH e, validOwners

// Step 1: Handle removed owners
OPTIONAL MATCH (e)-[r:HAS_OWNER]->(u:User)
WHERE NOT u.employeeNumber IN validOwners
WITH e, validOwners, r, u
FOREACH (_ IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
    DELETE r
    MERGE (e)-[:PREVIOUS]->(u)
)

WITH e, validOwners

// Step 2: Handle new or unchanged owners
UNWIND validOwners AS ownerId
MATCH (u:User {employeeNumber: ownerId})
MERGE (e)-[:HAS_OWNER]->(u)


One issue in this approach is, I am not obtaining the status of owners present in edw in the graph db.
When should I do it to have a optimized solution?

in delta step, find removed_owners as well. 


1.2 inactive owner is based on label of User node in neo4j, if it has Active label or not
correct removed definition: Owner exist in Neo4j data, but is missing in current EDW data

1.3 full code

2.1 I have below data:
entitlementName, targetSystem, edwOwners
How should I pass the data to update in neo4j using unwind. Like should I pass as a dataframe or dictionary?


3.1 I have data in edw db and in neo4j db related to entitlements.
The key is entitlementName and targetSystem. And i have to identify the new and updated data.

And then run two cypher quesries to load/update the data in neo4j.

The other columns are description, rishLevel, proviledgedAccess, entitlementType.

Total data i have is 5 million.

Approach 1: I am thinking is:
a. Read the data from EDW db in batches of 40k.
b. fetch the same data from graph db.
c. Identify the new and updated entitlements
d. Run two cypher queries.

Approach 2:
a. Read the data from EDW db in batches of 40k.
b. Take this data and do comparison in graph db and if there are mismatch or data not found,
then load the data or update the data accordingly.

which approach is better?

3.2 Identify the new and updated entitlements
The way I am doing is: I am creating pandas dataframe from the edw data and also from neo4j data.
new_entitlements = entitlements_edw[~entitlements_edw['concat_attr_entitlements1].isin(entitlements_neo4j['concat_attr_entitlements1'])]

what if i do entitlements_edw['concat_attr_entitlements1']- entitlements_neo4j['concat_attr_entitlements1']

3.3 """new_keys = set(entitlements_edw['concat_attr_entitlements1']) - set(entitlements_neo4j['concat_attr_entitlements1'])
new_entitlements = entitlements_edw[entitlements_edw['concat_attr_entitlements1'].isin(new_keys)]""" is better or """new_entitlements = entitlements_edw[~entitlements_edw['concat_attr_entitlements1].isin(entitlements_neo4j['concat_attr_entitlements1'])]"""



3.4 and how to find the updated data for concat_attr_entitlements2