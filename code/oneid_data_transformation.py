import pandas as pd
import logging
from one_id_generator import UserOneIDGenerator


class IAMDataTransformation:
    """
    This class contains data processing and standardization methods.
    """

    def __init__(self, default_ad_list, new_aetna_ad_list, new_corp_list, nonprod_domain_list):
        self.user_oneid_generator = UserOneIDGenerator()
        self.default_ad_list = default_ad_list
        self.new_aetna_ad_list = new_aetna_ad_list
        self.new_corp_ad_list = new_corp_list
        self.nonprod_domain_list = nonprod_domain_list

    def delta_source_vs_graph_for_user_profiles(self, src_usrs_df: pd.DataFrame, gdb_usrs: pd.DataFrame):
        """
        Transform data to identify the delta of users.
        Args:
            src_usrs_df (pd.DataFrame): dataframe of users from source
            gdb_usrs (pd.DataFrame): dataframe of users from graph
        Returns:
            delta_users (List): users from source not in the graph
        """
        try:
            logging.info("Identifying delta of users")
            d1 = src_usrs_df['CVSResourceid'].tolist()
            if len(gdb_usrs) == 0:
                d2 = []
            else:
                d2 = gdb_usrs['employeeNumber'].tolist()
            delta_users = list(set(d1) - set(d2))
            logging.info(f"Delta users: {len(delta_users)}")

            d1 = src_usrs_df['accountstatus'].tolist()
            if len(gdb_usrs) == 0:
                d2 = []
            else:
                d2 = gdb_usrs['accountstatus'].tolist()
            delta_labels = list(set(d1) - set(d2))
            logging.info(f"Delta labels: {len(delta_labels)}")

            return delta_users, src_usrs_df.loc[src_usrs_df['accountstatus'].isin(delta_labels), 'CVSResourceid'].tolist()
        except Exception as e:
            raise Exception(str(e))

    def delta_sro_vs_gdb_usrs_usraccts_profiles(
        self,
        src_usraccts_for_each_usr: pd.DataFrame,
        gdb_usrs_with_usraccts_has_oneid_list: pd.DataFrame
    ):
        """
        Transform data to identify the delta of users with user accounts that don't have OneIDs.
        Args:
            src_usraccts_for_each_usr (pd.DataFrame): dataframe of users from source
            gdb_usrs_with_usraccts_has_oneid_list (pd.DataFrame): dataframe of users from graph
        Returns:
            users_details_list, removed_user_accounts, new_pas_data
        """
        logging.info("Identifying delta of users and user accounts")
        new_pas_data = []
        removed_user_accounts = []

        df1 = pd.DataFrame(src_usraccts_for_each_usr)
        df2 = pd.DataFrame(gdb_usrs_with_usraccts_has_oneid_list)

        # Handle removed accounts
        if not len(df1):
            df1['concat_attr_col2'] = None
        removed_accounts = set(df2['concat_attr_col2']) - set(df1['concat_attr_col2']) if df2['concat_attr_col2'].tolist() != [None] else set()

        for account in removed_accounts:
            if account is not None and 'UNASSIGNED' not in account:
                split_account = account.split('|')
                removed_user_accounts.append({
                    'CVSResourceid': split_account[0],
                    'samaccountname_r': split_account[1],
                    'domain_n': split_account[2],
                    'label': 'UNASSIGNED'
                })

        if not len(df1):
            users_details_list1 = pd.DataFrame(columns=[
                "E_EmployeeID",
                "user_oneid",
                "user_accounts",
                "lastuseraccountoneid"
            ])
            return users_details_list1, removed_user_accounts, new_pas_data

        df1['usracct_oneid'] = None
        diff_accounts = set(df1['concat_attr_col1']) - set(df2['concat_attr_col1'])
        updated_accounts = set(df1['concat_attr_col1']) - set(df2['concat_attr_col1'])

        # New code to process user account when attributes change
        temp_df = df2[['E_EmployeeID', 'PrimaryAuth']]
        temp_df = temp_df.groupby('E_EmployeeID')['PrimaryAuth'].any().reset_index()

        updated_df = df1.loc[(~df1["concat_attr_col1"].isin(updated_accounts)) & (~df1["concat_attr_col1"].isin(diff_accounts))]
        indices_to_drop = []

        if not updated_df.empty:
            account_type_dict = dict(zip(df2['concat_attr_col'], df2['accountType']))
            updated_df = pd.merge(updated_df, temp_df, how='left', on='E_EmployeeID')
            updated_df['accountType'] = updated_df['concat_attr_col'].map(account_type_dict)

            for i, row in updated_df.iterrows():
                if row['PrimaryAuth'] or row['accountType'] != 'Primary':
                    logging.warning(
                        f"Found admin description and extensionattribute changed for "
                        f"(employeeNumber, samaccountname, domain) in {row['concat_attr_col'].split('|')}"
                    )
                    indices_to_drop.append(i)
                else:
                    diff_accounts.add(row['concat_attr_col'])

            updated_df.drop(indices_to_drop, inplace=True)
            for i, row in updated_df.iterrows():
                new_pas_data.append({
                    'E_EmployeeID': row['concat_attr_col'].split('|')[0],
                    'samaccountname': row['concat_attr_col'].split('|')[1],
                    'domain': row['concat_attr_col'].split('|')[2]
                })

        logging.info(f"Total removed user accounts: {len(removed_user_accounts)}")
        logging.info(f"Total new user accounts: {len(diff_accounts)}")

        # Build final DataFrame
        df1_tbm = df1.loc[df1["concat_attr_col"].isin(diff_accounts)][
            ["E_EmployeeID", "usracct_oneid", "samaccountname", "domain", "extensionattributes", "admin_description"]
        ].copy()
        df2 = df2[['E_EmployeeID', 'user_oneid', 'lastuseraccountoneid']].drop_duplicates(subset='E_EmployeeID', keep='first')
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

    def extract(self, group):
        oneid = group.user_oneid.values[0]
        lastuseraccountoneid = group.lastuseraccountoneid.values[0]
        user_accounts = [
            {
                "samaccountname": record.samaccountname,
                "usracct_oneid": None,
                "domain": record.domain,
                "extensionattribute3": record.extensionattributes,
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

    # Placeholder for other methods (determine_privileged_accounts, compute_primaryAuthSystem_nodes, etc.)
    # These methods can be cleaned and formatted similarly following the same pattern.
