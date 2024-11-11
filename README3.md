// Match the user node and up to three levels of managers
MATCH (user:User)
OPTIONAL MATCH (user)-[:REPORTS_TO]->(L1:User)
OPTIONAL MATCH (L1)-[:REPORTS_TO]->(L2:User)
OPTIONAL MATCH (L2)-[:REPORTS_TO]->(L3:User)

// Get name and email attributes for each level's manager
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_name:Name)
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_email:WorkEmail)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_name:Name)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_email:WorkEmail)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_name:Name)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_email:WorkEmail)

WITH user, L1, L2, L3,
     L1_name, L1_email, L2_name, L2_email, L3_name, L3_email,
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
    CASE WHEN Level >= 2 THEN L1.employeeNumber ELSE NULL END AS L1managerid,
    CASE WHEN Level >= 2 THEN L1_name.givenName ELSE NULL END AS L1managerFirstName,
    CASE WHEN Level >= 2 THEN L1_name.familyName ELSE NULL END AS L1managerLastName,
    CASE WHEN Level >= 2 THEN L1_email.WorkEmail ELSE NULL END AS L1managerEmail,
    
    // L2 manager details
    CASE WHEN Level >= 3 THEN L2.employeeNumber ELSE NULL END AS L2managerid,
    CASE WHEN Level >= 3 THEN L2_name.givenName ELSE NULL END AS L2managerFirstName,
    CASE WHEN Level >= 3 THEN L2_name.familyName ELSE NULL END AS L2managerLastName,
    CASE WHEN Level >= 3 THEN L2_email.WorkEmail ELSE NULL END AS L2managerEmail,
    
    // L3 manager details
    CASE WHEN Level >= 4 THEN L3.employeeNumber ELSE NULL END AS L3managerid,
    CASE WHEN Level >= 4 THEN L3_name.givenName ELSE NULL END AS L3managerFirstName,
    CASE WHEN Level >= 4 THEN L3_name.familyName ELSE NULL END AS L3managerLastName,
    CASE WHEN Level >= 4 THEN L3_email.WorkEmail ELSE NULL END AS L3managerEmail
