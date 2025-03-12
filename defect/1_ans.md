SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(TRIM(LastName), ''),
        -- Modified honorificSuffix logic to match Python
        CASE
            WHEN TRIM(preferredSuffix) != '' THEN TRIM(preferredSuffix)
            ELSE COALESCE(NULLIF(TRIM(lastnameSuffix), ''), '')
        END
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy;

Using coalese:

SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(TRIM(LastName), ''),
        -- Using COALESCE for honorificSuffix logic without 'DNE' check
        COALESCE(
            NULLIF(TRIM(preferredSuffix), ''),
            TRIM(SUBSTRING_INDEX(TRIM(lastnameSuffix), ' ', -1))
        ) AS honorificSuffix
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy;

Can we use below:
"""
SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(TRIM(LastName), ''),
        -- Using COALESCE for honorificSuffix logic without 'DNE' check
        nullif(
            COALESCE(TRIM(preferredSuffix), SUBSTRING_INDEX(TRIM(lastnameSuffix), ' ', -1),'')
        ) AS honorificSuffix
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy;
"""

Note: NULLIF function compares two values and returns NULL if they are equal

Modified solution by gpt:
"""SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(TRIM(LastName), ''),
        -- Using COALESCE for honorificSuffix logic without 'DNE' check
        nullif(COALESCE(TRIM(preferredSuffix), TRIM(SUBSTRING_INDEX(TRIM(lastnameSuffix), ' ', -1)), '')) AS honorificSuffix
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy;
"""

Explanation:
Yes, your updated SQL query can be used, but there’s a slight issue with how `NULLIF` is applied. The `NULLIF` function compares two values and returns `NULL` if they are equal, which is useful for eliminating empty strings or other values.

However, when using `NULLIF` on the result of `COALESCE`, you might end up with unexpected behavior because `NULLIF` compares two values, and it might not behave as intended if `COALESCE` already handles the empty string logic.

Let's refine the query to ensure it works as expected:

```sql
SELECT DISTINCT 
    CVSResourceid,
    CONCAT_WS(' ',
        nullif(TRIM(nameprefix), ''),
        nullif(TRIM(FirstName), ''),
        nullif(LEFT(TRIM(MiddleName), 1), ''),
        nullif(TRIM(LastName), ''),
        -- Using COALESCE for honorificSuffix logic without 'DNE' check
        nullif(COALESCE(TRIM(preferredSuffix), TRIM(SUBSTRING_INDEX(TRIM(lastnameSuffix), ' ', -1)), '')) AS honorificSuffix
    ) AS computed_concat_attr_Name
FROM glide.glide_sdp_sensitive_dataview_hierarchy;
```

### Explanation of changes:
1. **`COALESCE(TRIM(preferredSuffix), TRIM(SUBSTRING_INDEX(TRIM(lastnameSuffix), ' ', -1)), '')`**:
   - The `COALESCE` function checks the value of `preferredSuffix` (trimmed). If `preferredSuffix` is empty (i.e., `NULL` after `TRIM`), it will use the last word from `lastnameSuffix` (using `SUBSTRING_INDEX`).
   - If both are empty or `NULL`, it returns an empty string (`''`).

2. **`NULLIF(..., '')`**:
   - After `COALESCE` returns the result, the `NULLIF` is applied to convert empty strings (`''`) to `NULL`, which ensures that the final concatenation doesn't include empty values.

### Why this works:
- `COALESCE` handles the logic of choosing between `preferredSuffix` and `lastnameSuffix`, and if neither is available, it defaults to an empty string.
- `NULLIF(..., '')` ensures that any empty string result is treated as `NULL`, which is then omitted from the concatenation by `CONCAT_WS`.

This query should work as expected for computing the `computed_concat_attr_Name` while applying the `honorificSuffix` logic correctly. Let me know if you need further clarifications!