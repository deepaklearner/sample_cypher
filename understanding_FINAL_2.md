You could return `manager_ids` directly as `manager_levels`, but there are important reasons why the query uses the `REDUCE` function to manipulate the list. Let me explain the differences and why `REDUCE` might be necessary in this context.

### 1. **Limiting the Number of Manager Levels (15 levels)**

The main reason for using the `REDUCE` function is to limit the number of manager levels to **15**. 

- **What happens if you return `manager_ids` directly?**  
   If you simply returned `manager_ids`, it would give you the list of managers the user reports to, without any limit. If a user has more than 15 managers (which, in practice, is quite rare but possible), you would get a list longer than 15. 
   
   For example, if `manager_ids` has 20 items, returning it directly would give a list with all 20 managers. But the requirement might be that you only care about the first 15 manager levels (e.g., reporting lines up to 15 managers deep).

- **Why the `REDUCE` function is necessary**:  
   The `REDUCE` function ensures that you get **exactly 15 levels** of managers, or fewer if there are fewer managers in the reporting structure. This way, if a user has 3 managers, you get just those 3 managers, and if a user has 10 managers, you only return those 10.

### 2. **Filling Missing Levels with Empty Values**

In addition to limiting the list to 15 items, the `REDUCE` function is designed to **fill missing levels with empty values** (if the user reports to fewer than 15 managers). 

- **Example**:  
   If `manager_ids = [M101, M102, M103]`, the `REDUCE` function ensures the list will be filled up to 15 elements like this:
   ```cypher
   [M101, M102, M103, null, null, null, null, null, null, null, null, null, null, null]
   ```
   If you were to return `manager_ids` directly, you would only get:
   ```cypher
   [M101, M102, M103]
   ```
   However, by using the `REDUCE` function, you ensure that your output **always has 15 elements** (with `null` or empty values filling in the spots where the user has fewer managers). This can be important if the data consumers expect a fixed length (15) for manager levels, even when there are fewer managers.

### 3. **Customization and Flexibility of Manager Levels**

The `REDUCE` function gives you flexibility in customizing the output list:
- **Adding extra logic**: If you want to further customize how the list is built (e.g., formatting, filtering out some data, etc.), using `REDUCE` gives you more control.
- **Complex transformations**: With `REDUCE`, you could also transform or filter the manager IDs if needed, which wouldn't be as easy if you just returned `manager_ids` directly.

### 4. **Maintain Consistency for All Users**

By using `REDUCE`, you ensure **consistency** in the number of manager levels across all users. Without it:
- Some users could have a list with fewer than 15 manager IDs.
- Other users could have more than 15.
- Using `REDUCE`, you guarantee that all users' results are of the same format and size.

### Key Differences Between Returning `manager_ids` and Using `REDUCE`

- **Returning `manager_ids` directly**:
  - Returns exactly as many manager IDs as there are in the `manager_ids` list.
  - May return fewer than 15 elements if a user reports to fewer than 15 managers.
  - May not work as expected if you have more than 15 managers (i.e., it could return more than 15 managers).

- **Using `REDUCE`**:
  - Guarantees that the list of managers is exactly 15 elements long.
  - Fills missing positions with empty values (`null`) if the user reports to fewer than 15 managers.
  - Ensures consistent formatting of manager data for all users, regardless of the number of managers they report to.

### Conclusion

The `REDUCE` function is used in this query to:
- **Limit the number of manager levels** to 15.
- **Fill in empty positions** when there are fewer than 15 managers.
- Provide **consistent output** for all users, regardless of how many managers they report to.

If your application doesn't require a fixed-length list (or doesn't care about filling missing values), you **could** return `manager_ids` directly, but the `REDUCE` function is added for control, flexibility, and to meet the expected output format.