MATCH (user:User)
OPTIONAL MATCH (user)-[:REPORTS_TO]->(L1:User)
OPTIONAL MATCH (L1)-[:REPORTS_TO]->(L2:User)
OPTIONAL MATCH (L2)-[:REPORTS_TO]->(L3:User)

WITH user, L1, L2, L3,
     CASE 
       WHEN user.employeeNumber = user.managerid THEN 1
       WHEN L1 IS NOT NULL AND L2 IS NULL THEN 2
       WHEN L2 IS NOT NULL AND L3 IS NULL THEN 3
       WHEN L3 IS NOT NULL THEN 4
       ELSE NULL 
     END AS Level

RETURN 
    user.employeeNumber AS employeeNumber,
    user.managerid AS managerid,
    Level,
    
    // L1 manager details
    L1.employeeNumber AS L1managerid,
    L1_name.givenName AS L1managerFirstName,
    L1_name.familyName AS L1managerLastName,
    L1_email.WorkEmail AS L1managerEmail,
    
    // L2 manager details
    L2.employeeNumber AS L2managerid,
    L2_name.givenName AS L2managerFirstName,
    L2_name.familyName AS L2managerLastName,
    L2_email.WorkEmail AS L2managerEmail,
    
    // L3 manager details
    L3.employeeNumber AS L3managerid,
    L3_name.givenName AS L3managerFirstName,
    L3_name.familyName AS L3managerLastName,
    L3_email.WorkEmail AS L3managerEmail

// Get name and email attributes for each level's manager
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_name:Name)
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_email:WorkEmail)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_name:Name)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_email:WorkEmail)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_name:Name)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_email:WorkEmail)
