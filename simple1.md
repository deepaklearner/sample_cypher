v1.2 with loop

MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, [e.managerid] AS managers, 1 AS level  // Start with the first manager

// Collect manager hierarchy up to 15 levels, ensuring no duplicates
WITH e, managers, level
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})
WHERE m IS NOT NULL
WITH e, managers + [m.employeeNumber] AS managers, level + 1 AS level

WITH e, managers, level
OPTIONAL MATCH (m2:User {employeeNumber: head(managers)})
WHERE m2 IS NOT NULL
WITH e, CASE WHEN NOT m2.employeeNumber IN managers THEN managers + [m2.employeeNumber] ELSE managers END AS managers, level + 1 AS level

WITH e, managers, level
OPTIONAL MATCH (m3:User {employeeNumber: head(tail(managers))})
WHERE m3 IS NOT NULL
WITH e, CASE WHEN NOT m3.employeeNumber IN managers THEN managers + [m3.employeeNumber] ELSE managers END AS managers, level + 1 AS level

WITH e, managers, level
OPTIONAL MATCH (m4:User {employeeNumber: head(tail(tail(managers)))})
WHERE m4 IS NOT NULL
WITH e, CASE WHEN NOT m4.employeeNumber IN managers THEN managers + [m4.employeeNumber] ELSE managers END AS managers, level + 1 AS level

WITH e, managers, level
OPTIONAL MATCH (m5:User {employeeNumber: head(tail(tail(tail(managers))))})
WHERE m5 IS NOT NULL
WITH e, CASE WHEN NOT m5.employeeNumber IN managers THEN managers + [m5.employeeNumber] ELSE managers END AS managers, level + 1 AS level

// Repeat this pattern until up to 15 levels or as required

// Output the result
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid,
       CASE 
           WHEN size(managers) = 1 AND e.managerid = e.employeeNumber THEN 1 
           WHEN size(managers) = 1 AND e.managerid <> e.employeeNumber THEN 2
           WHEN size(managers) = 2 THEN 3
           WHEN size(managers) = 3 THEN 4
           WHEN size(managers) = 4 THEN 5
           WHEN size(managers) = 5 THEN 6
           // Add more conditions as necessary for higher levels
           ELSE 0 
       END AS Level,
       CASE WHEN size(managers) > 0 THEN managers[0] ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid,
       CASE WHEN size(managers) > 4 THEN managers[4] ELSE NULL END AS L5managerid
       // Add more manager levels up to L15managerid as necessary
ORDER BY e.employeeNumber





v1.1

MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, [e.managerid] AS managers

// Collect manager hierarchy up to 4 levels, ensuring no duplicates
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})
WITH e, m, 
     CASE WHEN NOT m.employeeNumber IN managers THEN managers + [m.employeeNumber] ELSE managers END AS managers
WHERE m IS NOT NULL

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})
WITH e, m2,
     CASE WHEN NOT m2.employeeNumber IN managers THEN managers + [m2.employeeNumber] ELSE managers END AS managers
WHERE m2 IS NOT NULL

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})
WITH e, m3,  
     CASE WHEN NOT m3.employeeNumber IN managers THEN managers + [m3.employeeNumber] ELSE managers END AS managers
WHERE m3 IS NOT NULL

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})
WITH e, m4,
     CASE WHEN NOT m4.employeeNumber IN managers THEN managers + [m4.employeeNumber] ELSE managers END AS managers
WHERE m4 IS NOT NULL

// Output the result
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid,
       CASE 
           WHEN size(managers) =1 and e.managerid = e.employeeNumber THEN 1 
           WHEN size(managers) =1 and e.managerid <> e.employeeNumber THEN 2
           WHEN size(managers) =2  THEN 3
           WHEN size(managers) =3  THEN 4
           ELSE 0 
       END AS Level,  // Adjust level for CEO
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

| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 5     | 2000001     | 2000001 |      2000001       |   2000001          |
| 2000002        | 2000001   | 5     | 2000001     |   2000001          |   2000001          |  2000001           |
| 2000003        | 2000002   | 5     | 2000002     | 2000001     |    2000001         |  2000001           |
| 2000004        | 2000003   | 5     | 2000003     | 2000002     | 2000001     |   2000001          |

| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 1     | 2000001     |  null       |  null       | null        |
| 2000002        | 2000001   | 5     | 2000001     |  null       |  null       |    null     |
| 2000003        | 2000002   | 5     | 2000002     | 2000001     |             |   null      |
| 2000004        | 2000003   | 5     | 2000003     | 2000002     | 2000001     |   null      |

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