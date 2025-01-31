Your project involves extracting identity and account-related data from **EDW tables**, processing it, and **loading structured relationships into Neo4j** for better identity correlation. Here’s a breakdown of your workflow:  

---

## **🔹 Project Overview**  
### **Goal**  
- Read **identities** and **user accounts** from EDW tables.  
- **Match & correlate** identities with their respective accounts.  
- **Filter out test domains** and only load **production domain data** into Neo4j.  
- Ensure multiple accounts **can be linked** to a single identity.  

---

## **🔹 Step-by-Step Process**  

### **1️⃣ Read Identity Data (`edwmaster.identitymaster`)**  
- Extract core identity details.  
- Important fields:  
  - **`global_id`** → Main identifier for identity.  
  - **`np_identity_id`** → Non-person identity ID.  
  - **`authorizer_account_id`** → Account that authorizes this identity.  

📌 **Example:**  
| `global_id` | `np_identity_id` | `authorizer_account_id` |  
|------------|-----------------|------------------------|  
| S000436    | S000436         | N940393                |  

---

### **2️⃣ Read User Account Data (`aethusers_clone`)**  
- Extract user accounts from **Active Directory (AD)** sources.  
- Match **`iamglobalidentifier`** with the identity table (`global_id`).  

📌 **Example:**  
| `user_id`   | `samaccountname` | `domain` | `accountdescription`                 | `iamglobalidentifier` |  
|------------|-----------------|----------|-------------------------------------|----------------------|  
| 5987396906 | S061628         | AETH     | Dev service account for Glide     | S061628             |  
| 5987396907 | S061628         | AETHQ    | Dev service account for Glide     | S061628             |  

---

### **3️⃣ Correlate User Accounts with Identities (`edwmaster.globalidentity`)**  
- Match `iamglobalidentifier` (from `aethusers_clone`) with `global_id` (from `identitymaster`).  
- Only load **production domain data** (ignore test domains).  
- Store relationships in **Neo4j** to track identity-account connections.  

📌 **Example:**  
| `user_id`  | `user_type`  | `np_identity_id` | `authorizer_account_id` |  
|-----------|------------|-----------------|------------------------|  
| S061628   | Non Person | S000436         | N940393                |  

---

## **🔹 What Happens in Neo4j?**  
- **Create nodes** for identities and user accounts.  
- **Establish relationships** between identities and accounts.  
- Enable **graph-based queries** to analyze identity-account connections.  

💡 **Example Neo4j Relationship:**  
```
(Identity:User {global_id: 'S000436'})  
    -[:HAS_ACCOUNT]->  
(Account {user_id: 'S061628', domain: 'AETH'})
```

---

## **🔹 Key Features of Your Project**  
✅ **Data Extraction** – Fetch from **EDW tables** (identity + accounts).  
✅ **Data Processing** – Filter & match identities to accounts.  
✅ **Graph Database Storage** – Load structured data into **Neo4j**.  
✅ **Production Filtering** – Ignore test domains, focus on **6 prod domains**.  
✅ **Identity Correlation** – Support **multiple accounts per identity**.  

---

## **🔹 Next Steps**  
1️⃣ **Implement a Python script** to extract, process, and push data to Neo4j.  
2️⃣ **Write Cypher queries** to build identity relationships in Neo4j.  
3️⃣ **Validate data consistency** by testing against real EDW data.  

---

🚀 **Would you like a Python script to automate this process?** I can help you write one! 😃