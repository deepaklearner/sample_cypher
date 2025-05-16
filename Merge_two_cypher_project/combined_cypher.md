Here is a **combined Cypher query** that merges the logic from both the `aetna_nw_identifier_query` and the `conversion_identifier_query` into **one unified query**, while maintaining their distinct conditional logic paths for:

* Regular users flagged with `Aetnaldentifier_flag = "y"`
* Conversion users with `is_conversion = 'Y'` and `Conversion` label

---

### ✅ **Unified Cypher Query**

```cypher
UNWIND $rows AS row
WITH row,
     row.Aetnaldentifier_flag = 'y' AS isAetnaFlagged,
     row.is_conversion = 'Y' AS isConversion

// Filter users
MATCH (usr:User {employeeNumber: row.CVSResourceid})

// Partition: Aetna users or Conversion users
WITH row, usr, isAetnaFlagged, isConversion
WHERE isAetnaFlagged OR (isConversion AND 'Conversion' IN labels(usr))

WITH COLLECT(usr) AS users, row, isAetnaFlagged, isConversion

// Fetch available AetnaNetworkIdentifier nodes not yet linked
MATCH (aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_nw_identifier)--()

WITH users, COLLECT(aetna_nw_identifier) AS identifiers, isAetnaFlagged, isConversion

UNWIND apoc.coll.zip(users, identifiers) AS pair
WITH 
    pair[0] AS u,
    pair[1] AS aetna_nw_identifier,
    isAetnaFlagged, isConversion,
    CASE 
        WHEN 'Employee' IN labels(pair[0]) THEN 'A'
        WHEN 'Contractor' IN labels(pair[0]) THEN 'N'
        ELSE 'DNE'
    END AS prefix

// Shared: set networkid format
SET aetna_nw_identifier.networkid = prefix + aetna_nw_identifier.uid

// Conversion-specific processing
CALL apoc.do.when(
    isConversion,
    '
    OPTIONAL MATCH (u)-[has_identifier_info:HAS_ATTRIBUTE]->(identifier_info:AetnaNetworkIdentifierInfo)
    OPTIONAL MATCH (identifier_info)-[r_curr:CURRENT]-(curr_aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
    OPTIONAL MATCH (identifier_info)-[r_has_aetna_id:HAS_AETNA_ID]-(curr_aetna_nw_identifier)
    
    WITH 
        u, aetna_nw_identifier, prefix, identifier_info, curr_aetna_nw_identifier, 
        COLLECT(r_has_aetna_id) AS rels_has_aetna_id, has_identifier_info, r_curr

    WITH *,
        CASE 
            WHEN curr_aetna_nw_identifier IS NULL 
                 OR (prefix + aetna_nw_identifier.uid) <> curr_aetna_nw_identifier.networkid 
                 THEN true 
            ELSE false 
        END AS codesDiffer

    WHERE codesDiffer

    CALL apoc.refactor.rename.type("HAS_AETNA_ID", "HAD_AETNA_ID", rels_has_aetna_id)
    YIELD committedOperations

    CREATE (new_identifier_info:AetnaNetworkIdentifierInfo {
        eventID: toString(u.employeeNumber) + (prefix + aetna_nw_identifier.uid) + "." + toString(datetime()),
        date: datetime()
    })

    MERGE (u)-[:HAS_ATTRIBUTE]->(new_identifier_info)
    MERGE (new_identifier_info)-[new_r_has_aetna_id:HAS_AETNA_ID]->(aetna_nw_identifier)
    SET 
        new_r_has_aetna_id.assigned_date = datetime(),
        new_r_has_aetna_id.assignedBy = "INT5043"

    MERGE (new_identifier_info)-[:CURRENT]->(aetna_nw_identifier)

    FOREACH (_ IN CASE WHEN identifier_info IS NOT NULL THEN [1] ELSE [] END |
        MERGE (new_identifier_info)-[:PREVIOUS]->(identifier_info)
    )

    SET 
        u.legacyaetnaresourceid = u.aetnaresourceid,
        u.aetnaresourceid = prefix + aetna_nw_identifier.uid,
        u.is_updated = "y"

    FOREACH (x IN CASE WHEN u.cvsnetworkid IS NULL OR u.cvsnetworkid = curr_aetna_nw_identifier.networkid THEN [1] ELSE [] END |
        SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
    )

    DELETE has_identifier_info, r_curr
    REMOVE curr_aetna_nw_identifier.networkid
    RETURN count(*) AS count
    ',
    '',
    {u: u, aetna_nw_identifier: aetna_nw_identifier, prefix: prefix}
) YIELD value

// Aetna flag-specific processing
CALL apoc.do.when(
    isAetnaFlagged AND NOT isConversion,
    '
    CREATE (new_identifier_info:AetnaNetworkIdentifierInfo {
        eventID: toString(u.employeeNumber) + (prefix + aetna_nw_identifier.uid) + "." + toString(datetime()),
        date: datetime()
    })

    MERGE (u)-[:HAS_ATTRIBUTE]->(new_identifier_info)
    MERGE (new_identifier_info)-[new_r_has_aetna_id:HAS_AETNA_ID]->(aetna_nw_identifier)
    SET 
        new_r_has_aetna_id.assigned_date = datetime(),
        new_r_has_aetna_id.assignedBy = "INT5043"

    MERGE (new_identifier_info)-[:CURRENT]->(aetna_nw_identifier)

    SET 
        u.aetnaresourceid = prefix + aetna_nw_identifier.uid,
        u.is_updated = "y"

    FOREACH (x IN CASE WHEN u.cvsnetworkid IS NULL THEN [1] ELSE [] END |
        SET u.cvsnetworkid = prefix + aetna_nw_identifier.uid
    )
    RETURN count(*) AS count
    ',
    '',
    {u: u, aetna_nw_identifier: aetna_nw_identifier, prefix: prefix}
) YIELD value

RETURN count(*) AS total
```

---

### 🔍 Key Notes:

* Uses `apoc.do.when()` to conditionally execute logic depending on user type (`Conversion` vs regular).
* Ensures consistent assignment of `networkid` using the correct prefix (`A` or `N`).
* Protects logic for:

  * Reuse of existing `AetnaNetworkIdentifierInfo`
  * Proper relationship replacement and cleanup
* `RETURN count(*)` at the end summarizes total updates.

Let me know if you want this split into reusable procedures or need performance optimization tips.
