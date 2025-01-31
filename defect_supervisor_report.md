what is use of manager_ids = manager_ids_df['manager_levels'].explode().unique()

I have a dataframe manager_ids_df in which I have a column ManagerLevel. I want to remove all rows where ManagerLevel is 0

i am printing in log manager_ids_df[manager_ids_df['ManagerLevel']==0],
how to print in list format

employee_ids_list = manager_ids_df[manager_ids_df['ManagerLevel'] == 0]['EmployeeID'].tolist()
print(employee_ids_list)
