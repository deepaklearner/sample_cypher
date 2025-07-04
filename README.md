1.1 I have a unix script which is calling a python script.
I am getting permission denied for a particular file date_time.yaml which is used as a temporary data
placeholder.

how to debug this issue?

How to check the user which is trying to access the file?

i checked in file system, owner is srv_s025010 and group neo4jadm
owner has R, W, X access
Group has R, X access 



1. 

df[i]= np.apply_along_axis(priority_cols, axis=1, arr=df[x].values)

I have a data like "deepak@gmail.com" this is getting cropped 


2.1 I have a node Name in neo4j. The property computedformattedName is UNIQUE is the constraints.
I have also a User node. with key as employeeNumber.

I am getting constraint error saying, Node already exist with label Name and property formattedName



"""UNWIND $rows AS row
OPTIONAL MATCH (usr:User {employeeNumber: row.CVSResourceid}) 
              -[r_has:HAS_ATTRIBUTE]-> (tgtNode:Name)
SET tgtNode.formattedName       = row.fullnameformatted,
    tgtNode.givenName           = row.givenName,
    tgtNode.middleName          = row.middleName,
    tgtNode.familyName          = row.familyName,
    tgtNode.honorificPrefix     = row.honorificPrefix,
    tgtNode.honorificSuffix     = row.honorificSuffix
REMOVE tgtNode.isTempProperty

WITH row, r_has,
     CASE 
         WHEN (row.concat_attr_Name <> tgtNode.computedformattedName OR tgtNode IS NULL) 
         THEN true 
         ELSE false 
     END AS codesDiffer
WHERE codesDiffer
DELETE r_has

WITH row
WHERE row.isName
MATCH (user_row:User {employeeNumber: row.CVSResourceid})
SET user_row.is_updated = 'Y'

MERGE (Name_node:Name {
    computedformattedName: row.concat_attr_Name
})
SET Name_node.formattedName   = row.fullnameformatted,
    Name_node.givenName       = row.givenName,
    Name_node.middleName      = row.middleName,
    Name_node.familyName      = row.familyName,
    Name_node.honorificPrefix = row.honorificPrefix,
    Name_node.honorificSuffix = row.honorificSuffix
MERGE (user_row)-[:HAS_ATTRIBUTE]->(Name_node)
REMOVE Name_node.isTempProperty

RETURN COUNT(*) AS total
"""

2.2 give me full cypher