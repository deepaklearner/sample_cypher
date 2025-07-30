1.1 I am loading data to neo4j in various nodes via  python etl process.
I have user node and various other nodes which are connected to user node.
in case any change is made to user node, I am adding a property usr.is_updated='Y'
And at end of the pipeline I am removing it after taking the count for tracking purpose.

But because my multiple stages are running in parallel, its giving me lock error. 
What solutions do we have here for this problem?

Solutions:
1. CREATE (u)-[:TOUCHED_AT]->(:UserTouch {timestamp: timestamp()})
2.  Retry on failure with exponential backoff
3.  Defer updates to a single-threaded batch


MATCH (u:User {id: $id})
CREATE (u)-[:TOUCHED_AT]->(:UserTouch {timestamp: timestamp()})

MATCH (u:User)-[r:TOUCHED_AT]->(touch:UserTouch)
DELETE r, touch
