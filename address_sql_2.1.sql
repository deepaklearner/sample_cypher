To translate the Python logic into the SQL query, the key task is to ensure that each part of the address is concatenated and that the default value (`'DNE'`) is applied when certain values are missing or `'DNE'`. In SQL, this can be achieved using a combination of `CASE`, `COALESCE`, `NULLIF`, and `CONCAT_WS`. 

Here is the equivalent SQL code that mirrors the logic of your Python code:

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
                                  NULLIF(WorkAddressLine1, 'DNE'), 
                                  NULLIF(WorkAddressLine2, 'DNE'),
                                  NULLIF(WorkCity, 'DNE'),
                                  NULLIF(WorkState, 'DNE'),
                                  NULLIF(PostalCode, 'DNE'),
                                  NULLIF(WorkCountryCode, 'DNE')), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', 
                                  NULLIF(WorkAddressLine1, 'DNE'), 
                                  NULLIF(WorkCity, 'DNE'), 
                                  NULLIF(WorkState, 'DNE'), 
                                  NULLIF(PostalCode, 'DNE'), 
                                  NULLIF(WorkCountryCode, 'DNE')), ''), 'DNE') 
END AS concat_attr_WorkAddress,

CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', 
                                  NULLIF(HomeAddress1, 'DNE'), 
                                  NULLIF(HomeAddress2, 'DNE'),
                                  NULLIF(HomeAddress3, 'DNE'),
                                  NULLIF(HomeAddress4, 'DNE'),
                                  NULLIF(HomeCity, 'DNE'),
                                  NULLIF(HomeState, 'DNE'),
                                  NULLIF(HomePostalCode, 'DNE'),
                                  NULLIF(HomeCountry, 'DNE')), ''), 'DNE')
    ELSE 
        COALESCE(FullHomeAddress, 
                 NULLIF(CONCAT_WS(' ', 
                                  NULLIF(HomeAddress1, 'DNE'), 
                                  NULLIF(HomeCity, 'DNE'), 
                                  NULLIF(HomeState, 'DNE'),
                                  NULLIF(HomePostalCode, 'DNE'),
                                  NULLIF(HomeCountry, 'DNE')), ''), 'DNE') 
END AS concat_attr_HomeAddress
```

### Breakdown of changes:

1. **`NULLIF(column, 'DNE')`**: This will replace `'DNE'` values with `NULL`, ensuring that only non-`'DNE'` values are included in the concatenation.
   
2. **`CONCAT_WS(' ', ...)`**: This function concatenates the non-`NULL` values, and it automatically handles the removal of any `NULL` values during the concatenation process, similar to the `filter(None, ...)` used in your Python code.

3. **`COALESCE`**: It ensures that if the concatenated result is an empty string (`''`), `'DNE'` is returned as a fallback.

4. **`CASE` conditions**: The conditions for `employeetype IN ('G', 'L')` determine whether to use the `FullWorkAddress` or `FullHomeAddress` field directly or concatenate individual components with checks for `'DNE'`.

This SQL implementation replicates the behavior of your Python code, ensuring that addresses are concatenated conditionally and the `'DNE'` value is applied where necessary.