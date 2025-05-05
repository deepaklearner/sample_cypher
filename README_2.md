3.1 I have a table entitlement_master, in which the key are: entitle_name and entitle_source columns.
I have another table eservice_data, in which primary key are entitle_name and platform ( entitle_source as in other table).

Read the data for entitle_name and entitle_source from entitlement_master.
Look up in eservice_data for entitle_name=entitle_name and platform=entitle_source for different rows.
You may find mutiple rows with different rank like 1, 2, 3.

In the new table, create new columns owner1 for rank=1, owner2 for rank=2, owner3 for rank=3 

3.2. How to improve efficienvy

3.3 My table entitlement_master is huge and i need to read in batches. How should we do then?
data in master table 8.8 million

3.4 can we do something in below join query only.. to return pivot reult
"""em_batch.merge(ed_df, on=['entitle_name', 'entitle_source'], how='left')"""