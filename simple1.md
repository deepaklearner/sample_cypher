In Neo4j, using this cypher “””CALL apoc.periodic.iterate( " MATCH (n:User) WHERE n.managerid IS NOT NULL RETURN n ", " OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User) WHERE n.managerid <> m.employeeNumber DELETE r WITH n MATCH (m:User {employeeNumber: n.managerid}) MERGE (n)-[:REPORTS_TO]->(m) ", {batchSize: 10000, parallel: false} )”””, I am creating some nodes and relationships.


Sample data:
(User: {employeeNumber: ‘2000004’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000003’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000002’}) -[:REPORTS_TO]->(User: {employeeNumber: ‘2000001’}) 

employeeNumber: ‘2000001’ is ceo. It should have Level value 1.

Sample output:

| employeeNumber | managerid | Level |
|----------------|-----------|-------|
| 2000001        | 2000001   | 1     |
| 2000002        | 2000001   | 2     |
| 2000003        | 2000002   | 3     |
| 2000004        | 2000003   | 4     |
