1.1
I have IAM data in edw(myswl database) and i am loading in neo4j.
While loading i am determining the primaryauth useraccount which will be used for login.

In one of the function in ETL i am have to modify the code to peform below:

# BUSINESS LOGIC SUMMARY

1. Find the correct **PrimaryAuthSystem** account based on current EDW data  
2. Check if user has PrimaryAuth in neo4j data.
3. If No, follow the regular process
4. If Yes, then check if PrimaryAuth changed
5. If Yes, then Retrieve all the accounts from User
6. If Yes, then check if user has other secondary accounts as well.
7. If No, then update the primaryAuth for the respective account.
8. If Yes, then check if PrimaryAuth set for secondary account.
9. If yes, then switch accounts to primary and secondary imn the domain
10. Check if any domains has this PAS account as secondary.
11. If Yes, then switch accounts to primary and secondary in each domain to match PAS


DUMOS Bar Stools Set of 4, 24 inch Counter Height Bar Stools, Upholstered Modern Kitchen Barstools with Metal Base, PU Leather Saddle Stools for Kitchen Island, White

Height-Adjustable Chair / Bar Stool
PU-leather white. With saddle seat and sturdy metal base. Clean and in great condition.
