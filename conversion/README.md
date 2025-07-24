1.1 I want below cypher to return labels as # separated instead of list

UNWIND $empids as emp_id
MATCH (u:User {employeeNumber: empid})
RETURN u.employeeNumber AS employeeNumber, labels(u) AS labels