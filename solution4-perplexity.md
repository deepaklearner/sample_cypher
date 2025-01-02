Your approach to storing the results in a CSV file, clearing it before starting the process, appending data during iterations, and then reading the complete file to group by manager_id and send emails is a good strategy. Here's a suggested implementation:

1. Clear the CSV file before starting:

```python
import os

def clear_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')  # Clear the file
    print(f"Cleared the contents of {file_path}")

# Usage
csv_file_path = 'missing_data_vendors.csv'
clear_csv_file(csv_file_path)
```

2. Modify the `identify_vendor_reject_records` function to append results to the CSV:

```python
def identify_vendor_reject_records(df, neo4j_driver, csv_file_path):
    # ... (existing code) ...

    # Append missing_data_vendors to CSV
    missing_data_vendors.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)

    return df, missing_data_vendors, missing_data_vendors_set
```

3. After all iterations, read the complete file, group by manager_id, and send emails:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_grouped_emails(csv_file_path, techops_email):
    # Read the complete CSV file
    all_data = pd.read_csv(csv_file_path)

    # Group by manager_id
    grouped_data = all_data.groupby('MANAGER_ID')

    for manager_id, group in grouped_data:
        manager_email = group['ManagerEmail'].iloc[0]
        if manager_email != 'NOT_FOUND':
            # Prepare email content
            email_content = f"Dear Manager (ID: {manager_id}),\n\nHere are the missing data vendors for your team:\n\n"
            email_content += group.to_string(index=False)

            # Send email to manager
            send_email(manager_email, "Missing Data Vendors Report", email_content)

    # Send summary email to techops team
    techops_content = "Summary of Missing Data Vendors:\n\n"
    techops_content += all_data.groupby('MANAGER_ID').size().to_string()
    send_email(techops_email, "Missing Data Vendors Summary", techops_content)

def send_email(to_email, subject, content):
    # Set up your email sending logic here
    # This is a placeholder function - replace with your actual email sending code
    print(f"Sending email to {to_email}")
    print(f"Subject: {subject}")
    print(f"Content: {content}")
    print("---")

# Usage
techops_email = "techops@example.com"
send_grouped_emails(csv_file_path, techops_email)
```

4. Main execution flow:

```python
# Clear the CSV file before starting
clear_csv_file(csv_file_path)

# Your batch processing loop
for batch in batches:
    df = process_batch(batch)  # Assume this function exists
    neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))  # Set up Neo4j driver
    df, missing_data_vendors, missing_data_vendors_set = identify_vendor_reject_records(df, neo4j_driver, csv_file_path)
    neo4j_driver.close()

# After all batches are processed
send_grouped_emails(csv_file_path, techops_email)
```

This approach allows you to:
1. Clear the CSV file before starting the process.
2. Append results to the CSV file during each iteration.
3. Read the complete file at the end.
4. Group the data by manager_id.
5. Send emails to managers with their specific data.
6. Send a summary email to the techops team.

Remember to replace the placeholder `send_email` function with your actual email sending logic, and adjust the email content formatting as needed.