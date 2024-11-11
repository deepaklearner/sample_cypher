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

Take inspiration from above cypher and helo me to write a new cypher query to create a report with below columns.

Sample report with sample data:
| employeeNumber | managerid | Level | L1managerid | L2managerid | L3managerid | L4managerid |
|----------------|-----------|-------|-------------|-------------|-------------|-------------|
| 2000001        | 2000001   | 1     | 2000001     |             |             |             |
| 2000002        | 2000001   | 2     | 2000001     |             |             |             |
| 2000003        | 2000002   | 3     | 2000002     | 2000001     |             |             |
| 2000004        | 2000003   | 4     | 2000003     | 2000002     | 2000001     |             |


        MATCH (employee:User)
        OPTIONAL MATCH (employee)-[:REPORTS_TO]->(L1:User)
        OPTIONAL MATCH (L1)-[:REPORTS_TO]->(L2:User)
        OPTIONAL MATCH (L2)-[:REPORTS_TO]->(L3:User)
        OPTIONAL MATCH (L3)-[:REPORTS_TO]->(L4:User)
        RETURN 
        employee.employeeNumber AS employeeNumber,
        employee.managerid AS managerid,
        CASE
            WHEN L4 IS NOT NULL THEN 4
            WHEN L3 IS NOT NULL THEN 3
            WHEN L2 IS NOT NULL THEN 2
            WHEN L1 IS NOT NULL THEN 1
            ELSE 0
        END AS Level,
        L1.employeeNumber AS L1managerid,
        L2.employeeNumber AS L2managerid,
        L3.employeeNumber AS L3managerid,
        L4.employeeNumber AS L4managerid
        ORDER BY employee.employeeNumber
