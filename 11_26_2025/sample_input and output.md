Sample input and output:

# INPUT
# data from EDW (mysql database)
remaining_accounts_list = [
    {
        'E_EmployeeID': '2017328','oneID': 'aa00002a3','user_accounts': [
            {
                        'samaccountname': 'C123',
                        'usracct_oneid': None,
                        'domain': 'CORP.CVSCAREMARK',
                        'extensionattribute3': 'CLOUD',
                        'admin_description': ''
                    },
                    {
                        'samaccountname': 'C456',
                        'domain': 'CAREMARKRX',
                        'extensionattribute3': '',
                        'admin_description': ''
                    }
        ]
    }
]

# data fetched from neo4j
primary_account_domains =
 [['CAREMARKRX', 'CAREMARKRX', 'CORP.CVSCAREMARK', 'CORP.CVSCAREMARK'], #domains
 ['CAREMARKRX'] ,     #primaryAuthDomain                   
['C123'],       #PrimaryAuthDomainName
 ['C123']    ,       # corp_account_names                     
[    {
        'samaccountname': 'C456',
        'domain': 'CORP.CVSCAREMARK',
        'extensionattribute3': '',
        'admin_description': ''                # primaryAccounts
    },
    {
        'samaccountname': 'C456',
        'domain': 'CAREMARKRX',
        'extensionattribute3': '',
        'admin_description': ''              # secondaryAccounts
    }
]

# OUTPUT (return_var) - Final desired state after reconciliation
return_var = [
    {
        'samaccountname': 'C123',
        'domain': 'CAREMARKRX',
        'admin_description': '',
        'extensionattribute3': '',
        'PrimaryAuthSystem': True,
        'AccountType': 'Primary',
        'oneID': 'aa00002a3',
        'CVSResourceAccount': False
    },
    {
        'samaccountname': 'C456',
        'domain': 'CAREMARKRX',
        'admin_description': '',
        'extensionattribute3': '',
        'PrimaryAuthSystem': False,
        'AccountType': 'Secondary',
        'oneID': 'aa00002a4',
        'CVSResourceAccount': False
    },
    {
        'samaccountname': 'C123',
        'domain': 'CORP.CVSCAREMARK',
        'admin_description': '',
        'extensionattribute3': 'CLOUD',
        'PrimaryAuthSystem': False,
        'AccountType': 'Secondary',
        'oneID': 'aa00002a3',
        'CVSResourceAccount': False
    },
    {
        'samaccountname': 'C456',
        'domain': 'CORP.CVSCAREMARK',
        'admin_description': '',
        'extensionattribute3': '',
        'PrimaryAuthSystem': False,
        'AccountType': 'Secondary',
        'oneID': 'aa00002a4',
        'CVSResourceAccount': False
    }
]

# Final primary account domains per some grouping logic (example output)
primary_account_domains_final = [
    ['TEST.CVSCAREMARK', 'AETNA'],
    ['AETNA'],
    ['0001'],
    []
]