Here’s the corrected and properly aligned SQL statement:  

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', WorkAddressLine1, WorkAddressLine2, WorkCity, 
                                  WorkState, PostalCode, WorkCountryCode), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', WorkAddressLine1, WorkCity, WorkState, 
                                  PostalCode, WorkCountryCode), ''), 'DNE') 
END AS concat_attr_WorkAddress
```

### Key Fixes:
1. **Fixed syntax errors:**
   - Replaced incorrect `* •` and `* '` with `' '` as the separator for `CONCAT_WS`.  
   - Removed extraneous `case` at the end, as it's not needed.  
   - Ensured `NULLIF` correctly checks for an empty string (`''`).  

2. **Corrected alignment and readability:**
   - Properly indented the `CASE` statement.  
   - Ensured `COALESCE` and `NULLIF` are correctly structured for handling missing values.  

Now, this SQL statement will correctly generate a concatenated work address while handling missing values.