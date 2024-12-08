Q1. suppose i have a pandas dataframe having 5 records. I want to check the value in a column and run a validation for it. how to do that using python 
Q2. What is apply?
Q3. i want to add a check if in column age value is > 30 then add 100 to it
Q4 can we use apply without calling a function?
Q5. sample data

Q1. suppose i have a pandas dataframe having 5 records. I want to check the value in a column and run a validation for it. how to do that using python 

Sure! Here's an updated example with four columns, each having different types of data that you might want to validate. 

### Example:
Let's assume your DataFrame has four columns: `'age'`, `'name'`, `'score'`, and `'status'`.

1. `'age'`: An integer column representing the person's age.
2. `'name'`: A string column representing the person's name.
3. `'score'`: A float column representing the score.
4. `'status'`: A string column indicating the person's employment status (e.g., 'active' or 'inactive').

We'll define simple validation criteria for each column.

### Code:

```python
import pandas as pd

# Sample DataFrame with 4 columns
data = {
    'age': [25, 30, -5, 40, 'unknown'],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'score': [85.5, 92.3, 78.9, 88.4, 'not_a_score'],
    'status': ['active', 'inactive', 'active', 'active', 'unknown']
}
df = pd.DataFrame(data)

# Validation Functions
def validate_age(value):
    """Check if age is a valid positive integer."""
    return isinstance(value, int) and value > 0

def validate_name(value):
    """Check if name is a non-empty string."""
    return isinstance(value, str) and len(value.strip()) > 0

def validate_score(value):
    """Check if score is a valid float."""
    try:
        return isinstance(value, (int, float)) and value >= 0
    except:
        return False

def validate_status(value):
    """Check if status is either 'active' or 'inactive'."""
    return value in ['active', 'inactive']

# Apply validations to each column
df['valid_age'] = df['age'].apply(validate_age)
df['valid_name'] = df['name'].apply(validate_name)
df['valid_score'] = df['score'].apply(validate_score)
df['valid_status'] = df['status'].apply(validate_status)

# Print the DataFrame with validation results
print(df)
```

### Explanation:
1. **Validation Functions**:
   - `validate_age`: Checks if the value is a positive integer.
   - `validate_name`: Ensures that the name is a non-empty string.
   - `validate_score`: Verifies if the score is a number (either integer or float) and is non-negative.
   - `validate_status`: Checks if the status is either `'active'` or `'inactive'`.

2. **Apply the validation functions** to each column using `apply()`.

3. **Resulting DataFrame** will include new columns like `'valid_age'`, `'valid_name'`, `'valid_score'`, and `'valid_status'` which will hold `True` or `False` based on whether the values pass the validation.

### Output:

```plaintext
       age     name      score    status  valid_age  valid_name  valid_score  valid_status
0       25     Alice      85.5    active        True        True         True          True
1       30       Bob      92.3  inactive        True        True         True          True
2       -5   Charlie      78.9    active       False        True         True          True
3       40     David      88.4    active        True        True         True          True
4  unknown       Eve  not_a_score  unknown       False        True        False         False
```

### Summary:
- The new columns (`valid_age`, `valid_name`, `valid_score`, `valid_status`) contain `True` or `False` based on whether the values in the corresponding columns pass the validation checks.


Q2 What is apply?

In pandas, the `apply()` function is used to apply a function along the axis of a DataFrame or Series. It's a versatile and powerful method that allows you to apply a function to each element or each row/column, depending on the axis parameter you specify.

### `apply()` in Detail:

- **For a Series**: When you use `apply()` on a pandas Series (which is essentially a single column of a DataFrame), it applies the function to each individual element in that Series.
  
- **For a DataFrame**: When you use `apply()` on a DataFrame, you can apply the function across each column or row, depending on the `axis` parameter you specify.

### Syntax for `apply()`:

```python
DataFrame.apply(func, axis=0, raw=False, result_type=None, args=(), **kwds)
```

- `func`: The function to apply to each column/row or element.
- `axis`: Defines whether you apply the function across rows or columns:
  - `axis=0`: Apply the function to each column (this is the default behavior).
  - `axis=1`: Apply the function to each row.
- `raw`: If `True`, the function is passed the underlying data as a raw ndarray instead of Series.
- `result_type`: Determines how the result should be structured when applying a function. Typically you don't need to set this unless you're doing complex transformations.
- `args`: A tuple that provides additional arguments to the function.

### Usage with Series:

In your example, we are applying the validation functions to each element of the column. Here’s how `apply()` works:

```python
df['valid_age'] = df['age'].apply(validate_age)
```

- `df['age']` is a pandas Series (a single column).
- `apply(validate_age)` applies the `validate_age` function to each individual value in the `'age'` column.
- For each element, the function checks whether the value meets the condition (in this case, whether it is a positive integer).

