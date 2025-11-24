1.1 I have a mysql database and a neo4j database.

In my mysql table, i have columns: EmployeeID, samaccountname, targetSystem, attribute3

In my neo4j, I have user node which is connected to UserAccount node having properties:
employeeNumber, targetSystem, PrimaryAuth (can be true or false), accountType (can be Primary or Secondary)

In my ETL process, I am computing the PrimaryAuth, accountType.

As per th eexisting logic:
I am only allowing the PAS to be changed when, 