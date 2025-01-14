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

# Function to create the columns for each manager level
def get_manager_info(managerlevels, level):
    # Initialize empty list for this level's manager info
    manager_info = {'managerid': None, 'manager_name': None, 'manager_email': None}
    
    if level <= len(managerlevels):
        manager_id = managerlevels[level - 1]
        # Get manager info for this id
        manager_info['managerid'] = manager_id
        manager_info_df = managers_id_name_email[managers_id_name_email['employeeid'] == manager_id]
        if not manager_info_df.empty:
            manager_info['manager_name'] = manager_info_df['manager_name'].values[0]
            manager_info['manager_email'] = manager_info_df['manager_email'].values[0]
    return manager_info

# Expand managerlevels into separate columns (up to 15 levels)
for i in range(1, 16):
    manager_ids_df[f'L{i}managerid'] = manager_ids_df['managerlevels'].apply(lambda x: get_manager_info(x, i)['managerid'])
    manager_ids_df[f'L{i}manager_name'] = manager_ids_df['managerlevels'].apply(lambda x: get_manager_info(x, i)['manager_name'])
    manager_ids_df[f'L{i}manager_email'] = manager_ids_df['managerlevels'].apply(lambda x: get_manager_info(x, i)['manager_email'])

# Drop the 'managerlevels' column as it's no longer needed
manager_ids_df = manager_ids_df.drop(columns=['managerlevels'])

# Output the final merged DataFrame
print(manager_ids_df.to_string())
