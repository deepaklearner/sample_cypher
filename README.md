I have a pandas dataframe df with many columns, one of the field is managerid. This df is created from a txt file.

I have a User node in neo4j db with property employeeNumber and managerid.
There is a 

write a cypher query to validate for every record in dataframe df, if the managerid exists in neo4j db then include it else exclude the record.

I already have a code:
df = df[~(df['START_DATE']=='DNE')&
         ~(df['END_DATE']=='DNE')
]
