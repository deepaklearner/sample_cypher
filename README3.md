MATCH (e:User)
WITH e
ORDER BY e.employeeNumber
WITH e, apoc.path.subgraphNodes(e, {relationshipFilter: "REPORTS_TO>"}) AS path
WITH e, path, size(path) AS level
UNWIND range(0, level-1) AS i
WITH e, path, level, i, 
     CASE WHEN i = 0 THEN e.employeeNumber ELSE (path[i]).employeeNumber END AS L1managerid,
     CASE WHEN i = 1 THEN (path[i]).employeeNumber ELSE null END AS L2managerid,
     CASE WHEN i = 2 THEN (path[i]).employeeNumber ELSE null END AS L3managerid,
     CASE WHEN i = 3 THEN (path[i]).employeeNumber ELSE null END AS L4managerid
RETURN e.employeeNumber AS employeeNumber,
       e.managerid AS managerid,
       level AS Level,
       L1managerid, L2managerid, L3managerid, L4managerid
ORDER BY e.employeeNumber
