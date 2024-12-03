Add a not check here "filtered_val = df[key].isin(val)" for exclusion_rule if added in yaml, then only assign cid. How to do that with minimal code change.

"""
sample yaml:
CVSIdentifier:
    aid_assignment_rule:
        -  division:
            - HEADQ
            jobcode:
            - '310105'
    exclusion_rule:
        -  division:
            - HEADQ
        organizationId:
            - '4022'
"""

"""
def data_manipulation_AetnaIdentifier (data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '• ' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

    combined_filter = None
    # Iterate over the assignment rules
    for rule in aid_assignment_rules:
        filtered_val = None
        for key, val in rule.items():
            # Convert column values to uppercase
            df[key] = df[key].str.upper()
            # Check if values are in 'val' list
            if filtered_val is None:
                filtered_val = df[key].isin(val)
            else:
                filtered_val &= df[key].isin(val)

        # Combine filters for each rule
        if combined_filter is None:
            combined_filter = filtered_val
        else:
            combined_filter |= filtered_val

    # Apply the combined filter
    df = df[combined_filter]

    # Convert all columns to string type
    df = df.astype(str)

    logging.info(df)

    return df"""

Solution 1:

def data_manipulation_AetnaIdentifier (data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']
    exclusion_rules = data_mapping.get('exclusion_rule', [])

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '• ' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

    # Apply exclusion rules
    for exclusion_rule in exclusion_rules:
        exclusion_filter = None
        for key, val in exclusion_rule.items():
            # Convert column values to uppercase
            df[key] = df[key].str.upper()
            # Exclude rows where the column matches the exclusion values
            if exclusion_filter is None:
                exclusion_filter = df[key].isin(val)
            else:
                exclusion_filter &= df[key].isin(val)
        # Exclude the rows that match the exclusion rule
        df = df[~exclusion_filter]

    combined_filter = None
    # Iterate over the assignment rules
    for rule in aid_assignment_rules:
        filtered_val = None
        for key, val in rule.items():
            # Convert column values to uppercase
            df[key] = df[key].str.upper()
            # Check if values are in 'val' list
            if filtered_val is None:
                filtered_val = df[key].isin(val)
            else:
                filtered_val &= df[key].isin(val)

        # Combine filters for each rule
        if combined_filter is None:
            combined_filter = filtered_val
        else:
            combined_filter |= filtered_val

    # Apply the combined filter
    df = df[combined_filter]

    # Convert all columns to string type
    df = df.astype(str)

    logging.info(df)

    return df

Solution 2:
Assume we are processing for CVSIdentifier. Read the AetnaIdentifier values from yaml and 
Add a not check in CVSIdenfier "filtered_val = df[key].isin(val)" for exclusion_rule if added in yaml, then only assign cid. How to do that with minimal code change.

I want to exclude the values for AetnaIdentifier aid_assignment_rule in CVSIdentifier

sample yaml:
"""
CVSIdentifier:
    aid_assignment_rule:
        -  division:
            - HEADQ
            jobcode:
            - '310105'

AetnaIdentifier:
    aid_assignment_rule:
        -  division:
            - HEADQ
            jobcode:
            - '310101'
"""

def data_manipulation_CVSIdentifier (data_mapping: dict, df: pd.DataFrame, aetna_data_mapping: dict):
    # Extract assignment rules from the CVSIdentifier mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']

    # Extract AetnaIdentifier assignment rules
    aetna_aid_assignment_rules = aetna_data_mapping['aid_assignment_rule']
    
    # Get all the values from AetnaIdentifier rules that we want to exclude
    exclude_values = {}
    for rule in aetna_aid_assignment_rules:
        for key, val in rule.items():
            if key not in exclude_values:
                exclude_values[key] = set(val)
            else:
                exclude_values[key].update(val)

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '• ' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

    combined_filter = None
    # Iterate over the assignment rules
    for rule in aid_assignment_rules:
        filtered_val = None
        for key, val in rule.items():
            # Convert column values to uppercase
            df[key] = df[key].str.upper()

            # Filter the values based on whether they are in exclude_values for that key
            condition = df[key].isin(val)
            
            # Exclude values that are in the AetnaIdentifier's values for the same key
            if key in exclude_values:
                condition &= ~df[key].isin(exclude_values[key])

            # Combine conditions for each key
            if filtered_val is None:
                filtered_val = condition
            else:
                filtered_val &= condition

        # Combine filters for each rule
        if combined_filter is None:
            combined_filter = filtered_val
        else:
            combined_filter |= filtered_val

    # Apply the combined filter
    df = df[combined_filter]

    # Convert all columns to string type
    df = df.astype(str)

    logging.info(df)

    return df
