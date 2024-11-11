// Match the user node and up to three levels of managers in reverse order
MATCH (user:User)
OPTIONAL MATCH (L1:User)-[:REPORTS_TO]->(L2:User)
OPTIONAL MATCH (L2)-[:REPORTS_TO]->(L3:User)
OPTIONAL MATCH (L3)-[:REPORTS_TO]->(user)

// Get name and email attributes for each level's manager and for the user (in case user is CEO)
OPTIONAL MATCH (user)-[:HAS_ATTRIBUTE]->(user_name:Name)
OPTIONAL MATCH (user)-[:HAS_ATTRIBUTE]->(user_email:WorkEmail)
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_name:Name)
OPTIONAL MATCH (L1)-[:HAS_ATTRIBUTE]->(L1_email:WorkEmail)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_name:Name)
OPTIONAL MATCH (L2)-[:HAS_ATTRIBUTE]->(L2_email:WorkEmail)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_name:Name)
OPTIONAL MATCH (L3)-[:HAS_ATTRIBUTE]->(L3_email:WorkEmail)

// Calculate Level based on manager hierarchy depth
WITH user, L1, L2, L3,
     user_name, user_email, L1_name, L1_email, L2_name, L2_email, L3_name, L3_email,
     CASE 
       WHEN user.employeeNumber = user.managerid THEN 1  // CEO
       WHEN L1 IS NOT NULL AND L2 IS NULL THEN 2  // Level 2 (one manager)
       WHEN L1 IS NOT NULL AND L2 IS NOT NULL AND L3 IS NULL THEN 3  // Level 3 (two managers)
       WHEN L1 IS NOT NULL AND L2 IS NOT NULL AND L3 IS NOT NULL THEN 4  // Level 4 (three managers)
       ELSE NULL 
     END AS Level

// Aggregate results to remove duplicates and ensure one row per employee
WITH user, Level, user_name, user_email, L1, L1_name, L1_email, L2, L2_name, L2_email, L3, L3_name, L3_email,
     CASE 
       WHEN Level = 1 THEN user.managerid 
       ELSE L1.employeeNumber 
     END AS L1managerid,

     CASE WHEN Level = 1 THEN user_name.givenName ELSE L1_name.givenName END AS L1managerFirstName,
     CASE WHEN Level = 1 THEN user_name.familyName ELSE L1_name.familyName END AS L1managerLastName,
     CASE WHEN Level = 1 THEN user_email.WorkEmail ELSE L1_email.WorkEmail END AS L1managerEmail,

     CASE WHEN Level >= 3 THEN L2.employeeNumber ELSE NULL END AS L2managerid,
     CASE WHEN Level >= 3 THEN L2_name.givenName ELSE NULL END AS L2managerFirstName,
     CASE WHEN Level >= 3 THEN L2_name.familyName ELSE NULL END AS L2managerLastName,
     CASE WHEN Level >= 3 THEN L2_email.WorkEmail ELSE NULL END AS L2managerEmail,

     CASE WHEN Level = 4 THEN L3.employeeNumber ELSE NULL END AS L3managerid,
     CASE WHEN Level = 4 THEN L3_name.givenName ELSE NULL END AS L3managerFirstName,
     CASE WHEN Level = 4 THEN L3_name.familyName ELSE NULL END AS L3managerLastName,
     CASE WHEN Level = 4 THEN L3_email.WorkEmail ELSE NULL END AS L3managerEmail

RETURN DISTINCT user.employeeNumber AS employeeNumber,
       user.managerid AS managerid,
       Level,
       L1managerid,
       L1managerFirstName,
       L1managerLastName,
       L1managerEmail,
       L2managerid,
       L2managerFirstName,
       L2managerLastName,
       L2managerEmail,
       L3managerid,
       L3managerFirstName,
       L3managerLastName,
       L3managerEmail
