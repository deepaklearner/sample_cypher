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
3. Then, check if user has secondary account > If no then update PrimaryAuth for respective account
4. If Yes, Then, check if PrimaryAuth set for seondary account > If yes, then switch accounts to Primary and secondary in the domain.
5. Then check, if any domains has this PAS account as secondary. If Yes, then swicth accounts to primary and secondayr in each domain to match PAS. 

This requirement is vague to me... and i need your help to think the possibilities... and think...in general for other IAM systems...

Ques 1: do i need to change the rejection logic "for an employee, the PrimaryAuth is true in neo4j or accountType is not 'Primary' in neo4j."? if i need to accomodate the new requirement?

NOTE: we dont have PrimaryAuth data in edw. It is computed based on a rule...
First time, when a useraccount data comes in neo4j. Then if that targetSystem is one of ['CORP','CSARMARK','CVS'] and 'cloud' keyword in extensionattribute3. And no primary account in neo4j for that user having PrimaryAuth as true. then this new useraccount becomes PrimaryAuth true.

Next, time if other useraccoutn data comes for same domain... that becomes secondary accountType.


Also, as per the requirement, further:




1.2 Compute PrimaryAuth from EDW data for the incoming account.

Summary:
The rule:

A user can have a PrimaryAuth account if:
targetSystem ∈ ['CORP', 'CSARMARK', 'CVS']
extensionAttribute3 contains "cloud"
The user has no existing account in Neo4j marked as PrimaryAuth=true
If these conditions are met → this account becomes PrimaryAuth=true
If the user already has a primary, OR the new account does not match the criteria → this is Secondary


1.3 
I didnt understand, this part:
If eligibleAccounts > 1 → reject (ambiguous)

But the current code is not rejecting in this scenario... what should i do?

Summary:
There are 2 correct approaches:
OPTION 1 — Matching your existing system (NO REJECTION)

If the rule is:

“PrimaryAuth is assigned one-time only.
Once assigned, all future eligible accounts become secondary.”
Then your behavior should be:
No rejection.
Use Neo4j’s current primary to break ties.

In this approach:
EligibleAccounts > 1 is NOT a problem
Neo4j already has the primary
You pick the existing primary and demote the rest
This is consistent with your legacy logic.

OPTION 2 — Strict IAM rule enforcement (REJECT)
If the rule is:
“PrimaryAuth must be determined solely from EDW attributes
and EDW must send exactly one primary account”
Then:
eligibleAccounts > 1 = Data Issue → REJECT
This is used in regulatory/critical systems.

Next,

Let’s check the new requirement text:

“Compute the PrimaryAuth from EDW accounts data.
If PrimaryAuth changed then retrieve all accounts from Neo4j…
Then switch accounts to Primary and Secondary in each domain…”

his implies:

✔ EDW-derived PrimaryAuth becomes authoritative
✔ Neo4j is no longer used to pick primary automatically
✔ PrimaryAuth should be consistent across domains

Therefore:

⛔ EDW must identify a single PrimaryAuth candidate
⛔ If EDW produces ambiguous PrimaryAuth candidates → data conflict

So with the new requirement, EDW must define one and only one primary candidate.

our ETL should reject eligibleAccounts > 1

UNLESS business tells you:

One system (CORP / CVS / CSARMARK) has priority

Or one attribute determines which should be primary

1.4 what about the existing rejection logic in code?
"for an employee, the PrimaryAuth is true in neo4j or accountType is not 'Primary' in neo4j."