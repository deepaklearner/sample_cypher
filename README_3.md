4.1 I have a python code that connects to mysql db and reads around 8 million rows in batches on 25k.
i feel the connection may disconnect in betweeen so i want retry mechanism. how to do that?

which approach would be good?

As of now, I am creating a connection object in the class __init__ method? Is this good or not good?

4.2 any change in main.py code

4.3. or should i use a common .. to retry all connections 3 times in some common fucntion?

4.4 refactored code
updated and created v1.1

4.5 i want to make my both codes more readable and easy to maintain... suggest 