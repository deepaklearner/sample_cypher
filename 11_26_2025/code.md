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