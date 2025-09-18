Project overview:
"""
I have three tables: 
a. entitlement_master (key: entitle_name and platform)
b. eservice_data (key: entitle_name and entitle_source) and 
c. entitlement_accounts: contains entitle_name, platform and accounts data

Data in neo4j should be like:
(ua:UserAccount)-[:HAS_ATTRIBUTE]->(EntitlementInfo)-[:CURRENT:HAS_ENTITLEMENT]->(e:Entitlement)
(e)-[:HAS_OWNER]->(:User)
(e)[:PREVIOUS]->(EntitlementOwnerInfo)-[:HAS_OWNER]->(User)

MySQL table details:
entitlement_master has 8.8 million rows
eservice_data has 213k rows
entitlement_user has 40 million rows

entitle_source and platform are same data.

I am reading data from entitlement_master in batches and then using keys searching them in eservice_data and then loading the data in neo4j."""

In my project, i am using Pandas and neo4j.

1.1 Considering the huge size of entitlement_master. I want to plan a suitable robust etl process. Please help me with ideas and also let me know the right questions about requirement I should ask.
1.2 As of now I am using Offset and Limit to read the data from entitlement_master in batches.
I am using MySQL, version 8.0.40.

Questions:
What if an account if removed from an Entitlement? Are we maintaining any history trail for that?

1.3
tell me overall strategy in least number of words in points

1.4 entitlement_accounts has 40 Million data