In neo4j, i have data like for below nodes:

(u1:User)-[:REPORTS_TO]->(u2:User)->[:REPORTS_TO]->(u3:User) and so on... till 15 levels

I have around half million user data in neo4j. I want to create a report in below format
employeeid, managerid, level, L1managerid, L2managerid.

Here, employeeid, managerid are properties of User node