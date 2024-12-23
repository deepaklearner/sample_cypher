I have a IAM data pipeline which is loading data from HR feed to Neo4J.

There are two accounts for a person, A100 and N100. The account N100 is primary.
If in HR feed, the N100 account is deleted then A100 should become primary and should be detached from Secondary UserAccount node.

But what is happenning is: A100 is connected to primary as well as secondary both UserAccount nodes.

How should i handle it?

Solution 1:
If N100 is deleted, you need to find all the relationships where A100 is currently connected to N100 as either a "primary" or "secondary" account.

1. Identify the Relationship Between A100 and N100:

    If N100 is deleted, you need to find all the relationships where A100 is currently connected to N100 as either a "primary" or "secondary" account.

2. Update the Primary Account:

    If N100 is deleted, make A100 the new primary account. This means you need to update the relationship between A100 and the UserAccount nodes in Neo4j, ensuring A100 is connected to the primary account and not to the secondary anymore.

        MATCH (a:A100)-[r:CONNECTED_TO]->(userAccount:UserAccount)
        WHERE userAccount.accountId = 'N100'
        DELETE r
3. Detach A100 from Secondary UserAccount:
    You need to check if A100 is connected to secondary UserAccount nodes. If it is, you should detach it from those nodes to ensure that A100 is no longer incorrectly linked as a secondary account.

        MATCH (a:A100)-[r:CONNECTED_TO]->(secondaryUserAccount:UserAccount)
        WHERE secondaryUserAccount.accountType = 'secondary'
        DELETE r
4. Create the New Primary Relationship:
    After detaching from N100 and the secondary account, you should establish a relationship where A100 is marked as the primary account.

        MATCH (a:A100), (newPrimary:UserAccount)
        WHERE newPrimary.accountId = 'A100'  // assuming A100 is now primary
        CREATE (a)-[:CONNECTED_TO {role: 'primary'}]->(newPrimary)
5. Final Check:

    Ensure that A100 is no longer connected to the secondary UserAccount node.
    Make sure the new relationships reflect A100 as the primary account and that N100 is properly deleted.

Full cypher:
        // Step 1: Detach A100 from N100 if N100 is deleted
        MATCH (a:A100)-[r:CONNECTED_TO]->(userAccount:UserAccount)
        WHERE userAccount.accountId = 'N100'
        DELETE r;

        // Step 2: Detach A100 from all secondary accounts
        MATCH (a:A100)-[r:CONNECTED_TO]->(secondaryUserAccount:UserAccount)
        WHERE secondaryUserAccount.accountType = 'secondary'
        DELETE r;

        // Step 3: Make A100 the new primary account
        MATCH (a:A100), (newPrimary:UserAccount)
        WHERE newPrimary.accountId = 'A100'
        CREATE (a)-[:CONNECTED_TO {role: 'primary'}]->(newPrimary);
