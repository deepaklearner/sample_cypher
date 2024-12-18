I have two dataframes. 

The key columns in df1 are E_EmployeeID, accountType and concat_attr_col2 (employeeNumber,|, userName,|, targetSystem,|, acctlabel)

They key columns in df2 are E_EmployeeID and concat_attr_col2 (employeeNumber,|, userName,|, targetSystem,|, acctlabel)

Then i am converting concat_attr_col2 to set and doing df1 - df2.


df1 and df2 are now list containg dictionaries like:
[{'CVSResourceid': '1','samaccountname':'N75001', 'domain_r':'AETH','label':'UNASSIGNED'},
{'CVSResourceid': '2','samaccountname':'N75002', 'domain_r':'AETT','label':'UNASSIGNED'}]

But i want to add the column accountType also in the result, how to do that?
i dont want to use accountType  in comparison

i dont want to convert the result to dataframe. I want to keep it as list of dictionaries like [{'CVSResourceid': '1','samaccountname':'N75001', 'domain_r':'AETH','label':'UNASSIGNED'},
{'CVSResourceid': '2','samaccountname':'N75002', 'domain_r':'AETT','label':'UNASSIGNED'}]

df1_set is just df1['concat_attr_col2']) and df2_set  is just df2['concat_attr_col2'])

how to check if any value for accountType is "primary" in [{'CVSResourceid': 3,
  'samaccountname': 'user3',
  'domain_r': 'system3',
  'label': 'label3',
  'accountType': 'C'}]

  extract those dictionaries only for which accountType is primary

  how to check if for column domain_r is there any value in the dataframe df2 which is secondary

  for matching E_EmployeeID in df2 with CVSResourceID in the output "[
    {'CVSResourceid': 4, 'samaccountname': 'user4', 'domain_r': 'system4', 'label': 'label4', 'accountType': 'primary'},
    {'CVSResourceid': 5, 'samaccountname': 'user5', 'domain_r': 'system5', 'label': 'label5', 'accountType': 'primary'}
]"