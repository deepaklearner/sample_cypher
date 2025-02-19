You're absolutely right to ask about the sequence!

In the Python code, you’re appending each component in a specific sequence for both work and home addresses:

1. `Street Address` + `Locality` + `Region` + `Postal Code` + `Country`

However, the SQL code I provided earlier uses `CONCAT_WS` to concatenate address fields, but the sequence might not fully match what you had in Python.

To align with the Python logic, where you concatenate each component in a specific order and append a comma (if the field isn't `'DNE'`), let's ensure the sequence is exactly as you want.

Here is the corrected version:

### Corrected SQL with Exact Sequence and Comma:

```sql
CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(', ', 
            NULLIF(WorkAddressLine1, NULL), 
            NULLIF(WorkAddressLine2, NULL), 
            NULLIF(WorkCity, NULL), 
            NULLIF(WorkState, NULL), 
            NULLIF(PostalCode, NULL), 
            NULLIF(WorkCountryCode, NULL)
        ), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(', ', 
                    NULLIF(WorkAddressLine1, NULL), 
                    NULLIF(WorkAddressLine2, NULL), 
                    NULLIF(WorkCity, NULL), 
                    NULLIF(WorkState, NULL), 
                    NULLIF(PostalCode, NULL), 
                    NULLIF(WorkCountryCode, NULL)
                 ), ''), 'DNE') 
END AS concat_attr_WorkAddress,

CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(', ', 
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
                 NULLIF(CONCAT_WS(', ', 
                    NULLIF(HomeAddress1, NULL), 
                    NULLIF(HomeAddress2, NULL), 
                    NULLIF(HomeCity, NULL), 
                    NULLIF(HomeState, NULL), 
                    NULLIF(HomePostalCode, NULL), 
                    NULLIF(HomeCountry, NULL)
                 ), ''), 'DNE') 
END AS concat_attr_HomeAddress
```

### Key Considerations:
1. **Sequence Matching**: The sequence in the SQL now matches the Python logic. 
   - For **Work Address**, the fields are: `WorkAddressLine1`, `WorkAddressLine2`, `WorkCity`, `WorkState`, `PostalCode`, `WorkCountryCode`.
   - For **Home Address**, the fields are: `HomeAddress1`, `HomeAddress2`, `HomeAddress3`, `HomeAddress4`, `HomeCity`, `HomeState`, `HomePostalCode`, `HomeCountry`.
   
2. **Commas**: Commas (`, `) will be inserted only between non-`NULL` fields.

### Sequence Breakdown:
- **Work Address Sequence**: 
  - `WorkAddressLine1` → `WorkAddressLine2` → `WorkCity` → `WorkState` → `PostalCode` → `WorkCountryCode`
- **Home Address Sequence**: 
  - `HomeAddress1` → `HomeAddress2` → `HomeAddress3` → `HomeAddress4` → `HomeCity` → `HomeState` → `HomePostalCode` → `HomeCountry`

This should now reflect the correct order and structure of the Python logic, with commas separating address components where applicable. Let me know if anything else needs further adjustments!