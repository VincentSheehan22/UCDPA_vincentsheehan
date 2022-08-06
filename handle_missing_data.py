import pandas as pd
import numpy as np


def replace_with_nan(df):
    """Function to process missing values in dataframe."""
    # Replace "--" entries in datframe with NaN.
    print("Replacing missing entries (--) with NaN...\n")
    df = df.replace("--", np.nan)

    # Count NaNs per column.
    null_check = df.isnull().sum()

    return df, null_check


def impute_with_mode(series):
    """Fill NA in Pandas Series with the mode (most frequent value) of the series."""
    mode = series.mode()

    print(f"Imputing {series.name} with mode: '{mode[0]}'...\n")
    series = series.fillna(mode[0])

    return series


def impute_with_mean(series):
    """Fill NA in Pandas Series with the mean of the series."""
    mean = np.mean(series)
    print(f"Imputing {series.name} with mean: '{mean}'...\n")
    series = series.fillna(mean)

    return series


if __name__ == '__main__':
    # Test replace_with_nan().
    df_test = pd.DataFrame({"col_1": [1, 2, "--", 4],
                            "col_2": ["--", "--", "--", "--"]})
    print(df_test)

    df_nan, null_count = replace_with_nan(df_test)

    print(df_nan)
    print(null_count)

    # Test impute_with_mode()
    df_test = pd.DataFrame({"col_1": ["L", "L", "R", np.nan, np.nan]})
    print(df_test)

    df_mode = impute_with_mode(df_test["col_1"])
    print(df_mode)

    # Test impute_with_mean()
    df_test = pd.DataFrame({"col_1": [1, 2, 3, np.nan, np.nan, 4, 5, 6, 8, 9, 10]})
    print(df_test)

    df_mean = impute_with_mean(df_test["col_1"])
    print(df_mean)