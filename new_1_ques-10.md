i have a pandas dataframe "manager_ids_df" with below columns:
employeeid, Level, managerlevels with data as:
row1: 1001, 1, [1001]
row2: 1002, 2, [1001]
row3: 1003, 3, [1002, 1001]
row4: 1004, 4, [1003, 1002, 1001]

and other dataframe "managers_id_name_email" with below columns:
employeeid, manager_name, manager_email with data as:
row1: 1001, Deepak, de@gmail.com
row1: 1002, Ram, pa@gmail.com
row1: 1003, Raushan, ra@gmail.com

I want to merge both and create below:
employeeid, L1managerid, L1manager_name, L1manager_email , L2managerid,L2manager_name, L3manager_email, L3managerid, L3manager_name, L3manager_email etc upto 15 levels

give me optimized way... as i need to do this for a .5 million of records

code:
import pandas as pd

# Sample DataFrames
manager_ids_data = {
    'employeeid': [1001, 1002, 1003, 1004],
    'Level': [1, 2, 3, 4],
    'managerlevels': [[1001], [1001], [1002, 1001], [1003, 1002, 1001]]
}
managers_data = {
    'employeeid': [1001, 1002, 1003],
    'manager_name': ['Deepak', 'Ram', 'Raushan'],
    'manager_email': ['de@gmail.com', 'pa@gmail.com', 'ra@gmail.com']
}

manager_ids_df = pd.DataFrame(manager_ids_data)
managers_id_name_email = pd.DataFrame(managers_data)

print(manager_ids_df, type(manager_ids_df))
print(managers_id_name_email, type(managers_id_name_email))