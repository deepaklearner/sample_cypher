import pandas as pd
import numpy as np
import logging

def transform_vendor_raw_data(df):
    """
    Cleans and processes raw vendor data while maintaining original data formats.
    
    Args:
        df (pd.DataFrame): Input DataFrame with vendor records.

    Returns:
        pd.DataFrame: Processed DataFrame with updated status columns.
    """

    dateformat = "%Y-%m-%d %H:%M:%S"
    
    # Get the current and next day dates
    current_date = pd.Timestamp.now(tz='UTC').normalize()
    next_day_date = current_date + pd.DateOffset(days=1)

    # Clean dates without converting their format
    df['END_DATE_upd'] = date_cleaner(df, colname="END_DATE")
    df['START_DATE_upd'] = date_cleaner(df, colname="START_DATE")

    # Flag END_DATE in the past
    df['is_end_date_past'] = np.where(df['END_DATE_upd'] < current_date, 'Y', 'N')

    # Set HRStatus based on end date condition
    df['HRStatus'] = np.where(df['is_end_date_past'] == 'Y', 'T', 'A')

    # Define a fixed future date (10 years ahead)
    future_date = (next_day_date + pd.DateOffset(years=10)).strftime(dateformat)

    # Identify new hires where START_DATE is in the future
    condition = df['START_DATE_upd'] >= current_date
    df['is_new_hire'] = np.where(condition, 'Y', 'N')

    # Assign date_current based on condition, but do not alter the format
    df['date_current'] = np.where(condition, df['START_DATE_upd'], current_date)
    df['date_current'].fillna(current_date, inplace=True)

    # Apply date cleaner while preserving original format
    df['date_current'] = date_cleaner(df, colname='date_current')
    df['date_current'] = df['date_current'].astype(str).replace('NaT', 'DNE')

    # Maintain original format for startDate without converting
    df['startDate'] = np.where(condition, df['START_DATE_upd'], future_date)
    df['startDate'].fillna(future_date, inplace=True)
    
    logging.info(f"deepak1 df: \n{df.to_string()}")

    # Clean startDate column and keep format intact
    df['startDate'] = date_cleaner(df, colname='startDate')
    df['startDate'] = df['startDate'].astype(str).replace('NaT', 'DNE').replace(future_date, 'DNE')

    logging.info(f"deepak2 df: \n{df.to_string()}")

    # Clean START_DATE and END_DATE columns without modifying format
    df['START_DATE'] = date_cleaner(df, colname='START_DATE_upd')
    df['END_DATE'] = date_cleaner(df, colname='END_DATE_upd')

    df['START_DATE'] = df['START_DATE'].astype(str).replace('NaT', 'DNE')
    df['END_DATE'] = df['END_DATE'].astype(str).replace('NaT', 'DNE')

    return df
