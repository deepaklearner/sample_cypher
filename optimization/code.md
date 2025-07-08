OPTIONAL MATCH (user:NewHire)-[rel:NEWHIRE]->(label:UserLabel)
WHERE rel.validFrom < datetime() - duration({hours: stream['new_hire_label_retention_hours']})

OPTIONAL MATCH (user_transfer:Transfer)-[rel_transfer:TRANSFER]->(label_transfer:UserLabel)
WHERE rel_transfer.validFrom < datetime() - duration({hours: stream['transfer_label_retention_hours']})

OPTIONAL MATCH (user_conversion:Conversion)-[rel_conversion:CONVERSION]->(label_conversion:UserLabel)
WHERE rel_conversion.validFrom < datetime() - duration({hours: stream['conversion_label_retention_hours']})

OPTIONAL MATCH (user_rehire:ReHire)-[rel_rehire:REHIRE]->(label_rehire:UserLabel)
WHERE rel_rehire.validFrom < datetime() - duration({hours: stream['rehire_label_retention_hours']})

DELETE rel, rel_transfer, rel_rehire, rel_conversion

REMOVE user:NewHire
REMOVE user_transfer:Transfer
REMOVE user_conversion:Conversion
REMOVE user_rehire:ReHire

RETURN count(*) AS total
