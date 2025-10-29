import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta
import timeit

def generate_flexible_dummy_dataframe(
    n_rows=1000,
    n_numeric=2,
    n_integer=2,
    n_text=1,
    n_date=1,
    n_bool=1,
    seed=42
):
    """Generate a dummy DataFrame with flexible column types."""
    np.random.seed(seed)
    random.seed(seed)

    df = pd.DataFrame()

    # Numeric columns
    for i in range(n_numeric):
        df[f"num_{i+1}"] = np.random.random(n_rows)

    # Integer columns
    for i in range(n_integer):
        df[f"int_{i+1}"] = np.random.randint(0, 1000, n_rows)

    # Text columns
    letters = string.ascii_lowercase
    for i in range(n_text):
        df[f"text_{i+1}"] = [
            ''.join(random.choices(letters, k=8)) for _ in range(n_rows)
        ]

    # Date columns
    start_date = datetime(2020, 1, 1)
    for i in range(n_date):
        df[f"date_{i+1}"] = [
            start_date + timedelta(days=int(x))
            for x in np.random.randint(0, 3650, n_rows)
        ]

    # Boolean columns
    for i in range(n_bool):
        df[f"bool_{i+1}"] = np.random.choice([True, False], n_rows)

    return df

def benchmark_dataframe_generation(n_rows=1000, n_iter=10, **kwargs):
    """Benchmark average generation time in milliseconds."""
    stmt = lambda: generate_flexible_dummy_dataframe(n_rows=n_rows, **kwargs)
    duration = timeit.timeit(stmt, number=n_iter)
    avg_ms = (duration / n_iter) * 1000
    print(f"Average duration per iteration: {avg_ms:.3f} ms")


# Example usage
if __name__ == "__main__":
    df = generate_flexible_dummy_dataframe(
        n_rows=10,
        n_numeric=2,
        n_integer=1,
        n_text=1,
        n_date=1,
        n_bool=1
    )
    print(df.head())

    benchmark_dataframe_generation(
        n_rows=1000,
        n_iter=20,
        n_numeric=3,
        n_integer=2,
        n_text=2,
        n_date=1,
        n_bool=1
    )