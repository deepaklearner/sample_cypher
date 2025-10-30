python -m venv venv
source /Users/ankitarani/VSCodeProjects/sample_cypher/venv/bin/activate


1.1 i have some python code... i need to generate dummy dataframe with flexible rows and columns... please give me the code.. also something like timeit to check the avg duration for one iteration

2.1 I am fetching 6 columns namely
entitle_name, entitle_source, entitle_desc, risk_rating, priv, resource_type from mysql.
Then using the keys (entitle_name, entitle_source) fetching same data from neo4j.

Then comparing both to find the new data added in mysql db and also the data which got modified (any of the entitle_desc, risk_rating, priv, resource_type) columns.
Tell me how to do this using pandas dataframe in an optimized manner. I have lot of data, so i want to optimize my code.

i dont want data type category for entitle_name and description

3.1
I am fetching below columns namely:
entitlementName, targetSystem, owner1, owner2, owner3 from mysql edw database.

Then using the keys (targetSystem, entitlementName) fetching same data from neo4j.

Then comparing both to find the new and removed owners.
Then update the data in neo4j accordingly. If the data is not present in neo4j, write a report for missing owners in neo4j and inactive owners in neo4j.
Tell me how to do this using pandas dataframe in an optimized manner. I have lot of data, so i want to optimize my code.

What if i do like this:
a. Read all the entitlements from neo4j (approx 11 Million) only columns entitlementName and targetSystem
b. Then in batch fetching the data for the key (targetSystem, entitlementName) from edw and neo4j with owner information
c. Then compare to find new owners, missing owners in neo4j and inactive owners in neo4j.
d. Create or update relationship in neo4j between User node and Entitlement node based on owner 

is this approach not good?

Are you telling:
a. Read the entitlements from edw entitlementName, targetSystem, owner1, owner2, owner3 from mysql edw database (in batch)
b. Then read the same data from neo4j
c. Then compare to find new owners, missing owners in neo4j and inactive owners in neo4j.
d. Create or update relationship in neo4j between User node and Entitlement node based on owner 

To fetch the data from edw in batch, will below query be fine or should we avoid group by:
SELECT entitlementName, targetSystem
    MAX(CASE WHEN `rank`=1 THEN E_EmployeeID END) AS owner1,
    MAX(CASE WHEN `rank`=2 THEN E_EmployeeID END) AS owner2,
    MAX(CASE WHEN `rank`=3 THEN E_EmployeeID END) AS owner3,
    FROM arrpum.eservice_data
    GROUP BY entitlementName, targetSystem
    LIMIT {chunksize} OFFSET {offset}

i dont want to use id as later we will be migrating to some other db

3.2 I have two dataframes one from mysql db and other from neo4j.
I want to compare the owners from both data sources. Sourch of trugh is edw.
And accordingly create relationship or remove relationship in neo4j.

SELECT entitlementName, targetSystem
    MAX(CASE WHEN `rank`=1 THEN E_EmployeeID END) AS owner1,
    MAX(CASE WHEN `rank`=2 THEN E_EmployeeID END) AS owner2,
    MAX(CASE WHEN `rank`=3 THEN E_EmployeeID END) AS owner3,
    FROM arrpum.eservice_data
    GROUP BY entitlementName, targetSystem
    LIMIT {chunksize} OFFSET {offset}

and other from:
UNWIND $entitlements as ent
MATCH (e:Entitlement {entitlementName: ent.entitlementName, targetSystem: ent.targetSystem})
OPTIONAL MATCH(e)-[:HAS_OWNER]->(u:User)
RETURN 
    e.entitlementName AS entitlementName,
    e.targetSystem AS targetSystem,
    COLLECT(DISTINCT u.employeeNumber) AS neo4jOwners

4.1
