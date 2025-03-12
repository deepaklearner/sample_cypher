SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(nameprefix, ''),
        nullif(FirstName, ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(LastName, ''),
        CASE 
            WHEN preferredSuffix != '' THEN preferredSuffix
            ELSE TRIM(SUBSTRING_INDEX(lastnameSuffix, ' ', -1))  -- Extract the last part of lastnameSuffix
        END,
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy


Solution with coalese

SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        COALESCE(NULLIF(nameprefix, ''), ''),
        COALESCE(NULLIF(FirstName, ''), ''),
        COALESCE(NULLIF(LEFT(TRIM(MiddleName), 1), ''), ''),
        COALESCE(NULLIF(LastName, ''), ''),
        COALESCE(
            NULLIF(preferredSuffix, ''), 
            TRIM(SUBSTRING_INDEX(lastnameSuffix, ' ', -1))
        )
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy
