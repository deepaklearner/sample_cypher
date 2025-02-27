// Assume df is already available as a list of rows with the required data
UNWIND $data AS row

// Match the existing User node based on CVSResourceid (which maps to employeeNumber in Neo4j)
MATCH (u:User {employeeNumber: row.CVSResourceid})

// Check if the properties of the User node need to be updated, and update if necessary
WITH u, row
WHERE u.aetnaresourceid <> row.AetnaResourceid 
    OR u.cvsnetworkid <> row.cvsnetworkid 
    OR u.cid <> row.cid  // Will check if cid differs

// Update the properties in the User node if there's any change
SET u.aetnaresourceid = row.AetnaResourceid,
    u.cvsnetworkid = row.cvsnetworkid,
    u.cid = row.cid  // This will remove the cid property if row.cid is null

// Create the AetnaNetworkIdentifier node if it doesn't already exist
MERGE (a:AetnaNetworkIdentifier {networkid: row.AetnaResourceid})
SET a.uid = row.AetnaResourceid  // Or any other property you want to set for AetnaNetworkIdentifier

// Create the relationship between the User and the AetnaNetworkIdentifier node
MERGE (u)-[r:HAS_AETNA_ID]->(a)
SET r.assigned_date = timestamp()  // Set the current timestamp for the assigned_date property

RETURN u, a, r
