import pandas as pd
import numpy as np


def handle_missing_data(df):
    """Function to process missing values in dataframe."""
    # Replace "--" entries in datframe with NaN.
    df = df.replace("--", np.nan)

    # Count NaNs per column.
    null_check = df.isnull().sum()

    return df, null_check


if __name__ == '__main__':
    df_test = pd.DataFrame({'col_1': [1, 2, "--", 4],
                            'col_2': ["--", "--", "--", "--"]})
    print(df_test)

    df_nan, null_count = handle_missing_data(df_test)

    print(df_nan)
    print(null_count)
