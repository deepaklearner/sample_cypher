In this functi
on, i dont want to change the case of data of dataframe df  "df[key].str.upper()". Help me modify the code.
without breaking logic df[key].isin(val).

"""
```python
def data_manipulation_AetnaIdentifier(data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    aid_assignment_rules = data_mapping['aid_assignment_rule']
    nid_assignment_rules = data_mapping['nid_assignment_rule']  # New line for NID assignment rules

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '.' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('.').str[0]

    # Initialize combined filter
    combined_filter = None

    # Apply filtering based on 'aid_assignment_rules'
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

        # Combine filters for aid rules
        if combined_filter is None:
            combined_filter = filtered_val
        else:
            combined_filter |= filtered_val  # OR combine filters for each rule

    # Apply filtering based on 'nid_assignment_rules' (new logic)
    for rule in nid_assignment_rules:
        filtered_val = None
        for key, val in rule.items():
            # Convert column values to uppercase
            df[key] = df[key].str.upper()
            # Check if values are in 'val' list
            if filtered_val is None:
                filtered_val = df[key].isin(val)
            else:
                filtered_val &= df[key].isin(val)

        # Combine filters for nid rules (OR combine with aid rules)
        if combined_filter is None:
            combined_filter = filtered_val
        else:
            combined_filter |= filtered_val  # OR combine filters for each rule

    # Apply the combined filter to the DataFrame
    df = df[combined_filter]

    # Convert all columns to string type
    df = df.astype(str)

    # Log the filtered DataFrame
    logging.info(df)

    return df
```
"""


can i write "filtered_val = df[key].isin(val)"
like this "filtered_val = df[key].str.upper().isin(val)"