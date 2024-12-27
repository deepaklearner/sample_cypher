"""CALL apoc.periodic.iterate(
    "
    MATCH (n:User)
    WHERE n.managerid IS NOT NULL 
      AND ('Employee' IN labels(n) OR 'Contractors' IN labels(n))
    RETURN n
    ",
    "
    // Delete mismatching managerid relationships
    OPTIONAL MATCH (n)-[r:REPORTS_TO]->(m:User)
    WHERE 
        (NOT TOUPPER(n.managerid) STARTS WITH 'A' AND n.managerid <> m.employeeNumber)
        OR (TOUPPER(n.managerid) STARTS WITH 'A' AND n.managerid <> m.aetnaresourceid)
    DELETE r

    // Determining managerid type
    WITH n,
         CASE 
            WHEN TOUPPER(n.managerid) STARTS WITH 'A' THEN 'aetna'
            ELSE 'other'
         END AS managerid_type

    // Match appropriate manager nodes using CASE
    OPTIONAL MATCH (m:User)
    WHERE
        CASE managerid_type
            WHEN 'other' THEN m.employeeNumber = n.managerid
            WHEN 'aetna' THEN m.aetnaresourceid = n.managerid
        END

    // Creating correct managerid relationships
    FOREACH (_ IN CASE WHEN m IS NOT NULL THEN [1] ELSE [] END |
        MERGE (n)-[:REPORTS_TO]->(m)
    )
    ",
    {batchSize: batch_size, parallel: false}
);
"""