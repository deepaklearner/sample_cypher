In below code, if userType column value in dataframe is "CONTRACTOR", then check networkAccess. If networkAccess is not null then assign cid based on it. If networkAccess is null then assign aid based on division.

"""
sample yaml:
CVSIdentifier:
    cid_assignment_rule:
        -  division:
            - HEADQ
            jobcode:
            - '310105'
        - networkAccess:
            - HEADQ
            userType:
            - CONTRACTOR

AetnaIdentifier:
    aid_assignment_rule:
        -  division:
            - HEADQ
            jobcode:
            - '310105'
"""

"""
def data_manipulation_AetnaIdentifier (data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']
    cid_assignment_rules = data_mapping['cid_assignment_rule']

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '• ' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

# CVSIdentifier
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

    if combined_filter.any():
        df['Identifier_flag'] = "C"
    else:
    # AetnaIdentifier
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

        if combined_filter.any():
            df['Identifier_flag'] = "C"

    # Convert all columns to string type
    df = df.astype(str)

    logging.info(df)

    return df
"""