5.1 In my code, I am reading around 8 million rows in batches from a table entitlement_master. Mainly columns entitle_name and entitle_source. (Here, entitle_name and entitle_source are primary key)
Then, reading eservice_data to get owner details for the entitle_name. 

Then doing a left join with table entitlement_master using key entitlementName and targetSystem.

Then loading data to Neo4j in Entitlement node and creating relationship with User node.

It also creates two reports, warning report and error report. Warning report when no owner inactive in neo4j and error report when owner is missign in neo4j 

Suggest a one liner description for the project.
Example: "This script processes EDW Entitlements from ..."