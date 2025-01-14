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
import pandas as pd
import numpy as np

# Assuming you have already created manager_ids_df and managers_id_name_email

# Step 1: Create a dictionary for quick manager lookup
manager_dict = managers_id_name_email.set_index('employeeid').to_dict('index')

# Step 2: Define a function to expand manager levels
def expand_manager_levels(row):
    levels = row['managerlevels']
    max_levels = 15
    expanded = levels + [None] * (max_levels - len(levels))
    return pd.Series(expanded, index=[f'L{i+1}managerid' for i in range(max_levels)])

# Step 3: Apply the function to create new columns
expanded_df = manager_ids_df.apply(expand_manager_levels, axis=1)

# Step 4: Concatenate the original dataframe with the expanded one
result_df = pd.concat([manager_ids_df[['employeeid', 'Level']], expanded_df], axis=1)

# Step 5: Create manager name and email columns
for i in range(1, 16):  # Up to 15 levels
    level_id = f'L{i}managerid'
    result_df[f'L{i}manager_name'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('manager_name'))
    result_df[f'L{i}manager_email'] = result_df[level_id].map(lambda x: manager_dict.get(x, {}).get('manager_email'))

# Step 6: Reorder columns
column_order = ['employeeid', 'Level']
for i in range(1, 16):
    column_order.extend([f'L{i}managerid', f'L{i}manager_name', f'L{i}manager_email'])

result_df = result_df[column_order]

# Display the first few rows of the result
print(result_df.to_string())
