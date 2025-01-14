i have a pandas dataframe "manager_ids_df" with below columns:
employeeid, Level, managerlevels with data as:
row1: 1001, 1, [1001]
row2: 1002, 2, [1001]
row2: 1003, 3, [1002, 1001]
row2: 1004, 4, [1003, 1002, 1001]

and other dataframe "managers_id_name_email" with below columns:
employeeid, manager_name, manager_email

I want to merge both and create below:
employeeid, L1managerid, L1manager_name, L1manager_email , L2managerid,L2manager_name, L3manager_email, L3managerid, L3manager_name, L3manager_email etc