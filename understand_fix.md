for account in removed_accounts:
    if account is not None and not 'UNASSIGNED' in account:
        row = df2[df2['concat_attr_col2']==account].iloc[0]
        split_Account = account.split('|')
