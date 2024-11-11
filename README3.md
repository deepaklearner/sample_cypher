MATCH (e:User)
OPTIONAL MATCH path = (e)-[:REPORTS_TO*]->(m:User)
WITH e, path, LENGTH(path) AS level, COLLECT(m.employeeNumber) AS managers
WITH e, level, managers
ORDER BY level DESC
WITH e, level, 
     CASE WHEN SIZE(managers) > 0 THEN managers[0] ELSE e.employeeNumber END AS L1managerid,
     CASE WHEN SIZE(managers) > 1 THEN managers[1] ELSE null END AS L2managerid,
     CASE WHEN SIZE(managers) > 2 THEN managers[2] ELSE null END AS L3managerid,
     CASE WHEN SIZE(managers) > 3 THEN managers[3] ELSE null END AS L4managerid
RETURN e.employeeNumber AS employeeNumber,
       e.managerid AS managerid,
       level + 1 AS Level,  // Adding 1 to Level to make it human-readable (1-based index)
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber
