# Understanding v1.1 solution

MATCH (e:User)
WHERE e.managerid IS NOT NULL

// multiple rows of json of e and.. managers a list of value fetched from every json

///////////////////////////////////////////////////////////////
WITH e, [e.managerid] AS managers // think this as outer loop
///////////////////////////////////////////////////////////////

// WITH operates on a row-by-row basis

// Collect manager hierarchy up to 4 levels, ensuring no duplicates 
OPTIONAL MATCH (m:User {employeeNumber: e.managerid})

WITH e, m, 
     CASE WHEN NOT m.employeeNumber IN managers THEN managers + [m.employeeNumber] ELSE managers END AS managers
WHERE m IS NOT NULL

OPTIONAL MATCH (m2:User {employeeNumber: m.managerid})
WITH e, m2,
     CASE WHEN NOT m2.employeeNumber IN managers THEN managers + [m2.employeeNumber] ELSE managers END AS managers
WHERE m2 IS NOT NULL

OPTIONAL MATCH (m3:User {employeeNumber: m2.managerid})
WITH e, m3,  
     CASE WHEN NOT m3.employeeNumber IN managers THEN managers + [m3.employeeNumber] ELSE managers END AS managers
WHERE m3 IS NOT NULL

OPTIONAL MATCH (m4:User {employeeNumber: m3.managerid})
WITH e, m4,
     CASE WHEN NOT m4.employeeNumber IN managers THEN managers + [m4.employeeNumber] ELSE managers END AS managers
WHERE m4 IS NOT NULL

// Output the result
RETURN e.employeeNumber AS employeeNumber, 
       e.managerid AS managerid,
       CASE 
           WHEN size(managers) =1 and e.managerid = e.employeeNumber THEN 1 
           WHEN size(managers) =1 and e.managerid <> e.employeeNumber THEN 2
           WHEN size(managers) =2  THEN 3
           WHEN size(managers) =3  THEN 4
           ELSE 0 
       END AS Level,  // Adjust level for CEO
       CASE WHEN size(managers) > 0 THEN managers[0] ELSE NULL END AS L1managerid,
       CASE WHEN size(managers) > 1 THEN managers[1] ELSE NULL END AS L2managerid,
       CASE WHEN size(managers) > 2 THEN managers[2] ELSE NULL END AS L3managerid,
       CASE WHEN size(managers) > 3 THEN managers[3] ELSE NULL END AS L4managerid
ORDER BY e.employeeNumber

Certainly! Let's break down the flow of the Cypher query into a **flowchart** that illustrates the sequence of operations, from the initial data retrieval to the recursive manager hierarchy matching, and finally the result processing.

### **Flowchart Breakdown of the Cypher Query**

1. **Initial Data Retrieval (`MATCH`)**
2. **Set up initial managers list (`WITH`)**
3. **Recursive manager matching (up to 4 levels)**
4. **Processing and updating manager hierarchy**
5. **Returning results**

---

### Flowchart Diagram

Here's a simplified flowchart to visualize the steps in your query:

```
            +--------------------+
            | 1. Start (MATCH)    |
            | - Find all Users    |
            | - Filter where       |
            |   managerid IS NOT  |
            |   NULL              |
            +--------------------+
                        |
                        v
            +---------------------------+
            | 2. Initialize Managers List|
            | - Set managers = [e.managerid] |
            +---------------------------+
                        |
                        v
            +---------------------------+
            | 3. OPTIONAL MATCH Level 1 |
            | - Match m:User where      |
            |   m.employeeNumber = e.managerid |
            | - Add m.employeeNumber to |
            |   managers list (if not  |
            |   already in it)          |
            | - If m is NULL, no change |
            +---------------------------+
                        |
                        v
            +---------------------------+
            | 4. OPTIONAL MATCH Level 2 |
            | - Match m2:User where     |
            |   m2.employeeNumber = m.managerid |
            | - Add m2.employeeNumber to|
            |   managers list (if not   |
            |   already in it)          |
            | - If m2 is NULL, no change|
            +---------------------------+
                        |
                        v
            +---------------------------+
            | 5. OPTIONAL MATCH Level 3 |
            | - Match m3:User where     |
            |   m3.employeeNumber = m2.managerid |
            | - Add m3.employeeNumber to|
            |   managers list (if not   |
            |   already in it)          |
            | - If m3 is NULL, no change|
            +---------------------------+
                        |
                        v
            +---------------------------+
            | 6. OPTIONAL MATCH Level 4 |
            | - Match m4:User where     |
            |   m4.employeeNumber = m3.managerid |
            | - Add m4.employeeNumber to|
            |   managers list (if not   |
            |   already in it)          |
            | - If m4 is NULL, no change|
            +---------------------------+
                        |
                        v
            +-----------------------------+
            | 7. Return Final Results     |
            | - Calculate Level           |
            |   (based on size of         |
            |    managers list)           |
            | - Output managers at each   |
            |   level (L1, L2, L3, L4)    |
            +-----------------------------+
```

