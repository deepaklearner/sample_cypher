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
is " pd.DataFrame([record.data() for record in result])" and 
"pd.DataFrame(data=[dict(record) for record in result.data()])" same?

1.3
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

1.4 I want to create some Entitlement nodes in neo4j and relationship with User node manually

1.5 I want to create a set of dictionaries and then subtract to find the missing pair of 
entitlementName and targetSystem from Neo4j.
 
2.1 I am fetching data from mysql db (source) using below sql query and also from neo4j (destination) using cypher. I want to find the new entitlements for key entitlementName and targetSystem in mysql db,
and also the updated entitlements for existing ones in neo4j using python.

SELECT
    entitle_name AS entitlementName,
    entitle_source AS targetSystem,
    entitle_desc AS description,
    risk_rating AS riskLevel,
    priv AS privilegedAccess,
    resource_type AS entitlementType,
    CONCAT(entitle_name, '|', entitle_source) AS concat_attr_entitlements1,
    CONCAT(
        entitle_name, '|',
        entitle_source, '|',
        COALESCE(entitle_desc, 'DNE'), '|',
        COALESCE(risk_rating, 'DNE'), '|',
        COALESCE(priv, 'DNE'), '|',
        COALESCE(resource_type, 'DNE')
    ) AS concat_attr_entitlements2
FROM edwmaster.entitlement_master
WHERE entitle_name LIKE 'APP_CTX%';


cypher:
UNWIND $entitlements AS ent
MATCH (e:Entitlement {
    entitlementName: ent.entitlementName,
    targetSystem: ent.targetSystem
})
OPTIONAL MATCH (e)-[:OWNER]->(u:User)
RETURN
    e.entitlementName AS entitlementName,
    e.targetSystem AS targetSystem,
    e.description AS description,
    e.riskLevel AS riskLevel,
    e.priviledgedAccess AS priviledgedAccess,
    e.entitlementType AS entitlementType,
    e.entitlementName + '|' + e.targetSystem AS concat_attr_entitlements1,
    e.entitlementName + '|' + e.targetSystem + '|' +
        coalesce(e.description, 'DNE') + '|' +
        coalesce(e.riskLevel, 'DNE') + '|' +
        coalesce(e.priviledgedAccess, 'DNE') + '|' +
        coalesce(e.entitlementType, 'DNE') AS concat_attr_entitlements2,
    collect(u.employeeNumber) AS owners;

