### Corrected and Cleaned-Up Code:
Here’s a cleaned-up version of the code with some corrections:

```python
import pandas as pd
import logging
import warnings

def data_manipulation(AetnaIdentifier, data_mapping: dict, df: pd.DataFrame):
    # Extract assignment rules from the mapping dictionary
    Lassignment_rules = data_mapping['aid_assignment_rule']

    # Filter rows where 'employmentStatus' is 'A'
    df = df[df['employmentStatus'] == 'A']

    # Ignore warnings
    warnings.simplefilter(action='ignore')

    # Clean the 'organizationId' column by splitting at '• ' and keeping the first part
    df['organizationId'] = df['organizationId'].str.split('• ').str[0]

    combined_filter = None
    # Iterate over the assignment rules
    for rule in Lassignment_rules:
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

    # Log the resulting DataFrame
    logging.info("deepak-2 df")
    logging.info(df)

    return df
```
