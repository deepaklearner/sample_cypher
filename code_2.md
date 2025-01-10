import logging

def date_parser_category_one(df):
    future_date = '2099-12-12 00:00:00'  # Placeholder for handling future dates
    
    # Applying a condition to fill missing values by backfilling across specified columns
    condition1 = df[['HireDate', 'ContBeginDate']].bfill(axis=1).iloc[:, 0] >= current_date
    
    # Logging the condition output
    logging.info(f"deepak condition1: \n{condition1}")
