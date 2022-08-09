# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
from get_dataset import get_dataset_excel
from summarise_dataset import summarise_dataset
from check_for_duplicates import check_for_duplicates
from find_and_replace import find_and_replace
import handle_missing_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Don't suppress columns in terminal output.
pd.options.display.width = 0
pd.options.display.max_rows = 7461

if __name__ == '__main__':
    # Data Collection
    # Compile dataframe from Excel files.
    df_nhl = get_dataset_excel("./Raw Data Files/")

    # Summarise dataset.
    summarise_dataset(df_nhl)

    # Data Cleaning
    # Check format of 4-digit value.
    print("Checking format of 4-digit values...\n",
          df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
          "\n")

    # Use Regex to remove ',' from four-digit values, with capture groups.
    df_nhl = find_and_replace(df_nhl, r'(\d),(\d)(\d)(\d)', r'\1\2\3\4')

    # Check format of 4-digit value after replacement.
    print("Checking format of 4-digit values...\n",
          df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
          "\n")

    # Sort dataframe by Points, Goals, and Assists and columns.
    print("Sorting by P, G, A...\n")
    df_nhl = df_nhl.sort_values(by=['P', 'G', 'A'], ascending=False).reset_index()

    summarise_dataset(df_nhl)

    # Check for duplicate rows.
    check_for_duplicates(df_nhl)

    # Handling Missing Data
    # Explore missing data to determine how best to handle.
    df_nhl, missing_count = handle_missing_data.replace_with_nan(df_nhl)
    print("Getting df_nhl.head()...\n", df_nhl.head(), "\n")
    print("Getting missing_count...\n", missing_count, "\n")

    # S/C - Impute with mode.
    df_nhl["S/C"] = handle_missing_data.impute_with_mode(df_nhl["S/C"])

    # EVG, EVP, PPG, PPP, SHG, SHP - Impute with mean.
    df_nhl["EVG"] = handle_missing_data.impute_with_mean(df_nhl["EVG"])
    df_nhl["EVP"] = df_nhl["EVP"].astype("float64")                        # Intermediate type coversion to resolve TypeError on impute_with_mean().
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
    print("Dropping TOI/GP and FOW% columns...\n")
    df_nhl = df_nhl.drop(["TOI/GP", "FOW%"], axis=1)

    summarise_dataset(df_nhl)

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
    summarise_dataset(df_nhl)

    # Exploratory Data Analysis
    print("Getting df_nhl.describe(include='all')...\n", df_nhl.describe(include="all"), "\n")

    # Extract standout players - per df_nhl.describe().
    # Extract players responsible for max values - iterating over cols_max.
    cols_max = ["GP", "G", "A", "P", "PIM", "P/GP", "EVG", "EVP", "PPG", "PPP", "SHG", "SHP", "OTG", "GWG", "S"]
    for col in cols_max:
        print(f"Getting player with most {col}...\n", df_nhl.loc[df_nhl[f"{col}"] == max(df_nhl[f"{col}"])], "\n")

    # Eliminate players with insignificant shot totals from max. S% calculation.
    df_significant_shots = df_nhl[df_nhl["S"] >= 100]

    # Extract player with max. S% (with minimum of 100 shots taken).
    print("Getting player with highest S% (min. 100 shots)...\n",
          df_significant_shots.loc[df_significant_shots["S%"] == max(df_significant_shots["S%"])], "\n")

    # Extract player with highest +/-.
    print("Getting player with highest +/-...\n", df_nhl.loc[df_nhl["+/-"] == max(df_nhl["+/-"])], "\n")

    # Extract player with lowest +/-.
    print("Getting player with lowest +/-...\n", df_nhl.loc[df_nhl["+/-"] == min(df_nhl["+/-"])], "\n")

    # Extract other noteworthy players, by name - using for loop.
    notable_players_1 = ["Mario Lemieux", "Mike Bossy", "Gordie Howe",
                       "Sidney Crosby", "Evgeni Malkin",
                       "Nicklas Lidstrom", "Erik Karlsson", "Cale Makar"]
    for name in notable_players_1:
        print(f"Getting player {name}...\n", df_nhl.loc[df_nhl["Player"] == name], "\n")

    # Extract other noteworthy players, by name - using for iter()/next().
    notable_players_2 = ["Connor McDavid", "Connor McDavid",    # Same value required twice for print statement using
                       "Auston Matthews", "Auston Matthews"]    # iter()/next(). For loop preferred for this use case.
    notable_players_2_iter = iter(notable_players_2)
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")

    # Plot Data for EDA.
    # Set plot theme.
    sns.set()

    # Define features of interest.
    games_played = df_nhl['GP']
    points = df_nhl['P']

    # Scatter plots of points/goals/assists vs. games played, using plt.
    fig1, axs = plt.subplots(3, 1)
    fig1.suptitle('Career Points/Goals/Assists vs. Games Played - Regular Season')

    sns.scatterplot(x=games_played, y=points, color='b', alpha=0.5, label='Points', ax=axs[0])
    axs[0].set(xlabel='Games Played')
    axs[0].set(ylabel='Count')
    axs[0].set_yticks(range(0, 3500, 500))
    axs[0].legend(loc='upper left')
    axs[0].text(1487, 2857, "Wayne Gretzky")
    axs[0].text(1779, 1197, "Patrick Marleau")
    axs[0].text(915, 1723, "Mario Lemieux")
    axs[0].text(752, 1126, "Mike Bossy")
    axs[0].text(1274, 1410, "Alex Ovechkin")
    axs[0].text(1108, 1409, "Sidney Crosby")

    sns.scatterplot(x=games_played, y=df_nhl['G'], color='r', alpha=0.5, label='Goals', ax=axs[1])
    axs[1].set(xlabel='Games Played')
    axs[1].set(ylabel='Count')
    axs[1].set_yticks(range(0, 3500, 500))
    axs[1].legend(loc='upper left')

    sns.scatterplot(x=games_played, y=df_nhl['A'], color='g', alpha=0.5, label='Assists', ax=axs[2])
    axs[2].set(xlabel='Games Played')
    axs[2].set(ylabel='Count')
    axs[2].set_yticks(range(0, 3500, 500))
    axs[2].legend(loc='upper left')

    plt.show()

    # Set up figure for multiple plots.
    f, axs = plt.subplots(1, 3)
    f.suptitle('Points per Position')

    # Box plot of P vs. Pos, using sns.
    sns.boxplot(data=df_nhl["P"], ax=axs[0])
    axs[0].grid(True, axis='both')
    axs[0].set(xlabel="Position")
    axs[0].set_xticklabels(["All"])
    axs[0].set(ylabel="Points")

    # Box plot of P vs. Pos, with further categorisation on S/C.
    sns.boxplot(x="Pos", y="P", data=df_nhl, ax=axs[1])
    axs[1].grid(True, axis='both')
    axs[1].set(xlabel="Position")
    axs[1].set(ylabel="Points")

    # Box plot of P vs. Pos, with further categorisation on S/C.
    sns.boxplot(x="Pos", y="P", hue="S/C", data=df_nhl, ax=axs[2])
    axs[2].grid(True, axis='both')
    axs[2].set(xlabel="Position")
    axs[2].set(ylabel="Points")

    plt.show()

    # Plot histogram of P.
    f, axs = plt.subplots(1, 2)
    f.suptitle('Points Histogram')
    sns.histplot(data=df_nhl, x=df_nhl["P"], ax=axs[0])
    axs[0].set(xlabel="Points")
    axs[0].set(ylabel="Player Count")

    # Zoom in on high-end.
    sns.histplot(data=df_nhl, x=df_nhl["P"], ax=axs[1])
    axs[1].set(xlim=(1200, 3001), ylim=(0, 20))
    axs[1].set(xlabel="Points")
    axs[1].set(ylabel="Player Count")

    plt.show()