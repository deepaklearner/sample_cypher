MATCH (ceo:User {employeeNumber: '2000001'})
CALL {
    WITH ceo
    MATCH (n:User)-[:REPORTS_TO*0..]->(m:User)
    WHERE n <> m  // Exclude self-references
    RETURN n, m, length(relationships((n)-[:REPORTS_TO*]->(m))) AS level
}
WITH n, m, level,
     COLLECT(CASE WHEN level = 1 THEN m.employeeNumber ELSE NULL END) AS L1,
     COLLECT(CASE WHEN level = 2 THEN m.employeeNumber ELSE NULL END) AS L2,
     COLLECT(CASE WHEN level = 3 THEN m.employeeNumber ELSE NULL END) AS L3,
     COLLECT(CASE WHEN level = 4 THEN m.employeeNumber ELSE NULL END) AS L4
RETURN n.employeeNumber AS employeeNumber, 
       n.managerid AS managerid, 
       level AS Level,
       HEAD(L1) AS L1managerid, 
       HEAD(L2) AS L2managerid, 
       HEAD(L3) AS L3managerid, 
       HEAD(L4) AS L4managerid
ORDER BY employeeNumber
