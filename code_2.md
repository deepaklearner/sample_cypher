query_cvs_identifier = """
UNWIND $rows AS row
MATCH (usr:User {employeeNumber: row.CVSResourceid})  
WITH usr, row  
WHERE (COALESCE(usr.cvsnetworkid, 'DNE') <> row.cvsnetworkid AND row.cvsnetworkid <> 'DNE')  
   OR (COALESCE(usr.cid, 'DNE') <> row.cvsnetworkid AND row.cid <> 'DNE')  

// Create or merge the new CVS identifier node  
WITH usr, row  
MERGE (cvs_identifier:CVSNetworkIdentifier:NetworkIdentifier {networkid: row.cvsnetworkid})  
SET cvs_identifier.uid = substring(row.cvsnetworkid, 1)  

// Create the relationship between the User and the new CVS identifier node  
MERGE (usr)-[r_has_cvsnetwork_id:HAS_CVSNETWORK_ID]->(cvs_identifier)  
SET r_has_cvsnetwork_id.assigned_date = localdatetime(),  
    r_has_cvsnetwork_id.assignedBy = 'ServiceNow'  

// Update the property in User node  
SET usr.cvsnetworkid = CASE WHEN row.cvsnetworkid <> 'DNE' THEN row.cvsnetworkid ELSE usr.cvsnetworkid END,  
    usr.cid = CASE WHEN row.cid <> 'DNE' THEN row.cid ELSE usr.cid END,  
    usr.is_updated = 'Y'  

RETURN count(*) AS total  
"""
