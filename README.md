1.1 
I am working in an IAM project.

I have a mysql database contains Employee and their accounts and a neo4j database.

In my mysql table, i have columns: EmployeeID, samaccountname, targetSystem, extensionattribute3

In my neo4j, I have user node which is connected to UserAccount node having properties:
employeeNumber, targetSystem, PrimaryAuth (can be true or false), accountType (can be Primary or Secondary)

In my ETL process, I am computing the PrimaryAuth, accountType.

As per the existing logic, for PAS related data:
I am rejecting the mysql data if:
for an employee, the PrimaryAuth is true in neo4j or accountType is not 'Primary' in neo4j.

As per the new rew requirement, I am supposed to:
1.read accounts from edw > Check for PrimaryAuth system > Check If User has PrimaryAuth > If "No" then Assign PrimaryAuth to Primary Account Else (2)
2. Compute the PrimaryAuth from EDW accounts data. If PrimaryAuth changed then Retrieve all the accounts for the User from neo4j.
3. continue...

This requirement is vague to me... and i need your help to think the possibilities... and think...in general for other IAM systems...

Ques 1: do i need to change the rejection logic "for an employee, the PrimaryAuth is true in neo4j or accountType is not 'Primary' in neo4j."? if i need to accomodate the new requirement?

NOTE: we dont have PrimaryAuth data in edw. It is computed based on a rule...
First time, when a useraccount data comes in neo4j. Then if that targetSystem is one of ['CORP','CSARMARK','CVS'] and 'cloud' keyword in extensionattribute3. And no primary account in neo4j for that user having PrimaryAuth as true. then this new useraccount becomes PrimaryAuth true.

Next, time if other useraccoutn data comes for same domain... that becomes secondary accountType.


1.2 Compute PrimaryAuth from EDW data for the incoming account.