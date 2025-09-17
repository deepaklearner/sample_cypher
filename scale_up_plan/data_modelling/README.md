1.5 Also please help me with data model

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
