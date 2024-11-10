CALL apoc.periodic.iterate(
  'MATCH (u:User) WHERE u.employeeNumber IS NOT NULL RETURN u',
  '
  // Matching up to 4 levels of reporting structure.
  OPTIONAL MATCH (u)-[:REPORTS_TO]->(m:User)
  OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(mName:Name)
  OPTIONAL MATCH (m)-[:HAS_ATTRIBUTE]->(mEmail:WorkEmail)
  
  OPTIONAL MATCH (m)-[:REPORTS_TO]->(l1:User)
  OPTIONAL MATCH (l1)-[:HAS_ATTRIBUTE]->(l1Name:Name)
  OPTIONAL MATCH (l1)-[:HAS_ATTRIBUTE]->(l1Email:WorkEmail)
  
  OPTIONAL MATCH (l1)-[:REPORTS_TO]->(l2:User)
  OPTIONAL MATCH (l2)-[:HAS_ATTRIBUTE]->(l2Name:Name)
  OPTIONAL MATCH (l2)-[:HAS_ATTRIBUTE]->(l2Email:WorkEmail)
  
  OPTIONAL MATCH (l2)-[:REPORTS_TO]->(l3:User)
  OPTIONAL MATCH (l3)-[:HAS_ATTRIBUTE]->(l3Name:Name)
  OPTIONAL MATCH (l3)-[:HAS_ATTRIBUTE]->(l3Email:WorkEmail)
  
  OPTIONAL MATCH (l3)-[:REPORTS_TO]->(l4:User)
  OPTIONAL MATCH (l4)-[:HAS_ATTRIBUTE]->(l4Name:Name)
  OPTIONAL MATCH (l4)-[:HAS_ATTRIBUTE]->(l4Email:WorkEmail)
  
  // Determine the level of the user in the hierarchy
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

       // Coalescing the manager details at each level, ensuring empty values when no manager exists
       COALESCE(m.managerid, '') AS L1managerid,
       COALESCE(mName.FirstName, '') AS L1managerFirstName,
       COALESCE(mName.LastName, '') AS L1managerLastName,
       COALESCE(mEmail.WorkEmail, '') AS L1managerEmail,

       COALESCE(l1.managerid, '') AS L2managerid,
       COALESCE(l1Name.FirstName, '') AS L2managerFirstName,
       COALESCE(l1Name.LastName, '') AS L2managerLastName,
       COALESCE(l1Email.WorkEmail, '') AS L2managerEmail,

       COALESCE(l2.managerid, '') AS L3managerid,
       COALESCE(l2Name.FirstName, '') AS L3managerFirstName,
       COALESCE(l2Name.LastName, '') AS L3managerLastName,
       COALESCE(l2Email.WorkEmail, '') AS L3managerEmail,

       COALESCE(l3.managerid, '') AS L4managerid,
       COALESCE(l3Name.FirstName, '') AS L4managerFirstName,
       COALESCE(l3Name.LastName, '') AS L4managerLastName,
       COALESCE(l3Email.WorkEmail, '') AS L4managerEmail,

       COALESCE(l4.managerid, '') AS L5managerid,
       COALESCE(l4Name.FirstName, '') AS L5managerFirstName,
       COALESCE(l4Name.LastName, '') AS L5managerLastName,
       COALESCE(l4Email.WorkEmail, '') AS L5managerEmail

  // Return the relevant columns, ordered by employee number and level
  RETURN u.employeeNumber, u.managerid, level,
         L1managerid, L1managerFirstName, L1managerLastName, L1managerEmail,
         L2managerid, L2managerFirstName, L2managerLastName, L2managerEmail,
         L3managerid, L3managerFirstName, L3managerLastName, L3managerEmail,
         L4managerid, L4managerFirstName, L4managerLastName, L4managerEmail,
         L5managerid, L5managerFirstName, L5managerLastName, L5managerEmail
  ORDER BY u.employeeNumber
  ',
  {batchSize: 10000, iterateList: true, parallel: true}
)




CALL apoc.export.csv.query(
  'MATCH (u:User) ...', // Your query here
  'file:///path/to/your/report.csv',
  {}
)
