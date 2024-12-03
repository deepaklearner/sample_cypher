filter from df the values for division having "HEADQ" and pass only them to exclusion "for" loop.

"""
def data_manipulation_AetnaIdentifier (data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']
    exclusion_rules = data_mapping.get('exclusion_rule', [])

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    df_headq = df[df['division'] == 'HEADQ']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '.' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

    # Apply exclusion rules
    for exclusion_rule in exclusion_rules:
        exclusion_filter = None
        for key, val in exclusion_rule.items():
            # Convert column values to uppercase
            df_headq[key] = df_headq[key].str.upper()
            # Exclude rows where the column matches the exclusion values
            if exclusion_filter is None:
                exclusion_filter = df_headq[key].isin(val)
            else:
                exclusion_filter &= df_headq[key].isin(val)
    # Collect the rows to exclude that match the exclusion rule
    df_headq = df_headq[~exclusion_filter]

    df = df - df_headq

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
"""

Solution 1:

import pandas as pd
import warnings
import logging

def data_manipulation_AetnaIdentifier(data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']
    exclusion_rules = data_mapping.get('exclusion_rule', [])

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Filter rows where 'division' is 'HEADQ'
    df_headq = df[df['division'] == 'HEADQ']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '.' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]
    df_headq['organizationId'] = df_headq['organizationId'].str.split('.').str[0]

    # Initialize exclusion filter as False for all rows in df_headq
    exclusion_filter = pd.Series([False] * len(df_headq), index=df_headq.index)

    # Apply exclusion rules to df_headq
    for exclusion_rule in exclusion_rules:
        for key, val in exclusion_rule.items():
            # Convert column values to uppercase for comparison
            df_headq[key] = df_headq[key].str.upper()
            # Update exclusion filter for rows matching the exclusion rule (using &= for AND)
            exclusion_filter &= df_headq[key].isin(val)

    # Collect the rows to exclude that match the exclusion rule (using exclusion_filter)
    rows_to_exclude = df_headq[exclusion_filter]

    # Remove the excluded rows from the original df based on their indices
    df = df[~df.index.isin(rows_to_exclude.index)]

    # Apply assignment rules to the remaining df
    combined_filter = None
    for rule in aid_assignment_rules:
        filtered_val = None
        for key, val in rule.items():
            # Convert column values to uppercase for comparison
            df[key] = df[key].str.upper()
            # Check if values are in the 'val' list
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
