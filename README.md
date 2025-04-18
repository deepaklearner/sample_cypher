1.
In below cypher query, where I am reading data from neo4j in batches. 
Here, there is a property globalID in User node. I want to pull only unique User nodes for globalID.
If for a employeeNumber, having multiple globalID, I want to pull only one record.

Also take care if the duplicate globalID one record is present in 1st batch and other in next batches.

MATCH (u:User)
WHERE u.managerid IS NOT NULL AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))
// Traverse the reporting structure (up to 15 levels)
OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)
WITH u, COLLECT(DISTINCT m.employeeNumber) AS manager_ids
RETURN u.employeeNumber AS EmployeeID,
       SIZE(manager_ids) AS ManagerLevel,
       manager_ids AS manager_levels
ORDER BY u.employeeNumber
SKIP {offset} LIMIT {batch_size}
