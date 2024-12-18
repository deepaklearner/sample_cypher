Here’s the properly aligned and corrected code for better readability:

```python
def delta_src_vs_gdb_usrs_usraccts_profiles(
    self, 
    src_usraccts_for_each_usr: pd.DataFrame, 
    gdb_usrs_with_usraccts_has_oneid_list: pd.DataFrame
):
    """
    Transform data to identify the delta of users with useraccounts that don't have OneIDs.

    Args:
        src_usraccts_for_each_usr (pd.DataFrame): dataframe of users from source.
        gdb_usrs_with_usraccts_has_oneid_list (pd.DataFrame): dataframe of users from graph.

    Returns:
        List: Delta of users with UserAccounts from source not in the graph.
    """
    logging.info("Identifying delta of users and useraccounts")
    new_pas_data = []
    removed_user_accounts = []

    df1 = pd.DataFrame(src_usraccts_for_each_usr)
    df2 = pd.DataFrame(gdb_usrs_with_usraccts_has_oneid_list)

    # New code to handle removed_accounts
    if not df1.empty:
        df1['concat_attr_col'] = None

    removed_accounts = (
        set(df2['concat_attr_col']) - set(df1['concat_attr_col']) 
        if df2['concat_attr_col'].tolist() != [None] else set()
    )

    for account in removed_accounts:
        if account and 'UNASSIGNED' not in account:
            split_account = account.split('|')
            removed_user_accounts.append({
                'CVSResourceid': split_account[0],
                'samaccountname_r': split_account[1],
                'domain_r': split_account[2],
                'label': 'UNASSIGNED'
            })

    if df1.empty:
        users_details_list1 = pd.DataFrame(columns=[
            "E_EmployeeID", "user_oneid", "user_accounts", "lastuseraccountoneid"
        ])
        return users_details_list1, removed_user_accounts, new_pas_data

    df1['usracct_oneid'] = None
    diff_accounts = set(df1['concat_attr_col']) - set(df2['concat_attr_col'])
    updated_accounts = set(df1['concat_attr_col1']) - set(df2['concat_attr_col1'])

    # Process user accounts when attributes change for a user who doesn't have PAS in graph
    temp_df = df2[['E_EmployeeID', 'PrimaryAuth']].groupby("E_EmployeeID")['PrimaryAuth'].any().reset_index()
    updated_df = df1.loc[
        (df1["concat_attr_col1"].isin(updated_accounts)) & 
        ~(df1["concat_attr_col"].isin(diff_accounts))
    ]
    indices_to_drop = []

    if not updated_df.empty:
        account_type_dict = dict(zip(df2['concat_attr_col'], df2['accountType']))
        updated_df = pd.merge(updated_df, temp_df, how='left', on='E_EmployeeID')
        updated_df['accountType'] = updated_df['concat_attr_col'].map(account_type_dict)

        for i, row in updated_df.iterrows():
            if row['PrimaryAuth'] or row['accountType'] != 'Primary':
                logging.warning(
                    f"Found admin_description and extensionattribute3 changed for "
                    f"(employeeNumber, samaccountname, domain) in "
                    f"({', '.join(row['concat_attr_col'].split('|'))})"
                )
                indices_to_drop.append(i)
            else:
                diff_accounts.add(row['concat_attr_col'])
                new_pas_data.append(dict(zip(
                    ['E_EmployeeID', 'samaccountname', 'domain'],
                    row['concat_attr_col'].split('|')
                )))

        updated_df.drop(indices_to_drop, inplace=True)

        if not updated_df['PrimaryAuth'].any():
            diff_accounts -= set(updated_df['concat_attr_col'].values)

    logging.info(f"Total removed user accounts: {len(removed_user_accounts)}")
    logging.info(f"Total new user accounts: {len(diff_accounts)}")

    df1_tbm = df1.loc[df1["concat_attr_col"].isin(diff_accounts)][[
        "E_EmployeeID", "usracct_oneid", "samaccountname", "domain", 
        "extensionattribute3", "admin_description"
    ]].copy()

    df2 = df2[['E_EmployeeID', 'user_oneid', 'lastuseraccountoneid']].drop_duplicates(
        subset='E_EmployeeID', keep='first'
    )
    df1_tbm = pd.merge(df1_tbm, df2, on='E_EmployeeID', how='left')

    diff_users = set(df1_tbm['E_EmployeeID'])

    try:
        users_details_list = (
            df1_tbm[df1_tbm["E_EmployeeID"].isin(diff_users)]
            .groupby('E_EmployeeID')
            .apply(lambda group: self.extract(group))
            .values
        )
    except Exception as e:
        logging.error(e)
        users_details_list1 = pd.DataFrame(users_details_list.tolist())
        return users_details_list1, removed_user_accounts, new_pas_data

    return users_details_list, removed_user_accounts, new_pas_data

def extract(self, group):
    oneid = group.user_oneid.values[0]
    lastuseraccountoneid = group.lastuseraccountoneid.values[0]
    user_accounts = [
        {
            "samaccountname": record.samaccountname,
            "usracct_oneid": None,
            "domain": record.domain,
            "extensionattribute3": record.extensionattribute3,
            "admin_description": record.admin_description
        } 
        for _, record in group.iterrows()
    ]
    return {
        "E_EmployeeID": group.name,
        "user_oneid": oneid,
        "user_accounts": user_accounts,
        "lastuseraccountoneid": lastuseraccountoneid
    }
```

This code should now be aligned and readable, making it easier to debug and maintain. Let me know if you need further modifications!