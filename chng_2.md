I want to log a warning in log, if row.current_manager is not present in neo4j.

from neo4j import GraphDatabase

# Establish connection to Neo4j
uri = "bolt://localhost:7687"  # Adjust for your Neo4j instance
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Define the Cypher query with RETURN for logging
cypher_query = """
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

// Check if User node exists and conditionally create the relationship
WITH row, dept, globalid
WHERE row.current_manager <> "DNE" AND row.is_manager_exist_in_INT5043 = 'Y'
OPTIONAL MATCH (usr:User {employeeNumber: row.current_manager})
WITH row, dept, usr
// If usr is not NULL, create the relationship
FOREACH (x IN CASE WHEN usr IS NOT NULL THEN [1] END |
    MERGE (usr)-[:MANAGES]->(dept)
)

// If the User node is not found, log the missing manager
WITH row, dept, usr
WHERE usr IS NULL
WITH 'Manager not found in Neo4j: ' + row.current_manager AS MissingManager

RETURN COUNT(*), COLLECT(MissingManager) AS MissingManagers
"""

# Sample data to pass as parameters
rows = [
    {"currentcode": "A01", "currentdesc": "Dept A", "currentlvl": 1, "parentcode": "DNE", "parentdesc": "N/A", "parentlvl": 0, "current_manager": "123", "is_manager_exist_in_INT5043": "Y"},
    {"currentcode": "B01", "currentdesc": "Dept B", "currentlvl": 2, "parentcode": "A01", "parentdesc": "Dept A", "parentlvl": 1, "current_manager": "999", "is_manager_exist_in_INT5043": "Y"},
    # Add more rows as needed
]

# Run the query
with driver.session() as session:
    result = session.run(cypher_query, rows=rows)

    # Capture results
    for record in result:
        if 'MissingManager' in record:
            print(record['MissingManager'])  # Log message for missing managers
        else:
            print(f"Departments processed: {record['COUNT(*)']}")

# Close the driver
driver.close()
