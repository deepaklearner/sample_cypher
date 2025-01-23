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
print(null_emp_number.sum())


i want the count of only True


---

In this line: 
new_record_warn_cond = (new_records[new_record_warning_cols] == 'DNE').any(axis=1)
I want to add a check for column "MANAGER_ID" should not be DNE

---
i have a python code:
new_record_warned = new_records[new_record_warn_cond].copy()
i want to add one more condition conditions_current as a OR to "new_record_warned = new_records[new_record_warn_cond].copy()"

