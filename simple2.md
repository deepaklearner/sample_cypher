v3.1 adding name

MATCH (e:User)
WHERE e.managerid IS NOT NULL

WITH e, [{employeeNumber: e.managerid, givenName: e.givenName, familyName: e.familyName}] AS managers

// Collect manager hierarchy up to 4 levels, ensuring no duplicates
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(n:Name)
WITH e, m, n, 
     CASE 
         WHEN NOT m.employeeNumber IN [manager.employeeNumber | manager IN managers] 
         THEN managers + [{employeeNumber: m.employeeNumber, givenName: n.givenName, familyName: n.familyName}] 
         ELSE managers 
     END AS managers
WHERE m IS NOT NULL

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})
OPTIONAL MATCH (m2)-[:HAS_ATTRIBUTE]->(n2:Name)
WITH e, m2, n2, 
     CASE 
         WHEN NOT m2.employeeNumber IN [manager.employeeNumber | manager IN managers] 
         THEN managers + [{employeeNumber: m2.employeeNumber, givenName: n2.givenName, familyName: n2.familyName}] 
         ELSE managers 
     END AS managers
WHERE m2 IS NOT NULL

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})
OPTIONAL MATCH (m3)-[:HAS_ATTRIBUTE]->(n3:Name)
WITH e, m3, n3, 
     CASE 
         WHEN NOT m3.employeeNumber IN [manager.employeeNumber | manager IN managers] 
         THEN managers + [{employeeNumber: m3.employeeNumber, givenName: n3.givenName, familyName: n3.familyName}] 
         ELSE managers 
     END AS managers
WHERE m3 IS NOT NULL

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})
OPTIONAL MATCH (m4)-[:HAS_ATTRIBUTE]->(n4:Name)
WITH e, m4, n4, 
     CASE 
         WHEN NOT m4.employeeNumber IN [manager.employeeNumber | manager IN managers] 
         THEN managers + [{employeeNumber: m4.employeeNumber, givenName: n4.givenName, familyName: n4.familyName}] 
         ELSE managers 
     END AS managers
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
       CASE WHEN size(managers) > 0 THEN managers[0].employeeNumber ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 0 THEN managers[0].givenName ELSE NULL END AS L1FirstName,
       CASE WHEN size(managers) > 0 THEN managers[0].familyName ELSE NULL END AS L1LastName,
       CASE WHEN size(managers) > 1 THEN managers[1].employeeNumber ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 1 THEN managers[1].givenName ELSE NULL END AS L2FirstName,
       CASE WHEN size(managers) > 1 THEN managers[1].familyName ELSE NULL END AS L2LastName,
       CASE WHEN size(managers) > 2 THEN managers[2].employeeNumber ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 2 THEN managers[2].givenName ELSE NULL END AS L3FirstName,
       CASE WHEN size(managers) > 2 THEN managers[2].familyName ELSE NULL END AS L3LastName,
       CASE WHEN size(managers) > 3 THEN managers[3].employeeNumber ELSE NULL END AS L4managerid,
       CASE WHEN size(managers) > 3 THEN managers[3].givenName ELSE NULL END AS L4FirstName,
       CASE WHEN size(managers) > 3 THEN managers[3].familyName ELSE NULL END AS L4LastName
ORDER BY e.employeeNumber

