Q. I want to implement same logic in this sql query.
in sql the data will never be DNE it can be null.

Thank you for the clarification! If the data in SQL is never `'DNE'` but can be `NULL`, we can adjust the logic accordingly. The goal is to concatenate the address components and ensure that `NULL` values are properly handled, replacing them with `'DNE'` when necessary. Here's the revised SQL query based on your explanation:

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
                                  NULLIF(WorkAddressLine1, NULL), 
                                  NULLIF(WorkAddressLine2, NULL),
                                  NULLIF(WorkCity, NULL),
                                  NULLIF(WorkState, NULL),
                                  NULLIF(PostalCode, NULL),
                                  NULLIF(WorkCountryCode, NULL)), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', 
                                  NULLIF(WorkAddressLine1, NULL), 
                                  NULLIF(WorkCity, NULL), 
                                  NULLIF(WorkState, NULL), 
                                  NULLIF(PostalCode, NULL), 
                                  NULLIF(WorkCountryCode, NULL)), ''), 'DNE') 
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
                                  NULLIF(HomeCountry, NULL)), ''), 'DNE')
    ELSE 
        COALESCE(FullHomeAddress, 
                 NULLIF(CONCAT_WS(' ', 
                                  NULLIF(HomeAddress1, NULL), 
                                  NULLIF(HomeCity, NULL), 
                                  NULLIF(HomeState, NULL),
                                  NULLIF(HomePostalCode, NULL),
                                  NULLIF(HomeCountry, NULL)), ''), 'DNE') 
END AS concat_attr_HomeAddress
```

### Changes made:

1. **`NULLIF(column, NULL)`**: Here, we replace any `NULL` values in the columns with `NULL`. This step is necessary to handle potential `NULL` values before concatenating them.
   
2. **`CONCAT_WS(' ', ...)`**: Concatenates the non-`NULL` values, just like before, and ensures that if all values are `NULL`, the result will be an empty string.

3. **`COALESCE(..., 'DNE')`**: If the result of the concatenation is an empty string, `'DNE'` will be used as the fallback.

In this version, we ensure that the `NULL` values are properly handled and replaced by `'DNE'` only when all parts of the address are `NULL` or when there is no address data to concatenate.