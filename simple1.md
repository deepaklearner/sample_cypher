v1.4

// Step 1: Find the CEO (user who reports to themselves) and set their level to 1
MATCH (ceo:User)
WHERE ceo.employeeNumber = ceo.managerid
WITH ceo
// Return the CEO with level 1
RETURN ceo.employeeNumber AS employeeNumber, ceo.employeeNumber AS managerid, 1 AS Level

UNION

// Step 2: Find direct reports to the CEO and set their level to 2
MATCH (n:User)-[:REPORTS_TO]->(ceo:User)
WHERE ceo.employeeNumber = n.managerid
RETURN n.employeeNumber AS employeeNumber, ceo.employeeNumber AS managerid, 2 AS Level

UNION

// Step 3: Find direct reports to users at level 2 (i.e., find Level 3 users)
MATCH (n:User)-[:REPORTS_TO]->(m:User)
WHERE m.employeeNumber IN [2000001, 2000002]  // This list includes the CEO and their direct reports
RETURN n.employeeNumber AS employeeNumber, m.employeeNumber AS managerid, 3 AS Level

UNION

// Step 4: Find direct reports to users at level 3 (i.e., find Level 4 users)
MATCH (n:User)-[:REPORTS_TO]->(m:User)
WHERE m.employeeNumber IN [2000001, 2000002, 2000003]  // Expand the list to include users at level 1-3
RETURN n.employeeNumber AS employeeNumber, m.employeeNumber AS managerid, 4 AS Level





In Neo4j, using this cypher “””CALL apoc.periodic.iterate( " MATCH (n:User) WHERE n.managerid IS NOT NULL RETURN n ", " OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User) WHERE n.managerid <> m.employeeNumber DELETE r WITH n MATCH (m:User {employeeNumber: n.managerid}) MERGE (n)-[:REPORTS_TO]->(m) ", {batchSize: 10000, parallel: false} )”””, I am creating some nodes and relationships.


Sample data:
(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’}) 

employeeNumber: ‘2000001’ is ceo. It should have Level value 1.

Sample output:

| employeeNumber | managerid | Level |
|----------------|-----------|-------|
| 2000001        | 2000001   | 1     |
| 2000002        | 2000001   | 2     |
| 2000003        | 2000002   | 3     |
| 2000004        | 2000003   | 4     |

v1.1:

    // Set Level for CEO first
    MATCH (ceo:User {employeeNumber: '2000001'})
    SET ceo.Level = 1

    // Traverse the hierarchy and update Level for others
    MATCH (n:User)-[:REPORTS_TO*]->(ceo)
    WITH n, LENGTH(relationshipPath(n, ceo)) AS level
    SET n.Level = level + 1

    // Optional: Ensure CEO has level 1 and others are numbered accordingly
    RETURN n.employeeNumber, n.managerid, n.Level
    ORDER BY n.Level

v1.2: 

    // Set Level for the CEO
    MATCH (ceo:User {employeeNumber: '2000001'})
    SET ceo.Level = 1

    // Use WITH to pass the ceo to the next part of the query
    WITH ceo

    // Now, traverse the hierarchy and calculate Level for others
    MATCH (n:User)-[:REPORTS_TO*]->(ceo)
    WITH n, LENGTH(relationshipPath(n, ceo)) AS level
    SET n.Level = level + 1

    // Return the updated results
    RETURN n.employeeNumber, n.managerid, n.Level
    ORDER BY n.Level

v1.3

    // Set Level for the CEO
    MATCH (ceo:User {employeeNumber: '2000001'})
    SET ceo.Level = 1

    // Traverse the hierarchy and calculate Level for others
    WITH ceo
    MATCH path = (n:User)-[:REPORTS_TO*]->(ceo)  // Match the path from the user to the CEO
    WITH n, LENGTH(path) AS level  // Calculate the length of the path (number of hops)
    SET n.Level = level + 1  // Set the level, adding 1 to the path length

    // Return the updated results
    RETURN n.employeeNumber, n.managerid, n.Level
    ORDER BY n.Level

Multiple issue. there are total 7 rows in output. Duplicate employeeNumber. also for 2000001 Level is coming as 2 instead of 1



















