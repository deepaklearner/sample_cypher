1.1 Please help me to fix this cypher query

"""
UNWIND $rows AS row
MATCH (usr:User {employeeNumber: row.CVSResourceid})-[:HAS_ATTRIBUTE]->(usrAct:UserAccount)
WHERE usrAct.accountType IN ['Primary', 'Secondary']

WHERE NOT (usrAct.targetSystem = 'Ping Directory' AND usrAct.accountType = 'Primary')

DETACH DELETE usrAct

RETURN COUNT(*) AS total
"""

why this cypher failing with error entitiyNotFound and trying to delete a UserAccount node which has accountType = "Privileged"
