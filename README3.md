MATCH (e:User)
OPTIONAL MATCH path = (e)-[:REPORTS_TO*]->(m:User)
WITH e, LENGTH(path) AS level, COLLECT(m.employeeNumber) AS managers
WITH e, 
     CASE WHEN e.employeeNumber IN managers THEN 1 ELSE level + 1 END AS finalLevel,  // Level 1 if employee is CEO
     managers
WITH e, finalLevel,
     CASE WHEN SIZE(managers) > 0 THEN managers[0] ELSE e.employeeNumber END AS L1managerid,
     CASE WHEN SIZE(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
     CASE WHEN SIZE(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
     CASE WHEN SIZE(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid
RETURN e.employeeNumber AS employeeNumber,
       e.managerid AS managerid,
       finalLevel AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber
