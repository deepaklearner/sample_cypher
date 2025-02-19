Q. the data in sql can never be "DNE". it can be NULL


Got it! If the data in the SQL columns can only be `NULL` (not `'DNE'`), we need to modify the logic to handle `NULL` values instead of `'DNE'`. 

Here’s how we can adjust the SQL logic based on the new requirement:

1. **Replace `NULL` values** in the address fields.
2. **Concatenate** the fields only if they are not `NULL`.
3. If the concatenated result is empty (after handling `NULL` values), replace it with a default value (`'DNE'` or similar if needed).

Here's the updated SQL query:

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
            NULLIF(WorkAddressLine1, NULL), 
            NULLIF(WorkAddressLine2, NULL), 
            NULLIF(WorkCity, NULL), 
            NULLIF(WorkState, NULL), 
            NULLIF(PostalCode, NULL), 
            NULLIF(WorkCountryCode, NULL)
        ), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', 
                    NULLIF(WorkAddressLine1, NULL), 
                    NULLIF(WorkCity, NULL), 
                    NULLIF(WorkState, NULL), 
                    NULLIF(PostalCode, NULL), 
                    NULLIF(WorkCountryCode, NULL)
                 ), ''), 'DNE') 
END AS concat_attr_WorkAddress,

CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
            NULLIF(HomeAddress1, NULL), 
            NULLIF(HomeAddress2, NULL), 
            NULLIF(HomeAddress3, NULL), 
            NULLIF(HomeAddress4, NULL), 
            NULLIF(HomeCity, NULL), 
            NULLIF(HomeState, NULL), 
            NULLIF(HomePostalCode, NULL), 
            NULLIF(HomeCountry, NULL)
        ), ''), 'DNE')
    ELSE 
        COALESCE(FullHomeAddress, 
                 NULLIF(CONCAT_WS(' ', 
                    NULLIF(HomeAddress1, NULL), 
                    NULLIF(HomeCity, NULL), 
                    NULLIF(HomeState, NULL), 
                    NULLIF(HomePostalCode, NULL), 
                    NULLIF(HomeCountry, NULL)
                 ), ''), 'DNE') 
END AS concat_attr_HomeAddress
```

### Key Changes:

1. **`NULLIF(<field>, NULL)`**: This ensures that if any of the fields are `NULL`, they are excluded from the concatenation.
   
2. **`COALESCE()`**: After concatenation, we check if the result is `NULL` or empty (`''`). If so, it will return `'DNE'` (or whatever default value you want).

3. **Empty String Handling**: `NULLIF(CONCAT_WS(' ', ...), '')` ensures that if the concatenated result is an empty string, it gets converted to `NULL`, and `COALESCE` then returns `'DNE'`.

This query will behave like your Python code but handles `NULL` values in the SQL context rather than `'DNE'`.