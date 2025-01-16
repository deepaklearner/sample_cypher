I want to move only the REDUCE logic to python... can we do that """MATCH (u:User) 
WHERE u.managerId IS NOT NULL 
  AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))

// Traverse the reporting structure (up to 15 levels)
OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)
WITH u, COLLECT(DISTINCT m.employeeNumber) AS manager_ids

RETURN u.employeeNumber AS EmployeeID,
CASE
  WHEN SIZE(manager_ids) = 1 AND u.employeeNumber <> manager_ids[0] THEN 1
  WHEN SIZE(manager_ids) = 2 THEN 2
  WHEN SIZE(manager_ids) = 3 THEN 3
  WHEN SIZE(manager_ids) = 4 THEN 4
  WHEN SIZE(manager_ids) = 5 THEN 5
  WHEN SIZE(manager_ids) = 6 THEN 6
  WHEN SIZE(manager_ids) = 7 THEN 7
  WHEN SIZE(manager_ids) = 8 THEN 8
  WHEN SIZE(manager_ids) = 9 THEN 9
  WHEN SIZE(manager_ids) = 10 THEN 10
  WHEN SIZE(manager_ids) = 11 THEN 11
  WHEN SIZE(manager_ids) = 12 THEN 12
  WHEN SIZE(manager_ids) = 13 THEN 13
  WHEN SIZE(manager_ids) = 14 THEN 14
  WHEN SIZE(manager_ids) = 15 THEN 15
END AS L1ManagerLevel,

// Select L1 to L15 manager IDs based on the number of managers
REDUCE(result = [], i IN RANGE(0, 14) | 
  CASE 
    WHEN i < SIZE(manager_ids) THEN result + [manager_ids[i]] 
    ELSE result 
  END
) AS manager_levels"""