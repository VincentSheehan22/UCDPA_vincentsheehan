import pandas as pd


def find_and_replace(df, find_string, replace_string):
    df = df.replace(to_replace=find_string, value=replace_string, regex=True)

    return df


if __name__ == '__main__':
    df = pd.DataFrame({'col_1': ["1,234", 1234]})
    print(df)

    find = r'(\d),(\d)(\d)(\d)'
    replace = r'\1\2\3\4'

    df_replaced = find_and_replace(df, find, replace)

    # Check that DataFrame content has changed to replacement string.
    print(df_replaced)

    # Check the data type.
    print(df.info())
    print(df_replaced.info())
