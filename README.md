1. Write the cypher query
2. Modify this line "SET a.uid = row.AetnaResourceid" to set the value after slicing row.AetnaResourceid value and leaving the 1st alphabet in the begnning.
3. In User node, sometimes it is possible, cid property wont be there. As it is only set when there will be data in mysql db.

if in mysql, cid is null then property cid should be removed else set
4. In Neo4j, if you set a property of a node or relationship to null, it effectively removes that property. 

5. If the properties aetnaresourceid or cvsnetworkid or cid is not present in User node in neo4j,
then it not going beying below line:
"WITH u, row
WHERE u.aetnaresourceid <> row.AetnaResourceid OR u.cvsnetworkid <> row.cvsnetworkid OR u.cid <> row.cid" 

6. If the value of u.aetnaresourceid initially not Null or empty and value row.AetnaResourceid having some other value then that is case for conversion.
   In that case, we need to remove the relationship 
r:HAS_AETNA_ID and delete the existing node aetna_identifier and create a new node aetna_identifier
and create a new relationship r:HAS_AETNA_ID