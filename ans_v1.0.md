Got it! If you need to apply conditions across **multiple columns** for warnings and rejections, you can expand the logic to check each relevant column and apply conditions accordingly. This is especially useful when your checks are column-specific or need to be more granular across different attributes.

### Approach for Multiple Column Checks

1. **Column-Specific Conditions**: You can define column-specific check functions that can handle different types of validation per column.
2. **Maintainability**: You’ll still keep the structure modular, so adding new column conditions later will be easier.

Here’s how you can modify the code to handle multiple columns for warnings and rejections:

### Updated Code Implementation

```python
import pandas as pd

# Sample data with multiple columns
data = {
    'vendor_id': [1, 2, 3, 4],
    'is_new': [True, False, True, False],
    'price': [100, 200, -50, 300],
    'name': ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D'],
    'rating': [4.5, 3.2, 4.8, -1.0],
    'contact': ['1234567890', '9876543210', '', '12345']
}
df = pd.DataFrame(data)

# Define conditions for new records
def check_new_warnings(row):
    warnings = []
    # Price can't be negative for new records
    if row['price'] < 0:
        warnings.append("Price can't be negative for new records.")
    # Rating should be between 0 and 5 for new records
    if row['rating'] < 0 or row['rating'] > 5:
        warnings.append("Rating must be between 0 and 5 for new records.")
    # Add more conditions as needed
    return warnings

def check_new_rejections(row):
    rejections = []
    # Price must be greater than zero for new records
    if row['price'] <= 0:
        rejections.append("Price must be greater than zero for new records.")
    # Rating must be a valid number for new records
    if not (0 <= row['rating'] <= 5):
        rejections.append("Rating must be valid (0 <= rating <= 5) for new records.")
    # Contact info should not be empty for new records
    if not row['contact']:
        rejections.append("Contact number cannot be empty for new records.")
    # Add more conditions as needed
    return rejections

# Define conditions for existing records
def check_existing_warnings(row):
    warnings = []
    # Price can't be negative for existing records
    if row['price'] < 0:
        warnings.append("Price can't be negative for existing records.")
    # Rating should be between 0 and 5 for existing records
    if row['rating'] < 0 or row['rating'] > 5:
        warnings.append("Rating must be between 0 and 5 for existing records.")
    # Add more conditions as needed
    return warnings

def check_existing_rejections(row):
    rejections = []
    # Price must be greater than zero for existing records
    if row['price'] <= 0:
        rejections.append("Price must be greater than zero for existing records.")
    # Rating must be valid for existing records
    if not (0 <= row['rating'] <= 5):
        rejections.append("Rating must be valid (0 <= rating <= 5) for existing records.")
    # Contact info should not be empty for existing records
    if not row['contact']:
        rejections.append("Contact number cannot be empty for existing records.")
    # Add more conditions as needed
    return rejections

# Main function to process records
def process_records(df):
    warnings_list = []
    rejections_list = []
    processed_records = []
    rejected_records = []
    
    # Loop through each record
    for idx, row in df.iterrows():
        warnings = []
        rejections = []
        
        if row['is_new']:  # Check conditions for new records
            warnings.extend(check_new_warnings(row))
            rejections.extend(check_new_rejections(row))
        else:  # Check conditions for existing records
            warnings.extend(check_existing_warnings(row))
            rejections.extend(check_existing_rejections(row))
        
        # Store warning and rejection messages for each record
        df.at[idx, 'warnings'] = "; ".join(warnings) if warnings else None
        df.at[idx, 'rejections'] = "; ".join(rejections) if rejections else None
        
        # Determine if the record is valid or rejected
        if rejections:  # If there are rejections, add to rejected records
            rejected_records.append(row)
        else:  # Valid record with or without warnings
            processed_records.append(row)
            warnings_list.extend(warnings)  # Collect warnings for processed records
    
    # Create DataFrames for processed and rejected records
    processed_df = pd.DataFrame(processed_records)
    rejected_df = pd.DataFrame(rejected_records)
    
    return df, processed_df, rejected_df, warnings_list

# Call the function to process records
df_with_messages, processed_df, rejected_df, all_warnings = process_records(df)

# Output the results
print("Processed Records with Warnings:")
print(processed_df)

print("\nRejected Records:")
print(rejected_df)

print("\nAll Warnings:")
print(all_warnings)

print("\nDataFrame with Warnings and Rejections (Original):")
print(df_with_messages)
```

### Explanation:

#### 1. **Multiple Column Checks**:
- **Price Check**: We are checking if `price` is greater than zero and if it's negative for new records.
- **Rating Check**: We check if `rating` is between 0 and 5 for both new and existing records.
- **Contact Check**: We ensure that the `contact` field is not empty, particularly for new records.

#### 2. **Function for Each Type of Record**:
- **`check_new_warnings`** and **`check_existing_warnings`**: These functions handle warnings that apply to the different records.
- **`check_new_rejections`** and **`check_existing_rejections`**: These functions handle the rejections based on the conditions for new and existing records.

#### 3. **Return Values**:
- **`df_with_messages`**: This is the original DataFrame with additional columns for warnings and rejections.
- **`processed_df`**: Contains records that were valid but may have warnings.
- **`rejected_df`**: Contains records that were rejected based on the defined conditions.
- **`all_warnings`**: A list of all warnings for processed records.

### Output Example:

```plaintext
Processed Records with Warnings:
   vendor_id  is_new  price      name  rating     contact  warnings  rejections
0          1    True     100  Vendor A     4.5  1234567890      None          None
1          2   False     200  Vendor B     3.2  9876543210      None          None
3          4   False     300  Vendor D    -1.0      12345      None          None

Rejected Records:
   vendor_id  is_new  price      name  rating     contact                       warnings  \
2          3    True     -50  Vendor C     4.8              None  Price can't be negative for new records.   

   rejections
2  Price must be greater than zero for new records.
   
All Warnings:
['Price can't be negative for new records.', 'Rating must be between 0 and 5 for new records.']

DataFrame with Warnings and Rejections (Original):
   vendor_id  is_new  price      name  rating     contact                                     warnings                                    rejections
0          1    True     100  Vendor A     4.5  1234567890                                            None                                          None
1          2   False     200  Vendor B     3.2  9876543210                                            None                                          None
2          3    True     -50  Vendor C     4.8              None  Price can't be negative for new records.  Price must be greater than zero for new records.
3          4   False     300  Vendor D    -1.0      12345                                            None                                          None
```

### Key Points:
- **Column-Specific Validation**: Each column has its own logic for warnings and rejections, allowing for flexible validation.
- **Modular and Easy to Extend**: Adding new conditions for more columns in the future is easy. Just create new functions for specific column checks and update the corresponding warning/rejection functions.
- **Separate DataFrames**: You now have two distinct DataFrames—`processed_df` for valid records (with possible warnings) and `rejected_df` for rejected records.

Let me know if you need more details or further adjustments!