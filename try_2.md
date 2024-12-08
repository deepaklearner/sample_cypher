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
    # Validate if userType is 'CONTRACTOR'
    valid_rows = True  # Start with assuming all rows are valid

    # Check for each row
    for index, row in df.iterrows():
        if row['userType'] == 'CONTRACTOR':
            if row['networkAccess'] == 'DNE':
                # If networkAccess is DNE, validate based on division rule
                if row['division'] != rule['division'][0]:
                    valid_rows &= False
            else:
                # If networkAccess is not DNE, validate based on both division and networkAccess rules
                if row['division'] != rule['division'][0] or row['networkAccess'] != rule['networkAccess'][0]:
                    valid_rows &= False
        else:
            # For non-CONTRACTOR, just check division and networkAccess
            if row['division'] != rule['division'][0] or row['networkAccess'] != rule['networkAccess'][0]:
                valid_rows &= False
        
    # Return the final validity of the rows
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
