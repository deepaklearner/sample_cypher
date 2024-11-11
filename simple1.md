v1.1

// Find the CEO (the user who doesn't report to anyone)
MATCH (ceo:User)
WHERE NOT (ceo)<-[:REPORTS_TO]-()
WITH ceo

// Traverse downwards from the CEO to find all employees and their reporting structure
OPTIONAL MATCH path = (ceo)<-[:REPORTS_TO*]-(n:User)
WITH n, path

// Calculate the level of each employee based on the length of the path (CEO is level 1)
WITH n, length(path) + 1 AS level, path

// Collect manager IDs for each level of the hierarchy
WITH n, level, 
     collect( CASE WHEN level = 1 THEN ceo.employeeNumber END ) AS L1managerid,
     collect( CASE WHEN level = 2 THEN head(nodes(path)).employeeNumber END ) AS L2managerid,
     collect( CASE WHEN level = 3 THEN head(nodes(tail(path))).employeeNumber END ) AS L3managerid,
     collect( CASE WHEN level = 4 THEN head(nodes(tail(tail(path)))).employeeNumber END ) AS L4managerid

// Return the employee information, their manager IDs, and the level
RETURN 
    n.employeeNumber AS employeeNumber, 
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