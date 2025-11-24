
    # Step 3: Compute delta of user accounts
    delta_usrs_usraccts_list, delta_usraccts_removed, new_pas_data = \
        iam_data_transformation.delta_src_vs_gdb_usrs_usraccts_profiles(src_usraccts_for_each_usr,gdb_usrs_with_usraccts_has_oneid)

    # Step 4: Logging
    logging.info(f"Number of users with new useraccounts: {len(delta_usrs_usraccts_list)}")

    # Step 6: Process new/updated useraccounts
    if len(delta_usrs_usraccts_list):

        try:
            # Create index for EmployeeID
            delta_usrs_usraccts_list["E_EmployeeID_index"] = delta_usrs_usraccts_list["E_EmployeeID"]
            delta_usrs_usraccts_list.set_index("E_EmployeeID_index", inplace=True)

            # Fetch primary account domains
            primary_account_domains = iam_create_graph.get_user_primary_domain(users)

            # Update primary account domain list using PAS data
            if new_pas_data is not None:
                for item in new_pas_data:
                    primary_account_domains.loc[
                        primary_account_domains["E_EmployeeID"] == emp_id,
                        "domains"
                    ] = primary_account_domains["domains"].apply(
                        lambda x: [i for i in x if i!=item['domain']])

            # Initialize new domain fields
            delta_usrs_usraccts_list["domains"] = [[]]*len(delta_usrs_usraccts_list)
            delta_usrs_usraccts_list["primaryAuthDomain"] = [[]]*len(delta_usrs_usraccts_list)
            delta_usrs_usraccts_list["primaryAuthDomainName"] = [[]]*len(delta_usrs_usraccts_list)
            delta_usrs_usraccts_list["corpAccountNames"] = [[]]*len(delta_usrs_usraccts_list)

            # Fill domain-related fields for each employee
            for emp in primary_account_domains.index:
                delta_usrs_usraccts_list.at[emp, "domains"] = primary_account_domains.at[emp, "domains"]
                delta_usrs_usraccts_list.at[emp, "primaryAuthDomain"] = primary_account_domains.at[emp, "primaryAuthDomain"]
                delta_usrs_usraccts_list.at[emp, "primaryAuthDomainName"] = primary_account_domains.at[emp, "primaryAuthDomainName"]
                delta_usrs_usraccts_list.at[emp, "corpAccountNames"] = primary_account_domains.at[emp, "corpAccountNames"]

            # Step 7: Compute oneIDs for each user
            delta_users_useraccounts_oneIDs_list = delta_usrs_usraccts_list.apply(
                lambda user_data: iam_data_transformation.compute_oneIDs_for_useraccounts(user_data),
                axis=1
            ).tolist()
        except Exception as e:
            logging.error(f"Error processing delta user accounts: {e}") 