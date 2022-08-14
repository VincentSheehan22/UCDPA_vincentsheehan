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
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as MSE
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

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

    # Extract other noteworthy players, by name - using iter()/next().
    notable_players_2 = ["Connor McDavid", "Connor McDavid",    # Same value required twice for print statement using
                       "Auston Matthews", "Auston Matthews"]    # iter()/next(). For loop preferred for this use case.
    notable_players_2_iter = iter(notable_players_2)
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")
    print(f"Getting player {next(notable_players_2_iter)}...\n",
          df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")

    # Plot data for EDA.
    # Set plot theme.
    sns.set()
    get_pga_scatterplot(df_nhl)
    # # Generate figure for subplots.
    # fig1, axs = plt.subplots(3, 1)
    # fig1.suptitle('Career Points/Goals/Assists vs. Games Played - Regular Season')
    #
    # # Plot Points vs. Games Played on subplot 0.
    # sns.scatterplot(x=df_nhl['GP'], y=df_nhl['P'], color='b', alpha=0.5, label='Points', ax=axs[0])
    # axs[0].set(xlabel='Games Played')
    # axs[0].set(ylabel='Count')
    # axs[0].set_yticks(range(0, 3500, 500))
    # axs[0].legend(loc='upper left')
    # axs[0].text(1487, 2857, "Wayne Gretzky")
    # axs[0].text(1779, 1197, "Patrick Marleau")
    # axs[0].text(915, 1723, "Mario Lemieux")
    # axs[0].text(752, 1126, "Mike Bossy")
    # axs[0].text(1274, 1410, "Alex Ovechkin")
    # axs[0].text(1108, 1409, "Sidney Crosby")
    #
    # # Plot Goals vs. Games Played on subplot 1.
    # sns.scatterplot(x=df_nhl['GP'], y=df_nhl['G'], color='r', alpha=0.5, label='Goals', ax=axs[1])
    # axs[1].set(xlabel='Games Played')
    # axs[1].set(ylabel='Count')
    # axs[1].set_yticks(range(0, 3500, 500))
    # axs[1].legend(loc='upper left')
    # axs[1].text(1487, 894, "Wayne Gretzky")
    # axs[1].text(1767, 801, "Gordie Howe")
    # axs[1].text(1274, 780, "Alex Ovechkin")
    #
    # # Plot Assists vs. Games Played on subplot 2.
    # sns.scatterplot(x=df_nhl['GP'], y=df_nhl['A'], color='g', alpha=0.5, label='Assists', ax=axs[2])
    # axs[2].set(xlabel='Games Played')
    # axs[2].set(ylabel='Count')
    # axs[2].set_yticks(range(0, 3500, 500))
    # axs[2].legend(loc='upper left')
    # axs[2].text(1487, 1963, "Wayne Gretzky")
    # axs[2].text(1731, 1249, "Ron Francis")
    # axs[2].text(1756, 1193, "Mark Messier")
    #
    # plt.show()

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
    # Define feature matrix X, and target (labels) y, for training the model.
    target = "S%"

    # Drop target from X.
    X = df_nhl.drop(target, axis=1)

    # Drop non-numeric features from X.
    X = X.drop(["Player", "S/C", "Pos"], axis=1)

    # Convert DataFrame X, and Series y to numpy arrays.
    X = X.values
    y = df_nhl[target].values

    # Craete single-feature array for preliminary use.
    X_feature = X[:, 4]

    print("Getting type(X_feature), type(y)...\n", type(X_feature), type(y), "\n")

    # Reshape numpy arrays to unknown number of rows, 1 column.
    y = y.reshape(-1, 1)
    X_feature = X_feature.reshape(-1, 1)

    # Define test and training data for DecisionTreeRegressor on single feature.
    X_train, X_test, y_train, y_test = train_test_split(X_feature, y, test_size=0.3, random_state=SEED)

    # Instantiate machine learning model - DecisionTreeRegressor.
    dt_X_feature = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.14, random_state=SEED)

    # Perform k-fold cross-validation to determine bias and variance.
    MSE_CV = - cross_val_score(dt_X_feature, X_train, y_train, cv=10,
                               scoring="neg_mean_squared_error",
                               n_jobs=-1)

    # Fit model to training data
    dt_X_feature.fit(X_train, y_train)

    # Predict the labels of the test and training sets.
    y_pred_train = dt_X_feature.predict(X_train)
    y_pred_test = dt_X_feature.predict(X_test)

    print(f"CV MSE: {MSE_CV.mean()}")
    print(f"Train MSE: {MSE(y_train, y_pred_train)}")
    print(f"Test MSE: {MSE(y_test, y_pred_test)}")

    RMSE_CV = (MSE_CV.mean()) ** (1 / 2)
    print(f"RMSE_CV: {RMSE_CV}")

    RMSE_train = (MSE(y_train, y_pred_train) ** (1 / 2))
    print(f"RMSE_train: {RMSE_train}")

    RMSE_test = (MSE(y_test, y_pred_test) ** (1 / 2))
    print(f"RMSE_test_single_feature: {RMSE_test}\n")


    # Define test and training data for DecisionTreeRegressor on full feature set.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

    dt_X = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.14, random_state=SEED)

    MSE_CV = - cross_val_score(dt_X, X_train, y_train, cv=10,
                               scoring="neg_mean_squared_error",
                               n_jobs=-1)

    dt_X.fit(X_train, y_train)

    y_pred_train = dt_X.predict(X_train)
    y_pred_test = dt_X.predict(X_test)

    print(f"CV MSE: {MSE_CV.mean()}")
    print(f"Train MSE: {MSE(y_train, y_pred_train)}")
    print(f"Test MSE: {MSE(y_test, y_pred_test)}")

    RMSE_CV = (MSE_CV.mean()) ** (1 / 2)
    print(f"RMSE_CV: {RMSE_CV}")

    RMSE_train = (MSE(y_train, y_pred_train) ** (1 / 2))
    print(f"RMSE_train: {RMSE_train}")

    RMSE_test = (MSE(y_test, y_pred_test) ** (1 / 2))
    print(f"RMSE_test_all_features: {RMSE_test}\n")

    # Implement ensembling with RandomForestRegressor.
    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=0.12, random_state=SEED)

    rf.fit(X_train, np.ravel(y_train))      # Using np.ravel() to convert from column-vector to 1d array, as promted by DataConversionWarning.
    y_pred = rf.predict(X_test)

    RMSE_rf_test = (MSE(y_test, y_pred) ** (1 / 2))
    print(f"RMSE_test_all_features_rf: {RMSE_rf_test}")

    # Plot feature importances.
    importances = pd.Series(data=rf.feature_importances_,
                            index=pd.Series(["GP", "G", "A", "P", "+/-", "PIM", "P/GP", "EVG", "EVP", "PPG", "PPP", "SHG",
                                          "SHP", "OTG", "GWG", "S", "S%"]))

    importances_sorted = importances.sort_values()

    importances_sorted.plot(kind='barh', color='lightgreen')
    plt.title(f'Feature Importance in Prediction of {target}')
    plt.show()

    # Hyperparameter tuning
