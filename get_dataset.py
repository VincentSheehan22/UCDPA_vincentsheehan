import pandas as pd
from glob import glob


def get_dataset_excel(directory):
    """Genearate Pandas DataFrame from input Excel files."""
    # Create empty dataframe.
    df_nhl = pd.DataFrame()

    # Iterate over .xlsx files in target directory.
    print("Compiling dataframe...")
    files_parsed = 0
    for file in glob(f"{directory}*.xlsx"):
        print(file)
        df_players = pd.read_excel(file, engine="openpyxl")

        files_parsed += 1

        # Concatenate existing dataframe with dataframe generated from file.
        df_nhl = pd.concat([df_nhl, df_players])

    print(f"\nFiles parsed: {files_parsed}\n")

    return df_nhl


if __name__ == '__main__':
    directory = './Raw Data Files/'
    df_nhl = get_dataset_excel(directory)

    print(df_nhl)

