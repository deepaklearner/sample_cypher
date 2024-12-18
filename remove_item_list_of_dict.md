data = [
    {'CVSResourceid': 4, 'samaccountname': 'user4', 'domain_r': 'system4', 'label': 'label4', 'accountType': 'primary'},
    {'CVSResourceid': 5, 'samaccountname': 'user5', 'domain_r': 'system5', 'label': 'label5', 'accountType': 'primary'}
]

# Remove 'accountType' from each dictionary
for item in data:
    del item['accountType']

print(data)