df1 is pandas dataframe and df2 is also pandas dataframe.
I want to check if any one row satisfies the criteria: (df1['E_EmployeeID'] == row['E_EmployeeID']) &  (df1['domain'] == 'AETH') & (df1['PrimaryAuthEDW_Original'] == True)

And in df2, i want to check if for that employee record, for non AETH all PrimaryAuth should be False.

row value is coming from a for loop reading a different dataframe row by row.

if (
    ((df1['E_EmployeeID'] == row['E_EmployeeID']) & 
     (df1['domain'] == 'AETH') & 
     (df1['PrimaryAuthEDW_Original'] == True)).any()
    and 
    ((df2['E_EmployeeID'] == row['E_EmployeeID']) & 
     (df2['domain'] != 'AETH') & 
     (df2['PrimaryAuth'] == False)).all()
):
    clear_selected_changed_user_accounts.update(diff_accounts)

