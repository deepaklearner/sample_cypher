v3.1 adding name

i want to have the FirstName and LastName from Name node as well in the RETURN which is connected with User Node with (u:User)-[:HAS_ATTRIBUTE]->(:Name). givenName property will be FirstName and familyName property can become LastName.

NOTE: 
1. Use apoc.coll.contains function.
2. Dont use pipe operator or list comprehension.
3. Add first name and last name in the managers list only.
4. Also, i want to have them in a new column in return as L1managerFirstName, L1managerLastName


"""
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
ORDER BY e.employeeNumber"""