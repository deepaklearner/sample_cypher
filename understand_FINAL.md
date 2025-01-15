

```cypher
MATCH (u:User) 
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
) AS manager_levels
```


Explanation:

This query is written in Cypher, the query language for the Neo4j graph database. The query retrieves information about users (employees or contractors) in an organizational structure, focusing on their reporting lines and the levels of management. Here's a breakdown of the components:

### 1. **Match Users with a Manager**  
```cypher
MATCH (u:User)
WHERE u.managerId IS NOT NULL
  AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))
```
- **MATCH (u:User)**: This finds all nodes of type `User` in the graph.
- **WHERE u.managerId IS NOT NULL**: Filters out users who do not have a `managerId` (i.e., they don't report to anyone).
- **AND ("Employee" IN labels(u) OR "Contractor" IN labels(u))**: Filters for nodes that are labeled either as `Employee` or `Contractor`. This ensures only employees or contractors are included in the results.

### 2. **Traverse Reporting Structure**  
```cypher
OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)
WITH u, COLLECT(DISTINCT m.employeeNumber) AS manager_ids
```
- **OPTIONAL MATCH (u)-[:REPORTS_TO*1..15]->(m:User)**: This matches the reporting relationships between users. The `[:REPORTS_TO*1..15]` specifies a variable-length path where the relationship `REPORTS_TO` can be traversed between 1 and 15 levels. It means the query is trying to find up to 15 levels of managers that a user reports to.
  - The `OPTIONAL MATCH` is used, meaning the query will still return results even if there are no matching `REPORTS_TO` relationships (i.e., if the user doesn’t report to any manager).
- **WITH u, COLLECT(DISTINCT m.employeeNumber) AS manager_ids**: After finding the users and their reporting relationships, this collects the distinct `employeeNumber` of all the managers the user reports to and stores them in a list called `manager_ids`.

### 3. **Return Employee Information with Manager Levels**  
```cypher
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
```
- **RETURN u.employeeNumber AS EmployeeID**: Returns the `employeeNumber` of each user as `EmployeeID`.
- **CASE**: This block checks the size of the `manager_ids` list (i.e., how many managers the user reports to) and assigns a corresponding manager level. If the user reports to 1 manager, the result will be `L1ManagerLevel = 1`, and so on up to 15.

  The logic inside the `CASE` statement is:
  - **If the user has exactly 1 manager and their own employee number is not equal to the manager's number**: They are assigned `L1ManagerLevel = 1`.
  - **If the user has exactly 2 managers**: They are assigned `L1ManagerLevel = 2`, and so on.
  
  The logic implies that the user can report to more than one manager (as seen from `SIZE(manager_ids)`).

### 4. **Generate Manager Levels for Reporting Structure**  
```cypher
REDUCE(result = [], i IN RANGE(0, 14) | 
  CASE 
    WHEN i < SIZE(manager_ids) THEN result + [manager_ids[i]] 
    ELSE result 
  END
) AS manager_levels
```
- **REDUCE(result = [], i IN RANGE(0, 14)**: This iterates over a range from 0 to 14 (i.e., up to 15 managers). The `REDUCE` function accumulates the manager IDs into a list (`result`).
  - For each `i` in the range, the query checks if the `i`-th manager exists in the `manager_ids` list.
  - **When `i < SIZE(manager_ids)`**: It appends the manager ID at index `i` to the `result` list.
  - **ELSE**: If `i` exceeds the size of `manager_ids`, it simply keeps the `result` list unchanged.
  
  This will generate a list of manager IDs (`manager_levels`) up to the 15th level, with missing levels being empty if the user reports to fewer managers.

### Final Output
The query will return:
- **EmployeeID**: The employee number of each user.
- **L1ManagerLevel**: The number of distinct managers the user reports to (up to 15).
- **manager_levels**: A list of the managers (employee numbers) the user reports to, up to 15 levels.

### Example Use Case
- **EmployeeID**: `E123`
- **L1ManagerLevel**: `3` (this employee reports to 3 managers)
- **manager_levels**: `[M101, M102, M103]` (the list of employee numbers of the managers this employee reports to)

### Summary
This query is designed to navigate through an organizational hierarchy, collect distinct managers up to 15 levels deep, and return both the hierarchical level (`L1ManagerLevel`) and a list of the managers (`manager_levels`) for each employee or contractor who reports to one or more managers.