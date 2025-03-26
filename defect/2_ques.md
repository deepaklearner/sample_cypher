I have a sql:
"""SELECT DISTINCT 
    CVSResourceid,
    COALESE(TRIM(LastNameSuffix), 'DNE') AS honorificSuffix
FROM glide.glide_sdp_sensitive_dataview_hierarchy"""

I want to add this python logic to sql:

"""df['honorificSuffix'] = np.where(df['preferredSuffix'] != 'DNE',
                                 df['preferredSuffix'],
                                 df['lastnameSuffix'].str.split(' ').str[-1]) """


Answer1:
SELECT DISTINCT 
    CVSResourceid,
    COALESCE(TRIM(PreferredSuffix), TRIM(SUBSTRING_INDEX(LastNameSuffix, ' ', -1))) AS honorificSuffix
FROM glide.glide_sdp_sensitive_dataview_hierarchy

Answer2:
SELECT DISTINCT 
    CVSResourceid,
    COALESCE(TRIM(PreferredSuffix), TRIM(SUBSTRING_INDEX(LastNameSuffix, ' ', -1)), 'DNE') AS honorificSuffix
FROM glide.glide_sdp_sensitive_dataview_hierarchy
