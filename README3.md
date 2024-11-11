MATCH (user:User)
OPTIONAL MATCH (user)-[:REPORTS_TO*0..]->(manager:User)
WITH user, manager, length((user)-[:REPORTS_TO*]->(manager)) AS level
WITH user, manager, level, 
     COLLECT(manager.employeeNumber) AS managerIds,
     COLLECT(manager) AS managers
WITH user, level, managerIds, managers, 
     REDUCE(names = "", m IN managers | names + m.employeeNumber + ", ") AS managerNumbers,
     REDUCE(names = "", m IN managers | names + m.name.givenName + ", ") AS firstNames,
     REDUCE(names = "", m IN managers | names + m.name.familyName + ", ") AS lastNames,
     REDUCE(names = "", m IN managers | names + m.workEmail.email + ", ") AS emails
RETURN user.employeeNumber AS employeeNumber,
       user.managerid AS managerid,
       level,
       managerIds[0] AS L1managerid,
       firstNames[0] AS L1managerFirstName,
       lastNames[0] AS L1managerLastName,
       emails[0] AS L1managerEmail,
       managerIds[1] AS L2managerid,
       firstNames[1] AS L2managerFirstName,
       lastNames[1] AS L2managerLastName,
       emails[1] AS L2managerEmail,
       managerIds[2] AS L3managerid,
       firstNames[2] AS L3managerFirstName,
       lastNames[2] AS L3managerLastName,
       emails[2] AS L3managerEmail,
       managerIds[3] AS L4managerid,
       firstNames[3] AS L4managerFirstName,
       lastNames[3] AS L4managerLastName,
       emails[3] AS L4managerEmail
