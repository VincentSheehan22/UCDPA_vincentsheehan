import pandas as pd
from glob import glob


def get_dataset_excel_summary(directory):
    """Generate Pandas DataFrame from input Excel files."""
    # Create empty dataframe.
    df_nhl = pd.DataFrame()

    # Iterate over .xlsx files in target directory.
    print("Compiling dataframe from Summary report...")
    files_parsed = 0
    for file in glob(f"{directory}/Summary*.xlsx"):
        print(file)
        df_players = pd.read_excel(file, engine="openpyxl")

        files_parsed += 1

        # Concatenate existing dataframe with dataframe generated from file.
        df_nhl = pd.concat([df_nhl, df_players])

    print(f"\nFiles parsed: {files_parsed}\n")

    return df_nhl


def get_dataset_excel_bio(directory):
    """Generate Pandas DataFrame from input Excel files."""
    # Create empty dataframe.
    df_nhl = pd.DataFrame()

    # Iterate over .xlsx files in target directory.
    print("Compiling dataframe from Bio Info report...")
    files_parsed = 0
    for file in glob(f"{directory}/Bio*.xlsx"):
        print(file)
        df_players = pd.read_excel(file, engine="openpyxl")

        files_parsed += 1

        # Concatenate existing dataframe with dataframe generated from file.
        df_nhl = pd.concat([df_nhl, df_players])

    print(f"\nFiles parsed: {files_parsed}\n")

    return df_nhl


if __name__ == '__main__':
    directory = './Raw Data Files/'

    df_nhl_summary = get_dataset_excel_summary(directory)
    print(df_nhl_summary)

    df_nhl_bio = get_dataset_excel_bio(directory)
    print(df_nhl_bio)

