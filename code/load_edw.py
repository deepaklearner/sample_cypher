# Step 1: Fetch user accounts from EDU
src_usraccts_for_each_usr = iam_data_ingestion_edw.fetch_useraccounts_from_edw(
    feature_name,
    sql_edw_query_param,
    users
)

# Step 2: Fetch users from Graph DB who have useraccounts with oneID
gdb_usrs_with_usraccts_has_oneid = iam_create_graph.fetch_users_with_useraccounts_has_oneid(
    users,
    domain_list
)

# Step 3: Compute delta of user accounts
delta_usrs_usraccts_list, delta_usraccts_removed, new_pas_data = \
    iam_data_transformation.delta_sro_vs_gdb_usrs_usraccts_profiles(
        src_usraccts_for_each_usr,
        gdb_usrs_with_usraccts_has_oneid
    )

# Step 4: Logging
logging.info(
    f"Number of users with new useraccounts: {len(delta_usrs_usraccts_list)}"
)

# Step 5: Handle removed useraccounts
if len(delta_usraccts_removed):
    try:
        iam_create_graph.update_removed_useraccounts(delta_usraccts_removed)
    except Exception as e:
        logging.error(e)

# Step 6: Process new/updated useraccounts
if len(delta_usrs_usraccts_list):

    # Create index for EmployeeID
    delta_usrs_usraccts_list["E_EmployeeID_index"] = delta_usrs_usraccts_list["E_EmployeeID"]
    delta_usrs_usraccts_list.set_index("E_EmployeeID_index", inplace=True)

    # Fetch primary account domains
    primary_account_domains = iam_create_graph.get_user_primary_domain(users)

    # Update primary account domain list using PAS data
    if new_pas_data is not None:
        for item in new_pas_data:
            emp_id = item["E_EmployeeID"]
            domain = item["domain"]

            primary_account_domains.loc[
                primary_account_domains["E_EmployeeID"] == emp_id,
                "domains"
            ] = primary_account_domains["domains"].apply(
                lambda x: x + [domain] if domain not in x else x
            )

    # Initialize new domain fields
    delta_usrs_usraccts_list["domains"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["primaryAuthDomain"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["primaryAuthDomainName"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["corpAccountNames"] = [[] for _ in range(len(delta_usrs_usraccts_list))]

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
