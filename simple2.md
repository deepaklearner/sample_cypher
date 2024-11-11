v3.1 adding name

MATCH (e:User)
WHERE e.managerid IS NOT NULL

// Initialize the managers list with the first manager
WITH e, [[e.managerid, e.givenName, e.familyName]] AS managers

// Collect manager hierarchy up to 4 levels, ensuring no duplicates
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(n:Name)
WITH e, m, n, managers, 
     CASE 
         WHEN NOT m.employeeNumber IN [manager[0] FROM manager IN managers]  // Check if the employeeNumber already exists in managers list
         THEN managers + [[m.employeeNumber, n.givenName, n.familyName]] 
         ELSE managers 
     END AS managers
WHERE m IS NOT NULL

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})
OPTIONAL MATCH (m2)-[:HAS_ATTRIBUTE]->(n2:Name)
WITH e, m2, n2, managers, 
     CASE 
         WHEN NOT m2.employeeNumber IN [manager[0] FROM manager IN managers] 
         THEN managers + [[m2.employeeNumber, n2.givenName, n2.familyName]] 
         ELSE managers 
     END AS managers
WHERE m2 IS NOT NULL

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})
OPTIONAL MATCH (m3)-[:HAS_ATTRIBUTE]->(n3:Name)
WITH e, m3, n3, managers, 
     CASE 
         WHEN NOT m3.employeeNumber IN [manager[0] FROM manager IN managers] 
         THEN managers + [[m3.employeeNumber, n3.givenName, n3.familyName]] 
         ELSE managers 
     END AS managers
WHERE m3 IS NOT NULL

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})
OPTIONAL MATCH (m4)-[:HAS_ATTRIBUTE]->(n4:Name)
WITH e, m4, n4, managers, 
     CASE 
         WHEN NOT m4.employeeNumber IN [manager[0] FROM manager IN managers] 
         THEN managers + [[m4.employeeNumber, n4.givenName, n4.familyName]] 
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
       CASE WHEN size(managers) > 0 THEN managers[0][0] ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 0 THEN managers[0][1] ELSE NULL END AS L1FirstName,
       CASE WHEN size(managers) > 0 THEN managers[0][2] ELSE NULL END AS L1LastName,
       CASE WHEN size(managers) > 1 THEN managers[1][0] ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 1 THEN managers[1][1] ELSE NULL END AS L2FirstName,
       CASE WHEN size(managers) > 1 THEN managers[1][2] ELSE NULL END AS L2LastName,
       CASE WHEN size(managers) > 2 THEN managers[2][0] ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 2 THEN managers[2][1] ELSE NULL END AS L3FirstName,
       CASE WHEN size(managers) > 2 THEN managers[2][2] ELSE NULL END AS L3LastName,
       CASE WHEN size(managers) > 3 THEN managers[3][0] ELSE NULL END AS L4managerid,
       CASE WHEN size(managers) > 3 THEN managers[3][1] ELSE NULL END AS L4FirstName,
       CASE WHEN size(managers) > 3 THEN managers[3][2] ELSE NULL END AS L4LastName
ORDER BY e.employeeNumber



