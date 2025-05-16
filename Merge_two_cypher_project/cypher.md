aetna_nw_identifier_query =
'''
UNWIND $rows AS row
WITH row
WHERE row.Aetnaldentifier_flag = "y"

MATCH (usr:User {employeeNumber: row.CVSResourceid})
WHERE NOT (usr)-[:HAS_ATTRIBUTE]->(:AetnaNetworkIdentifierInfo)

WITH COLLECT(usr) AS user_array

MATCH (aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_nw_identifier)-[]-()

WITH aetna_nw_identifier, user_array
ORDER BY aetna_nw_identifier.networkid ASC

WITH COLLECT(aetna_nw_identifier) AS id_array, user_array

UNWIND apoc.coll.zip(user_array, id_array) AS row
WITH 
    row[0] AS u,
    row[1] AS aetna_nw_identifier,
    CASE 
        WHEN 'Employee' IN labels(row[0]) THEN 'A'
        WHEN 'Contractor' IN labels(row[0]) THEN 'N'
    END AS prefix

// Add networkid in the available Aetna identifier node
SET aetna_nw_identifier.networkid = prefix + aetna_nw_identifier.uid

// Create new IdentifierInfo node
CREATE (new_identifier_info:AetnaNetworkIdentifierInfo {
    eventID: toString(u.employeeNumber) + '' + (prefix + aetna_nw_identifier.uid) + '.' + toString(datetime()),
    date: datetime()
})

// Establish new relationships
MERGE (u)-[:HAS_ATTRIBUTE]->(new_identifier_info)
MERGE (new_identifier_info)-[new_r_has_aetna_id:HAS_AETNA_ID]->(aetna_nw_identifier)
SET 
    new_r_has_aetna_id.assigned_date = datetime(),
    new_r_has_aetna_id.assignedBy = 'INT5043'

MERGE (new_identifier_info)-[:CURRENT]->(aetna_nw_identifier)

// Update User properties
SET 
    u.aetnaresourceid = prefix + aetna_nw_identifier.uid,
    u.is_updated = 'y'

FOREACH (x IN CASE WHEN u.cvsnetworkid IS NULL THEN [1] ELSE [] END |
    SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
)

RETURN count(*) AS total
'''

conversion_identifier_query =
'''
UNWIND $rows AS row

MATCH (usr:User {employeeNumber: row.CVSResourceid})
WHERE 'Conversion' IN labels(usr) 
  AND row.is_conversion = 'Y'

WITH COLLECT(usr) AS usr_array, row

MATCH (aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_nw_identifier)-[]-()

WITH usr_array, COLLECT(aetna_nw_identifier) AS aetna_array

UNWIND apoc.coll.zip(usr_array, aetna_array) AS row

WITH 
    row[0] AS u,
    row[1] AS aetna_nw_identifier,
    CASE 
        WHEN 'Employee' IN labels(row[0]) THEN 'A'
        WHEN 'Contractor' IN labels(row[0]) THEN 'N'
        ELSE 'DNE'
    END AS prefix

// Find existing identifier info and relationships
OPTIONAL MATCH (u)-[has_identifier_info:HAS_ATTRIBUTE]->(identifier_info:AetnaNetworkIdentifierInfo)
OPTIONAL MATCH (identifier_info)-[r_curr:CURRENT]-(curr_aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
OPTIONAL MATCH (identifier_info)-[r_has_aetna_id:HAS_AETNA_ID]-(curr_aetna_nw_identifier)

WITH 
    u, aetna_nw_identifier, prefix, has_identifier_info, identifier_info, 
    r_curr, curr_aetna_nw_identifier, COLLECT(r_has_aetna_id) AS rels_has_aetna_id,
    CASE 
        WHEN curr_aetna_nw_identifier IS NULL 
             OR (prefix + aetna_nw_identifier.uid) <> curr_aetna_nw_identifier.networkid 
             THEN true 
        ELSE false 
    END AS codesDiffer

WHERE codesDiffer

// Rename HAS_AETNA_ID to HAD_AETNA_ID while keeping properties
CALL apoc.refactor.rename.type("HAS_AETNA_ID", "HAD_AETNA_ID", rels_has_aetna_id)
YIELD committedOperations

WITH u, aetna_nw_identifier, prefix, identifier_info, curr_aetna_nw_identifier, has_identifier_info, r_curr

// Add networkid in the available Aetna identifier node
SET aetna_nw_identifier.networkid = prefix + aetna_nw_identifier.uid

// Create new IdentifierInfo node
CREATE (new_identifier_info:AetnaNetworkIdentifierInfo {
    eventID: toString(u.employeeNumber) + (prefix + aetna_nw_identifier.uid) + '.' + toString(datetime()),
    date: datetime()
})

// Establish new relationships
MERGE (u)-[:HAS_ATTRIBUTE]->(new_identifier_info)
MERGE (new_identifier_info)-[new_r_has_aetna_id:HAS_AETNA_ID]->(aetna_nw_identifier)
SET 
    new_r_has_aetna_id.assigned_date = datetime(),
    new_r_has_aetna_id.assignedBy = 'INT5043'

MERGE (new_identifier_info)-[:CURRENT]->(aetna_nw_identifier)

// Link to previous identifier info if it exists
FOREACH (_ IN CASE WHEN identifier_info IS NOT NULL THEN [1] ELSE [] END |
    MERGE (new_identifier_info)-[:PREVIOUS]->(identifier_info)
)

// Update User properties
SET 
    u.legacyaetnaresourceid = u.aetnaresourceid,
    u.aetnaresourceid = prefix + aetna_nw_identifier.uid,
    u.is_updated = 'y'

FOREACH (x IN CASE WHEN u.cvsnetworkid IS NULL OR u.cvsnetworkid = curr_aetna_nw_identifier.networkid THEN [1] ELSE [] END |
    SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
)

// Delete old relationships if they exist
DELETE has_identifier_info, r_curr
REMOVE curr_aetna_nw_identifier.networkid

RETURN count(*) AS total
'''