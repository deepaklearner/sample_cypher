v1.3

MATCH (e:User)
WHERE e.managerid IS NOT NULL
WITH e, [] AS path

// First level of reporting
OPTIONAL MATCH (e)-[:REPORTS_TO]->(m:User)
WITH e, m, path + m AS path

// Second level of reporting
OPTIONAL MATCH (m)-[:REPORTS_TO]->(m2:User)
WITH e, m2, path + m2 AS path

// Third level of reporting
OPTIONAL MATCH (m2)-[:REPORTS_TO]->(m3:User)
WITH e, m3, path + m3 AS path

// Fourth level of reporting
OPTIONAL MATCH (m3)-[:REPORTS_TO]->(m4:User)
WITH e, m4, path + m4 AS path

// Extract manager IDs based on path length
WITH e,
     CASE WHEN size(path) > 0 THEN path[0].employeeNumber ELSE null END AS L1managerid,
     CASE WHEN size(path) > 1 THEN path[1].employeeNumber ELSE null END AS L2managerid,
     CASE WHEN size(path) > 2 THEN path[2].employeeNumber ELSE null END AS L3managerid,
     CASE WHEN size(path) > 3 THEN path[3].employeeNumber ELSE null END AS L4managerid

RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid, 
       CASE 
         WHEN L1managerid IS NOT NULL THEN 1 
         WHEN L2managerid IS NOT NULL THEN 2 
         WHEN L3managerid IS NOT NULL THEN 3 
         WHEN L4managerid IS NOT NULL THEN 4 
         ELSE 0 
       END AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber;




v1.2

MATCH (e:User)
WHERE e.managerid IS NOT NULL
WITH e, [e] AS path
OPTIONAL MATCH (e)-[:REPORTS_TO]->(m:User)
WITH e, m, path + m AS path
OPTIONAL MATCH (m)-[:REPORTS_TO]->(m2:User)
WITH e, m, m2, path + m2 AS path
OPTIONAL MATCH (m2)-[:REPORTS_TO]->(m3:User)
WITH e, m, m2, m3, path + m3 AS path
OPTIONAL MATCH (m3)-[:REPORTS_TO]->(m4:User)
WITH e, m, m2, m3, m4, path + m4 AS path
WITH e,
     CASE WHEN size(path) > 0 THEN path[0].employeeNumber ELSE null END AS L1managerid,
     CASE WHEN size(path) > 1 THEN path[1].employeeNumber ELSE null END AS L2managerid,
     CASE WHEN size(path) > 2 THEN path[2].employeeNumber ELSE null END AS L3managerid,
     CASE WHEN size(path) > 3 THEN path[3].employeeNumber ELSE null END AS L4managerid
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid, 
       CASE 
         WHEN L1managerid IS NOT NULL THEN 1 
         WHEN L2managerid IS NOT NULL THEN 2 
         WHEN L3managerid IS NOT NULL THEN 3 
         WHEN L4managerid IS NOT NULL THEN 4 
         ELSE 0 
       END AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber;





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

Can you help me to write a cypher query to create a report. Sample report mentioned below for below sample data.


Sample data:
(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’}) 

employeeNumber matching with managerid is ceo. It should have Level value 1.
Note: 
1. Dont hardcode ceo logic.
2. Dont use set statement.

Sample report:

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