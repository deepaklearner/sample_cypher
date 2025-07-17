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