1. Entitlement master thable has both entitlement and owner information. Also load risk rating etc
2. Owner information, we are going to maintain history of it.

NOTE:
1. Ensure whenever you are using any MERGE statement, it should not fail due to constraint violation.
Best practice is MERGE and in same line mention the key values name. Domnt add any sub properties in the same line.

We wont make use of id because at some point we will change the source from mysql to AD.

2. How to takle when our job fails. How to restart from that point, it has processed the data?
    Find distinct source - There are 11905
    
a. First we will do the primary ones, we will import the Entitlements for each domain and make a separate stage for each:
    'ABC1', 'ABC2', 'ABC3','ABC4','ABC5', 'ABC5'





