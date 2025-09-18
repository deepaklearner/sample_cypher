Project overview:
"""
I have three tables: 
a. entitlement_master (key: entitle_name and platform)
b. eservice_data (key: entitle_name and entitle_source) and 
c. entitlement_accounts: contains entitle_name, platform and accounts data

Data in neo4j should be like:
(ua:UserAccount)-[:HAS_ATTRIBUTE]->(ei:EntitlementInfo)
(ei)-[:CURRENT]->(e:Entitlement)
(ei)-[:HAS_ENTITLEMENT]->(e)

(e)-[:HAS_OWNER]->(:User)
(e)[:PREVIOUS]->(EntitlementOwnerInfo)-[:HAS_OWNER]->(User)

MySQL table details:
entitlement_master has 8.8 million rows
eservice_data has 213k rows
entitlement_user has 40 million rows

entitle_source and platform are same data.

I am reading data from entitlement_master in batches and then using keys searching them in eservice_data and then loading the data in neo4j."""

In my project, i am using Pandas and neo4j.

1.1 Please help me with data model

Sample existing data model which i want to improve:
"""
(ua:UserAccount)-[:HAS_ATTRIBUTE]->(ei:EntitlementInfo)
(ei)-[:CURRENT]->(e:Entitlement)
(ei)-[:HAS_ENTITLEMENT]->(e:Entitlement)
(e)-[:HAS_ATTRIBUTE]->(oi:OwnerInfo)
(oi)-[:HAS_OWNER]->(o:User)
(oi)-[:CURRENT]->(o)"""

New data model I am trying to build, which is in progress:
"""
(ua:UserAccount)-[:HAS_ATTRIBUTE]->(ei:EntitlementInfo)
(ei)-[:CURRENT]->(e:Entitlement)
(e)-[:HAS_OWNER]->(oi:EntitlementOwnerInfo)
(e)-[:PREVIOUS]->(oi2:EntitlementOwnerInfo)
(oi)-[:HAS_OWNER]->(o:User)
"""
Please help with the new data model which will be good for large scale data.

1.6
I want 
"""
(ua:UserAccount)-[:HAS_ATTRIBUTE]->(ei:EntitlementInfo)
(ei)-[:CURRENT]->(e:Entitlement)

(e:Entitlement)-[:HAS_OWNER]->(eoi:EntitlementOwnerInfo {current: true})
(e:Entitlement)-[:HAD_OWNER]->(eoi2:EntitlementOwnerInfo {current: false})

(eoi)-[:HAS_OWNER]->(u:User)
(eoi)-[:VALID_FROM]->(:Date)
(eoi)-[:VALID_TO]->(:Date)          // optional, for tracking ownership periods
"""
