how to backfill a column using bfill


df['combinedNetwork'] = np.where(
    df['userType'].str.upper() == 'CONTRACTOR',
    df[['networkAccess', 'division']].fillna(axis=1).iloc[:, 0],
    df['division']
)

