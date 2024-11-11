MATCH (e:User)
OPTIONAL MATCH path = (e)-[:REPORTS_TO*]->(m:User)
WITH e, path, LENGTH(path) AS level, COLLECT(m.employeeNumber) AS managers
WITH e, 
     CASE WHEN e.employeeNumber IN managers THEN 1 ELSE level + 1 END AS finalLevel,  // Level 1 if employee is CEO
     managers
UNWIND range(0, 3) AS i  // Generate levels 0 to 3 for L1 to L4
WITH e, finalLevel, i, managers,
     CASE WHEN i = 0 AND SIZE(managers) > 0 THEN managers[0] ELSE e.employeeNumber END AS L1managerid,
     CASE WHEN i = 1 AND SIZE(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
     CASE WHEN i = 2 AND SIZE(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
     CASE WHEN i = 3 AND SIZE(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid
RETURN DISTINCT e.employeeNumber AS employeeNumber,
       e.managerid AS managerid,
       finalLevel AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber
