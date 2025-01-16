After running below cypher, i want to check usign python, that if any value for L1ManagerLevel > 15

"""MATCH (u:User) 
WHERE u.managerId IS NOT NULL 
  AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))

// Traverse the reporting structure (up to 15 levels)
OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)
WITH u, COLLECT(DISTINCT m.employeeNumber) AS manager_ids

RETURN u.employeeNumber AS EmployeeID,
CASE
  WHEN SIZE(manager_ids) = 1 AND u.employeeNumber == manager_ids[0] THEN 1
  WHEN SIZE(manager_ids) = 2 AND u.employeeNumber <> manager_ids[0] THEN 2
  WHEN SIZE(manager_ids) > 1 THEN SIZE(manager_ids)+1
END AS L1ManagerLevel,
manager_ids AS manager_levels"""