# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
import matplotlib.pyplot as plt
from get_dataset import get_dataset_excel
from find_and_replace import find_and_replace

# Don't suppress columns in terminal output.
pd.options.display.width = 0
pd.options.display.max_rows = 7461

if __name__ == '__main__':
    # Compile dataframe from Excel files.
    df_nhl = get_dataset_excel("./Raw Data Files/")

    # Check format of 4-digit value.
    print("\nChecking format of 4-digit values...\n", df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'], "\n")

    # Use Regex to remove ',' from four-digit values, with capture groups.
    df_nhl = find_and_replace(df_nhl, r'(\d),(\d)(\d)(\d)', r'\1\2\3\4')

    # Check format of 4-digit value after replacement.
    print("Reformatted 4-digit values...\n", df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'], "\n")

    # Sort dataframe by Points ('P') and Games Played ('GP') columns.
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

    # Handle missing data.
    # Dataset contains entries for players who played prior to modern record keeping. Missing values are represented
    # with '--'.
    # Options:
    #     1. Replace '--' with NaN, and use .dropna().
    #         * Excludes notable players from analysis.
    #     2. Replace '--' with 0.
    #         * May under-represent actual value.
    #         * Lowers mean of the series.
    #     3. Replace '--' with league mean.
    #         * May over- or under-represent actual value.
    #         * Preserves mean of the series.

    # Convert data types.
    # Requires replacement of '--' in series.
    # df_nhl['EVG'] = df_nhl['EVG'].astype('int64')

    print(df_nhl.info())

    # Check for missing data.

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
