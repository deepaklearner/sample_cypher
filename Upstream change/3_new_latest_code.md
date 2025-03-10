UNWIND $rows as row
MATCH (usr:User {employeeNumber: row.CVSResourceid})

// Find existing identifier info and relationships
OPTIONAL MATCH (usr)-[has_identifier_info:HAS_ATTRIBUTE]->(identifier_info:AetnaNetworkIdentifierInfo)
OPTIONAL MATCH (identifier_info)-[r_curr:CURRENT]-(aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)

WITH usr, row, has_identifier_info, identifier_info, r_curr, aetna_nw_identifier,
     CASE 
         WHEN ((aetna_nw_identifier IS NULL OR row.AetnaResourceid <> aetna_nw_identifier.networkid) 
               AND row.AetnaResourceid <> 'DNE') 
         THEN true 
         ELSE false 
     END AS codesDiffer
WHERE codesDiffer

// Delete old relationships and remove networkid if they exist
DELETE has_identifier_info, r_curr
REMOVE aetna_nw_identifier.networkid

// Create new Aetna identifier node
MERGE (new_aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier { 
    fuid: substring(row.AetnaResourceid, 1) 
})
SET new_aetna_nw_identifier.networkid = row.AetnaResourceid

// Create new IdentifierInfo node
CREATE (new_identifier_info:AetnaNetworkIdentifierInfo { 
    eventID: toString(row.CVSResourceid) + '' + toString(row.AetnaResourceid) + 
             '-' + toString(datetime()), 
    date: datetime() 
})

// Establish new relationships
MERGE (usr)-[:HAS_ATTRIBUTE]->(new_identifier_info)
MERGE (new_identifier_info)-[r_has_aetna_id:HAS_AETNA_ID]->(new_aetna_nw_identifier)
SET r_has_aetna_id.assigned_date = datetime(),
    r_has_aetna_id.assignedBy = 'GLIDE'

MERGE (new_identifier_info)-[:CURRENT]->(new_aetna_nw_identifier)

// Link to previous identifier info if it exists
FOREACH (_ IN CASE WHEN identifier_info IS NOT NULL THEN [1] ELSE [] END |
    MERGE (new_identifier_info)-[:PREVIOUS]->(identifier_info)
)

// Update User properties
SET usr.aetnaresourceid = CASE 
                              WHEN row.AetnaResourceid <> 'DNE' 
                              THEN row.AetnaResourceid 
                              ELSE usr.aetnaresourceid 
                          END,
    usr.legacyaetnaresourceid = CASE 
                                     WHEN row.LegacyAetnaResourceid <> 'DNE' 
                                     THEN row.LegacyAetnaResourceid 
                                     ELSE usr.legacyaetnaresourceid 
                                 END,
    usr.is_updated = 'Y'

RETURN count(*) AS total
