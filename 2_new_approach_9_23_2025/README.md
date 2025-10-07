1.1 i am not able to think clearly, how to setup the code structure...for an etl process. what should i do.. should i write first step or start with flow chart. 

 I am starting to write a etl process in python pandas. I am confused, if i should use main here or go without main

1.2
My process is:
1. Extract:
   - Read primary domains list
   - Get no primary domains list
   - Read data for primary domains one by one from edw mysql db
   - Transform and load data primary domains one by one into neo4j
   - Read data for non primary domains in batch of 3200 from edw mysql db
   - Transform and load data non primary domains into neo4j
  
1.3 ok. now show me sample code

1.5 But I have one more step to do... let me tell in detail:
step 1: Load Entitlement from mysql to neo4j
step 2: Fetch owner data from mysql db and create relationship with Entitlements

I am thining to break both the steps in stages then how to plan for main().
Should i keep common stuff between both steps. but there is nothing common between them