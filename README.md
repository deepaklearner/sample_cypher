1. Read EDW table edwmaster identitymaster (identity master table) and create all the identities (user_id) in neo4j.
### **Table 1: Identity Master** (`edwmaster.identitymaster`)  

| `global_id` | `np_identity_id` | `authorizer_account_id` |  
|-----------------|-----------------|------------------------|  
| S000436         | S000436        | N940393                 |  

2. Read accounts from EDW table aethusers_clone i.e. column iamglobalidentifier (coming from AD)
### **Table 2: User Accounts** (`aethusers_clone`)  

| `user_id`   | `samaccountname` | `domain` | `accountdescription`                 | `iamglobalidentifier` |  
|------------|-----------------|----------|-------------------------------------|----------------------|  
| 5987396906 | S061628         | AETH     | Dev service account for Glide     | S061628             |  
| 5987396907 | S061628         | AETHQ    | Dev service account for Glide     | S061628             |  


3. This application account (iamglobalidentifier) has to be coorelated with Application Identity Its possible to have multiple accounts for an identity.
Right now, we don't want to load test domains. We only want to load prod domain data (mainly 6 prod domains).
Match iamglobalidentifier data(from accounts table) with user_id column (table edwmaster.globalidentity) (here user_id is identity)

### **Table 3: Global Identity Mapping** (`edwmaster.globalidentity`)  

| `user_id`  | `user_type`  | `p_identity_id` | `authorizer_account_id` |  
|-----------|------------|-----------------|------------------------|  
| S061628   | Non Person | S000436         | N940393                |  

And it goes to applicate status and other stuff.