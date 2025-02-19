CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', HomeAddress1, HomeAddress2, HomeAddress3, HomeAddress4, 
                                  HomeCity, HomeState, HomePostalCode, HomeCountry), ''), 'DNE')
    ELSE 
        COALESCE(FullHomeAddress, 
                 NULLIF(CONCAT_WS(' ', HomeAddress1, HomeCity, HomeState, HomePostalCode, HomeCountry), ''), 
                 'DNE') 
END AS concat_attr_HomeAddress,

CASE 
    WHEN employeetype IN ('G', 'L') THEN 
        COALESCE(NULLIF(CONCAT_WS(' ', WorkAddressLine1, WorkAddressLine2, WorkCity, 
                                  WorkState, PostalCode, WorkCountryCode), ''), 'DNE')
    ELSE 
        COALESCE(FullWorkAddress, 
                 NULLIF(CONCAT_WS(' ', WorkAddressLine1, WorkCity, WorkState, 
                                  PostalCode, WorkCountryCode), ''), 'DNE') 
END AS concat_attr_WorkAddress


