solution2: can we rename dne_mask as reject_condition.
solution3: rename column rejection_reason as FailureReason and
also, include the manager email from neo4j. We have a WorkEmail node having property email which is having below relationship with User node.
I want the manager email only for invalid records having DNE not for the valid records.
Do this using a single cypher query.