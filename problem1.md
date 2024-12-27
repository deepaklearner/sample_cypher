There is a User node in which, we have properties employeeNumber, managerid.
If manager id contains id starting with A example A001, then i need to do a lookup.

Lookup logic is:
Search for another User node where aetnaresourceid is matching with the manager if A001, then lookup another property employeeNumber for that node.

update the obtained employeeNumber in managerid of 1st User node.

Solution1:
MATCH (u:User) 
WHERE u.managerid STARTS WITH 'A'  // Identify the User nodes where managerid starts with 'A'
MATCH (m:User) 
WHERE m.aetnaresourceid = u.managerid // Look for the User node where aetnaresourceid matches the managerid
SET u.managerid = m.employeeNumber  // Update the managerid with the employeeNumber of the found User node
RETURN u.employeeNumber, u.managerid // Return the updated node


Accomodate this logic in below cypher before MATCH SET
"""UNWIND $rows AS row
WITH row
MATCH (globalid:GlobalidentifierCounter)
OPTIONAL MATCH (hrhub_identifier:CVSIdentifier {networkid: row.CVSResourceid})
MERGE (apn:ApplicationAccount {applicationAccountName: row.applicationAccount, targetSystem: 'Neo4j'})
ON CREATE SET 
    apn.applicationAccountId = apoc.create.uuid()

MERGE (usr:User {employeeNumber: row.CVSResourceid})
ON CREATE SET 
    usr.userProfileID = apoc.create.uuid(),
    usr.acquisitionCode = row.AcquisitionCode,
    usr.globalID = toString(toInteger(globalid.lastAssignedCouterValue) + 1),
    usr.eligibilityCode = row.EligibilityCode,
    usr.is_entered = 'Y',
    usr.managerid = row.ManagerId,
    usr.transactionType = row.TransactionType,
    usr.transactionCode = row.TransactionCode,
    usr.aetnaresourceid = row.aetnaNetworkID,
    globalid.lastexecutionDate = localdatetime(),
    globalid.lastAssignedCouterValue = toString(toInteger(globalid.lastAssignedCouterValue) + 1)
ON MATCH SET 
    usr.acquisitionCode = row.AcquisitionCode,
    usr.eligibilityCode = row.EligibilityCode,
    usr.is_updated = 'Y',
    usr.managerid = row.ManagerId,
    usr.transactionType = row.TransactionType,
    usr.transactionCode = row.TransactionCode,
    usr.aetnaresourceid = row.aetnaNetworkID

"""

full solution 1:

UNWIND $rows AS row
WITH row
MATCH (globalid:GlobalidentifierCounter)
OPTIONAL MATCH (hrhub_identifier:CVSIdentifier {networkid: row.CVSResourceid})

MERGE (apn:ApplicationAccount {applicationAccountName: row.applicationAccount, targetSystem: 'Neo4j'})
ON CREATE SET 
    apn.applicationAccountId = apoc.create.uuid()

// If ManagerId starts with "A", lookup the corresponding User node by aetnaresourceid
WITH row, globalid, hrhub_identifier
OPTIONAL MATCH (mgr:User {aetnaresourceid: row.ManagerId})
WITH row, globalid, hrhub_identifier, mgr

// Create or merge the User node and set the properties
MERGE (usr:User {employeeNumber: row.CVSResourceid})
ON CREATE SET 
    usr.userProfileID = apoc.create.uuid(),
    usr.acquisitionCode = row.AcquisitionCode,
    usr.globalID = toString(toInteger(globalid.lastAssignedCouterValue) + 1),
    usr.eligibilityCode = row.EligibilityCode,
    usr.is_entered = 'Y',
    // Set managerid to the employeeNumber of the matched manager node if found
    usr.managerid = CASE WHEN mgr IS NOT NULL THEN mgr.employeeNumber ELSE row.ManagerId END,
    usr.transactionType = row.TransactionType,
    usr.transactionCode = row.TransactionCode,
    usr.aetnaresourceid = row.aetnaNetworkID,
    globalid.lastexecutionDate = localdatetime(),
    globalid.lastAssignedCouterValue = toString(toInteger(globalid.lastAssignedCouterValue) + 1)

ON MATCH SET 
    usr.acquisitionCode = row.AcquisitionCode,
    usr.eligibilityCode = row.EligibilityCode,
    usr.is_updated = 'Y',
    usr.managerid = row.ManagerId,
    usr.transactionType = row.TransactionType,
    usr.transactionCode = row.TransactionCode,
    usr.aetnaresourceid = row.aetnaNetworkID



