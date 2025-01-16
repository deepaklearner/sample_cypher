Ah, I see! You're specifically asking to translate the `REDUCE` logic from Cypher to Python, not the entire query.

In Cypher, `REDUCE` works by accumulating a result over a list, like so:

```cypher
REDUCE(result = [], i IN RANGE(0, 14) | 
  CASE 
    WHEN i < SIZE(manager_ids) THEN result + [manager_ids[i]] 
    ELSE result 
  END
) AS manager_levels
```

This iterates over a range (from 0 to 14) and appends elements from the `manager_ids` list to the `result` list as long as the index is less than the size of `manager_ids`.

In Python, we can replicate this `REDUCE` behavior using a `for` loop, similar to how the `reduce` function works in Python (though we don't need to use the `functools.reduce` function directly here). We can manually build the `manager_levels` list using list slicing or appending.

### Python Equivalent of the `REDUCE` Logic:

```python
def reduce_manager_ids(manager_ids):
    # Create an empty list to accumulate results
    result = []

    # Iterate through the range 0 to 14 (15 iterations)
    for i in range(15):
        if i < len(manager_ids):
            result.append(manager_ids[i])  # Append the i-th manager ID if it exists
        else:
            break  # Stop if we've exhausted the manager_ids list

    return result

# Example usage:
manager_ids = [101, 102, 103, 104]  # Example manager IDs

manager_levels = reduce_manager_ids(manager_ids)
print(manager_levels)
```

### Explanation:

- **`for i in range(15)`**: This simulates the range from `0..14` in Cypher. We're iterating up to 15 because that's the maximum number of levels we care about.
  
- **`if i < len(manager_ids)`**: If the current index `i` is less than the length of `manager_ids`, we append the manager ID at index `i` to the result list.
  
- **`break`**: If `i` exceeds the length of `manager_ids` (meaning we run out of manager IDs), we break out of the loop early.

This approach will accumulate manager IDs in `manager_levels` up to a maximum of 15, just like the Cypher `REDUCE` function.

### Example Output:

For `manager_ids = [101, 102, 103, 104]`, the output will be:

```python
[101, 102, 103, 104]
```

If there were fewer manager IDs, for example:

```python
manager_ids = [101, 102]
```

The output will be:

```python
[101, 102]
```

This logic replicates the behavior of the `REDUCE` in Cypher to accumulate a list of manager IDs up to 15 levels.

