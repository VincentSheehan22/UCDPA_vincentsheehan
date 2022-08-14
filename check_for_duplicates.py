import pandas as pd


def check_for_duplicates(df):
    """Check DataFrame for duplicate rows.

    Prints any duplicates found, and returns dataframe with duplicates dropped.
    """
    print("Checking for duplicates...\n")
    df_duplicates = df[df.duplicated()]

    print("Getting duplicates...\n", df_duplicates, "\n")

    df = df.drop_duplicates(keep='last')

    return df


if __name__ == '__main__':
    df_without_dupes = pd.DataFrame({"col_1": [0, 1, 2, 3],
                                     "col_2": [4, 5, 6, 7]})

    df_with_dupes = pd.DataFrame({"col_1": [0, 1, 2, 2],
                                  "col_2": [4, 5, 6, 6]})

    df_without_dupes_checked = check_for_duplicates(df_without_dupes)
    print(df_without_dupes_checked)

    df_with_dupes_checked = check_for_duplicates(df_with_dupes)
    print(df_with_dupes_checked)
