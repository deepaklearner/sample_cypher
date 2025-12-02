1.1 Please help me to fix this cypher query

"""
UNWIND $rows AS row
MATCH (usr:User {employeeNumber: row.CVSResourceid})-[:HAS_ATTRIBUTE]->(UsrAct:UserAccount)
OPTIONAL MATCH (additionalUsrAct:UserAccount {targetSystem: "Ping Directory"})-[r_has_mapping:HAS_ACCOUNT_MAPPING]->(UsrAct)
FOREACH (_ IN CASE WHEN r_has_mapping IS NOT NULL THEN [1] ELSE [] END |
    DELETE r_has_mapping
)
WITH usr, UsrAct
FOREACH (_ IN CASE WHEN UsrAct IS NOT NULL AND NOT (UsrAct.targetSystem = 'Ping Directory' AND UsrAct.accountType = 'Primary') THEN [1] ELSE []END |
    DETACH DELETE UsrAct
)

RETURN count(*) AS total"""

Error: """EntityNotFound. A node with id <> has been deleted in thhis transaction"""
