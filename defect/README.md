1. Is below corect in SQL

nullif(COALESCE(TRIM(preferredSuffix), TRIM(lastNameSuffix),''))

Logic in Python:

df['honorificSuffix'] = np.where(df['preferredSuffix'] != 'DNE',
                                 df['preferredSuffix'],
                                 df['lastnameSuffix'].str.split(' ').str[-1])

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

SQL:
SELECT DISTINCT 
    CVSResourceid,
CASE 
        WHEN COALESCE(TRIM(FullName), 
            CONCAT_WS(' ', 
                TRIM(nameprefix), 
                TRIM(LastName), 
                LEFT(TRIM(MiddleName), 1), 
                TRIM(FirstName)
            )
        ) = '' THEN 'N' 
        ELSE 'Y' 
    END AS is_Name,

    -- New computed column similar to 'computed_concat_attr_Name'
    CONCAT_WS(' ',
        CASE WHEN TRIM(nameprefix) = 'DNE' THEN NULL ELSE TRIM(nameprefix) END,
        CASE WHEN TRIM(FirstName) = 'DNE' THEN NULL ELSE TRIM(FirstName) END,
        CASE WHEN TRIM(MiddleName) = 'DNE' THEN NULL ELSE LEFT(TRIM(MiddleName), 1) END,
        CASE WHEN TRIM(LastName) = 'DNE' THEN NULL ELSE TRIM(LastName) END,
        CASE WHEN TRIM(honorificSuffix) = 'DNE' THEN NULL ELSE TRIM(honorificSuffix) END
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy
WHERE 
    LENGTH(TRIM(CVSResourceid)) > 0 
    AND CVSResourceid IS NOT NULL 
    AND CVSResourceid IN ('7304012');
