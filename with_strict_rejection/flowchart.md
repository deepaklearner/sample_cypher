Absolutely — that aligns with strict IAM governance and avoids assigning the wrong primary account. Let’s update the flow accordingly.

Here’s the **revised logic for multiple eligible accounts**:

---

# **Updated Flowchart (Text Version)**

```
START
   │
   ▼
Fetch EDW accounts for user
   │
   ▼
Compute "eligible primary accounts" from EDW
(TargetSystem in ['CORP','CSARMARK','CVS'] AND 'cloud' in extensionAttribute3)
   │
   ▼
Are there multiple eligible accounts?
   ├─ Yes ─► REJECT / LOG ERROR
   │           "Ambiguous PrimaryAuth candidates in EDW"
   │
   └─ No ─► Continue
   │
   ▼
Is there a single eligible account?
   ├─ Yes ─► Mark as computedPrimary
   │
   └─ No ─► computedPrimary = None
   │
   ▼
Fetch Neo4j accounts for user
   │
   ▼
Is there an existing Neo4j primary?
   ├─ Yes ─►
   │        Does Neo4j primary match computedPrimary?
   │           ├─ Yes ─► No change needed
   │           └─ No ─► Demote old primary to secondary
   │                    Assign computedPrimary as primary
   └─ No ─►
            Assign computedPrimary as primary (if exists)
   │
   ▼
Assign secondary accounts
(Every other account not marked as primary becomes Secondary)
   │
   ▼
Propagate PAS primary across other domains
   ├─ Any domain has PAS primary incorrectly marked as secondary?
   │      └─ Yes ─► Switch accounts: make PAS account primary in domain
   │
   ▼
Update domain-related fields in ETL table:
  - domains
  - primaryAuthDomain
  - primaryAuthDomainName
  - corpAccountNames
   │
   ▼
END / Proceed to Step 7 (Compute oneIDs)
```

---

# **Key Points with Strict Rejection**

1. **EDW data is authoritative**: multiple eligible accounts = invalid data.
2. **No silent assignment** — prevents wrong primary assignment.
3. **ETL should log and optionally alert business** for manual correction.
4. Neo4j reconciliation happens **only if EDW passes validation**.

---

If you want, I can **also modify your `load_edw.py` pseudocode** to include this **strict rejection step** so that your ETL rejects ambiguous EDW batches automatically.

Do you want me to do that next?
