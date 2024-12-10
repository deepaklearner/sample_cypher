UNWIND $rows AS row
MATCH (usr:User {employeeNumber: row.CVSResourceid})

WITH row, usr
OPTIONAL MATCH (usr) - []-(:UserTypeInfo) - [:CURRENT] -(user_type:UserType)

WITH usr, row, user_type
WHERE user_type.userType = 'Contractor' AND row.userType = 'Employee'

WITH COLLECT(usr) AS usr_array, row
MATCH (aetna_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_identifier) - [] - ()

WITH usr_array, aetna_identifier
ORDER BY aetna_identifier.networkid ASC

WITH usr_array, COLLECT(aetna_identifier) AS aetna_array
UNWIND apoc.coll.zip(usr_array, aetna_array) AS row

WITH row[0] AS usr, row[1] AS aetna_identifier
OPTIONAL MATCH (usr) -[r]-(aid:AetnaNetworkIdentifier:NetworkIdentifier)
FOREACH (x IN CASE WHEN LEFT(tostring(aid.networkid), 1) = 'N' THEN [1] END |
    MERGE (usr) - [:HAS_AETNA_ID {assigned_date: localdatetime()}] - (aetna_identifier)
    SET aetna_identifier.networkid = 'A' + aetna_identifier.uid
    REMOVE aid.networkid
    DELETE r
)
FOREACH (y IN CASE WHEN LEFT(tostring(usr.cvsnetworkid), 1) = 'N' THEN [1] END |
    SET usr.cvsnetworkid = aetna_identifier.networkid
)
RETURN COUNT(*) AS total
