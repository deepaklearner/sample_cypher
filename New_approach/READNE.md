1.1 

a. In neo4j, I have a node, Entitlement with property entitlementName, targetSystem, description, riskLevel, priviledgedAccess, entitlementType.
Note: entitlementName, targetSystem are constraints

And other node User having property employeeNumber.

b. The Entitlement node and User node are having relationship OWNER.
(Entitlement)-[:OWNER]->(User)

c. I am reading a couple of Entitlements along with targetSystem and description, riskLevel, priviledgedAccess and entitlementType from another mysql db as python pandas dataframe. 

d. I want to fetch the compare the data from Neo4j for below properties:
description, riskLevel, priviledgedAccess and entitlementType
and create if its not present for the constraints or update if there is a mismatch.

from the pandas dataframe. 

Note: One Entitlement can have multiple owners 

e. Return the entitlementName and Owner details

f. Use UNWIND and all in single cypher query.

Approach:2
a. First using the entitlementName and targetSystem (fetched from mysql db), for the existing Entitlement nodes fetch the Owner details and below properties values 
description, riskLevel, priviledgedAccess and entitlementType

b. Compare the mysql df if there is any change in below properties:
description, riskLevel, priviledgedAccess and entitlementType

c. Create the Entitlement nodes if its not present in Neo4j.

Is this approach better than previous?

1.2 
I have a python dataframe containing 
entitlementName, targetSystem, description, riskLevel, priviledgedAccess and entitlementType.
I want to create a list of dictionaries as below

Prepare a list of dictionaries for UNWIND to use in cypher:
    entitlement_list = [
        {
            "entitlementName": row["entitlementName"],
            "targetSystem": row["targetSystem"]
        }
    ]