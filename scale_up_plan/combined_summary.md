1.1
Process data in batches (with recovery support - re-runnable code)
Perform joins/lookups efficiently

### Efficient Lookup in eservice_data:
Load eservice_data once in memory if possible (213K rows is small)

How to do "Track progress in a checkpoint file or metadata table (for resumability)"?

### Logging & Checkpointing:
Log stats: batch size, matched users, missing eservice rows
Save last_processed_id to disk/DB for restart.

what is "last_processed_id" here?

### Optimization Tips:
Parallelize batch processing using threads or multiprocessing (limit based on I/O or Neo4j throughput)
Deduplicate data before loading into Neo4j
Retry logic for transient Neo4j errors
Neo4j Indexing: Ensure index on entitle_name, platform, employeeNumber
Enable transaction batching in Neo4j (don't send one Cypher query at a time)

1.2
Use id instead of offset and limit if your db is huge.

Main logics:
1. Retry mechanism
2. Rerunnablity with resume mechanism
3. Using id instead of offset and limit
4. Using multiprocessing