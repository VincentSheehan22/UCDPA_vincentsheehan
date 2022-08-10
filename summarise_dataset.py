import pandas as pd


def summarise_dataset(df):
    """Function to get summary of dataset - .shape, .head(), .tail(), .describe(), .info()"""
    print("Getting .shape...\n", df.shape, "\n")
    print("Getting .head()...\n", df.head(), "\n")
    print("Getting .tail()...\n", df.tail(), "\n")
    print("Getting .describe()...\n", df.describe(), "\n")
    print("Getting .info()...")     # Separating print statements for .info() as output conflicts when combined.
    print(df.info(), "\n")


if __name__ == '__main__':
    df_test = pd.DataFrame({"col_1": [1, 2, 3],
                            "col_2": ["a", "b", "c"]})

    summarise_dataset(df_test)