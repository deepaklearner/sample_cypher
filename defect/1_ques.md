I have this python code """df['computed_concat_attr_Name'] = list(
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
)""" and equivalent sql """ SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName),1), ''),
        nullif(TRIM(LastName), ''),
        nullif(TRIM(honorificSuffix), ''),
    ) AS computed_concat_attr_Name

FROM glide.glide_sdp_sensitive_dataview_hierarchy"""

I want to add this python logic as well to sql:

"""df['honorificSuffix'] = np.where(df['preferredSuffix'] != 'DNE',
                                 df['preferredSuffix'],
                                 df['lastnameSuffix'].str.split(' ').str[-1]) """