v1.1

MATCH (n:User)
WHERE n.managerid IS NOT NULL
WITH n
// Step 1: Get the direct manager of the employee
OPTIONAL MATCH (n)-[:REPORTS_TO]->(m1:User)
WITH n, m1
// Step 2: Get the second-level manager (manager of the manager)
OPTIONAL MATCH (m1)-[:REPORTS_TO]->(m2:User)
WITH n, m1, m2
// Step 3: Get the third-level manager (manager of the second-level manager)
OPTIONAL MATCH (m2)-[:REPORTS_TO]->(m3:User)
WITH n, m1, m2, m3
// Step 4: Get the fourth-level manager (manager of the third-level manager)
OPTIONAL MATCH (m3)-[:REPORTS_TO]->(m4:User)
WITH n, m1, m2, m3, m4
RETURN 
  n.employeeNumber AS employeeNumber,
  n.managerid AS managerid,
  CASE WHEN m1 IS NULL THEN 1 ELSE 2 END AS Level, 
  m1.employeeNumber AS L1managerid,
  m2.employeeNumber AS L2managerid,
  m3.employeeNumber AS L3managerid,
  m4.employeeNumber AS L4managerid
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