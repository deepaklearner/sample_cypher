Q1. Add a validation rule in yaml file 

Q1. Add a validation rule in yaml file 

validation_rule:
    -  division:
        - CMARK
    -  networkAccess:
       -  HEADQ
       userType:
       - CONTRACTOR

for
data = {
    'employeeNumber': [100, 101, 102, 103, 104 ],
    'division': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'HEADQ'],
    'networkAccess': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'CMARK'],
    'userType': ['EMPLOYEE', 'EMPLOYEE', 'EMPLOYEE', 'CONTRACTOR', 'CONTRACTOR']
}
df = pd.DataFrame(data)

add check, if userType is "CONTRACTOR" then check networkAccess value and validate data, if networkAccess value is "DNE" then use division column and division rule in yaml file to validate data


To enhance the validation rule to include a check for `networkAccess` when the `userType` is "CONTRACTOR", we can add an additional condition. Specifically, if the `userType` is "CONTRACTOR", we need to check if `networkAccess` is **not** equal to "DNE". If `networkAccess` is "DNE", we should mark the row as invalid, otherwise, it should be valid.

Let's modify the validation function and the rule to incorporate this check:

### Updated YAML Configuration:
The YAML structure will remain the same since the validation for `networkAccess` when `userType` is "CONTRACTOR" will be handled in the code.

```yaml
validation_rule:
  - division:
      - HEADQ
  - networkAccess:
      - HEADQ
  - userType:
      - CONTRACTOR
```

### Updated Python Code:

```python
import pandas as pd

# Sample data
data = {
    'employeeNumber': [100, 101, 102, 103, 104],
    'division': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'HEADQ'],
    'networkAccess': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'DNE'],
    'userType': ['EMPLOYEE', 'EMPLOYEE', 'EMPLOYEE', 'CONTRACTOR', 'CONTRACTOR']
}

# Create DataFrame
df = pd.DataFrame(data)

# Validation logic
def apply_validation_rule(df, rule):
    # Apply the rule: Check if division == 'HEADQ' and networkAccess == 'HEADQ'
    valid_rows = (df['division'] == rule['division'][0]) & (df['networkAccess'] == rule['networkAccess'][0])
    
    # Apply rule for userType to be 'CONTRACTOR' where the above conditions hold
    valid_rows &= (df['userType'] == rule['userType'][0])
    
    # Additional check: If userType is 'CONTRACTOR', networkAccess must not be 'DNE'
    valid_rows &= ~((df['userType'] == 'CONTRACTOR') & (df['networkAccess'] == 'DNE'))

    # Add a column 'is_valid' to the dataframe based on the validation result
    df['is_valid'] = valid_rows

    return df

# Define the rule based on YAML configuration
rule = {
    'division': ['HEADQ'],
    'networkAccess': ['HEADQ'],
    'userType': ['CONTRACTOR']
}

# Apply validation rule to the dataframe
df = apply_validation_rule(df, rule)

# Show the result
print(df)
```

### Explanation of Changes:

1. **Validation for `userType == 'CONTRACTOR'` and `networkAccess != 'DNE'`**:
   - After checking the original validation conditions (i.e., `division == 'HEADQ'` and `networkAccess == 'HEADQ'`), we add an additional condition to check if `userType` is "CONTRACTOR". If it is, we ensure that `networkAccess` is **not** "DNE" using this condition:  
     ```python
     valid_rows &= ~((df['userType'] == 'CONTRACTOR') & (df['networkAccess'] == 'DNE'))
     ```
     The `~` operator is used for negation (to ensure `networkAccess != 'DNE'`).

2. **Final Validation Column**:
   - The result is stored in a new column `is_valid` that indicates whether each row meets the validation rules.

### Output:

The resulting DataFrame will look like this:

```python
   employeeNumber division networkAccess  userType  is_valid
0             100    HEADQ         HEADQ  EMPLOYEE     False
1             101    HEADQ         HEADQ  EMPLOYEE     False
2             102    HEADQ         HEADQ  EMPLOYEE     False
3             103    HEADQ         HEADQ  CONTRACTOR   True
4             104    HEADQ          DNE  CONTRACTOR   False
```

### Explanation of the Output:

- For rows with `userType == 'EMPLOYEE'`, they are invalid (`False`) because the rule specifies that `userType` must be "CONTRACTOR".
- For row 3 (`employeeNumber == 103`), both `division == 'HEADQ'`, `networkAccess == 'HEADQ'`, and `userType == 'CONTRACTOR'` are valid, so it's marked as valid (`True`).
- For row 4 (`employeeNumber == 104`), even though the `division` and `userType` are correct, the `networkAccess` is "DNE" and the rule specifies that `userType == 'CONTRACTOR'` requires `networkAccess != 'DNE'`. Hence, it's marked as invalid (`False`).

This approach ensures that all the conditions from the validation rule are applied properly.