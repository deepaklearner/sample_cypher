You can combine both `aetna_nw_identifier_query` and `conversion_identifier_query` into a single Cypher query by handling their respective conditions (`row.Aetnaldentifier_flag = "y"` and `row.is_conversion = 'Y' AND 'Conversion' IN labels(usr)`) in a unified `UNWIND` loop and using `CASE` clauses or conditional `FOREACH` blocks to separate their logic. Here's the combined query:

```cypher
UNWIND $rows AS row

// Fetch users who match either AetnaIdentifier or Conversion conditions
MATCH (usr:User {employeeNumber: row.CVSResourceid})
WHERE 
    (row.Aetnaldentifier_flag = "y" AND NOT (usr)-[:HAS_ATTRIBUTE]->(:AetnaNetworkIdentifierInfo)) 
    OR 
    (row.is_conversion = 'Y' AND 'Conversion' IN labels(usr))

WITH row, usr
ORDER BY usr.employeeNumber

// Get available Aetna identifiers
MATCH (aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_nw_identifier)--()

WITH COLLECT(DISTINCT usr) AS usr_array, COLLECT(DISTINCT aetna_nw_identifier) AS id_array
UNWIND apoc.coll.zip(usr_array, id_array) AS row_pair

WITH 
    row_pair[0] AS u,
    row_pair[1] AS aetna_nw_identifier,
    CASE 
        WHEN 'Employee' IN labels(row_pair[0]) THEN 'A'
        WHEN 'Contractor' IN labels(row_pair[0]) THEN 'N'
        ELSE 'DNE'
    END AS prefix

// Determine if user is a conversion user
WITH u, aetna_nw_identifier, prefix,
     CASE WHEN 'Conversion' IN labels(u) THEN true ELSE false END AS is_conversion

// ---- Conversion path ----
OPTIONAL MATCH (u)-[has_identifier_info:HAS_ATTRIBUTE]->(identifier_info:AetnaNetworkIdentifierInfo)
OPTIONAL MATCH (identifier_info)-[r_curr:CURRENT]-(curr_aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
OPTIONAL MATCH (identifier_info)-[r_has_aetna_id:HAS_AETNA_ID]-(curr_aetna_nw_identifier)

WITH 
    u, aetna_nw_identifier, prefix, is_conversion,
    identifier_info, curr_aetna_nw_identifier, has_identifier_info,
    COLLECT(r_has_aetna_id) AS rels_has_aetna_id,
    CASE 
        WHEN curr_aetna_nw_identifier IS NULL 
             OR (prefix + aetna_nw_identifier.uid) <> curr_aetna_nw_identifier.networkid 
             THEN true 
        ELSE false 
    END AS codesDiffer

// Conversion-specific logic
FOREACH (_ IN CASE WHEN is_conversion AND codesDiffer THEN [1] ELSE [] END |
    CALL apoc.refactor.rename.type("HAS_AETNA_ID", "HAD_AETNA_ID", rels_has_aetna_id) YIELD committedOperations
)

WITH u, aetna_nw_identifier, prefix, is_conversion, identifier_info, curr_aetna_nw_identifier, has_identifier_info, codesDiffer

SET aetna_nw_identifier.networkid = prefix + aetna_nw_identifier.uid

CREATE (new_identifier_info:AetnaNetworkIdentifierInfo {
    eventID: toString(u.employeeNumber) + prefix + aetna_nw_identifier.uid + '.' + toString(datetime()),
    date: datetime()
})

MERGE (u)-[:HAS_ATTRIBUTE]->(new_identifier_info)
MERGE (new_identifier_info)-[new_r_has_aetna_id:HAS_AETNA_ID]->(aetna_nw_identifier)
SET 
    new_r_has_aetna_id.assigned_date = datetime(),
    new_r_has_aetna_id.assignedBy = 'INT5043'

MERGE (new_identifier_info)-[:CURRENT]->(aetna_nw_identifier)

FOREACH (_ IN CASE WHEN is_conversion AND identifier_info IS NOT NULL THEN [1] ELSE [] END |
    MERGE (new_identifier_info)-[:PREVIOUS]->(identifier_info)
)

SET 
    u.is_updated = 'y',
    u.aetnaresourceid = prefix + aetna_nw_identifier.uid

FOREACH (_ IN CASE WHEN is_conversion THEN [1] ELSE [] END |
    SET u.legacyaetnaresourceid = u.aetnaresourceid
)

FOREACH (_ IN CASE WHEN NOT is_conversion AND u.cvsnetworkid IS NULL THEN [1] ELSE [] END |
    SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
)

FOREACH (_ IN CASE WHEN is_conversion AND (u.cvsnetworkid IS NULL OR u.cvsnetworkid = curr_aetna_nw_identifier.networkid) THEN [1] ELSE [] END |
    SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
)

FOREACH (_ IN CASE WHEN is_conversion AND has_identifier_info IS NOT NULL THEN [1] ELSE [] END |
    DELETE has_identifier_info, r_curr
    REMOVE curr_aetna_nw_identifier.networkid
)

RETURN count(*) AS total
```

### Key Notes:

* The logic paths are determined using `CASE` and `FOREACH` to conditionally apply mutations based on the user's label and flags in the row.
* Shared logic is centralized to avoid duplication (e.g., setting the `networkid`, creating `AetnaNetworkIdentifierInfo`).
* Conversion-specific logic (renaming relationships, linking to previous identifier info, legacy ID tracking) only activates for conversion users.

Let me know if you'd like this modularized for reuse or turned into a script for parameterized execution.
