CALL apoc.periodic.iterate(
  'MATCH (u:User) WHERE u.employeeNumber IS NOT NULL RETURN u LIMIT 10',  // Limit to 10 users for testing
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
       CASE WHEN m IS NOT NULL THEN COALESCE(m.managerid, '') ELSE '' END AS L1managerid,
       CASE WHEN m IS NOT NULL THEN COALESCE(mName.FirstName, '') ELSE '' END AS L1managerFirstName,
       CASE WHEN m IS NOT NULL THEN COALESCE(mName.LastName, '') ELSE '' END AS L1managerLastName,
       CASE WHEN m IS NOT NULL THEN COALESCE(mEmail.WorkEmail, '') ELSE '' END AS L1managerEmail,

       CASE WHEN l1 IS NOT NULL THEN COALESCE(l1.managerid, '') ELSE '' END AS L2managerid,
       CASE WHEN l1 IS NOT NULL THEN COALESCE(l1Name.FirstName, '') ELSE '' END AS L2managerFirstName,
       CASE WHEN l1 IS NOT NULL THEN COALESCE(l1Name.LastName, '') ELSE '' END AS L2managerLastName,
       CASE WHEN l1 IS NOT NULL THEN COALESCE(l1Email.WorkEmail, '') ELSE '' END AS L2managerEmail,

       CASE WHEN l2 IS NOT NULL THEN COALESCE(l2.managerid, '') ELSE '' END AS L3managerid,
       CASE WHEN l2 IS NOT NULL THEN COALESCE(l2Name.FirstName, '') ELSE '' END AS L3managerFirstName,
       CASE WHEN l2 IS NOT NULL THEN COALESCE(l2Name.LastName, '') ELSE '' END AS L3managerLastName,
       CASE WHEN l2 IS NOT NULL THEN COALESCE(l2Email.WorkEmail, '') ELSE '' END AS L3managerEmail,

       CASE WHEN l3 IS NOT NULL THEN COALESCE(l3.managerid, '') ELSE '' END AS L4managerid,
       CASE WHEN l3 IS NOT NULL THEN COALESCE(l3Name.FirstName, '') ELSE '' END AS L4managerFirstName,
       CASE WHEN l3 IS NOT NULL THEN COALESCE(l3Name.LastName, '') ELSE '' END AS L4managerLastName,
       CASE WHEN l3 IS NOT NULL THEN COALESCE(l3Email.WorkEmail, '') ELSE '' END AS L4managerEmail,

       CASE WHEN l4 IS NOT NULL THEN COALESCE(l4.managerid, '') ELSE '' END AS L5managerid,
       CASE WHEN l4 IS NOT NULL THEN COALESCE(l4Name.FirstName, '') ELSE '' END AS L5managerFirstName,
       CASE WHEN l4 IS NOT NULL THEN COALESCE(l4Name.LastName, '') ELSE '' END AS L5managerLastName,
       CASE WHEN l4 IS NOT NULL THEN COALESCE(l4Email.WorkEmail, '') ELSE '' END AS L5managerEmail

  // Return the relevant columns, ordered by employee number and level
  RETURN u.employeeNumber, u.managerid, level,
         L1managerid, L1managerFirstName, L1managerLastName, L1managerEmail,
         L2managerid, L2managerFirstName, L2managerLastName, L2managerEmail,
         L3managerid, L3managerFirstName, L3managerLastName, L3managerEmail,
         L4managerid, L4managerFirstName, L4managerLastName, L4managerEmail,
         L5managerid, L5managerFirstName, L5managerLastName, L5managerEmail
  ORDER BY u.employeeNumber
  ',
  {batchSize: 10, iterateList: true, parallel: false}
)





CALL apoc.export.csv.query(
  'MATCH (u:User) ...', // Your query here
  'file:///path/to/your/report.csv',
  {}
)
