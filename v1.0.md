v0 

Modify the cypher to run in batch mode Using call apoc.perodic.iterate

"""
OPTIONAL MATCH (user:NewHire)-[rel:NEWHIRE]->(label:UserLabel) 
WHERE rel.validFrom < datetime() - duration({hours: new_hire_label_retention_hours})

OPTIONAL MATCH (user_transfer:Transfer)-[rel_transfer:TRANSFER]->(label_transfer:UserLabel) 
WHERE rel_transfer.validFrom < datetime() - duration({hours: transfer_label_retention_hours})

OPTIONAL MATCH (user_conversion:Conversion)-[rel_conversion:CONVERSION]->(label_conversion:UserLabel) 
WHERE rel_conversion.validFrom < datetime() - duration({hours: conversion_label_retention_hours})

OPTIONAL MATCH (user_rehire:ReHire)-[rel_rehire:REHIRE]->(label_rehire:UserLabel) 
WHERE rel_rehire.validFrom < datetime() - duration({hours: rehire_label_retention_hours})

DELETE rel, rel_transfer, rel_conversion, rel_rehire
REMOVE user:NewHire
REMOVE user_transfer:Transfer
REMOVE user_conversion:Conversion
REMOVE user_rehire:ReHire

RETURN count(*) AS total"""


Solution 1:
CALL apoc.periodic.iterate(
    "
    OPTIONAL MATCH (user:NewHire)-[rel:NEWHIRE]->(label:UserLabel)
    WHERE rel.validFrom < datetime() - duration({hours: new_hire_label_retention_hours})
    
    OPTIONAL MATCH (user_transfer:Transfer)-[rel_transfer:TRANSFER]->(label_transfer:UserLabel)
    WHERE rel_transfer.validFrom < datetime() - duration({hours: transfer_label_retention_hours})
    
    OPTIONAL MATCH (user_conversion:Conversion)-[rel_conversion:CONVERSION]->(label_conversion:UserLabel)
    WHERE rel_conversion.validFrom < datetime() - duration({hours: conversion_label_retention_hours})
    
    OPTIONAL MATCH (user_rehire:ReHire)-[rel_rehire:REHIRE]->(label_rehire:UserLabel)
    WHERE rel_rehire.validFrom < datetime() - duration({hours: rehire_label_retention_hours})
    
    RETURN user, rel, user_transfer, rel_transfer, user_conversion, rel_conversion, user_rehire, rel_rehire
    ",
    "
    DELETE rel, rel_transfer, rel_conversion, rel_rehire
    REMOVE user:NewHire
    REMOVE user_transfer:Transfer
    REMOVE user_conversion:Conversion
    REMOVE user_rehire:ReHire
    ",
    {batchSize: 1000, parallel: true}
)
YIELD batches, total, timeTaken
RETURN batches, total, timeTaken


Solution 2:

WITH 0 AS batch
FOREACH (i IN RANGE(0, 1000) |
    OPTIONAL MATCH (user:NewHire)-[rel:NEWHIRE]->(label:UserLabel)
    WHERE rel.validFrom < datetime() - duration({hours: new_hire_label_retention_hours})
    WITH COLLECT(rel) AS rels_to_delete, COUNT(rel) AS cnt
    WHERE cnt > 0
    OPTIONAL MATCH (user_transfer:Transfer)-[rel_transfer:TRANSFER]->(label_transfer:UserLabel)
    WHERE rel_transfer.validFrom < datetime() - duration({hours: transfer_label_retention_hours})
    WITH rels_to_delete + COLLECT(rel_transfer) AS rels_to_delete, cnt
    OPTIONAL MATCH (user_conversion:Conversion)-[rel_conversion:CONVERSION]->(label_conversion:UserLabel)
    WHERE rel_conversion.validFrom < datetime() - duration({hours: conversion_label_retention_hours})
    WITH rels_to_delete + COLLECT(rel_conversion) AS rels_to_delete, cnt
    OPTIONAL MATCH (user_rehire:ReHire)-[rel_rehire:REHIRE]->(label_rehire:UserLabel)
    WHERE rel_rehire.validFrom < datetime() - duration({hours: rehire_label_retention_hours})
    WITH rels_to_delete + COLLECT(rel_rehire) AS rels_to_delete, cnt
    // Limit the number of relationships to delete in this batch
    LIMIT 1000
    FOREACH (rel IN rels_to_delete |
        DELETE rel
    )
)
RETURN count(*) AS total
