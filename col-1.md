MATCH (u:User) 
WHERE u.managerid IS NOT NULL 
  AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))

// Traverse the reporting structure (up to 15 levels)
OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(n:Name)
OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(w:WorkEmail)

WITH u, COLLECT(DISTINCT {
    managerid: m.employeeNumber,
    manager_fname: n.givenName,
    manager_lname: n.familyName,
    manager_work_email: w.email
}) AS managers

UNWIND range(0, 14) AS level
WITH u, managers, level
WHERE level < SIZE(managers)

// Dynamically get the manager information based on the level
WITH u,
     CASE WHEN level < SIZE(managers) THEN managers[level].managerid ELSE NULL END AS managerid,
     CASE WHEN level < SIZE(managers) THEN managers[level].manager_fname ELSE NULL END AS manager_fname,
     CASE WHEN level < SIZE(managers) THEN managers[level].manager_lname ELSE NULL END AS manager_lname,
     CASE WHEN level < SIZE(managers) THEN managers[level].manager_work_email ELSE NULL END AS manager_work_email,
     level

RETURN u.employeeNumber AS employeeid,
       CASE 
           WHEN SIZE(managers) = 1 AND u.employeeNumber = managers[0].managerid THEN 1
           WHEN SIZE(managers) = 1 AND u.employeeNumber <> managers[0].managerid THEN 2
           WHEN SIZE(managers) = 2 THEN 3
           WHEN SIZE(managers) = 3 THEN 4
           WHEN SIZE(managers) = 4 THEN 5
           WHEN SIZE(managers) = 5 THEN 6
           WHEN SIZE(managers) = 6 THEN 7
           WHEN SIZE(managers) = 7 THEN 8
           WHEN SIZE(managers) = 8 THEN 9
           WHEN SIZE(managers) = 9 THEN 10
           WHEN SIZE(managers) = 10 THEN 11
           WHEN SIZE(managers) = 11 THEN 12
           WHEN SIZE(managers) = 12 THEN 13
           WHEN SIZE(managers) = 13 THEN 14
           ELSE 15
       END AS Level,
       managerid, manager_fname, manager_lname, manager_work_email,
       CASE WHEN level = 0 THEN managerid ELSE NULL END AS L1managerid,
       CASE WHEN level = 0 THEN manager_fname ELSE NULL END AS L1managerFirstName,
       CASE WHEN level = 0 THEN manager_lname ELSE NULL END AS L1managerLastName,
       CASE WHEN level = 0 THEN manager_work_email ELSE NULL END AS L1managerEmail,
       CASE WHEN level = 1 THEN managerid ELSE NULL END AS L2managerid,
       CASE WHEN level = 1 THEN manager_fname ELSE NULL END AS L2managerFirstName,
       CASE WHEN level = 1 THEN manager_lname ELSE NULL END AS L2managerLastName,
       CASE WHEN level = 1 THEN manager_work_email ELSE NULL END AS L2managerEmail,
       // Add further levels as needed

ORDER BY u.employeeNumber
SKIP {offset} LIMIT {batch_size};
