v3.1 adding name email

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

// Fetching FirstName, LastName, and Email for each manager level
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(name:Name)
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(email:HomeEmail)

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
       CASE WHEN size(managers) > 0 THEN managers[0] ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid,
       
       // Manager Details
       CASE WHEN size(managers) > 0 THEN name.givenName ELSE NULL END AS L1managerFirstName,
       CASE WHEN size(managers) > 0 THEN name.familyName ELSE NULL END AS L1managerLastName,
       CASE WHEN size(managers) > 0 THEN email.email ELSE NULL END AS L1managerEmail,

       CASE WHEN size(managers) > 1 THEN name.givenName ELSE NULL END AS L2managerFirstName,
       CASE WHEN size(managers) > 1 THEN name.familyName ELSE NULL END AS L2managerLastName,
       CASE WHEN size(managers) > 1 THEN email.email ELSE NULL END AS L2managerEmail,

       CASE WHEN size(managers) > 2 THEN name.givenName ELSE NULL END AS L3managerFirstName,
       CASE WHEN size(managers) > 2 THEN name.familyName ELSE NULL END AS L3managerLastName,
       CASE WHEN size(managers) > 2 THEN email.email ELSE NULL END AS L3managerEmail,

       CASE WHEN size(managers) > 3 THEN name.givenName ELSE NULL END AS L4managerFirstName,
       CASE WHEN size(managers) > 3 THEN name.familyName ELSE NULL END AS L4managerLastName,
       CASE WHEN size(managers) > 3 THEN email.email ELSE NULL END AS L4managerEmail

ORDER BY e.employeeNumber
