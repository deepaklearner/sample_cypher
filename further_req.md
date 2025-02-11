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
3.2 glide.iamidsidentities is a huge table having .7 million rows. i dont think "SELECT resourceid FROM glide.iamidsidentities" is a good idea

4. In 1.2 solution, I want to separate the delete data from table logic in a separate function bkp_tbl_n_delete_data. Take backup in table glidesupervisorhierachy_backup. I want to retain the data for 7 days only in backup table. Make use of column CreateTimestamp.

4.1 How to backup .7 million rows.
4.2 when writing data to backup table. also add a new column BackupTimestamp.
The column BackupTimestamp is not present in original table. This will exist only in backup table.
Populate the value from python and pass it to db.


5. This is my code
5.1 How can i make my code easy to maintain. 
5.2 gpt missed to add below code:
"with open(report_output_file_with_timestamp, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    header_written = False

    if iam_graph_operations:
        backup_success = iam_data_export_glide.backup_table_data(
            table_name="glide.glidesupervisorhierarchy",
            backup_table_name="glide.glidesupervisorhierarchy_backup"
        )
        
        if backup_success:
            iam_data_export_glide.del_7days_old_data(
                backup_table_name="glide.glidesupervisorhierarchy_backup",
                chunk_size=chunk_size
            )
            iam_data_export_glide.del_data_frm_table(
                table_name="glide.glidesupervisorhierarchy",
                chunk_size=chunk_size
            )
            flag_success = True
        else:
            logging.info("Backup failed, skipping deletion of old data")
            flag_success = False"

5.3. where is "iam_data_export_glide.close_connections()"

6. mysql db operations code 
6.1 How can i make my code easy to maintain. 
6.2 where is executemany?
6.3 where is rollback in update_data_to_identities
6.4 where is logic for missing_resource_ids

6.5 i am getting error in this line """ data_to_update = [(tuple([row[idx] for idx in req_columns] + [row['resourceid']])) for row in batch.values]""" error fetching data: only intezers, slices (':', ellipses, numpy.newaxis, None and or boolean arrays are valid indices

7. code for identities update
7.1. How can i make my code easy to maintain. 

8. I am running function update_data_to_identities on .7 million rows. And its running very slow. How can we optimize it. Also, there are lot of records which are not missing. so missing_resource_ids dataframe is very large. Please suggest optimize ideas.

8.1 by deepseek
8.2 can you please rename existing_resource_ids with glide_resource_ids and all_resource_ids to graphdb_resource_ids

9. code of populate supervisor hierachy
