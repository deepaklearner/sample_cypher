// Assume df is already available as a list of rows with the required data
UNWIND $data AS row

// Match the existing User node based on CVSResourceid (which maps to employeeNumber in Neo4j)
MATCH (u:User {employeeNumber: row.CVSResourceid})

// Check if the properties of the User node need to be updated
WITH u, row
WHERE COALESCE(u.aetnaresourceid, 'DNE') <> row.AetnaResourceid
    OR COALESCE(u.cvsnetworkid, 'DNE') <> row.cvsnetworkid
    OR COALESCE(u.cid, 'DNE') <> row.cid

// Handle the case when aetnaresourceid changes (needs conversion)
OPTIONAL MATCH (u)-[r:HAS_AETNA_ID]->(a:AetnaNetworkIdentifier)
WHERE u.aetnaresourceid IS NOT NULL AND u.aetnaresourceid <> row.AetnaResourceid
WITH u, row, r, a
// Remove the old relationship and delete the old node
FOREACH (_ IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END |
    DELETE r
)
FOREACH (_ IN CASE WHEN a IS NOT NULL THEN [1] ELSE [] END |
    DELETE a
)

// Update the properties in the User node if necessary
SET u.aetnaresourceid = row.AetnaResourceid,
    u.cvsnetworkid = row.cvsnetworkid,
    u.cid = row.cid

// Create or merge the new AetnaNetworkIdentifier node
WITH u, row
WHERE row.AetnaResourceid <> 'DNE'
MERGE (a_new:AetnaNetworkIdentifier:NetworkIdentifier {networkid: row.AetnaResourceid})
SET a_new.uid = row.AetnaResourceid  // Or any other property you want to set for AetnaNetworkIdentifier

// Create the relationship between the User and the new AetnaNetworkIdentifier node
MERGE (u)-[r_new:HAS_AETNA_ID]->(a_new)
SET r_new.assigned_date = timestamp()  // Set the current timestamp for the assigned_date property

RETURN u, a_new, r_new