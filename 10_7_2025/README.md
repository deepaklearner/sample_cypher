### 1. I am reading data from mysql database using python.
In one of the column entitle_name the data constains escape character like "c:\\abcd"

I want to fetch them as it is. how to do that

####
escaped_df = df.applymap(repr)
logging.info(escaped_df.to_string(index=False))

### 2. 
i tried """escaped_df = df.applymap(repr) logging.info(escaped_df.to_string(index=False))""" but when there are three \\\ it is shown as \\ only . but when there are four \\\\ its shown corectly why?

#### 
Final

for col in df.select_dtypes(include='object'):
    df[col] = df[col].apply(
        lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x
    )

logging.info(df.to_string(index=False))

### 3
I am using mysql version 8.0.40. I have a table entitlement_master.
In one of the column entitle_name the data constains escape character like "\" or "\\" or
"\\\" or "\\\\".

How to replace them in mysql using sql to forward slashes. Use case statement.

I am reading the data from mysql database and loading into neo4j via a python pandas based etl process.
I want to load data as it is. Is it possible?

