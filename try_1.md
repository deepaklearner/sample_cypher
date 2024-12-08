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
    'networkAccess': ['CMARK'],
    'userType': ['CONTRACTOR']
}

# Apply validation rule to the dataframe
df = apply_validation_rule(df, rule)

# Show the result
print(df)