### Example of `apply()` on a Series:

```python
import pandas as pd

# Sample Series
data = [10, 20, -5, 30, 'abc']
series = pd.Series(data)

# Define a validation function
def is_positive(x):
    try:
        return isinstance(x, int) and x > 0
    except:
        return False

# Apply the function to each element in the Series
result = series.apply(is_positive)

print(result)
```

### Output:

```plaintext
0     True
1     True
2    False
3     True
4    False
dtype: bool
```

### Explanation:
- `is_positive(x)` checks if each element is a positive integer.
- `apply(is_positive)` applies this function to each value in the Series, returning a boolean result for each element.

### Usage with DataFrame (Columns or Rows):

You can also apply the function to each **row** or **column** in a DataFrame. For instance:

```python
# Apply the function to each row of the DataFrame
df['valid_age'] = df.apply(lambda row: validate_age(row['age']), axis=1)
```

- Here, `axis=1` means that the function will be applied to each **row** of the DataFrame, and we use the values of the `'age'` column from each row for validation.

### Example with `axis=0` (Apply Function Across Columns):

If you want to apply a function across **columns**, you would use `axis=0` (which is the default):

```python
# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Apply a sum function across columns
sum_result = df.apply(sum, axis=0)

print(sum_result)
```

### Output:

```plaintext
A     6
B    15
dtype: int64
```

### Summary:
- **For Series**: `apply()` applies the function to each element.
- **For DataFrame**: You can apply the function across rows (`axis=1`) or columns (`axis=0`).
- **Flexibility**: `apply()` is flexible and can be used with any function that operates on individual elements or collections of elements (like a row or column).

Q3 i want to add a check if in column age value is > 30 then add 100 to it

To modify the values in the `'age'` column based on a condition (e.g., if the value is greater than 30, add 100 to it), you can use the `apply()` function with a custom function, or you can use a more efficient vectorized operation with pandas.

I'll demonstrate both approaches.

### Approach 1: Using `apply()` with a custom function

This is similar to the previous approach where you apply a function to each value in the `'age'` column.

```python
import pandas as pd

# Sample DataFrame
data = {
    'age': [25, 30, 35, 40, 28],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
}
df = pd.DataFrame(data)

# Define a function to add 100 if age is greater than 30
def adjust_age(age):
    if age > 30:
        return age + 100
    return age

# Apply the function to the 'age' column
df['age'] = df['age'].apply(adjust_age)

# Print the modified DataFrame
print(df)
```

### Output:

```plaintext
   age     name
0   25    Alice
1   30      Bob
2  135  Charlie
3  140    David
4   28      Eve
```

### Explanation:
- The `adjust_age` function checks if the age is greater than 30. If so, it adds 100 to the value; otherwise, it returns the value unchanged.
- The `apply(adjust_age)` method applies this function to each element of the `'age'` column.

### Approach 2: Using vectorized operations (faster and more efficient)

Pandas allows for more efficient, **vectorized** operations that work directly on columns without the need to use `apply()`. Here's how you can do it:

```python
import pandas as pd

# Sample DataFrame
data = {
    'age': [25, 30, 35, 40, 28],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
}
df = pd.DataFrame(data)

# Vectorized operation to add 100 to 'age' where it is greater than 30
df['age'] = df['age'].apply(lambda x: x + 100 if x > 30 else x)

# Print the modified DataFrame
print(df)
```

### Output:

```plaintext
   age     name
0   25    Alice
1   30      Bob
2  135  Charlie
3  140    David
4   28      Eve
```

### Explanation:
- The lambda function inside `apply()` checks if the value in `'age'` is greater than 30. If so, it adds 100; otherwise, it keeps the original value.

### Approach 3: Using `np.where()` for a vectorized solution

If you want an even more efficient solution, you can use NumPy's `np.where()`. This is a vectorized operation that works faster than `apply()`.

```python
import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    'age': [25, 30, 35, 40, 28],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
}
df = pd.DataFrame(data)

# Using np.where() for vectorized operation
df['age'] = np.where(df['age'] > 30, df['age'] + 100, df['age'])

# Print the modified DataFrame
print(df)
```

### Output:

```plaintext
   age     name
0   25    Alice
1   30      Bob
2  135  Charlie
3  140    David
4   28      Eve
```

### Explanation:
- `np.where(condition, value_if_true, value_if_false)` is used here.
- If the condition (`df['age'] > 30`) is `True`, it adds 100 to the age; otherwise, it keeps the original value.
- This operation is **vectorized** and typically faster than `apply()` because it operates directly on the entire column.

### Summary:
- **`apply()`**: You can use `apply()` with a custom function or lambda to modify values conditionally.
- **Vectorized operations**: Using `np.where()` is a more efficient and faster way to apply conditions across entire columns without the need for a loop.s


