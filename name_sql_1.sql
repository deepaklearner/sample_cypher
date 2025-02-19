SELECT DISTINCT 
    CVSResourceid,

    COALESCE(HomeAddress1, 'DNE') AS hm_streetAddress,
    COALESCE(HomeCity, 'DNE') AS hm_locality,
    COALESCE(HomeState, 'DNE') AS hm_region,
    COALESCE(HomeCountry, 'DNE') AS hm_country,

    COALESCE(TRIM(preferredFirstname), 'DNE') AS prefGivenName,
    CONCAT_WS(' ', 
        TRIM(preferredprefix), 
        TRIM(preferredLastname), 
        LEFT(TRIM(preferredMiddlename), 1), 
        TRIM(preferredFirstname)
    ) AS concat_attr_PreferredName,

    COALESCE(TRIM(preferredMiddlename), 'DNE') AS prefMiddleName,
    COALESCE(TRIM(preferredLastname), 'DNE') AS prefFamilyName,
    COALESCE(TRIM(preferredprefix), 'DNE') AS prefHonorificPrefix,
    COALESCE(TRIM(preferredSuffix), 'DNE') AS prefHonorificSuffix,
    COALESCE(TRIM(isLegalNameprefName), 'DNE') AS isLegalNamePreferred,

    CASE 
        WHEN CONCAT_WS(' ', 
            TRIM(preferredprefix), 
            TRIM(preferredLastname), 
            LEFT(TRIM(preferredMiddlename), 1), 
            TRIM(preferredFirstname)
        ) = '' THEN 'N' 
        ELSE 'Y' 
    END AS is_PreferredName,

    COALESCE(TRIM(FullName), 
        CONCAT_WS(' ', 
            TRIM(nameprefix), 
            TRIM(LastName), 
            LEFT(TRIM(MiddleName), 1), 
            TRIM(FirstName)
        )
    ) AS concat_attr_Name,

    COALESCE(TRIM(FirstName), 'DNE') AS givenName,
    COALESCE(TRIM(MiddleName), 'DNE') AS middleName,
    COALESCE(TRIM(LastName), 'DNE') AS FamilyName,
    COALESCE(TRIM(nameprefix), 'DNE') AS honorificPrefix,

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
    END AS is_Name

FROM glide.glide_sdp_sensitive_dataview_hierarchy

WHERE 
    LENGTH(TRIM(CVSResourceid)) > 0 
    AND CVSResourceid IS NOT NULL 
    AND CVSResourceid IN ('7304012');
