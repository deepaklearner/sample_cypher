v1.2

// Step 1: Find the CEO (Level 1) and set their Level and L1managerid
MATCH (n:User {employeeNumber: '2000001'})
SET n.Level = 1, n.L1managerid = n.employeeNumber

// Step 2: Assign Levels and Manager IDs for other users (Level 2 and onwards)
MATCH (n:User)-[:REPORTS_TO]->(m:User)
WITH n, m
ORDER BY n.employeeNumber
SET n.Level = m.Level + 1, 
    n.L1managerid = m.L1managerid, 
    n.L2managerid = m.employeeNumber

// Step 3: Repeat for deeper levels (L3, L4, etc.)
// You can adjust the following pattern if you need to go deeper than 2 levels
MATCH (n:User)-[:REPORTS_TO]->(m:User)-[:REPORTS_TO]->(l:User)
WITH n, m, l
ORDER BY n.employeeNumber
SET n.L2managerid = m.employeeNumber, 
    n.L3managerid = l.employeeNumber

MATCH (n:User)-[:REPORTS_TO]->(m:User)-[:REPORTS_TO]->(l:User)-[:REPORTS_TO]->(k:User)
WITH n, m, l, k
ORDER BY n.employeeNumber
SET n.L3managerid = l.employeeNumber,
    n.L4managerid = k.employeeNumber


v1.1

MATCH (n:User)
WHERE n.managerid IS NOT NULL
WITH n, 1 AS level
CALL {
  WITH n, level
  MATCH (m:User {employeeNumber: n.managerid})
  RETURN m, level + 1 AS newLevel
}
RETURN n.employeeNumber AS employeeNumber, n.managerid AS managerid, newLevel AS Level
ORDER BY newLevel


# Ques

In Neo4j, using this cypher “””CALL apoc.periodic.iterate( " MATCH (n:User) WHERE n.managerid IS NOT NULL RETURN n ", " OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User) WHERE n.managerid <> m.employeeNumber DELETE r WITH n MATCH (m:User {employeeNumber: n.managerid}) MERGE (n)-[:REPORTS_TO]->(m) ", {batchSize: 10000, parallel: false} )”””, I am creating some nodes and relationships.


Sample data:
(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’}) 

employeeNumber matching with managerid is ceo. It should have Level value 1.

Sample output:

| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 1     | 2000001     |             |             |             |
| 2000002        | 2000001   | 2     | 2000001     |             |             |             |
| 2000003        | 2000002   | 3     | 2000002     | 2000001     |             |             |
| 2000004        | 2000003   | 4     | 2000003     | 2000002     | 2000001     |             |

Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.


---

| employeeNumber | managerid | Level |
|----------------|-----------|-------|
| 2000001        | 2000001   | 1     |
| 2000002        | 2000001   | 2     |
| 2000003        | 2000002   | 3     |
| 2000004        | 2000003   | 4     |

Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.