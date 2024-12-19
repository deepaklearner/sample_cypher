import pandas as pd

# Sample DataFrame (df1)
df1 = pd.DataFrame({
    'E_EmployeeID': [1, 2, 1, 3],
    'samaccountname': ['N75001', 'N75002', 'N75003', 'N75004'],
    'domain': ['AETH', 'AETT', 'AETH', 'AETT'],
    'accountType': ['Secondary', 'Secondary', 'Primary', 'Secondary'],
    'concat_attr_col1': ['A', 'B', 'C', 'D']
})

# Example parameters for cvs_resource_id, samaccountname, and domain_r
cvs_resource_id = 1
samaccountname = 'N75003'
domain_r = 'AETH'

# Find matching rows where accountType is 'Secondary', samaccountname is not equal, and other conditions match
matched_rows = df1[
    (df1['E_EmployeeID'] == cvs_resource_id) & 
    (df1['samaccountname'] != samaccountname) & 
    (df1['domain'] == domain_r) & 
    (df1['accountType'] == 'Secondary')
]

# Print matched rows for debugging
print("Matched rows where accountType is 'Secondary' and samaccountname is not equal:")
print(matched_rows)

# If matched rows exist, update the accountType from 'Secondary' to 'Primary'
if not matched_rows.empty:
    df1.loc[
        (df1['E_EmployeeID'] == cvs_resource_id) & 
        (df1['samaccountname'] != samaccountname) & 
        (df1['domain'] == domain_r) & 
        (df1['accountType'] == 'Secondary'), 
        'accountType'
    ] = 'Primary'
    print(f"Updated accountType to 'Primary' for {domain_r}")
else:
    print(f"No Secondary account found for {domain_r}")

# Print the updated df1 to see changes
print("\nUpdated df1:")
print(df1)
