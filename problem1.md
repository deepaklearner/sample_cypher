Step1:

I have a pandas dataframe df1, with columns E_EmployeeID, samaccountname, domain.
And I have a pandas dataframe df2, with columns E_EmployeeID, samaccountname, domain, accountType

I want to add a new column accountType in df1 based on samaccountname.
there are some other columns also in df2 and df1. i want to retain them as it is.

Solution:
# Assuming df1 and df2 are already defined
# Merge df1 and df2 on 'samaccountname', and select only the 'accountType' column from df2
df1 = pd.merge(df1, df2[['E_EmployeeID','samaccountname', 'domain','accountType']], on=['E_EmployeeID','samaccountname','domain'], how='left')


Step2:

Now I have a list of dictionaries removed_accounts.
removed_accounts = [
    {'CVSResourceid': '1','samaccountname':'N75001', 'domain_r':'AETH','label':'UNASSIGNED','accountType':'Primary'},
    {'CVSResourceid': '2','samaccountname':'N75002', 'domain_r':'AETT','label':'UNASSIGNED','accountType':'Primary'}]
I want to search for combination: CVSResourceid, samaccountname, domain_r for accountType='Primary' for each dictionary entry in my list in df1, if df1 has  accountType='Secondary' present.

df1 is a pandas dataframe and has these columns: 
'E_EmployeeID','samaccountname', 'domain','accountType'.
Here E_EmployeeID is same as CVSResourceid, and domain_r is same as domain.

    '''
    for entry in removed_accounts:
        # Extract the relevant fields from the dictionary
        cvs_resource_id = entry['CVSResourceid']
        samaccountname = entry['samaccountname']
        domain_r = entry['domain_r']
        
        # Check if df1 has a matching entry where accountType is 'Secondary'
        matched_rows = df1[(df1['E_EmployeeID'] == cvs_resource_id) & 
                        (df1['samaccountname'] == samaccountname) & 
                        (df1['domain'] == domain_r) & 
                        (df1['accountType'] == 'Secondary')]
    '''

Step3:
If match found, then update the accountType from Secondary to Primary in df1

    # If matched rows exist, update the accountType from 'Secondary' to 'Primary'
    if not matched_rows.empty:
        df1.loc[(df1['E_EmployeeID'] == cvs_resource_id) & 
                (df1['samaccountname'] == samaccountname) & 
                (df1['domain'] == domain_r) & 
                (df1['accountType'] == 'Secondary'), 'accountType'] = 'Primary'
        print(f"Updated accountType to 'Primary' for {samaccountname}")
    else:
        print(f"No Secondary account found for {samaccountname}")
--
Solution #1: in same for loop

    # Check if df1 has a matching entry where accountType is 'Secondary' and update it
    df1.loc[
        (df1['E_EmployeeID'] == cvs_resource_id) & 
        (df1['samaccountname'] == samaccountname) & 
        (df1['domain'] == domain_r) & 
        (df1['accountType'] == 'Secondary'), 
        'accountType'
    ] = 'Primary'  # Update the accountType to 'Primary'

Solution 2: Separate


    # Find matching rows in df1 where accountType is 'Secondary'
    matched_rows = df1[(df1['E_EmployeeID'] == cvs_resource_id) & 
                       (df1['samaccountname'] == samaccountname) & 
                       (df1['domain'] == domain_r) & 
                       (df1['accountType'] == 'Secondary')]

    # If matched rows exist, update the accountType from 'Secondary' to 'Primary'
    if not matched_rows.empty:
        df1.loc[(df1['E_EmployeeID'] == cvs_resource_id) & 
                (df1['samaccountname'] == samaccountname) & 
                (df1['domain'] == domain_r) & 
                (df1['accountType'] == 'Secondary'), 'accountType'] = 'Primary'
        print(f"Updated accountType to 'Primary' for {samaccountname}")
    else:
        print(f"No Secondary account found for {samaccountname}")