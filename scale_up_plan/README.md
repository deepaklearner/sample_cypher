Project overview:
"""
I have two tables: 
a. entitlement_master (key: entitle_name and platform)
b. eservice_data (key: entitle_name and entitle_source) and 
c. entitlement_user: contains entitle_name and platform and employeeNumber

entitlement_master has 8.8 million rows
eservice_data has 213k rows
entitlement_user has 40 million rows

entitle_source and platform are same data.

I am reading data from entitlement_master in batches and then using keys searching them in eservice_data and then loading the data in neo4j."""

In my project, i am using Pandas.

1.1 Considering the huge size of entitlement_master. I want to plan a suitable robust etl process. Please help me with ideas.