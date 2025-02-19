Q. i want to apply the logic mentioned in this python code to the sql query python code 

To adapt the Python logic to SQL, we want to follow the same approach: 

1. Concatenate address fields, ensuring that `DNE` (or equivalent) values are handled by replacing or omitting them.
2. Only include non-null, non-empty values when concatenating.
3. If the concatenated result is empty (after removing `DNE` values), replace it with `DNE`.

### Here’s how we can apply this logic in SQL:

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
            NULLIF(NULLIF(WorkAddressLine1, 'DNE'), ''), 
            NULLIF(NULLIF(WorkAddressLine2, 'DNE'), ''), 
            NULLIF(NULLIF(WorkCity, 'DNE'), ''), 
            NULLIF(NULLIF(WorkState, 'DNE'), ''), 
            NULLIF(NULLIF(PostalCode, 'DNE'), ''), 
            NULLIF(NULLIF(WorkCountryCode, 'DNE'), '')
        ), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', 
                    NULLIF(NULLIF(WorkAddressLine1, 'DNE'), ''), 
                    NULLIF(NULLIF(WorkCity, 'DNE'), ''), 
                    NULLIF(NULLIF(WorkState, 'DNE'), ''), 
                    NULLIF(NULLIF(PostalCode, 'DNE'), ''), 
                    NULLIF(NULLIF(WorkCountryCode, 'DNE'), '')
                 ), ''), 'DNE') 
END AS concat_attr_WorkAddress,

CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
            NULLIF(NULLIF(HomeAddress1, 'DNE'), ''), 
            NULLIF(NULLIF(HomeAddress2, 'DNE'), ''), 
            NULLIF(NULLIF(HomeAddress3, 'DNE'), ''), 
            NULLIF(NULLIF(HomeAddress4, 'DNE'), ''), 
            NULLIF(NULLIF(HomeCity, 'DNE'), ''), 
            NULLIF(NULLIF(HomeState, 'DNE'), ''), 
            NULLIF(NULLIF(HomePostalCode, 'DNE'), ''), 
            NULLIF(NULLIF(HomeCountry, 'DNE'), '')
        ), ''), 'DNE')
    ELSE 
        COALESCE(FullHomeAddress, 
                 NULLIF(CONCAT_WS(' ', 
                    NULLIF(NULLIF(HomeAddress1, 'DNE'), ''), 
                    NULLIF(NULLIF(HomeCity, 'DNE'), ''), 
                    NULLIF(NULLIF(HomeState, 'DNE'), ''), 
                    NULLIF(NULLIF(HomePostalCode, 'DNE'), ''), 
                    NULLIF(NULLIF(HomeCountry, 'DNE'), '')
                 ), ''), 'DNE') 
END AS concat_attr_HomeAddress
```

### Breakdown of the SQL Logic:

- **`CONCAT_WS(' ', ...)`**: This concatenates multiple fields with a space between them. We use `CONCAT_WS` instead of `CONCAT` because it ignores any `NULL` values.
  
- **`NULLIF(<field>, 'DNE')`**: This checks if the field is equal to `'DNE'`, and if it is, it returns `NULL`. This is similar to the behavior in the Python code where `DNE` values are replaced by an empty string.
  
- **`COALESCE()`**: This function returns the first non-null value. We use it to return a valid concatenated address or `'DNE'` if the concatenated result is empty or null.
  
- **`NULLIF(..., '')`**: This checks if the result of the concatenation is an empty string and converts it to `NULL`. The `COALESCE` then ensures that `'DNE'` is returned if the result is `NULL`.

This SQL code should replicate the logic in your Python code and handle the same cases for address concatenation and replacement of `'DNE'`.