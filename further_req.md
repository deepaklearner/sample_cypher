1.0.
I am told to write a csv report to a sql table as well for .7 million rows using python.
I already have code to write the data from pandas df to csv.

Connect to the MySQL database using pymysql.connect
How should i plan? Should i delete everything and write fresh in batches?

1.1.
i have so many columns and most of them are same the column name in pandas dataframe except 2 of them

1.2.
there is one column which is ManagerLevel in datafarme and level in table
How should i plan? Should i delete everything and write fresh in batches?

2.
Requirement to code in python """

Update table glide.iamidsidentities in mysql db. Find the record based on primary key user id (resourceid), and update only those records and only columns that i have in my dataframe. Leave the other columns as it is with no change in data.
"""
2.1 i have huge data .7 million
2.2 can we avoid iterrows
3. If the resourceid is present in df but not present in iamidsidentities. print those resourceid in form of a list in the log for the batch.
3.1 Give me full code


