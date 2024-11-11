v1.2 with loop

MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, [e.managerid] AS managers

// Loop to gather up to 4 levels of managers
UNWIND range(1, 4) AS levelIndex
OPTIONAL MATCH (m:User {employeeNumber: head(managers)})
WITH e, m, managers + [m.employeeNumber] AS updatedManagers
WHERE m IS NOT NULL

// Repeat process for subsequent levels of managers
WITH e, updatedManagers
UNWIND range(1, 3) AS levelIndex2
OPTIONAL MATCH (m2:User {employeeNumber: head(updatedManagers)})
WITH e, m2, updatedManagers + [m2.employeeNumber] AS deeperManagers
WHERE m2 IS NOT NULL

// Repeat for 3rd and 4th levels of managers
WITH e, deeperManagers
UNWIND range(1, 2) AS levelIndex3
OPTIONAL MATCH (m3:User {employeeNumber: head(deeperManagers)})
WITH e, m3, deeperManagers + [m3.employeeNumber] AS bottomUpManagers
WHERE m3 IS NOT NULL

WITH e, bottomUpManagers

// Output the result
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid,
       CASE 
           WHEN size(bottomUpManagers) = 1 AND e.managerid = e.employeeNumber THEN 1 
           WHEN size(bottomUpManagers) = 1 AND e.managerid <> e.employeeNumber THEN 2
           WHEN size(bottomUpManagers) = 2 THEN 3
           WHEN size(bottomUpManagers) = 3 THEN 4
           ELSE 0 
       END AS Level,  // Adjust level for CEO
       CASE WHEN size(bottomUpManagers) > 0 THEN bottomUpManagers[0] ELSE NULL END AS L1managerid,
       CASE WHEN size(bottomUpManagers) > 1 THEN bottomUpManagers[1] ELSE NULL END AS L2managerid,
       CASE WHEN size(bottomUpManagers) > 2 THEN bottomUpManagers[2] ELSE NULL END AS L3managerid,
       CASE WHEN size(bottomUpManagers) > 3 THEN bottomUpManagers[3] ELSE NULL END AS L4managerid
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