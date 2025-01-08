I want to make a change in below part, such that 
if employeeNumber should be present in Neo4J as a User node property. 
If its not present, dont create User node.

"""FOREACH (x IN CASE WHEN row.current_manager <> "DNE" AND row.is_manager_exist_in_INT5043 = 'Y' THEN [1] END |
    MERGE (usr:User {employeeNumber: row.current_manager})
    ON CREATE SET usr.userProfileID = apoc.create.uuid(),
                  usr.globalID = toString(toInteger(globalid.lastAssignedCounterValue) + 1),
                  globalid.lastExecutionDate = localdatetime(),
                  globalid.lastAssignedCounterValue = toString(toInteger(globalid.lastAssignedCounterValue) + 1)
    MERGE (usr)-[:MANAGES]->(dept)
)
"""

Solution 1:

To modify the Cypher query so that the `User` node is not created if the `employeeNumber` does not exist in the Neo4j database, we need to adjust the logic around the `MERGE` statement. Specifically, instead of using `MERGE` (which creates the node if it doesn't exist), we will first check if the `User` node already exists by matching on `employeeNumber`, and only create the relationship if the node exists.

Here’s how you can modify the code:

### Updated Cypher Query:

```cypher
FOREACH (x IN CASE WHEN row.current_manager <> "DNE" AND row.is_manager_exist_in_INT5043 = 'Y' THEN [1] END |
    // Check if the User node already exists with the employeeNumber
    MATCH (usr:User {employeeNumber: row.current_manager})
    // Create the relationship only if the User node exists
    MERGE (usr)-[:MANAGES]->(dept)
)
```

### Explanation of Changes:
1. **MATCH instead of MERGE**: 
   - We use `MATCH` to check if the `User` node already exists with the given `employeeNumber` (`{employeeNumber: row.current_manager}`). This ensures we only act on existing `User` nodes.
   - If the node doesn’t exist, no action will be taken, meaning no new `User` node will be created.

2. **MERGE Relationship**: 
   - After confirming that the `User` node exists, we create the `MANAGES` relationship between the `User` and the `Department`.
   - The `MERGE` here ensures that the `MANAGES` relationship is created if it doesn't already exist. If it exists, no new relationship is created, which is efficient.

3. **No `ON CREATE` logic**:
   - Since we are no longer creating a new `User` node, the `ON CREATE` section (which would set the `userProfileID`, `globalID`, etc.) is removed. There's no need to create or update properties on a non-existing `User` node because we’re ensuring the node exists beforehand.

### Important Notes:
- **Performance**: This approach ensures that we don't create unnecessary `User` nodes if they don’t already exist in the database.
- **Consistency**: If `row.current_manager` points to a manager who doesn’t have a corresponding `User` node, no relationship is created, maintaining data consistency.

### Full Modified Cypher Query (for reference):

```cypher
UNWIND $rows AS row
MERGE (dept:Department {departmentCode: row.currentcode})
SET dept.department = row.currentdesc,
    dept.deptLevel = row.currentlvl
WITH row, dept

// Match existing relationships and delete them if necessary
OPTIONAL MATCH (:User)-[r_has:MANAGES]->(dept)
OPTIONAL MATCH (dept)-[r_report_to:REPORTS_TO]->(:Department)
MATCH (globalid:GlobalIdentifierCounter)
DELETE r_has, r_report_to

// Create parent department relationship
FOREACH (x IN CASE WHEN row.parentcode <> "DNE" THEN [1] END |
    MERGE (dept2:Department {departmentCode: row.parentcode})
    ON CREATE SET dept2.department = row.parentdesc,
                  dept2.deptLevel = row.parentlvl
    MERGE (dept)-[:REPORTS_TO]->(dept2)
)

// Create user-manager relationship (only if User node exists)
FOREACH (x IN CASE WHEN row.current_manager <> "DNE" AND row.is_manager_exist_in_INT5043 = 'Y' THEN [1] END |
    MATCH (usr:User {employeeNumber: row.current_manager})
    MERGE (usr)-[:MANAGES]->(dept)
)
RETURN COUNT(*)
```

This should now only create the `MANAGES` relationship if a `User` node already exists for the specified `employeeNumber`. If no `User` exists, no action will be taken for that particular manager.