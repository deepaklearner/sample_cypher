python -m venv venv
source /Users/ankitarani/VSCodeProjects/sample_cypher/venv/bin/activate


1.1 i have some python code... i need to generate dummy dataframe with flexible rows and columns... please give me the code.. also something like timeit to check the avg duration for one iteration

2.1 I am fetching 6 columns namely
entitle_name, entitle_source, entitle_desc, risk_rating, priv, resource_type from mysql.
Then using the keys (entitle_name, entitle_source) fetching same data from neo4j.

Then comparing both to find the new data added in mysql db and also the data which got modified (any of the entitle_desc, risk_rating, priv, resource_type) columns.
Tell me how to do this using pandas dataframe in an optimized manner. I have lot of data, so i want to optimize my code.

i dont want data type category for entitle_name and description