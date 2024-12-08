I am having some rules to filter the data in  yaml file like below.
I want to create only one id for an employee. How can i plan to ensure that.

"""
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
  AETNAIdentifier:
    aid_assignment_rule:
        -  division:
            - AETNA
"""
Using python, if i am reading a dataframe from csv and then using a for loop and passing that dataframe to different classes.
In one of the class method, I want to add a new column to a dataframe. 

If the first for loop, that dataframe is passed to next iteration, how can i retain that new column and access it later.

Q. how to add a new column in pandas dataframe 


Q. In this code I want to add a flag as a new column in the dataframe with value Y, where combined_filter when its True
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

    return df
    """