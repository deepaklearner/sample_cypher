query aetna_identifier =  '''
UNWIND $rows AS row  
MATCH (usr:User {employeeNumber: row.CVSResourceid})  
WITH usr, row  
OPTIONAL MATCH (usr)-[has_identifier_info:HAS_ATTRIBUTE]->(identifier_info:IdentifierInfo)  
OPTIONAL MATCH (identifier_info)-[r_curr:CURRENT]->(aetna_identifier:AetnaNetworkIdentifier:NetworkIdentifier)  
WITH row, usr, has_identifier_info, identifier_info, r_curr, aetna_identifier,  
     CASE  
         WHEN ((row.AetnaResourceid <> aetna_identifier.networkid OR aetna_identifier IS NULL)  
               AND row.AetnaResourceid <> 'ONE')  
         THEN true  
         ELSE false  
     END AS codesDiffer  
WHERE codesDiffer  

// Delete existing relationships if they exist  
FOREACH (_ IN CASE WHEN has_identifier_info IS NOT NULL THEN [1] ELSE [] END | DELETE has_identifier_info)  
FOREACH (_ IN CASE WHEN r_curr IS NOT NULL THEN [1] ELSE [] END | DELETE r_curr)  

// Create new Aetna identifier node  
MERGE (new_aetna_identifier:AetnaNetworkIdentifier:NetworkIdentifier {networkid: row.AetnaResourceid})  
SET new_aetna_identifier.uid = substring(row.AetnaResourceid, 1)  

// Create new IdentifierInfo node  
MERGE (new_identifier_info:IdentifierInfo {eventID: row.CVSResourceid + '.' + datetime()})  
SET new_identifier_info.date = row.date_current  

// Create relationships  
MERGE (usr)-[:HAS_ATTRIBUTE]->(new_identifier_info)  
MERGE (new_identifier_info)-[r_has_aetna_id:HAS_AETNA_ID]->(new_aetna_identifier)  
SET r_has_aetna_id.assigned_date = localdatetime(),  
    r_has_aetna_id.assignedBy = 'ServiceNow'  

MERGE (new_identifier_info)-[:CURRENT]->(new_aetna_identifier)  

// Link previous identifier if it exists  
WITH row, usr, new_identifier_info, identifier_info  
WHERE identifier_info IS NOT NULL  
MERGE (new_identifier_info)-[:PREVIOUS]->(identifier_info)  

// Update User node properties  
SET usr.aetnaresourceid = CASE  
                              WHEN row.AetnaResourceid <> 'ONE' THEN row.AetnaResourceid  
                              ELSE usr.aetnaresourceid  
                          END,  
    usr.is_updated = 'Y'  

'''
