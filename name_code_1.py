import pandas as pd
import numpy as np

df['computed_concat_attr_Name'] = list(
    map(
        lambda x: " ".join(filter(None, x)),  # Join non-empty elements with a space
        zip(
            np.where(df.honorificPrefix == "DNE", "", df.honorificPrefix),
            np.where(df.givenName == "DNE", "", df.givenName),
            np.where(df.MiddleName == "DNE", "", df.MiddleName.str[0]),  # Only first letter of MiddleName
            np.where(df.familyName == "DNE", "", df.familyName),
            np.where(df.honorificSuffix == "DNE", "", df.honorificSuffix),
        ),
    )
)
