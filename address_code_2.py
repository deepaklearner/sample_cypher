import numpy as np

df['concat_attr_WorkAddress'] = list(map(
    lambda x: ' '.join(filter(None, x)),
    zip(
        np.where(df.WorkstreetAddress == 'DNE', '', df.WorkstreetAddress + ','),
        np.where(df.worklocality == 'DNE', '', df.worklocality + ','),
        np.where(df.workregion == 'DNE', '', df.workregion),
        np.where(df.workpostalCode == 'DNE', '', df.workpostalCode),
        np.where(df.workcountry == 'DNE', '', df.workcountry)
    )
))

df['concat_attr_HomeAddress'] = list(map(
    lambda x: ' '.join(filter(None, x)),
    zip(
        np.where(df.HomestreetAddress == 'DNE', '', df.HomestreetAddress + ','),
        np.where(df.Homelocality == 'DNE', '', df.Homelocality + ','),
        np.where(df.Homeregion == 'DNE', '', df.Homeregion),
        np.where(df.HomepostalCode == 'DNE', '', df.HomepostalCode),
        np.where(df.Homecountry == 'DNE', '', df.Homecountry)
    )
))
