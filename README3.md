MATCH (e:User)
OPTIONAL MATCH path = (e)-[:REPORTS_TO*]->(m:User)
WITH e, path, LENGTH(path) AS level, COLLECT(m.employeeNumber) AS managers
WITH e, level, managers,
     CASE WHEN e.employeeNumber IN managers THEN 1 ELSE level + 1 END AS finalLevel,  // Set Level to 1 if employee is the CEO
     CASE WHEN SIZE(managers) > 0 THEN managers[0] ELSE e.employeeNumber END AS L1managerid,
     CASE WHEN SIZE(managers) > 1 THEN managers[1] ELSE null END AS L2managerid,
     CASE WHEN SIZE(managers) > 2 THEN managers[2] ELSE null END AS L3managerid,
     CASE WHEN SIZE(managers) > 3 THEN managers[3] ELSE null END AS L4managerid
RETURN e.employeeNumber AS employeeNumber,
       e.managerid AS managerid,
       finalLevel AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber
