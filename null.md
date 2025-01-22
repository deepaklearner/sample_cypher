import pandas as pd

# Sample DataFrame
data = {
    'CM_PERS_ID': ['12345', 'DNE', '67890', 'DNE', '11223'],
    'EmployeeName': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
}

df = pd.DataFrame(data)

# Check where 'CM_PERS_ID' is 'DNE'
null_emp_number = df['CM_PERS_ID'] == 'DNE'

print(null_emp_number)


i want the count of only True