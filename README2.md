CALL apoc.periodic.iterate(
  'MATCH (u:User) WHERE u.employeeNumber IS NOT NULL RETURN u',
  '
  OPTIONAL MATCH (u)-[:REPORTS_TO]->(m:User)
  OPTIONAL MATCH (m)-[:REPORTS_TO]->(l1:User)
  OPTIONAL MATCH (l1)-[:REPORTS_TO]->(l2:User)
  OPTIONAL MATCH (l2)-[:REPORTS_TO]->(l3:User)
  OPTIONAL MATCH (l3)-[:REPORTS_TO]->(l4:User)
  
  WITH u, m, l1, l2, l3, l4,
       CASE
           WHEN u.employeeNumber = u.managerid THEN 1
           WHEN m IS NOT NULL THEN 2
           WHEN l1 IS NOT NULL THEN 3
           WHEN l2 IS NOT NULL THEN 4
           WHEN l3 IS NOT NULL THEN 5
           WHEN l4 IS NOT NULL THEN 6
           ELSE 0
       END AS level,

       COALESCE(m.managerid, '') AS L1managerid,
       COALESCE(m.FirstName, '') AS L1managerFirstName,
       COALESCE(m.LastName, '') AS L1managerLastName,

       COALESCE(l1.managerid, '') AS L2managerid,
       COALESCE(l1.FirstName, '') AS L2managerFirstName,
       COALESCE(l1.LastName, '') AS L2managerLastName,

       COALESCE(l2.managerid, '') AS L3managerid,
       COALESCE(l2.FirstName, '') AS L3managerFirstName,
       COALESCE(l2.LastName, '') AS L3managerLastName,

       COALESCE(l3.managerid, '') AS L4managerid,
       COALESCE(l3.FirstName, '') AS L4managerFirstName,
       COALESCE(l3.LastName, '') AS L4managerLastName,

       COALESCE(l4.managerid, '') AS L5managerid,
       COALESCE(l4.FirstName, '') AS L5managerFirstName,
       COALESCE(l4.LastName, '') AS L5managerLastName
  
  RETURN u.employeeNumber, u.managerid, level,
         L1managerid, L1managerFirstName, L1managerLastName,
         L2managerid, L2managerFirstName, L2managerLastName,
         L3managerid, L3managerFirstName, L3managerLastName,
         L4managerid, L4managerFirstName, L4managerLastName,
         L5managerid, L5managerFirstName, L5managerLastName',
  {batchSize: 10000, iterateList: true, parallel: true}
)



CALL apoc.export.csv.query(
  'MATCH (u:User) ...', // Your query here
  'file:///path/to/your/report.csv',
  {}
)
