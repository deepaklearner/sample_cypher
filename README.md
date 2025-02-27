Problem: Help me to write a cypher query.
1. I have following nodes in Neo4j: 
a. User node with properties employeeNumber, aetnaresourceid, cvsnetworkid, cid etc.
b. AetnaNetworkIdentifier node with properties networkid and uid

2. Following relationships exist between nodes:
a. (u:User)-[:HAS_AETNA_ID]->(a:AetnaNetworkIdentifier:NetworkIdentifier)
HAS_AETNA_ID property is assigned_date with current date time stamp


