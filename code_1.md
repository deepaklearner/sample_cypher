pd.to_datetime(
    df[colname], 
    format='%Y-%m-%dT%H:%M:%SZ', 
    errors='coerce', 
    utc=True
).fillna(
    pd.to_datetime(
        df[colname], 
        format='%Y-%m-%d %H:%M:%S', 
        errors='coerce', 
        utc=True
    )
).fillna(
    pd.to_datetime(
        df[colname], 
        format='%Y-%m-%d', 
        errors='coerce', 
        utc=True
    )
).fillna(
    pd.to_datetime(
        df[colname], 
        format='%Y%m%d', 
        errors='coerce', 
        utc=True
    )
).fillna(
    pd.to_datetime(
        df[colname], 
        format='%m/%d/%Y', 
        errors='coerce', 
        utc=True
    )
)


