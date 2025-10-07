### 1. I am reading data from mysql database using python.
In one of the column entitle_name the data constains escape character like "c:\\abcd"

I want to fetch them as it is. how to do that

####
escaped_df = df.applymap(repr)
logging.info(escaped_df.to_string(index=False))

### 2. 
i tried """escaped_df = df.applymap(repr) logging.info(escaped_df.to_string(index=False))""" but when there are three \\\ it is shown as \\ only . but when there are four \\\\ its shown corectly why?

#### 

