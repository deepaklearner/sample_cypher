1.1 combine these two cypher queries into a single cypher query 
1.2 can we further simplify and make it easy to read
1.3 i want to use order by for aetna_nw_identifier
1.4 repeat MATCH (aetna_nw_identifier:AetnaNetworkIdentifier:NetworkIdentifier)
WHERE NOT (aetna_nw_identifier)--() logic

1.5
I want to add here """    WITH *,
        CASE 
            WHEN curr_aetna_nw_identifier IS NULL 
                 OR (prefix + aetna_nw_identifier.uid) <> curr_aetna_nw_identifier.networkid 
                 THEN true 
            ELSE false 
        END AS codesDiffer"""" WHEN curr_aetna_nw_identifier IS NULL AND isAetnaFlagged is True

1.5 In below cypher,
instead of 
"""CALL apoc.do.when(
    isConversion,""" can we use """row.is_conversion = 'Y'"""