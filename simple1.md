v1.1

MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, 1 AS level, [e.managerid] AS managers

// Recursively collect manager hierarchy up to 4 levels
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})
WITH e, m, level, managers
WHERE m IS NOT NULL
WITH e, m, level + 1 AS level, managers + [m.employeeNumber] AS managers

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})
WITH e, m2, level, managers
WHERE m2 IS NOT NULL
WITH e, m2, level + 1 AS level, managers + [m2.employeeNumber] AS managers

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})
WITH e, m3, level, managers
WHERE m3 IS NOT NULL
WITH e, m3, level + 1 AS level, managers + [m3.employeeNumber] AS managers

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})
WITH e, m4, level, managers
WHERE m4 IS NOT NULL
WITH e, m4, level + 1 AS level, managers + [m4.employeeNumber] AS managers

// Output the result
RETURN e.employeeNumber AS employeeNumber, e.managerid AS managerid,
       level AS Level,
       CASE WHEN size(managers) > 0 THEN managers[0] ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid
ORDER BY e.employeeNumber




# Ques

In Neo4j, I am using below cypher to create graph: """
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

Write a very simple cypher, which is easy to debug and easiy to understand for beginners to create a report. employeeNumber matching with managerid is ceo. It should have Level value 1.

Sample report format:
"""
| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 1     | 2000001     |             |             |             |
| 2000002        | 2000001   | 2     | 2000001     |             |             |             |
| 2000003        | 2000002   | 3     | 2000002     | 2000001     |             |             |
| 2000004        | 2000003   | 4     | 2000003     | 2000002     | 2000001     |             |
"""
Sample data:
"""(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’})"""

Note: 
1. Dont hardcode ceo logic.
2. Dont use set statement.
3. Keep the solution very simple.
4. Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.


---

| employeeNumber | managerid | Level |
|----------------|-----------|-------|
| 2000001        | 2000001   | 1     |
| 2000002        | 2000001   | 2     |
| 2000003        | 2000002   | 3     |
| 2000004        | 2000003   | 4     |

Avoid using relationship() function. Dont use "REPORTS_TO*" . Keep the solution very simple and easy to understand.