# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
from get_dataset import get_dataset_excel
from summarise_dataset import summarise_dataset
from check_for_duplicates import check_for_duplicates
from find_and_replace import find_and_replace
import handle_missing_data
import matplotlib.pyplot as plt
import seaborn as sns
from get_pga_scatterplot import get_pga_scatterplot
from get_p_pos_boxplot import get_p_pos_boxplot
from get_p_histogram import get_p_histogram
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as MSE
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from implement_decision_tree import implement_decision_tree
from implement_random_forest import implement_random_forest

SEED = 1

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
    print("Checking format of 4-digit values...\n", df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'], "\n")

    # Use Regex to remove ',' from four-digit values, with capture groups.
    df_nhl = find_and_replace(df_nhl, r"(\d),(\d)(\d)(\d)", r"\1\2\3\4")

    # Check format of 4-digit value after replacement.
    print("Checking format of 4-digit values...\n", df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'], "\n")

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
    df_nhl["EVP"] = df_nhl["EVP"].astype("float64")                        # Intermediate type coversion to resolve
                                                                           # TypeError on impute_with_mean().
                                                                           # Include conversion in impute_with_mean()
                                                                           # function definition?
    df_nhl["EVP"] = handle_missing_data.impute_with_mean(df_nhl["EVP"])    # TypeError: can only concatenate str (not
                                                                           # "int") to str
    df_nhl["PPG"] = handle_missing_data.impute_with_mean(df_nhl["PPG"])
    df_nhl["PPP"] = handle_missing_data.impute_with_mean(df_nhl["PPP"])
    df_nhl["SHG"] = handle_missing_data.impute_with_mean(df_nhl["SHG"])
    df_nhl["SHP"] = handle_missing_data.impute_with_mean(df_nhl["SHP"])

    # S, S% - Impute with mean.
    df_nhl["S"] = df_nhl["S"].astype("float64")
    df_nhl["S"] = handle_missing_data.impute_with_mean(df_nhl["S"])        # TypeError: can only concatenate str (not
                                                                           # "int") to str
    df_nhl["S%"] = df_nhl["S%"].astype("float64")
    df_nhl["S%"] = handle_missing_data.impute_with_mean(df_nhl["S%"])      # TypeError: can only concatenate str (not
                                                                           # "int") to str

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

    # Extract other noteworthy players, by name - using iter()/next().
    notable_players_2 = ["Connor McDavid", "Connor McDavid",    # Same value required twice for print statement using
                       "Auston Matthews", "Auston Matthews"]    # iter()/next(). For loop preferred for this use case.
    notable_players_2_iter = iter(notable_players_2)
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")

    # Plot data for EDA.
    # Set seaborn plot theme.
    sns.set()

    # Run custom plotting functions.
    get_pga_scatterplot(df_nhl)
    get_p_pos_boxplot(df_nhl)
    get_p_histogram(df_nhl)

    # Merging Dataframes
    # Generating second data frame based on the 'Bio Info' report from NHL.com. Only the fist page is taken, sorted by
    # P, G, A, for additional analysis on top 100 players in the df_nhl dataset.
    df_bio_top_100 = get_dataset_excel("./Raw Data Files/", report="Bio Info")
    print("Getting df_bio_top_100.head()...\n", df_bio_top_100.head(), "\n")

    # Copy top 100 players (based on earlier sorting by P, G, A) from df_nhl into df_nhl_top_100.
    df_nhl_top_100 = df_nhl.head(100)

    df_nhl_top_100_extended = pd.merge(df_nhl_top_100,
                                       df_bio_top_100[["DOB", "Birth City", "S/P", "Ctry", "Ntnlty", "Ht", "Wt",
                                                      "Draft Yr", "Round", "Overall", "1st Season", "HOF"]],
                                       left_on=df_nhl_top_100["Player"],
                                       right_on=df_bio_top_100["Player"])
    print("Getting df_nhl_top_100_extended.head()...\n", df_nhl_top_100_extended.head(), "\n")
    df_nhl_top_100_extended = df_nhl_top_100_extended.drop("key_0", axis=1)
    print("Getting df_nhl_top_100_extended.describe(include='all'').T...\n",
          df_nhl_top_100_extended.describe(include="all").T, "\n")

    # Machine Learning
    # Define feature matrix X, and target (labels) y.
    target = "S%"

    # Drop target from X.
    X_all_features = df_nhl.drop(target, axis=1)

    # Drop non-numeric features from X.
    X_all_features = X_all_features.drop(["Player", "S/C", "Pos"], axis=1)

    # Convert DataFrame X, and Series y to numpy arrays.
    X_all_features = X_all_features.values
    y = df_nhl[target].values

    # Create single-feature array for preliminary use.
    X_single_feature = X_all_features[:, 4]

    print("Getting type(X_single_feature)...\n", type(X_single_feature), "\n")
    print("Getting type(X_all_features)...\n", type(X_all_features), "\n")
    print("Getting type(y)...\n", type(y), "\n")

    # Reshape numpy arrays to unknown number of rows, 1 column.
    y = y.reshape(-1, 1)
    X_single_feature = X_single_feature.reshape(-1, 1)

    # Implement decision tree with single feature, and all features in feature matrix X.
    implement_decision_tree(X_single_feature, y, SEED)
    implement_decision_tree(X_all_features, y, SEED)

    # Implement ensembling with RandomForestRegressor. Target string is specified as argument for plotting purposes.
    rf = implement_random_forest(X_all_features, y, SEED, target)

    # Hyperparameter tuning
    print("Getting RandomForestRegressor hyperparamters...\n", rf.get_params(), "\n")