---

### **Step-by-Step Explanation in the Flowchart**

#### **1. Start (MATCH)**  
- **Operation:**  
  - The query begins by matching all users (`User` nodes) who have a non-null `managerid`. This gives us the initial dataset of users who have managers.
  
#### **2. Initialize Managers List (`WITH`)**  
- **Operation:**  
  - For each user `e`, a new list `managers` is initialized with the `managerid` of `e` as its only element (`[e.managerid]`).

#### **3. OPTIONAL MATCH Level 1 (Direct Manager)**
- **Operation:**  
  - The query tries to match the direct manager `m` of `e` using the `managerid` of `e`. If `m` is found, it is added to the `managers` list (ensuring no duplicates).  
  - If no manager is found (i.e., `m` is `NULL`), the list remains unchanged.

#### **4. OPTIONAL MATCH Level 2 (Manager's Manager)**  
- **Operation:**  
  - The query now attempts to find the manager of `m` (referred to as `m2`) using the `managerid` of `m`. If `m2` exists, it is added to the `managers` list.  
  - If no `m2` is found (i.e., `m2` is `NULL`), the list remains unchanged.

#### **5. OPTIONAL MATCH Level 3 (Manager's Manager's Manager)**  
- **Operation:**  
  - The query attempts to find `m3`, the manager of `m2`, and adds `m3` to the `managers` list (if not already present).
  - If `m3` does not exist, it is skipped, and the list remains the same.

#### **6. OPTIONAL MATCH Level 4 (Manager's Manager's Manager's Manager)**  
- **Operation:**  
  - The query tries to find `m4`, the manager of `m3`, and adds `m4` to the `managers` list (if not already present).
  - If `m4` is not found, the list remains unchanged.

#### **7. Return Final Results**
- **Operation:**  
  - Once the manager hierarchy (up to 4 levels) is gathered, the query calculates the level of each user based on the size of their `managers` list:
    - Level 1: Self-managed (if `e.managerid = e.employeeNumber`).
    - Level 2: Direct manager exists but not self-managed.
    - Level 3: Two levels of managers.
    - Level 4: Three levels of managers.
    - Level 0: For any edge cases (such as no managers or other).
  - The query then returns:
    - `employeeNumber` and `managerid` of each user.
    - The hierarchy levels for each user (`L1managerid`, `L2managerid`, `L3managerid`, `L4managerid`).

---

### **How It Behaves Row by Row**

1. **For each user** (`e`):
   - The `WITH` clause initializes the `managers` list with their direct manager.
   - The subsequent `OPTIONAL MATCH` clauses process one manager level at a time.
   - At each level (up to 4 levels), it checks for a manager and, if found, appends the manager's `employeeNumber` to the list (if not already present).
   - This process is repeated row-by-row for every employee.

2. **End of Execution**:
   - After traversing up to four levels of managers, the query calculates and returns the manager hierarchy for each employee and outputs the result.

---

This flowchart and breakdown should give you a clear visual idea of how the query operates and the sequence of steps involved in processing the data.