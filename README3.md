MATCH (user:User)
OPTIONAL MATCH (user)-[:REPORTS_TO*]->(manager:User)
WITH user, manager, length((user)-[:REPORTS_TO*]->(manager)) AS pathLength
WITH user, 
     CASE 
         WHEN user.managerid = user.employeeNumber THEN 1  // CEO (self-reporting) has level 1
         ELSE pathLength + 1  // Level is number of hops to CEO + 1
     END AS level,
     COLLECT(manager) AS managers
WITH user, level, managers[0] AS L1manager, managers[1] AS L2manager, managers[2] AS L3manager, managers[3] AS L4manager
RETURN user.employeeNumber AS employeeNumber,
       user.managerid AS managerid,
       level,
       CASE WHEN L1manager IS NOT NULL THEN L1manager.employeeNumber END AS L1managerid,
       CASE WHEN L1manager IS NOT NULL THEN L1manager.name.givenName END AS L1managerFirstName,
       CASE WHEN L1manager IS NOT NULL THEN L1manager.name.familyName END AS L1managerLastName,
       CASE WHEN L1manager IS NOT NULL THEN L1manager.workEmail.email END AS L1managerEmail,
       CASE WHEN L2manager IS NOT NULL THEN L2manager.employeeNumber END AS L2managerid,
       CASE WHEN L2manager IS NOT NULL THEN L2manager.name.givenName END AS L2managerFirstName,
       CASE WHEN L2manager IS NOT NULL THEN L2manager.name.familyName END AS L2managerLastName,
       CASE WHEN L2manager IS NOT NULL THEN L2manager.workEmail.email END AS L2managerEmail,
       CASE WHEN L3manager IS NOT NULL THEN L3manager.employeeNumber END AS L3managerid,
       CASE WHEN L3manager IS NOT NULL THEN L3manager.name.givenName END AS L3managerFirstName,
       CASE WHEN L3manager IS NOT NULL THEN L3manager.name.familyName END AS L3managerLastName,
       CASE WHEN L3manager IS NOT NULL THEN L3manager.workEmail.email END AS L3managerEmail,
       CASE WHEN L4manager IS NOT NULL THEN L4manager.employeeNumber END AS L4managerid,
       CASE WHEN L4manager IS NOT NULL THEN L4manager.name.givenName END AS L4managerFirstName,
       CASE WHEN L4manager IS NOT NULL THEN L4manager.name.familyName END AS L4managerLastName,
       CASE WHEN L4manager IS NOT NULL THEN L4manager.workEmail.email END AS L4managerEmail
