import pandas as pd
from glob import glob


def get_dataset_excel(directory, report="Summary"):
    """Generate Pandas DataFrame from input Excel files.

    Takes two strings as input: the directory path and the report type (represented in file name). Returns DataFrame
    compiled from input files.
    """
    # Create empty dataframe.
    df_nhl = pd.DataFrame()

    # Iterate over .xlsx files in target directory, of target report type.
    print(f"Compiling dataframe from {report} report...")
    files_parsed = 0
    for file in glob(f"{directory}/{report}*.xlsx"):
        print(file)
        df_players = pd.read_excel(file, engine="openpyxl")

        files_parsed += 1

        # Concatenate existing dataframe with dataframe generated from file.
        df_nhl = pd.concat([df_nhl, df_players])

    print(f"\nFiles parsed: {files_parsed}\n")

    return df_nhl


if __name__ == '__main__':
    directory = './Raw Data Files/'

    df_nhl_summary = get_dataset_excel(directory, "Summary")
    print(df_nhl_summary, "\n")

    df_nhl_bio = get_dataset_excel(directory, "Bio Info")
    print(df_nhl_bio, "\n")

