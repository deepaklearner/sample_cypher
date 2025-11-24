import pandas as pd
import logging


class IAMDataTransformation:
    def __init__(self, default_ad_list=None, new_corp_ad_list=None,
                 new_aetna_ad_list=None, nonprod_domain_list=None):
        self.user_oneid_generator = UserOneIDGenerator()
        self.default_ad_list = default_ad_list
        self.new_corp_ad_list = new_corp_ad_list
        self.new_aetna_ad_list = new_aetna_ad_list
        self.nonprod_domain_list = nonprod_domain_list

    def delta_src_vs_gdb_usrs_usraccts_profiles(
        self, src_usraccts_for_each_usr: pd.DataFrame, gdb_usrs_with_usraccts_has_oneid_list: pd.DataFrame
    ):
        """
        Identify delta of users with useraccounts that don't have OneIDs.
        """
        logging.info("Identifying delta of users and useraccounts")
        new_pas_data = []
        removed_user_accounts = []
        df1 = pd.DataFrame(src_usraccts_for_each_usr)
        df2 = pd.DataFrame(gdb_usrs_with_usraccts_has_oneid_list)

        if not len(df1):
            df1['concat_attr_col2'] = None
        removed_accounts = set(df2['concat_attr_col2']) - set(df1['concat_attr_col2']) \
            if df2['concat_attr_col2'].tolist() != [None] else set()
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
                "E_EmployeeID", "user_oneid", "user_accounts", 'lastuseraccountoneid'
            ])

        df1['usracct_oneid'] = None
        diff_accounts = set(df1['concat_attr_col']) - set(df2['concat_attr_col'])
        updated_accounts = set(df1['concat_attr_col1']) - set(df2['concat_attr_col1'])

        temp_df = df2[['E_EmployeeID', 'PrimaryAuth']]
        temp_df = temp_df.groupby('E_EmployeeID')['PrimaryAuth'].any().reset_index()

        updated_df = df1.loc[
            (df1["concat_attr_col1"].isin(updated_accounts)) & ~(df1["concat_attr_col1"].isin(diff_accounts))
        ]

        indices_to_drop = []

        if not updated_df.empty:
            account_type_dict = dict(zip(df2['concat_attr_col'], df2['accountType']))
            updated_df = pd.merge(updated_df, temp_df, how='left', on='E_EmployeeID')
            updated_df['accountType'] = updated_df['concat_attr_col'].map(account_type_dict)

            for i, row in updated_df.iterrows():
                if row['PrimaryAuth'] or row['accountType'] != 'Primary':
                    logging.warning(
                        f"Found admin description and extensionattribute changed for {row['concat_attr_col'].split('|')}"
                    )
                    indices_to_drop.append(i)
                else:
                    diff_accounts.add(row['concat_attr_col'])

            updated_df.drop(indices_to_drop, inplace=True)
            if not updated_df['PrimaryAuth'].any:
                diff_accounts.update(updated_df['concat_attr_col'].values)

        logging.info(f"Total removed user accounts: {len(removed_user_accounts)}")
        logging.info(f"Total new user accounts: {len(diff_accounts)}")

        df1_tbm = df1.loc[df1["concat_attr_col"].isin(diff_accounts)][[
            "E_EmployeeID", "usracct_oneid", "samaccountname", "domain",
            "extensionattributes", "admin_description"
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
            users_details_list1 = pd.DataFrame(users_details_list.tolist())
        except Exception as e:
            logging.error(e)

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

    def check_user_account(self, user_account, domain_list, account_prefixes):
        return (
            user_account['domain'].lower() in domain_list
            and user_account['samaccountname']
            and any(user_account['samaccountname'].lower().startswith(prefix) for prefix in account_prefixes)
        )

    def determine_privileged_accounts(self, user_accounts_data):
        """
        Compute privileged accounts and their OneIDs.
        """
        privileged_accounts_oneids_list = []
        CVSResourceid = user_accounts_data["E_EmployeeID"]
        user_oneid = user_accounts_data['user_oneid']
        last_useraccount_oneid = user_accounts_data['lastuseraccountoneid']

        for user_account in user_accounts_data["user_accounts"]:
            if (
                self.check_user_account(user_account, self.default_ad_list + self.new_corp_ad_list, ["a_", "adm_"])
                or self.check_user_account(user_account, ["aeth", "aett", "atha"] + self.new_aetna_ad_list, ["zz", "ma", "mn"])
                or (user_account['domain'].lower() in self.new_corp_ad_list + self.new_aetna_ad_list + ["aett", "aethq"]
                    and "admin" in str(user_account['samaccountname']).lower())
            ):
                oneID = self.user_oneid_generator.useracct_oneid_generator(user_oneid, last_useraccount_oneid)
                last_useraccount_oneid = oneID
                temp_dict = {
                    "samaccountname": user_account['samaccountname'],
                    "extensionattribute3": user_account['extensionattribute3'],
                    "oneID": oneID,
                    "AccountType": "Privileged",
                    "CVSResourceid": CVSResourceid,
                    "domain": user_account['domain'],
                    "admin_description": user_account['admin_description']
                }
                privileged_accounts_oneids_list.append(temp_dict)

        return privileged_accounts_oneids_list, last_useraccount_oneid

    def compute_PrimaryAuthsystem_nodes(self, remaining_accounts_list, primary_account_domains):
        try:
            return_var = None

            # Step 1: Filter user_accounts based on target system
            aeth_accounts = [
                account for account in remaining_accounts_list["user_accounts"]
                if account.get("domain") == "AETH"
            ]

            other_accounts = [
                account for account in remaining_accounts_list["user_accounts"]
                if account.get("domain") != "AETH"
            ]

            # Step 2: Combine the filtered accounts
            ordered_user_accounts = aeth_accounts + other_accounts

            # Step 3: Update remaining_accounts_list with ordered_user_accounts
            ordered_accounts = remaining_accounts_list.copy()
            ordered_accounts["user_accounts"] = ordered_user_accounts

            primary_auth = [] if not len(primary_account_domains[1]) else primary_account_domains[1]

            for user_account in ordered_accounts["user_accounts"]:

                if (
                    user_account["domain"] == "AETH"
                    and (
                        user_account["samaccountname"].lower().startswith("a") or
                        user_account["samaccountname"].lower().startswith("n")
                    )
                    and (
                        str(user_account.get("admin_description")) == "nan"
                        or user_account.get("admin_description") is None
                        or user_account.get("admin_description") in ["NULL", "", "DNE"]
                    )
                    or (
                        user_account["domain"].lower() in self.default_ad_list
                        and "cloud" in str(user_account.get("extensionattribute", "")).lower()
                    )
                ):
                    primary_auth.append(user_account["domain"])

                if (
                    user_account["domain"] not in primary_account_domains[1]
                    and len(primary_auth) == 1
                ):
                    user_account["PrimaryAuthsystem"] = True
                    user_account["AccountType"] = "Primary"
                    user_account["oneID"] = ordered_accounts["oneID"]
                    user_account["CVSResourceid"] = ordered_accounts["E_EmployeeID"]

                    return_var = user_account

                    primary_account_domains[0].append(user_account["domain"])
                    primary_account_domains[1].append(user_account["domain"])
                    primary_account_domains[2].append(user_account["samaccountname"])

            if len(primary_auth) > 1:
                logging.warning(
                    f'Found more than one primary auth system for user '
                    f'{ordered_accounts["E_EmployeeID"]} and domain names {", ".join(primary_auth)}'
                )

            return return_var, primary_account_domains


        except Exception as e:
            logging.error(f"Exception occurred at compute_PrimaryAuthsystem_nodes: {str(e)}")


    def determine_primary_accounts(
        self, remaining_accounts_list, domains, primary_account_domains1,
        primaryAuthDomainName, corpAccountNames1
    ):
        """
        Compute Primary accounts and their OneIDs.
        """
        try:
            useraccounts_with_oneids_list = []
            primary_account_domains = [domains, primary_account_domains1, primaryAuthDomainName, corpAccountNames1]

            usracct_with_primaryauthsystem, primary_account_domains = self.compute_PrimaryAuthsystem_nodes(
                remaining_accounts_list, primary_account_domains
            )

            if usracct_with_primaryauthsystem is not None:
                useraccounts_with_oneids_list.append(usracct_with_primaryauthsystem)

            for user_account in remaining_accounts_list["user_accounts"]:
                user_account["PrimaryAuthSystem"] = False
                user_account["AccountType"] = "Primary"
                user_account["oneID"] = remaining_accounts_list["oneID"]
                user_account["CVSResourceid"] = remaining_accounts_list["E_EmployeeID"]
                useraccounts_with_oneids_list.append(user_account)
                primary_account_domains[0] += [user_account['domain']]

            return useraccounts_with_oneids_list
        except Exception as e:
            logging.error(f"Exception at determine_primary_accounts: {str(e)}")
            return []

    def determine_secondary_accounts_list(self, remaining_accounts_list, usraccts_last_oneid):
        """
        Compute Secondary accounts and their OneIDs.
        """
        try:
            secondary_accounts_oneids_list = []
            CVSResourceid = remaining_accounts_list["E_EmployeeID"]
            user_oneid = remaining_accounts_list['user_oneid']

            for user_account in remaining_accounts_list["user_accounts"]:
                oneID = self.user_oneid_generator.useracct_oneid_generator(user_oneid, usraccts_last_oneid)
                usraccts_last_oneid = oneID
                temp_dict = {
                    "samaccountname": user_account['samaccountname'],
                    "domain": user_account['domain'],
                    "admin_description": user_account['admin_description'],
                    "extensionattributes": user_account['extensionattribute3'],
                    "PrimaryAuthsystem": False,
                    "AccountType": "Secondary",
                    "oneID": oneID,
                    "CVSResourceid": CVSResourceid
                }
                secondary_accounts_oneids_list.append(temp_dict)

            return secondary_accounts_oneids_list, usraccts_last_oneid
        except Exception as e:
            logging.error(f"Exception at determine_secondary_accounts_list: {str(e)}")
            return [], usraccts_last_oneid

    def compute_oneIDs_for_useraccounts(self, user_data):
        """
        Compute OneIDs for all user accounts, including privileged, primary, and secondary accounts.
        """
        try:
            all_users_useraccounts_final_data = []

            domains = user_data['domains'].copy()
            primaryAuthDomain = user_data['primaryAuthDomain'].copy()
            primaryAuthDomainName = user_data['primaryAuthDomainName'].copy()
            corpAccountNames = user_data['corpAccountNames'].copy()
            usraccts_last_oneid = user_data["lastuseraccountoneid"]

            privileged_accounts, usraccts_last_oneid = self.determine_privileged_accounts(user_data)
            user_data['lastuseraccountoneid'] = usraccts_last_oneid

            total_user_accounts_ids = [
                (usr_acct["samaccountname"], usr_acct["domain"])
                for usr_acct in user_data["user_accounts"]
            ]
            privileged_samaccounts_ids = [
                (usr_acct["samaccountname"], usr_acct["domain"]) for usr_acct in privileged_accounts
            ]

            remaining_accounts_ids_list = list(set(total_user_accounts_ids) - set(privileged_samaccounts_ids))

            remaining_accounts_data_list = {
                "E_EmployeeID": user_data["E_EmployeeID"],
                "oneID": user_data["user_oneid"],
                "user_accounts": [
                    next(
                        usr_acct_data for usr_acct_data in user_data["user_accounts"]
                        if usr_acct_data['samaccountname'] == samaccount and usr_acct_data['domain'] == domain
                    )
                    for (samaccount, domain) in remaining_accounts_ids_list
                ]
            }

            primary_accounts = self.determine_primary_accounts(
                remaining_accounts_data_list, domains, primaryAuthDomain,
                primaryAuthDomainName, corpAccountNames
            )
            primary_accounts_ids_list = [(acct["samaccountname"], acct["domain"]) for acct in primary_accounts]

            remaining_accounts_ids_list = list(set(remaining_accounts_ids_list) - set(primary_accounts_ids_list))
            remaining_accounts_data_list = {
                "E_EmployeeID": user_data["E_EmployeeID"],
                "user_oneid": user_data["user_oneid"],
                "user_accounts": [
                    next(
                        usr_acct_data for usr_acct_data in user_data["user_accounts"]
                        if usr_acct_data['samaccountname'] == samaccount and usr_acct_data['domain'] == domain
                    )
                    for (samaccount, domain) in remaining_accounts_ids_list
                ]
            }

            secondary_accounts, usraccts_last_oneid = self.determine_secondary_accounts_list(
                remaining_accounts_data_list, usraccts_last_oneid
            )
            user_data['lastuseraccountoneid'] = usraccts_last_oneid

            all_users_useraccounts_final_data.extend(privileged_accounts + primary_accounts + secondary_accounts)
            return all_users_useraccounts_final_data
        except Exception as e:
            logging.error(f"Error at compute_oneIDs_for_useraccounts: {str(e)}")
            return []
