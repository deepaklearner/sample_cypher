    CALL apoc.periodic.iterate(
      "
        MATCH (n:User)
        WHERE n.managerid IS NOT NULL
        RETURN n
      ",
      "
        OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User)
        WHERE n.managerid <> m.employeeNumber
        DELETE r
        WITH n
        MATCH (m:User {employeeNumber: n.managerid})
        MERGE (n)-[:REPORTS_TO]->(m)
      ",
      {batchSize: 10000, parallel: false}
    )

Explanation:
CALL apoc.periodic.iterate: This is used for executing the periodic batch processing.
First part (the MATCH query): This retrieves users (n) where the managerid is not null.
Second part (the OPTIONAL MATCH, DELETE, and MERGE query): It finds any existing REPORTS_TO relationships that are invalid (where n.managerid does not match m.employeeNumber), deletes them, and then ensures the correct relationship is established by MERGEing a new one.
batchSize: 10000: Processes in batches of 10,000 nodes.
parallel: false: Runs the query in a single-threaded manner.