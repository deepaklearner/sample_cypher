How to optimize this cypher. I have half million User data. Also check if i made any logical mistake.

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

RETURN u.employeeNumber AS employeeid,
managers[0].managerid AS managerid,
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
    WHEN SIZE(managers) = 14 THEN 15
    ELSE 16
END AS Level,

CASE 
    WHEN SIZE(managers) > 0 THEN managers[0].managerid 
    ELSE NULL 
END AS L1managerid,
CASE 
    WHEN SIZE(managers) > 0 THEN managers[0].manager_fname 
    ELSE NULL 
END AS L1managerFirstName,
CASE 
    WHEN SIZE(managers) > 0 THEN managers[0].manager_lname 
    ELSE NULL 
END AS L1managerLastName,
CASE 
    WHEN SIZE(managers) > 0 THEN managers[0].manager_work_email 
    ELSE NULL 
END AS L1managerEmail,

CASE 
    WHEN SIZE(managers) > 1 THEN managers[1].managerid 
    ELSE NULL 
END AS L2managerid,
CASE 
    WHEN SIZE(managers) > 1 THEN managers[1].manager_fname 
    ELSE NULL 
END AS L2managerFirstName,
CASE 
    WHEN SIZE(managers) > 1 THEN managers[1].manager_lname 
    ELSE NULL 
END AS L2managerLastName,
CASE 
    WHEN SIZE(managers) > 1 THEN managers[1].manager_work_email 
    ELSE NULL 
END AS L2managerEmail,

// Continue for L3 to L15 managers in a similar pattern...

ORDER BY u.employeeNumber
SKIP {offset} LIMIT {batch_size};
