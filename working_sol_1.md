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

# By chatgpt

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


# By perplexity

To optimize the process for handling 0.5 million records, we can use vectorized operations and merge functions in pandas. Here's an optimized approach:

```python
import pandas as pd

# Assuming manager_ids_df and managers_id_name_email are already created

# Step 1: Explode the managerlevels column
exploded_df = manager_ids_df.explode('managerlevels')

# Step 2: Merge with managers_id_name_email
result_df = exploded_df.merge(managers_id_name_email, 
                              left_on='managerlevels', 
                              right_on='employeeid', 
                              suffixes=('_employee', '_manager'))

# Step 3: Group by employee and aggregate manager information
final_df = result_df.groupby('employeeid_employee').agg({
    'Level': 'first',
    'manager_name': lambda x: list(x),
    'manager_email': lambda x: list(x)
}).reset_index()

# Rename columns for clarity
final_df.columns = ['employeeid', 'Level', 'manager_names', 'manager_emails']

print(final_df)
```

This optimized approach has several advantages:

1. **Vectorization**: We use pandas' built-in functions like `explode()` and `merge()`, which are optimized for large datasets.

2. **Single merge operation**: Instead of iterating through each employee, we perform a single merge operation.

3. **Efficient grouping**: We use `groupby()` and `agg()` to efficiently collect manager information for each employee.

4. **Memory efficiency**: This approach avoids creating large intermediate lists or dictionaries in memory.

5. **Scalability**: This method should scale well for 0.5 million records, as it leverages pandas' optimized C-based operations.

To further optimize for very large datasets:

1. **Chunking**: If memory is an issue, you can process the data in chunks using `pd.read_csv()` with the `chunksize` parameter.

2. **Parallel processing**: For even larger datasets, you might consider using libraries like Dask or Vaex, which allow for out-of-core and parallel processing.

3. **Indexing**: If you'll be performing frequent lookups, consider setting appropriate indexes on your DataFrames.

4. **Data types**: Ensure you're using the most memory-efficient data types for your columns (e.g., categories for strings with limited unique values).

Remember to monitor memory usage and processing time when working with large datasets, and adjust the approach if needed.