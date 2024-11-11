// Match all User nodes and retrieve the hierarchy to the CEO for each
MATCH (user:User)-[:REPORTS_TO*0..]->(manager:User)
WHERE user.employeeNumber IS NOT NULL
WITH user, COLLECT(manager) AS hierarchy, SIZE(COLLECT(manager)) AS level
ORDER BY user.employeeNumber

// Add name and email attributes for each level
WITH user, hierarchy, level,
     [x IN RANGE(0, level - 1) | hierarchy[x].employeeNumber] AS manager_ids,
     [x IN RANGE(0, level - 1) | head([(hierarchy[x])-[:HAS_ATTRIBUTE]->(name:Name) | name.givenName])] AS manager_firstnames,
     [x IN RANGE(0, level - 1) | head([(hierarchy[x])-[:HAS_ATTRIBUTE]->(name:Name) | name.familyName])] AS manager_lastnames,
     [x IN RANGE(0, level - 1) | head([(hierarchy[x])-[:HAS_ATTRIBUTE]->(email:WorkEmail) | email.WorkEmail])] AS manager_emails

// Format the output with the required columns
RETURN user.employeeNumber AS employeeNumber,
       user.managerid AS managerid,
       CASE level WHEN 1 THEN "1"
                  WHEN 2 THEN "2"
                  WHEN 3 THEN "3"
                  ELSE level END AS Level,
       manager_ids[0] AS L1managerid,
       manager_firstnames[0] AS L1managerFirstName,
       manager_lastnames[0] AS L1managerLastName,
       manager_emails[0] AS L1managerEmail,
       manager_ids[1] AS L2managerid,
       manager_firstnames[1] AS L2managerFirstName,
       manager_lastnames[1] AS L2managerLastName,
       manager_emails[1] AS L2managerEmail,
       manager_ids[2] AS L3managerid,
       manager_firstnames[2] AS L3managerFirstName,
       manager_lastnames[2] AS L3managerLastName,
       manager_emails[2] AS L3managerEmail,
       // Extend for more levels as needed
       ...
