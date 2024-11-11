# Understanding v1.1 solution

MATCH (e:User)
WHERE e.managerid IS NOT NULL

// multiple rows of json of e and.. managers a list of value fetched from every json
WITH e, [e.managerid] AS managers

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
