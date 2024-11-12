v3.1 adding name

in this query i want to have in managers list, i want to fetch the FirstName and LastName from Name node which is connected with User Node with (u:User)-[:HAS_ATTRIBUTE]->(:Name). givenName property will be FirstName and familyName property can become LastName


MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, [{employeeNumber: e.managerid}] AS managers

// Collect manager hierarchy up to 4 levels, ensuring no duplicates
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})-[:HAS_ATTRIBUTE]->(n:Name)
WITH e, m, n, 
     CASE WHEN NOT m.employeeNumber IN [manager.employeeNumber | manager IN managers] 
          THEN managers + [{employeeNumber: m.employeeNumber, FirstName: n.givenName, LastName: n.familyName}] 
          ELSE managers END AS managers
WHERE m IS NOT NULL

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})-[:HAS_ATTRIBUTE]->(n2:Name)
WITH e, m2, n2, 
     CASE WHEN NOT m2.employeeNumber IN [manager.employeeNumber | manager IN managers] 
          THEN managers + [{employeeNumber: m2.employeeNumber, FirstName: n2.givenName, LastName: n2.familyName}] 
          ELSE managers END AS managers
WHERE m2 IS NOT NULL

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})-[:HAS_ATTRIBUTE]->(n3:Name)
WITH e, m3, n3, 
     CASE WHEN NOT m3.employeeNumber IN [manager.employeeNumber | manager IN managers] 
          THEN managers + [{employeeNumber: m3.employeeNumber, FirstName: n3.givenName, LastName: n3.familyName}] 
          ELSE managers END AS managers
WHERE m3 IS NOT NULL

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})-[:HAS_ATTRIBUTE]->(n4:Name)
WITH e, m4, n4, 
     CASE WHEN NOT m4.employeeNumber IN [manager.employeeNumber | manager IN managers] 
          THEN managers + [{employeeNumber: m4.employeeNumber, FirstName: n4.givenName, LastName: n4.familyName}] 
          ELSE managers END AS managers
WHERE m4 IS NOT NULL

// Output the result
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid,
       CASE 
           WHEN size(managers) = 1 AND e.managerid = e.employeeNumber THEN 1 
           WHEN size(managers) = 1 AND e.managerid <> e.employeeNumber THEN 2
           WHEN size(managers) = 2 THEN 3
           WHEN size(managers) = 3 THEN 4
           ELSE 0 
       END AS Level,  // Adjust level for CEO
       CASE WHEN size(managers) > 0 THEN managers[0] ELSE NULL END AS L1Manager,
       CASE WHEN size(managers) > 1 THEN managers[1] ELSE NULL END AS L2Manager,
       CASE WHEN size(managers) > 2 THEN managers[2] ELSE NULL END AS L3Manager,
       CASE WHEN size(managers) > 3 THEN managers[3] ELSE NULL END AS L4Manager
ORDER BY e.employeeNumber
