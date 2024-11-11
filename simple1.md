v1.1

MATCH (n:User)
WHERE n.managerid IS NOT NULL
WITH n
  // Build the path for each employee to their manager(s)
  OPTIONAL MATCH path = (n)-[:REPORTS_TO*]->(m:User)
WITH n, path, m
// Calculate level based on path length
WITH n, m, length(path) + 1 AS level, path
// Gather managerids for each level up the chain
WITH n, m, level, collect( CASE WHEN level = 1 THEN m.employeeNumber END ) AS L1managerid,
     collect( CASE WHEN level = 2 THEN m.employeeNumber END ) AS L2managerid,
     collect( CASE WHEN level = 3 THEN m.employeeNumber END ) AS L3managerid,
     collect( CASE WHEN level = 4 THEN m.employeeNumber END ) AS L4managerid
RETURN n.employeeNumber AS employeeNumber, 
       n.managerid AS managerid,
       level AS Level,
       head(L1managerid) AS L1managerid,
       head(L2managerid) AS L2managerid,
       head(L3managerid) AS L3managerid,
       head(L4managerid) AS L4managerid
ORDER BY n.employeeNumber;


# Ques

In Neo4j, I am using below cypher """
    CALL apoc.periodic.iterate(
      "
        MATCH (n:User)
        WHERE n.managerid IS NOT NULL
        RETURN n
      ",
      "
        OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User)
        WHERE n.managerid <> m.employeeNumber
        DELETE r
        WITH n
        MATCH (m:User {employeeNumber: n.managerid})
        MERGE (n)-[:REPORTS_TO]->(m)
      ",
      {batchSize: 10000, parallel: false}
    )"""

I want to create a report for below data. employeeNumber matching with managerid is ceo. It should have Level value 1.

Sample data:
"""(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’})"""

Note: 
1. Dont hardcode ceo logic.
2. Dont use set statement.
3. Keep the solution very simple.
4. Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.

Sample report:
"""
| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 1     | 2000001     |             |             |             |
| 2000002        | 2000001   | 2     | 2000001     |             |             |             |
| 2000003        | 2000002   | 3     | 2000002     | 2000001     |             |             |
| 2000004        | 2000003   | 4     | 2000003     | 2000002     | 2000001     |             |
"""


---

| employeeNumber | managerid | Level |
|----------------|-----------|-------|
| 2000001        | 2000001   | 1     |
| 2000002        | 2000001   | 2     |
| 2000003        | 2000002   | 3     |
| 2000004        | 2000003   | 4     |

Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.