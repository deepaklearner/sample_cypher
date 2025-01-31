....Basic things you need to remember to Understand the complex stuff....

Import Non Person Accounts into Neo4j

Access of service account for me...

2025 planning


why earlier for ManagerLevel 0, it was not failing...

Earlier:
1657711 1 [1657711 ]
0016540 3 [2330185, 1657711]

For scenario manager_ids empty list, ManagerLevel was coming null because we didnt have any condition for SIZE(manager_ids) have 0 value, so ManagerLevel value as null.
and we removed those records.

After 1/31 change:
for scenario manager_ids empty list, ManagerLevel was coming as 0.

Now,
0016540 2 [2330185, 1657711]

because for empty ones, ManagerLevel was coming null