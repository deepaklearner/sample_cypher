To create a new column similar to `'computed_concat_attr_Name'` based on the logic you shared previously, we can apply a similar approach to your SQL query. Specifically, the goal is to join the columns with a space, excluding any `"DNE"` values, and use only the first letter of the `MiddleName`.

### Here’s how you can do that:

You can use the same method of `COALESCE()` and `CONCAT_WS()` to handle empty or `DNE` values. To ensure you only join non-"DNE" values and use the first letter of `MiddleName`, we'll modify the logic as needed.

#### Modified SQL Query

```sql
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
```

### Key Changes:
1. **`computed_concat_attr_Name` logic**: 
   - We use `CONCAT_WS()` to concatenate the relevant columns (`nameprefix`, `FirstName`, `MiddleName`, `LastName`, `honorificSuffix`).
   - **Conditions**: For each column, we check if it is `"DNE"` and replace it with `NULL` (since `NULL` values are ignored in `CONCAT_WS()`).
   - For `MiddleName`, we use `LEFT(MiddleName, 1)` to get the first letter, similar to the Python code you mentioned earlier.

2. **Filtering out `"DNE"` values**: The `CASE` statements handle the `"DNE"` replacement, ensuring only valid non-`"DNE"` values are included in the concatenated result.

### Output:
- This will create a new column `computed_concat_attr_Name` where the name components are concatenated together with a space between them, but only if they are not equal to `"DNE"`.
- The result will be similar to the `computed_concat_attr_Name` column logic in your Python code but implemented entirely in SQL.

Let me know if you need further clarification or adjustments!