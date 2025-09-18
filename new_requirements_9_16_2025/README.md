1. Entitlement master thable has both entitlement and owner information. Also load risk rating etc
2. Owner information, we are going to maintain history of it.

NOTE:
1. Ensure whenever you are using any MERGE statement, it should not fail due to constraint violation.
Best practice is MERGE and in same line mention the key values name. Domnt add any sub properties in the same line.

We wont make use of id because at some point we will change the source from mysql to AD.

2. How to takle when our job fails. How to restart from that point, it has processed the data?
    Find distinct source - There are 11905
    
a. First we will do the primary ones, we will import the Entitlements for each domain and make a separate stage for each:
    'ABC1', 'ABC2', 'ABC3','ABC4','ABC5', 'ABC6'
    Put in feature config and put them in primary domains and run through each stage.

 For example if you are running AETH, then only for AETH
 And then move onto next domain.
 Iterate for each domain

b. Then do a distinct on entitle_source: which comes close to 63k.
Get the list by running the query:
    SELECT distinct entitle_source from entitlement_master
    where entitle_source NOT in ('ABC1', 'ABC2', 'ABC3','ABC4','ABC5', 'ABC6') 
    order by 1 asc;

    Filter primary domains from this list

    Then go for like first 1000 entitlement source.

    Then process the next 1000

    Make it like 20 batches..

    63657/20 = 3200 

    batch size is 3200 domains





