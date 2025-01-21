1.I have IAM data in neo4j. Like below ndoes:
User with labels such as Active, COntractor, Transfer etc and properties employeeNumber, managerid etc
UserAccount with labels such as Enabled and properties targetSystem, accountType, PrimaryAuthSystem etc
DepartmentInfo properties such as date, eventID etc

And the relationships such as:
User-[:HAS_ATTRIBUTE]->UserAccount
User-[:HAS_ATTRIBUTE]->(di:DepartmentInfo)-[:PREVIOUS]->(di2:DepartmentInfo)
                        di->[:CURRENT]->(d:Department)
                        di->[:HAS_DEPARTMENT]->(d)
                        
Suggest me simple ideas for recommendation system use cases.

2.tell me details about """User Role/Access Recommendation"""