1.I have IAM data in neo4j. Like below ndoes:

And the relationships such as:
User-[:HAS_ATTRIBUTE]->UserAccount
User-[:HAS_ATTRIBUTE]->(di:DepartmentInfo)-[:CURRENT]->(d1:Department)
                        di->[:PREVIOUS]->(d2:Department)
                        di->[:HAS_DEPARTMENT]->(d)

1. The properties for Department node are:
department, departmentCode, deptLevel

2. The properties for DepartmentInfo node are:
changeReasonCode, date, eventID, jobResponsibilitiesChanged, startDate

3. The properties for User node are:
acquisionCode, eligibilityCode, employeeNumber, globalID, managerid, transactionType

Make use of these nodes relationship and suggest some good and easy to implement usecase to show good use of
graph db 