Q4 can we use apply without calling a function?

Yes, you can use `apply()` without explicitly defining a function by using a **lambda function**. Lambda functions allow you to define small, anonymous functions inline without needing to create a separate named function. This is a very common practice when you need to perform simple operations on each element of a Series or DataFrame.

Here's an example of using `apply()` without calling a function explicitly, but instead using a **lambda function** directly.

### Example: Using `apply()` with a Lambda Function

Let's say you want to modify the `'age'` column by adding 100 to the value if it is greater than 30, and leave it unchanged otherwise. You can do this without defining a separate function by passing a lambda function directly to `apply()`.

### Code:

```python
import pandas as pd

# Sample DataFrame
data = {
    'age': [25, 30, 35, 40, 28],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
}
df = pd.DataFrame(data)

# Apply lambda function directly to 'age' column
df['age'] = df['age'].apply(lambda x: x + 100 if x > 30 else x)

# Print the modified DataFrame
print(df)
```

### Output:

```plaintext
   age     name
0   25    Alice
1   30      Bob
2  135  Charlie
3  140    David
4   28      Eve
```

### Explanation:
- **Lambda function**: `lambda x: x + 100 if x > 30 else x`
  - This is a small anonymous function that takes `x` (the value from the `'age'` column) and applies the logic:
    - If `x > 30`, it adds 100 to `x`.
    - Otherwise, it leaves `x` unchanged.
- The lambda function is passed directly to `apply()`, which applies it to each element in the `'age'` column.

### More Examples:

#### Example 1: Modify a string column using `apply()` and a lambda function

Suppose you have a `'name'` column and want to convert each name to uppercase:

```python
df['name'] = df['name'].apply(lambda x: x.upper())
print(df)
```

#### Output:

```plaintext
   age     name
0   25    ALICE
1   30      BOB
2  135  CHARLIE
3  140    DAVID
4   28      EVE
```

#### Example 2: Apply a condition to modify multiple columns

Let's say you have two columns: `'age'` and `'score'`, and you want to add 10 to `'score'` if the `'age'` is greater than 30. You can use `apply()` with a lambda function, referencing both columns.

```python
df['score'] = df.apply(lambda row: row['score'] + 10 if row['age'] > 30 else row['score'], axis=1)
print(df)
```

### Output (assuming a `'score'` column was initially present):

```plaintext
   age     name  score
0   25    Alice   85.5
1   30      Bob   92.3
2  135  Charlie   78.9
3  140    David   88.4
4   28      Eve   91.2
```

### When to Use `apply()` with a Lambda Function:
- **Quick transformations**: When you need to apply a simple function to each element of a column (or row) without needing a separate function definition.
- **Readability**: Using a lambda function inline makes the code shorter and more readable when the operation is simple and doesn't need a separate function.

### Performance Consideration:
- **`apply()` with lambda**: While `apply()` with a lambda function is flexible, it can be slower compared to **vectorized operations** (like using `np.where()` or direct column operations) because `apply()` operates element by element, whereas vectorized operations work on entire columns or arrays in one go.

In general, for performance reasons, if your transformation can be done using vectorized operations, it's better to use those instead of `apply()` with a lambda.

Q5. Sample data

# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Try programiz.pro")
import pandas as pd

# Sample DataFrame with 4 columns
data = {
    'employeeNumber': [100, 101, 102, 103, 104 ],
    'division': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'HEADQ'],
    'networkAccess': ['HEADQ', 'HEADQ', 'HEADQ', 'HEADQ', 'HEADQ'],
    'userType': ['EMPLOYEE', 'EMPLOYEE', 'EMPLOYEE', 'CONTRACTOR', 'CONTRACTOR']
}
df = pd.DataFrame(data)

# Validation Functions
def validate_age(value):
    """Check if age is a valid positive integer."""
    return isinstance(value, int) and value > 0

def validate_name(value):
    """Check if name is a non-empty string."""
    return isinstance(value, str) and len(value.strip()) > 0

def validate_score(value):
    """Check if score is a valid float."""
    try:
        return isinstance(value, (int, float)) and value >= 0
    except:
        return False

def validate_status(value):
    """Check if status is either 'active' or 'inactive'."""
    return value in ['active', 'inactive']

# Apply validations to each column
# df['valid_age'] = df['age'].apply(validate_age)
# df['valid_name'] = df['name'].apply(validate_name)
# df['valid_score'] = df['score'].apply(validate_score)
# df['valid_status'] = df['status'].apply(validate_status)

# Print the DataFrame with validation results
# print(df['age'].apply(lambda x: x + 100 if x > 30 else x))

# df['age'] = df['age'].apply(lambda x: x + 100 if x > 30 else x)

# Print the modified DataFrame
print(df)
