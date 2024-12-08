Modify try_1 code 

add check, if userType is "CONTRACTOR" in the dataframe data, create a new column, contractor_flag.
also, create a new column network_access_flag, and set it to True when networkAccess value in dataframe data is not "DNE".

If contractor_flag is True and network_access_flag is also True then use networkAccess column from dataframe to validate the data from rule else use division column in dataframe to validate the data.


"""
try_1.md code
"""

Solution 1:

To achieve the desired functionality, we will:

1. Add a `contractor_flag` column to the DataFrame. This column will be `True` if `userType` is "CONTRACTOR".
2. Add a `network_access_flag` column that will be `True` if the `networkAccess` value is not "DNE".
3. Use the `contractor_flag` and `network_access_flag` to conditionally apply the validation rule using either the `networkAccess` column or the `division` column for validation.
   
Here's how we can implement it:

```python
import pandas as pd

# Sample data
data = {
    'employeeNumber': [100, 101, 102, 103, 104],
    'division': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'HEADQ'],
    'networkAccess': ['HEADQ', 'HEADQ', 'HEADQ', 'DNE', 'CMARK'],
    'userType': ['EMPLOYEE', 'EMPLOYEE', 'EMPLOYEE', 'CONTRACTOR', 'CONTRACTOR']
}

# Create DataFrame
df = pd.DataFrame(data)

# Add contractor_flag and network_access_flag columns
df['contractor_flag'] = df['userType'] == 'CONTRACTOR'
df['network_access_flag'] = df['networkAccess'] != 'DNE'

# Validation logic function
def apply_validation_rule(df, rule):
    # Apply the rule: Check if division == 'HEADQ' and networkAccess == 'CMARK'
    valid_rows = (df['division'] == rule['division'][0])

    # Check based on user type
    valid_rows &= (df['userType'] == rule['userType'][0])

    # If contractor_flag is True and network_access_flag is True, use networkAccess for validation
    valid_rows &= ((df['contractor_flag'] & df['network_access_flag'] & (df['networkAccess'] == rule['networkAccess'][0])) |
                   (~df['contractor_flag'] & (df['division'] == rule['division'][0])))

    # Add a column 'is_valid' to the dataframe based on the validation result
    df['is_valid'] = valid_rows

    return df

# Define the rule based on YAML configuration
rule = {
    'division': ['HEADQ'],
    'networkAccess': ['CMARK'],
    'userType': ['CONTRACTOR']
}

# Apply validation rule to the dataframe
df = apply_validation_rule(df, rule)

# Show the result
print(df)
```

### Explanation:
1. **Add Columns**: 
   - `contractor_flag` is `True` when `userType` is "CONTRACTOR".
   - `network_access_flag` is `True` when `networkAccess` is not "DNE".
   
2. **Apply Validation Logic**:
   - If `contractor_flag` is `True` and `network_access_flag` is `True`, the `networkAccess` column will be used to check if it matches the value in the rule (`'CMARK'` in this case).
   - If the above condition is not met, the validation will fall back to the `division` column for validation.

3. **Final Validation**: The rule is applied to each row using these flags and conditionally checking the `networkAccess` or `division`.

### Output:

This will produce the following output:

```
   employeeNumber division networkAccess   userType  contractor_flag  network_access_flag  is_valid
0             100    HEADQ          HEADQ   EMPLOYEE             False                 True     False
1             101    HEADQ          HEADQ   EMPLOYEE             False                 True     False
2             102    HEADQ          HEADQ   EMPLOYEE             False                 True     False
3             103    HEADQ            DNE  CONTRACTOR              True                False     False
4             104    HEADQ         CMARK  CONTRACTOR              True                 True      True
```

In this case:
- Employee rows (`userType == EMPLOYEE`) are marked as invalid because they don't meet the network access rule for "CONTRACTOR".
- Contractor rows with valid network access (`networkAccess == "CMARK"`) are valid according to the rule.
- Contractor rows with "DNE" in `networkAccess` are marked invalid.