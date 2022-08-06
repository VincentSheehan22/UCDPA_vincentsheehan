# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
import matplotlib.pyplot as plt
from get_dataset import get_dataset_excel
from find_and_replace import find_and_replace
import handle_missing_data
import numpy as np

# Don't suppress columns in terminal output.
pd.options.display.width = 0
pd.options.display.max_rows = 7461

if __name__ == '__main__':
    # Data Collection
    # Compile dataframe from Excel files.
    df_nhl = get_dataset_excel("./Raw Data Files/")

    # Summarise dataset.
    print(df_nhl.head(), "\n")
    print(df_nhl.tail(), "\n")
    print(df_nhl.describe(), "\n")
    print(df_nhl.info(), "\n")

    # Data Cleaning
    # Check format of 4-digit value.
    print("Checking format of 4-digit values...\n",
          df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
          "\n")

    # Use Regex to remove ',' from four-digit values, with capture groups.
    print("Reformatting 4-digit values...\n")
    df_nhl = find_and_replace(df_nhl, r'(\d),(\d)(\d)(\d)', r'\1\2\3\4')

    # Check format of 4-digit value after replacement.
    print("Checking format of 4-digit values...\n",
          df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
          "\n")

    # Sort dataframe by Points, Goals, and Assists and columns.
    print("Sorting by P, G, A...")
    df_nhl = df_nhl.sort_values(by=['P', 'G', 'A'], ascending=False).reset_index()

    # Summarise dataset.
    print(df_nhl.head(), "\n")
    print(df_nhl.tail(), "\n")
    print(df_nhl.describe(), "\n")
    print(df_nhl.info(), "\n")

    # Check for duplicate rows.
    print("Checking for duplicates...\n")
    duplicates = df_nhl.duplicated()

    if True in duplicates:
        raise Exception("Duplicate entry found.\n")
    elif True not in duplicates:
        print("Duplicate entry not found.\n")
    else:
        print("Duplicate check conditions not met. Continuing...\n")

    # Handling Missing Data
    # Explore missing data to determine how best to handle.
    df_nhl, missing_count = handle_missing_data.replace_with_nan(df_nhl)
    print(df_nhl.head(), "\n")
    print(missing_count, "\n")

    # S/C - Impute with mode.
    df_nhl["S/C"] = handle_missing_data.impute_with_mode(df_nhl["S/C"])

    # EVG, EVP, PPG, PPP, SHG, SHP - Impute with mean.
    df_nhl["EVG"] = handle_missing_data.impute_with_mean(df_nhl["EVG"])
    df_nhl["EVP"] = df_nhl["EVP"].astype("float64")                        # Intermediate type coversion to resolve TypeError on impute_with_mean.
                                                                           # Include conversion in impute_with_mean() function definition?
    df_nhl["EVP"] = handle_missing_data.impute_with_mean(df_nhl["EVP"])    # TypeError: can only concatenate str (not "int") to str
    df_nhl["PPG"] = handle_missing_data.impute_with_mean(df_nhl["PPG"])
    df_nhl["PPP"] = handle_missing_data.impute_with_mean(df_nhl["PPP"])
    df_nhl["SHG"] = handle_missing_data.impute_with_mean(df_nhl["SHG"])
    df_nhl["SHP"] = handle_missing_data.impute_with_mean(df_nhl["SHP"])

    # S, S% - Impute with mean.
    df_nhl["S"] = df_nhl["S"].astype("float64")
    df_nhl["S"] = handle_missing_data.impute_with_mean(df_nhl["S"])        # TypeError: can only concatenate str (not "int") to str
    df_nhl["S%"] = df_nhl["S%"].astype("float64")
    df_nhl["S%"] = handle_missing_data.impute_with_mean(df_nhl["S%"])      # TypeError: can only concatenate str (not "int") to str

    # TOI/GP, FOW % - Drop columns.
    print("Dropping TOI/GP and FOW% colums...\n")
    df_nhl = df_nhl.drop(["TOI/GP", "FOW%"], axis=1)

    print(df_nhl.head())
    print(df_nhl.describe())
    print(df_nhl.info())

    # Convert data types.
    print("Converting data types...\n")
    df_nhl["Player"] = df_nhl["Player"].astype("string")
    df_nhl["S/C"] = df_nhl["S/C"].astype("string")
    df_nhl["Pos"] = df_nhl["Pos"].astype("string")
    df_nhl["GP"] = df_nhl["GP"].astype("int64")
    df_nhl["A"] = df_nhl["A"].astype("int64")
    df_nhl["P"] = df_nhl["P"].astype("int64")
    df_nhl["PIM"] = df_nhl["PIM"].astype("int64")
    df_nhl["P/GP"] = df_nhl["P/GP"].astype("float64").round(2)
    df_nhl["EVG"] = df_nhl["EVG"].astype("int64")
    df_nhl["EVP"] = df_nhl["EVP"].astype("int64")
    df_nhl["PPG"] = df_nhl["PPG"].astype("int64")
    df_nhl["PPP"] = df_nhl["PPP"].astype("int64")
    df_nhl["SHG"] = df_nhl["SHG"].astype("int64")
    df_nhl["SHP"] = df_nhl["SHP"].astype("int64")
    df_nhl["OTG"] = df_nhl["OTG"].astype("int64")
    df_nhl["GWG"] = df_nhl["GWG"].astype("int64")
    df_nhl["S"] = df_nhl["S"].astype("int64")
    df_nhl["S%"] = df_nhl["S%"].astype("float64").round(1)

    # Summarise dataset after cleaning.
    print(df_nhl.head(), "\n")
    print(df_nhl.tail(), "\n")
    print(df_nhl.describe(), "\n")
    print(df_nhl.info(), "\n")

    # Exploratory Data Analysis
    # Define features of interest.
    games_played = df_nhl['GP']
    points = df_nhl['P']

    # Explore dataset with scatter plots of points/goals/assists vs. games played.
    fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
    fig.suptitle('Career Points/Goals/Assists vs. Games Played - Regular Season')

    ax0.plot(games_played, points, 'o', color='b', alpha=0.5, label='Points')
    ax0.set_xlabel('Games Played')
    ax0.set_ylabel('Count')
    ax0.set_yticks(range(0, 3500, 500))
    ax0.legend(loc='upper left')

    ax1.plot(games_played, df_nhl['G'], 'o', color='r', alpha=0.5, label='Goals')
    ax1.set_xlabel('Games Played')
    ax1.set_ylabel('Count')
    ax1.set_yticks(range(0, 3500, 500))
    ax1.legend(loc='upper left')

    ax2.plot(games_played, df_nhl['A'], 'o', color='g', alpha=0.5, label='Assists')
    ax2.set_xlabel('Games Played')
    ax2.set_ylabel('Count')
    ax2.set_yticks(range(0, 3500, 500))
    ax2.legend(loc='upper left')

    plt.show()
