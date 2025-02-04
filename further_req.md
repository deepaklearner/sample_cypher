1.
I am told to write a csv report to a sql table as well for .7 million rows using python.
I already have code to write the data from pandas df to csv.

<<<<<<< HEAD
How should i plan? Should i delete everything and write fresh in batches?

2.
I am confused for this requirement to code in python """Create a delta job -
Delta job changes only the records with the changes (i.e. change in modified date for a User node in neo4j data) in table glide.iamidssupervisorhierarchy and glide.iamidsidentities.
Based on Last modified date of a User node. i.e. last 30 min, (current date - last modified date), if delta is greater than 30 min i.e. (we are ignoring last 30 min changes). Get those records to build the hierachy (i.e. run populate_supervisor_hierarchy.sh ?) then run generate_supervisor_hierarchy_report.sh to update table glide.iamidssupervisorhierarchy and glide iamidsidentities.
Full job, will run weekly once.
Write the report to table glide.amidssupervisorhierarchy in dev along with cs file. i.e. a full refresh (remove all records and write all data?).
Update table glide iamidsidentities. Find the user id (resourceid), and update only those records"""
=======
Connect to the MySQL database using pymysql.connect
How should i plan? Should i delete everything and write fresh in batches?

2.
i have so many columns and most of them are same the column name in pandas dataframe except 2 of them

3.
there is one column which is ManagerLevel in datafarme and level in table
>>>>>>> 17e0e4eb4529f9a32dc8a129c00d4a3ee050a981
