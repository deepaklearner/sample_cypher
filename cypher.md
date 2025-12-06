UNWIND $owners AS owner

// Step 1: Try employeeNumber
CALL {
    WITH owner
    OPTIONAL MATCH (u1:User { employeeNumber: owner })
    RETURN u1
}

// Step 2: Try aetnaresourceid only if u1 did NOT match
CALL {
    WITH owner, u1
    OPTIONAL MATCH (u2:User { aetnaresourceid: owner })
    WHERE u1 IS NULL
    RETURN u2
}

// Final fallback: use whichever matched
WITH owner, u1, u2, coalesce(u1, u2) AS u

RETURN owner AS EntitlementOwner,
       CASE 
         WHEN u IS NULL THEN 'Missing in Neo4J'
         WHEN NOT u:Active THEN 'Inactive in Neo4J'
         ELSE 'OK'
       END AS Status;
