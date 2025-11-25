Perfect! Let’s update your **Step 6** in `load_edw.py` and `one_id_transformation.py` to include **strict rejection for multiple eligible PrimaryAuth accounts**.

I’ll provide **Python-flavored pseudocode** with clear comments.

---

# 🔹 Modified Step 6 with Strict Rejection

```python
# Step 6: Process new/updated useraccounts with PrimaryAuth computation and reconciliation
if len(delta_usrs_usraccts_list):

    # Create index for EmployeeID
    delta_usrs_usraccts_list["E_EmployeeID_index"] = delta_usrs_usraccts_list["E_EmployeeID"]
    delta_usrs_usraccts_list.set_index("E_EmployeeID_index", inplace=True)

    # Fetch Neo4j current user accounts (primary/secondary info)
    neo4j_usraccts = iam_create_graph.fetch_users_all_accounts(users)

    # Initialize fields for domain & primaryAuth info
    delta_usrs_usraccts_list["domains"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["primaryAuthDomain"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["primaryAuthDomainName"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["corpAccountNames"] = [[] for _ in range(len(delta_usrs_usraccts_list))]
    delta_usrs_usraccts_list["computedPrimaryAuth"] = False  # default

    for emp_id in delta_usrs_usraccts_list.index:

        emp_accounts = delta_usrs_usraccts_list.loc[emp_id]
        neo4j_accounts = neo4j_usraccts.get(emp_id, [])

        # --- Compute PrimaryAuth based on EDW rules ---
        # Rule: targetSystem in ['CORP','CSARMARK','CVS'] AND 'cloud' in extensionAttribute3
        eligible_accounts = [
            acc for acc in emp_accounts
            if acc["targetSystem"] in ['CORP','CSARMARK','CVS']
            and 'cloud' in acc.get("extensionAttribute3", "").lower()
        ]

        # --- STRICT REJECTION FOR MULTIPLE ELIGIBLE ACCOUNTS ---
        if len(eligible_accounts) > 1:
            logging.error(f"Employee {emp_id} has multiple eligible primary accounts in EDW. Rejecting user for manual review.")
            continue  # Skip reconciliation for this employee

        elif len(eligible_accounts) == 1:
            primary_candidate = eligible_accounts[0]
            delta_usrs_usraccts_list.at[emp_id, "computedPrimaryAuth"] = True

        else:  # len(eligible_accounts) == 0
            primary_candidate = None

        # --- Reconcile with Neo4j ---
        neo4j_primary = next((acc for acc in neo4j_accounts if acc.get("PrimaryAuth") == True), None)

        if primary_candidate:
            if neo4j_primary:
                if primary_candidate["samaccountname"] != neo4j_primary["samaccountname"]:
                    # Switch primary/secondary
                    logging.info(f"Employee {emp_id}: Switching primary account to {primary_candidate['samaccountname']}")
                    neo4j_primary["PrimaryAuth"] = False
                    primary_candidate["PrimaryAuth"] = True
                else:
                    primary_candidate["PrimaryAuth"] = True
            else:
                # No primary exists in Neo4j: assign primary
                primary_candidate["PrimaryAuth"] = True

        # --- Assign secondary accounts ---
        for acc in emp_accounts:
            if acc != primary_candidate:
                acc["PrimaryAuth"] = False

        # --- Propagate PAS primary across other domains ---
        pas_accounts = [acc for acc in emp_accounts if acc["targetSystem"] in ['CORP','CSARMARK','CVS']]
        if primary_candidate in pas_accounts:
            for acc in emp_accounts:
                if acc != primary_candidate and acc["PrimaryAuth"]:
                    logging.info(f"Employee {emp_id}: Demoting incorrect primary in other domain: {acc['samaccountname']}")
                    acc["PrimaryAuth"] = False

        # --- Populate domain-related fields ---
        delta_usrs_usraccts_list.at[emp_id, "domains"] = [acc["targetSystem"] for acc in emp_accounts]
        delta_usrs_usraccts_list.at[emp_id, "primaryAuthDomain"] = [primary_candidate["targetSystem"]] if primary_candidate else []
        delta_usrs_usraccts_list.at[emp_id, "primaryAuthDomainName"] = [primary_candidate["samaccountname"]] if primary_candidate else []
        delta_usrs_usraccts_list.at[emp_id, "corpAccountNames"] = [acc["samaccountname"] for acc in emp_accounts if acc["targetSystem"] in ['CORP','CSARMARK','CVS']]
```

---

# ✅ Key Updates

1. **Added strict rejection**:

```python
if len(eligible_accounts) > 1:
    logging.error(f"Employee {emp_id} has multiple eligible primary accounts in EDW. Rejecting user for manual review.")
    continue
```

* If multiple accounts match the PrimaryAuth rule, the employee is skipped and logged for manual review.
* No reconciliation occurs for ambiguous data.

2. **All old Neo4j-based rejection logic is removed.**
3. Primary/secondary assignment and PAS propagation remain intact.
4. Domain fields (`domains`, `primaryAuthDomain`, etc.) updated only if the employee passes validation.

---

If you want, I can also **draw a clear visual flowchart including the strict rejection step** so your team can use it for documentation and code walkthroughs.

Do you want me to create that diagram next?
