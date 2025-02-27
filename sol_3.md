// Assume df is already available as a list of rows with the required data
UNWIND $data AS row

// Match the existing User node based on CVSResourceid (which maps to employeeNumber in Neo4j)
MATCH (u:User {employeeNumber: row.CVSResourceid})

// Check if the properties of the User node need to be updated, and update if necessary
WITH u, row
WHERE u.aetnaresourceid <> row.AetnaResourceid 
    OR u.cvsnetworkid <> row.cvsnetworkid 
    OR (row.cid IS NOT NULL AND u.cid <> row.cid)  // Update cid only if it's not null and different

// Update the properties in the User node if there's any change
SET u.aetnaresourceid = row.AetnaResourceid,
    u.cvsnetworkid = row.cvsnetworkid

// If cid is not null, set the cid, otherwise remove the cid property
WITH u, row
WHERE row.cid IS NOT NULL
SET u.cid = row.cid

// If cid is null in MySQL, remove the cid property from the User node
WITH u, row
WHERE row.cid IS NULL
REMOVE u.cid

// Create the AetnaNetworkIdentifier node if it doesn't already exist
MERGE (a:AetnaNetworkIdentifier {networkid: row.AetnaResourceid})
SET a.uid = substring(row.AetnaResourceid, 1)  // Slicing off the first character

// Create the relationship between the User and the AetnaNetworkIdentifier node
MERGE (u)-[r:HAS_AETNA_ID]->(a)
SET r.assigned_date = timestamp()  // Set the current timestamp for the assigned_date property

RETURN u, a, r
