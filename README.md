# UCDPA Project Assignment - Analysing NHL Regular Season Career Statistics

## GitHub URL
https://github.com/VincentSheehan22/UCDPA_vincentsheehan

## Abstract
The aim of this project is to explore and demonstrate the learning outcomes of the UCD Professional Academy Specialist
Certificate in Data Analytics Essentials course. The project aims to cover the scope of a typical data analytics
workflow, including data collection, data cleaning, exploratory data analysis with summary statistics and visualisation,
merging of DataFrames, and application of a machine learning algorithm to the dataset.

The workflow, described in detail below, begins with collecting and compiling the dataset into a Pandas DataFrame object
for further analysis. The dataset is then cleaned of stray characters, missing values and incorrect data types, and 
checked for duplicate entries. The DataFrame object is summarised at multiple points to demonstrate the transformation.

Once a clean DataFrame is arrived at, some first impressions are drawn form the DataFrame description table. Values of
interest from the DataFrame description table are used to present the associated players (i.e., leaders in points,
goals, etc.). A list of otherwise notable players is also provided in order to obtain their entries from the dataset
for comparative purposes.

The DataFrame is then visualised by way of a scatter plot of points/goals/assists vs games played, with annotations
locating some noteworthy players. A box plot is generated to visualise the points data in terms of percentiles, with
some categorisation on player position and the 'shoots/catches' attribute. A histogram is also provided, giving the
distribution of players vs. number of points.

DataFrame merging is demonstrated with a subset of the top 100 entries in the dataset (sorted on points, goal, assists).
A supplemental dataset for the same 100 players, also available from https://www.nhl.com (National Hockey League 2022),
is supplied for the merge. This dataset provides biographical information, such as date-of-birth, height, weight, and
nationality - further attributes that could be applied for classification use cases.

Supervised machine learning is applied to the dataset using a decision tree regressor from the scikit-learn package. The
target chosen for prediction, y, is goals (G) as being one of the most indicative measures of player performance.
The model is first trained using only one column of the dataset in the feature matrix, X. Games played is chosen for
this as it is explored earlier via scatter plot. The metric used for evaluating model performance is the 
root-mean-squared-error. RMSE is calculated on the negative cross-validation score of the training data, as a baseline
metric. The RMSE of prediction of y on the training data, and on the test data is the calculated for comparison with
RMSE of cross-validation. Similar values are obtained for all RMSEs, though RMSE for prediction on the test set is
lower than that on the training set, suggesting the model is not well-fitted to the data.

The model is then trained by fitting with all numeric features in the feature matrix. An improvement in RMSE is observed
with a higher number of features included.

Ensembling is explored using the RandomForestRegressor algorithm from Scikit-Learn, and RMSE measured again. With
default hyperparameters, the RandomForestRegressor does not improve model performance. Feature importances are plotted
as a bar chart, showing relatively few features taken into account.

Hyperparameter tuning of the RandomForestRegresoor model, using GridSearchCV, is performed. Iterating through a set of
hyperparameter values defined in a dictionary, the best model is determined. The best model is fitted to the training
set, and prediction for y made on test set. The RMSE of test set prediction is calculated, showing an improvement over
both the DecisionTreeRegrssor and un-tuned RandomForestRegressor model. Feature importances are again plotted as bar
chart, showing that more features are taken into account by the best model based on tuned hyperparameters.

Output plots, along with a terminal log of `main.py` execution are included in the repository.

## Introduction
The dataset chosen for this project is a mostly numeric dataset containing player statistics from the National Hockey
League. This dataset was chosen as it is of personal interest, and as having a degree of familiarity with the contents.
It is a large dataset offering opportunities for exploring regression and classification techniques.

## Dataset
The National Hockey League, a North American ice-hockey league, operating since 1917 maintains on its website - 
https://www.nhl.com - a record of player statistics dating back to the inaugural 1917-18 season. This dataset includes
entries for over 7000 players to have played a regular season game in the NHL, and offers player-by-player comparison
in areas such as games played, goals, assists (primary and secondary passes leading to goals), and points (goals +
assists).

The website provides filtering of stats by season, team, player position and game type, among others. Data is available
in several reports, with different statistics tracked in each. For the scope of this project, analysis will be performed
on the Skaters/All-Time/Regular Season/Summary report, the first page of which is available at the link below. 

NHL all-time player statistics for regular season games - Summary report:  
https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100

Analysis of other available reports in combination with the summary report is explored briefly with the Bio Info report,
but left largely as an exercise, beyond the scope of this project.

NHL all-time player statistics for regular season games - Bio Info report:  
https://www.nhl.com/stats/skaters?report=bios&reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100

## Implementation Process
### Data Import
Multiple methods of data import were explored, including via API, web scraping, and Pandas read functions.

#### NHL Stats API
Dataset collection via API was explored. An API was found to be available, but not well documented.

Team and season data can be found at below links, but a useful API for the player career stats dataset was not found. 
* https://statsapi.web.nhl.com/api/v1/teams
* https://statsapi.web.nhl.com/api/v1/seasons

#### Web Scraping
Dataset collection via web scraping was explored, but the tabular data on NHL.com was found to be implemented as
ReactTable objects, and not parsable with the BeautifulSoup package.

#### Pandas File Reading
NHL.com provides the stats data for download in Excel format. This was found to be the most direct approach to acquiring
the dataset. However, the table view, and thus exported Excel file, is limited to 100 rows per page.

A script - `get_data_urls.py` - was created for pagination of the tabular data by incrementing the page number within
the URL, writing all page URLs to file for future reference. It is left as an exercise, beyond the scope of this
project, to utilise page URLs for browser automation of the Excel file export.

The dataset was manually downloaded as a set of 75 Excel files (~100 entries apiece), containing 7461 records - player
career statistics from 1917-18 to 2021-2022 seasons.

With the data collected and stored in the `Raw Data Files` directory, the `pandas.read_excel()` function is used to
compile the Excel file into a DataFrame, within the `get_dataset_excel()` function defined in `get_dataset.py`. The
returned DataFrame is assigned to the variable `df_nhl`.

```Python
df_nhl = get_dataset_excel("./Raw Data Files/")
```

### Data Cleaning
#### Sanity Check
Once generated, the `df_nhl` DataFrame is inspected to assess any further operations required before analysis can be
performed. This is done using the `summarise_dataset()` function from `summarise_dataset.py`. This takes a DataFrame as
argument and bundles calls to the `.shape()`, `.head()`, `.tail()`, `.describe()`, and `.info()` functions on the input
DataFrame, printing their output. This function is called at multiple points in the execution to demonstrate how the
DataFrame is transformed as data cleaning operations are performed.

#### Regex Replacement
The dataset contains text and numeric data. Numeric values greater than 3 digits are represented as `"1,234"`. This is
problematic for sorting and for assessing the column as a continuous range, for example, plotting as axis ticks. Regex
is used to convert to the required `1234` format:  
* Find: `(\d),(\d)(\d)(\d)`  
* Replace: `\1\2\3\4`

The above regex strings are provided as parameters to the `find_and replace()` function defined in
`find_and_replace.py`, along with the dataframe `df_nhl`. The regex strings use capture groups (parentheses) to capture
and return the 1st, 2nd, 3rd and 4th digit characters, eliminating the `,` character.

```Python
# Check format of 4-digit value.
print("\nChecking format of 4-digit values...\n",
      df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
      "\n")

# Use Regex to remove ',' from four-digit values, with capture groups.
df_nhl = find_and_replace(df_nhl, r'(\d),(\d)(\d)(\d)', r'\1\2\3\4')

# Check format of 4-digit value after replacement.
print("Reformatted 4-digit values...\n",
      df_nhl.loc[df_nhl['Player'] == 'Wayne Gretzky'],
      "\n")
```

```
Checking format of 4-digit values...
           Player S/C Pos     GP    G      A      P  +/-  PIM  P/GP  EVG    EVP  PPG  PPP SHG  SHP  OTG  GWG      S    S% TOI/GP FOW%
0  Wayne Gretzky   L   C  1,487  894  1,963  2,857  520  577  1.92  617  1,818  204  890  73  149    2   91  5,088  17.6     --   49 

Reformatted 4-digit values...
           Player S/C Pos    GP    G     A     P  +/-  PIM  P/GP  EVG   EVP  PPG  PPP SHG  SHP  OTG  GWG     S    S% TOI/GP FOW%
0  Wayne Gretzky   L   C  1487  894  1963  2857  520  577  1.92  617  1818  204  890  73  149    2   91  5088  17.6     --   49 
```

#### Sorting
With the comma characters removed from 4-digit values, the Dataframe can be sorted by 'P' (points), 'G' (goals), and 'A'
(assists) columns, with index reset, to match the default presentation of the data on https://www.nhl.com. This is the
most useful ranking for this analysis as points, goals, and assists are the most direct indicators of performance.

```Python
df_nhl = df_nhl.sort_values(by=['P', 'G', 'A'], ascending=False).reset_index()
```

```
Getting .head()...
    index         Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP  EVG   EVP  PPG  PPP SHG  SHP  OTG  GWG     S    S% TOI/GP  FOW%
0      0  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617  1818  204  890  73  149    2   91  5088  17.6     --    49
1      1   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538  1296  217  610  11   15   19  135  5637  13.6     --  24.5
2      2   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452  1162  179  581  63  144    8   92  4221  16.4     --  54.7
3      3    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566  1250  211  564  24   36    0  121  3803    --     --    --
4      4    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349  1040  188  727  12   31    4   79  3756  14.6     --  54.8
```

#### Duplicate Data
The `df_nhl` DataFrame is checked for duplicate entries with the custom function `check_for_duplicates()`. This takes a
DataFrame as argument, uses the .duplicated() function to check for duplicates, prints duplicates if found, and drops
duplicates from DataFrame, returning the DataFrame without  duplicates. In this instance no duplicate entries are found.

```Python
check_for_duplicates(df_nhl)
```

```
Checking for duplicates...

Getting duplicates...
 Empty DataFrame
Columns: [index, Player, S/C, Pos, GP, G, A, P, +/-, PIM, P/GP, EVG, EVP, PPG, PPP, SHG, SHP, OTG, GWG, S, S%, TOI/GP, FOW%]
Index: []
```

#### Missing Data
The dataset contains entries for players who played prior to modern record keeping. Some columns such as 'EVG' contain
missing data, represented as '--'. These require replacement in order to complete type conversion.

Several replacement options were considered, including those listed below:
1. Replace `--` with `NaN`, and use `.dropna()`.
    * Excludes notable players from analysis.
2. Replace `--` with 0.
    * May under-represent actual value.
    * Lowers mean of the series.
3. Replace `--` with league mean.
   * May over- or under-represent actual value.
   * Preserves mean of the series.
4. Remove columns containing `--`.
   * Excludes feature from further analysis.

Missing data was explored to determine how best to handle. A module, `handle_missing_data.py`, was created to define
functions for dealing with missing data. The first function defined here, `replace_with_nan()`, takes a DataFrame as
input and converts entries with value `--` - representing missing data in the NHL dataset - to numpy `NaN` objects. With
`NaN` objects populated in the dataframe, the function then obtains a count of missing data per column. The modified
DataFrame and missing data counts are then returned.

```Python
# Explore missing data to determine how best to handle.
df_nhl, missing_count = handle_missing_data.replace_with_nan(df_nhl)
print("Getting df_nhl.head()...\n", df_nhl.head(), "\n")
print("Getting missing_count...\n", missing_count, "\n")
```

Passing `df_nhl` to `handle_missing_data()`, conversion of missing data to `NaN` is successful, as shown with
`df_nhl.head()`:

```
Getting df_nhl.head()...
    index         Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP    EVG   EVP    PPG    PPP   SHG    SHP  OTG  GWG     S    S% TOI/GP  FOW%
0      0  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617.0  1818  204.0  890.0  73.0  149.0    2   91  5088  17.6    NaN  49.0
1      1   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538.0  1296  217.0  610.0  11.0   15.0   19  135  5637  13.6    NaN  24.5
2      2   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452.0  1162  179.0  581.0  63.0  144.0    8   92  4221  16.4    NaN  54.7
3      3    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566.0  1250  211.0  564.0  24.0   36.0    0  121  3803   NaN    NaN   NaN
4      4    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349.0  1040  188.0  727.0  12.0   31.0    4   79  3756  14.6    NaN  54.8
```

The missing data counts provide some insight on how to handle missing values for each column.

```
Getting missing_count...
 index        0
Player       0
S/C         74
Pos          0
GP           0
G            0
A            0
P            0
+/-          0
PIM          0
P/GP         0
EVG        272
EVP        272
PPG        272
PPP        272
SHG        272
SHP        272
OTG          0
GWG          0
S         1057
S%        1461
TOI/GP    4321
FOW%      4680
dtype: int64
```

* **S/C (Shoots/Catches)**: Represents 'handedness' of the player, either left (L) or right (R). In this in instance,
exploring only out-field players and not the Goalie position, this field refers to shooting hand.
  * One approach to impute this, would be to take the ratio of L:R for the available data and distribute 'L' and 'R'
  values for the missing data, according to the overall ratio.
  * Another option is to replace with mode, the most frequently occurring value.
    * Suitable given low number of missing values, assuming right-handedness is prevalent.
    * Skews dataset in favour of L or R, which may not be representative.
  * It may also be useful to drop this column, as having limited applicability. However, analysis of success for
  left-handed vs. right-handed shooters may be of interest.
* **EVG/EVP/PPG/PPP/SHG/SHP**: Represent goals and points in various game scenarios.
  * EV: Even-strength, both teams have the same number of players on the ice.
  * PP: Power-play, team has additional players(s) on the ice relative to opponent due to a penalty situation.
  * SH: Shorthanded, team has fewer players(s) on the ice relative to opponent due to a penalty situation.
  * As there are relatively few missing entries, values are imputed to league mean.
* **S**: Shots taken by player.
  * Imputed to league mean.
    * Does not account for historical variance in playing styles.
* **S%**: Shooting percentage, i.e., `(goals / shots) * 100`.
  * Imputed to league mean.
    * Does not account for historical variance in playing styles.
* **TOI/GP**: Time-on-ice per game played. Skaters rotate onto and off the playing surface in shifts of ~30-90 seconds
duration. Typical cumulative time-on-ice for a player in a 60-minute game can range from 5 to 20 minutes. Data likely
unavailable due to recency of player location tracking technology.
  * As data is not available for over 50% of players in the dataset, this column will be dropped.
* **FOW%**: Face-off win percentage. Game scenario in which two players contest possession of the puck. Typically, taken
by players in the centre position.
  * As data is not available for over 50% of players in the dataset, this column will be dropped.

Based on the above assessment two further functions are defined in `handle_missing-data.py`: `impute_with_mode()` and
`impute_with_mean()`. Both take a Pandas series (DataFrame column) as argument and replace `NaN` values with mode and
mean, respectively.

`NaN` values are imputed as follows:
```Python
# S/C - Impute with mode.
df_nhl["S/C"] = handle_missing_data.impute_with_mode(df_nhl["S/C"])

# EVG, EVP, PPG, PPP, SHG, SHP - Impute with mean.
df_nhl["EVG"] = handle_missing_data.impute_with_mean(df_nhl["EVG"])
```

TOI/GP and FOW% columns are dropped as follows:
```Python
df_nhl = df_nhl.drop(["TOI/GP", "FOW%"], axis=1)
```

```
Imputing S/C with mode: 'L'...

Imputing EVG with mean: '36.007372374460985'...

Imputing EVP with mean: '94.09514536096815'...

Imputing PPG with mean: '11.648629851161497'...

Imputing PPP with mean: '33.25441646960634'...

Imputing SHG with mean: '1.598970649603561'...

Imputing SHP with mean: '3.24634858812074'...

Imputing S with mean: '497.60805746408494'...

Imputing S% with mean: '8.098416666666697'...

Dropping TOI/GP and FOW% columns...
```

#### Type Conversion
The `df_nhl` DataFrame contains numeric columns stored as object type, as shown by `.info()`. As such, these
columns are not represented with `df_nhl.describe()` Conversion to int and float types is required. The string-based
columns Player, S/C, and Pos are also explicitly converted to string type.

```
Getting .info()...
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7461 entries, 0 to 7460
Data columns (total 21 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   index   7461 non-null   int64  
 1   Player  7461 non-null   object 
 2   S/C     7461 non-null   object 
 3   Pos     7461 non-null   object 
 4   GP      7461 non-null   object 
 5   G       7461 non-null   int64  
 6   A       7461 non-null   object 
 7   P       7461 non-null   object 
 8   +/-     7461 non-null   int64  
 9   PIM     7461 non-null   object 
 10  P/GP    7461 non-null   float64
 11  EVG     7461 non-null   float64
 12  EVP     7461 non-null   float64
 13  PPG     7461 non-null   float64
 14  PPP     7461 non-null   float64
 15  SHG     7461 non-null   float64
 16  SHP     7461 non-null   float64
 17  OTG     7461 non-null   int64  
 18  GWG     7461 non-null   int64  
 19  S       7461 non-null   float64
 20  S%      7461 non-null   float64
dtypes: float64(9), int64(5), object(7)
memory usage: 1.2+ MB
None 
```

```
Getting .describe()...
              index            G          +/-         P/GP          EVG          EVP          PPG          PPP          SHG          SHP          OTG          GWG            S           S%
count  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000
mean     49.340571    48.807935    -2.009382     0.300495    36.007372    94.095145    11.648630    33.254416     1.598971     3.246349     0.593486     6.973596   497.608057     8.098417
std      28.847304    90.376002    50.052797     0.240286    61.805525   147.620471    26.892534    74.652991     4.122534     7.390476     1.702940    13.465574   698.925321     6.877763
min       0.000000     0.000000  -257.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000
25%      24.000000     1.000000   -14.000000     0.130000     1.000000     3.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000    28.000000     4.400000
50%      49.000000    10.000000    -1.000000     0.250000     9.000000    29.000000     1.000000     3.000000     0.000000     0.000000     0.000000     1.000000   256.000000     8.098417
75%      74.000000    53.000000     0.000000     0.430000    39.000000   118.000000    11.000000    33.000000     1.000000     3.246349     0.000000     7.000000   554.000000    10.700000
max      99.000000   894.000000   722.000000     1.920000   617.000000  1818.000000   285.000000   890.000000    73.000000   149.000000    24.000000   135.000000  6209.000000   100.000000 

```

Type conversion is performed column-by-column with the Pandas .`astype()` function as follows:
```Python
df_nhl["Player"] = df_nhl["Player"].astype("string")
```

This is done for all remaining columns in the dataset, concluding data cleaning operations.
```
Getting .info()...
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7461 entries, 0 to 7460
Data columns (total 21 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   index   7461 non-null   int64  
 1   Player  7461 non-null   string 
 2   S/C     7461 non-null   string 
 3   Pos     7461 non-null   string 
 4   GP      7461 non-null   int64  
 5   G       7461 non-null   int64  
 6   A       7461 non-null   int64  
 7   P       7461 non-null   int64  
 8   +/-     7461 non-null   int64  
 9   PIM     7461 non-null   int64  
 10  P/GP    7461 non-null   float64
 11  EVG     7461 non-null   int64  
 12  EVP     7461 non-null   int64  
 13  PPG     7461 non-null   int64  
 14  PPP     7461 non-null   int64  
 15  SHG     7461 non-null   int64  
 16  SHP     7461 non-null   int64  
 17  OTG     7461 non-null   int64  
 18  GWG     7461 non-null   int64  
 19  S       7461 non-null   int64  
 20  S%      7461 non-null   float64
dtypes: float64(2), int64(16), string(3)
memory usage: 1.2 MB
None 
```

The Pandas `.describe()` method now returns a more complete picture of the dataset, showing summary statistics for all
numeric fields.
```
Getting .describe()...
              index           GP            G            A            P          +/-          PIM         P/GP          EVG          EVP          PPG          PPP          SHG          SHP          OTG          GWG            S           S%
count  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000
mean     49.340571   275.735692    48.807935    79.347675   128.155609    -2.009382   226.903096     0.300495    36.007104    94.091677    11.624983    33.245141     1.577134     3.237368     0.593486     6.973596   497.521914     8.098727
std      28.847304   333.120972    90.376002   137.938019   223.013756    50.052797   385.208034     0.240286    61.805525   147.620472    26.892809    74.653007     4.124062     7.390620     1.702940    13.465574   698.925353     6.877763
min       0.000000     1.000000     0.000000     0.000000     0.000000  -257.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000
25%      24.000000    20.000000     1.000000     2.000000     3.000000   -14.000000     8.000000     0.130000     1.000000     3.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000    28.000000     4.400000
50%      49.000000   119.000000    10.000000    18.000000    29.000000    -1.000000    60.000000     0.250000     9.000000    29.000000     1.000000     3.000000     0.000000     0.000000     0.000000     1.000000   256.000000     8.100000
75%      74.000000   453.000000    53.000000    97.000000   156.000000     0.000000   276.000000     0.430000    39.000000   118.000000    11.000000    33.000000     1.000000     3.000000     0.000000     7.000000   554.000000    10.700000
max      99.000000  1779.000000   894.000000  1963.000000  2857.000000   722.000000  3971.000000     1.920000   617.000000  1818.000000   285.000000   890.000000    73.000000   149.000000    24.000000   135.000000  6209.000000   100.000000 ```
```

### Exploratory Data Analysis
#### Dataset Summary Statistics
Specifying the `include` parameter with value `all` for `.describe()` expands analysis to non-numeric fields - adding Player,
S/C, and Pos columns.

```
Getting df_nhl.describe(include='all')...
               index          Player   S/C   Pos           GP            G            A            P          +/-          PIM         P/GP          EVG          EVP          PPG          PPP          SHG          SHP          OTG          GWG            S           S%
count   7461.000000            7461  7461  7461  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000
unique          NaN            7413     2     4          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
top             NaN  Mikko Lehtonen     L     D          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
freq            NaN               3  4746  2434          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
mean      49.340571             NaN   NaN   NaN   275.735692    48.807935    79.347675   128.155609    -2.009382   226.903096     0.300495    36.007104    94.091677    11.624983    33.245141     1.577134     3.237368     0.593486     6.973596   497.521914     8.098727
std       28.847304             NaN   NaN   NaN   333.120972    90.376002   137.938019   223.013756    50.052797   385.208034     0.240286    61.805525   147.620472    26.892809    74.653007     4.124062     7.390620     1.702940    13.465574   698.925353     6.877763
min        0.000000             NaN   NaN   NaN     1.000000     0.000000     0.000000     0.000000  -257.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000
25%       24.000000             NaN   NaN   NaN    20.000000     1.000000     2.000000     3.000000   -14.000000     8.000000     0.130000     1.000000     3.000000     0.000000     0.000000     0.000000     0.000000     0.000000     0.000000    28.000000     4.400000
50%       49.000000             NaN   NaN   NaN   119.000000    10.000000    18.000000    29.000000    -1.000000    60.000000     0.250000     9.000000    29.000000     1.000000     3.000000     0.000000     0.000000     0.000000     1.000000   256.000000     8.100000
75%       74.000000             NaN   NaN   NaN   453.000000    53.000000    97.000000   156.000000     0.000000   276.000000     0.430000    39.000000   118.000000    11.000000    33.000000     1.000000     3.000000     0.000000     7.000000   554.000000    10.700000
max       99.000000             NaN   NaN   NaN  1779.000000   894.000000  1963.000000  2857.000000   722.000000  3971.000000     1.920000   617.000000  1818.000000   285.000000   890.000000    73.000000   149.000000    24.000000   135.000000  6209.000000   100.000000 
```

Some immediate insights can be obtained from this:
* Of 7461 player names, only 7413 are unique - implying that 48 players share a name with another player in the dataset.
* The most frequent name is Mikko Lehtonen, occurring 3 times.
* The majority of players (~63%) shoot left (i.e., carry the stick blade on their left side). This appears to be
counterintuitive to the general prevalence of right-hand dominance (~90%) (Wikipedia 2022). Some initial reading
suggests that the reasoning for the prevalence of left side shooting is that the dominant hand is most-effective at the
butt of the stick (hockeyhow.com 2022). However, if taking L from this dataset to represent right-hand dominance, there
is still a disparity with the general distribution. An analysis of the equivalent Goalie dataset may give insight to
whether there is adaptation in response to coaching, in order to exploit weaknesses in Goalie effectiveness.
* The most frequent player position is defense (D), representing 33% of the dataset. Unlike the forward positions
(centre, left wing, right wing). The defense position is not further sub-divided. A team typically plays with 1
left-side defender and 1 right-side defender on the ice at a given time - 6 per team, and 12 forwards. The ratio of
defenders in the dataset aligns with the standard team composition. Further analysis is to be performed to confirm if
the same is true of other positions.

The Pandas `.loc` function is used to retrieve players responsible for max values of columns in the `.describe()`
table. Max. +/- is excluded here for the purpose of later comparison with min. +/-. S% is also excluded as further
calculation, performed later, is required to arrive at a meaningful value.

```Python
cols_max = ["GP", "G", "A", "P", "PIM", "P/GP", "EVG", "EVP", "PPG", "PPP", "SHG", "SHP", "OTG", "GWG", "S"]
for col in cols_max:
    print(f"Getting player with most {col}...\n", df_nhl.loc[df_nhl[f"{col}"] == max(df_nhl[f"{col}"])], "\n")
```

```
Getting player with most GP...
     index           Player S/C Pos    GP    G    A     P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
49     49  Patrick Marleau   L   C  1779  566  631  1197  -27  527  0.67  377  761  172  415   17   21   11  109  4333  13.1 

Getting player with most G...
    index         Player S/C Pos    GP    G     A     P  +/-  PIM  P/GP  EVG   EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
0      0  Wayne Gretzky   L   C  1487  894  1963  2857  520  577  1.92  617  1818  204  890   73  149    2   91  5088  17.6  
```

The player with the highest shooting percentage is taken as the player with the highest shooting percentage having a
minimum of 100 shots taken, as multiple players have 1 shot and 1 goal in few games played. This is calculated as
follows:

```Python
# Eliminate players with insignificant shot totals from max. S% calculation.
df_significant_shots = df_nhl[df_nhl["S"] >= 100]

# Extract player with max. S% (with minimum of 100 shots taken).
print("Getting player with highest S% (min. 100 shots)...\n",
      df_significant_shots.loc[df_significant_shots["S%"] == max(df_significant_shots["S%"])], "\n")
```

```
Getting player with highest S% (min. 100 shots)...
       index     Player S/C Pos   GP   G   A   P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG    S    S%
3073     73  Mal Davis   L   L  100  31  22  53   -5   34  0.53   20   30   11   23    0    0    0    8  125  24.8 
```

The player with minimum +/- of -257 is also retrieved, as being a notable value, along with the player with maximum +/-
for comparison.

+/- represents a player's presence on the ice at the time of goals for (+1) and goals against (-1). A positive +/- value
indicates a player is present mostly for goals for, whereas a negative score indicates a player is present mostly for
goals against. +/- is cumulative over games played. A negative +/- may infer a player has defensive limitations, while
also not contributing offensively.

```Python
# Extract player with highest +/-.
print("Getting player with highest +/-...\n", df_nhl.loc[df_nhl["+/-"] == max(df_nhl["+/-"])], "\n")

# Extract player with lowest +/-.
print("Getting player with lowest +/-...\n", df_nhl.loc[df_nhl["+/-"] == min(df_nhl["+/-"])], "\n")
```

```
Getting player with highest +/-...
      index          Player S/C Pos    GP    G    A    P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S   S%
104      4  Larry Robinson   L   D  1384  208  750  958  722  793  0.69  139  639   66  309    3   10    0   29  2332  8.9 

Getting player with lowest +/-...
       index       Player S/C Pos   GP   G    A    P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG    S   S%
2089     89  Bob Stewart   L   D  575  27  101  128 -257  809  0.22   23  113    4   10    0    5    0    1  552  4.9 
```

Given that the player with lowest +/- has a moderate career duration of 575 games played, it can be inferred that they
give a valuable contribution outside the standard offense/defense roles. This player's role and playing style may be
geared more towards agitation and disrupting the opponents momentum and rhythm. This is borne out by the
penalties-in-minutes (PIM) accrued, which is relatively high for the number of games played.

The Pandas `loc` function is also used to retrieve a number of otherwise noteworthy players by name, iterated over as a
list of strings, using a for loop.

```Python
# Extract other noteworthy players, by name - using for loop.
notable_players_1 = ["Mario Lemieux", "Mike Bossy", "Gordie Howe",
                     "Sidney Crosby", "Evgeni Malkin",
                     "Nicklas Lidstrom", "Erik Karlsson", "Cale Makar"]
for name in notable_players_1:
    print(f"Getting player {name}...\n", df_nhl.loc[df_nhl["Player"] == name], "\n")
```

```
Getting player Mario Lemieux...
    index         Player S/C Pos   GP    G     A     P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
7      7  Mario Lemieux   R   C  915  690  1033  1723  114  834  1.88  405  951  236  701   49   71   11   74  3633  19.0 

Getting player Mike Bossy...
     index      Player S/C Pos   GP    G    A     P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
60     60  Mike Bossy   R   R  752  573  553  1126  380  210   1.5  385  739  180  378    8    9    4   80  2707  21.2 
```

For comparative purposes, a second list of player names is specified, to be iterated over with iter()/next() syntax.
```Python
# Extract other noteworthy players, by name - using iter()/next().
notable_players_2 = ["Connor McDavid", "Connor McDavid",      # Same value required twice for print statement using
                     "Auston Matthews", "Auston Matthews"]    # iter()/next(). For loop preferred for this use case.
notable_players_2_iter = iter(notable_players_2)
print(f"Getting player {next(notable_players_2_iter)}...\n",
      df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")
print(f"Getting player {next(notable_players_2_iter)}...\n",
      df_nhl.loc[df_nhl["Player"] == next(notable_players_2_iter)], "\n")
```

```
Getting player Connor McDavid...
      index          Player S/C Pos   GP    G    A    P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
253     53  Connor McDavid   L   C  487  239  458  697   92  183  1.43  186  470   50  218    3    9   13   53  1596  15.0 

Getting player Auston Matthews...
      index           Player S/C Pos   GP    G    A    P  +/-  PIM  P/GP  EVG  EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%
599     99  Auston Matthews   L   C  407  259  198  457   78   74  1.12  196  336   63  121    0    0    9   45  1577  16.4 
```

The points (P), goals (G), assists (A), and games played (GP) of select players retrieved above are used to annotate
the EDA scatter plots which follow.

#### Visualising the Dataset
Multiple plots are generated to visualise the dataset. Custom functions as defined to perform the plotting operations:
* get_pga_scatterplot(): Generate seaborn scatter plots of point, goals, and assists vs. games played for all players in
the dataset.
* get_p_pos_boxlot(): Generate seaborn box plots of point, breakdown by position and S/C attributes.
* get_p_histogram(): Generate seaborn histogram plot of the distribution of player counts for all points values.

The seaborn theme is set in `main.py`, and plotting functions called as follows:

```Python
# Plot data for EDA.
# Set seaborn plot theme.
sns.set(rc={'figure.figsize': (16, 9)})

# Run custom plotting functions.
get_pga_scatterplot(df_nhl)
get_p_pos_boxplot(df_nhl)
get_p_histogram(df_nhl)
```

Plotting operations are generalised below - from `get_pga_scatterplot.py`:

```Python
# Generate figure for subplots.
fig, axs = plt.subplots(3, 1)
fig.suptitle('Career Points/Goals/Assists vs. Games Played - Regular Season')

# Plot Points vs. Games Played on subplot 0.
sns.scatterplot(x=df_nhl['GP'], y=df_nhl['P'], color='b', alpha=0.5, label='Points', ax=axs[0])
axs[0].set(xlabel='Games Played')
axs[0].set(ylabel='Count')
axs[0].set_yticks(range(0, 3500, 500))
axs[0].legend(loc='upper left')
axs[0].text(1487, 2857, "Wayne Gretzky")
axs[0].text(1779, 1197, "Patrick Marleau")
```

Resulting plots are show below.

##### Scatter Plot of Points-Goals-Assists vs. Games Played
![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/P-G-A%20vs.%20Games%20Played%20Scatter%20Plot.png)
* The top plot shows points vs. games played.
* The middle plot shows goals vs. games played.
* The bottom plot shows assists vs. games played.
* Plots are annotated with outstanding players in each field.
* The player Wayne Gretzky (retired) can be seen to hold a clear lead in all three categories. With lead in points 
likely to remain unsurpassed by any player in the dataset.
* Patrick Marleau (retired) holds the most games played.
* The lead in goals is within reach by still active player Alex Ovechkin, having a 114 goal deficit to Wayne Gretzky in
213 fewer games played, requiring 186 games (2.26 full seasons) at current goal scoring pace of 0.61 goals per game
played. Wayne Gretzky's career goals per game pace is calculated to be 0.60.

##### Box Plot of Points vs. Player Position
![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/P%20vs.%20Pos%20Box%20Plot.png)
* Left plot shows percentiles for all player positions combined.
* Centre plot shows percentiles for each player position: Centre (C), Right Wing (R), Defense (D), Left Wing (L).
* Right plot shows the same categorisation as the centre plot, further broken down by shooting hand (left (L) or right
* (R)).

From this, it is clear that tha data contains many outliers, with point totals skewing low.

##### Histogram of Points
![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Points%20Histogram.png)
* Left plot shows complete histogram of Points for all players in the dataset.
* Right plot shows the same histogram zoomed in at the high end (P >= 1200).

#### Merging Dataframes for Further Analysis on Top 100
In addition to the Summary report described earlier, a supplemental Bio Info report is available on NHL.com (National
Hockey League 2022). This includes biographical information of players, such as first season, height, weight, and
nationality. This provides opportunities for categorical classification, more so than the mostly numeric data in the
Summary report.

For the purpose of further analysis on highest performing players (as sorted by P, G, A), the first 100 entries of the
Bio Info report is merged with the top 100 entries in df_nhl (representing the same group of players). It is left as an
exercise, beyond the scope of this project, to expand this merge to all 7461 players in the df_nhl dataset. Bio Info
is collected in the same manner as the summary report, from the below URL, with particular attention payed to sorting
method:
https://www.nhl.com/stats/skaters?report=bios&reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100

The Bio Info report (first page, containing top 100 players ranked by P, G, A) is stored in the 'Raw Data Files'
directory as 'Bio Info-01.xlsx'. the dataframe df_bio_top_100 is compiled from this with a call to the
`get_dataset_excel()` function from the `get_dataset.py` module. The first argument, `directory`, is the path name
`"./Raw Data Files/"` as for the first call to generate df_nhl. However, in this case the second argument, 'report', is
set to 'Bio Info' to differentiate between report types. The default value of `report` is defined as 'Summary'.

The new dataframe, `df_bio_top_100` is cleaned as per `df_nhl` earlier, with some notable differences:
* Contains multiple columns with date entries.
* Contains column S/P, representing State/Province, which does not apply to European players.
  * Not logical to impute values for these.
* Height and weight are in imperial units, and height provided only in inches.
  * Metric conversions to be performed.
* Not all players have a draft year. Notably, the data indicates that Wayne Gretzky was not drafted to the NHL.
  * Not logical to impute values for these.
* 1st Season column contains values that are represented as YYYYYYYY (e.g., 19791980).
  * To use regex to insert `-` between years. Replace `(\d\d\d\d)(\d\d\d\d)` with `\1-\2`.
* Some columns duplicate data found in df_nhl. These are dropped, with the exception of the Player column, on which the
merge is performed.

The merge is performed in `main.py`, merging on the shared Player column. The new merged DataFrame
`df_nhl_top_100_extended` is summarised with `.head()` and `.describe()`. Output of `.describe()` is transposed for
readability.

```Python
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
```

```
Compiling dataframe from Bio Info report...
./Raw Data Files/Bio Info-01.xlsx

Files parsed: 1

Getting df_bio_top_100.head()...
           Player S/C Pos         DOB        Birth City S/P Ctry Ntnlty  Ht   Wt Draft Yr Round Overall  1st Season HOF     GP    G      A      P
0  Wayne Gretzky   L   C  1961-01-26         Brantford  ON  CAN    CAN  72  185       --    --      --    19791980   Y  1,487  894  1,963  2,857
1   Jaromir Jagr   L   R  1972-02-15            Kladno  --  CZE    CZE  75  230     1990     1       5    19901991   N  1,733  766  1,155  1,921
2   Mark Messier   L   C  1961-01-18          Edmonton  AB  CAN    CAN  74  211     1979     3      48    19791980   Y  1,756  694  1,193  1,887
3    Gordie Howe   R   R  1928-03-31            Floral  SK  CAN    CAN  72  205       --    --      --    19461947   Y  1,767  801  1,049  1,850
4    Ron Francis   L   C  1963-03-01  Sault Ste. Marie  ON  CAN    CAN  75  200     1981     1       4    19811982   Y  1,731  549  1,249  1,798

Getting df_nhl_top_100_extended.head()...
            key_0  index         Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP  EVG   EVP  PPG  PPP  SHG  SHP  OTG  GWG     S    S%         DOB        Birth City S/P Ctry Ntnlty  Ht   Wt Draft Yr Round Overall  1st Season HOF
0  Wayne Gretzky      0  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617  1818  204  890   73  149    2   91  5088  17.6  1961-01-26         Brantford  ON  CAN    CAN  72  185       --    --      --    19791980   Y
1   Jaromir Jagr      1   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538  1296  217  610   11   15   19  135  5637  13.6  1972-02-15            Kladno  --  CZE    CZE  75  230     1990     1       5    19901991   N
2   Mark Messier      2   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452  1162  179  581   63  144    8   92  4221  16.4  1961-01-18          Edmonton  AB  CAN    CAN  74  211     1979     3      48    19791980   Y
3    Gordie Howe      3    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566  1250  211  564   24   36    0  121  3803   8.1  1928-03-31            Floral  SK  CAN    CAN  72  205       --    --      --    19461947   Y
4    Ron Francis      4    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349  1040  188  727   12   31    4   79  3756  14.6  1963-03-01  Sault Ste. Marie  ON  CAN    CAN  75  200     1981     1       4    19811982   Y

Getting df_nhl_top_100_extended.describe(include='all'').T...
             count unique            top  freq         mean           std         min         25%         50%         75%         max
index       100.0    NaN            NaN   NaN         49.5     29.011492         0.0       24.75        49.5       74.25        99.0
Player        100    100  Wayne Gretzky     1          NaN           NaN         NaN         NaN         NaN         NaN         NaN
S/C           100      2              L    60          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Pos           100      4              C    51          NaN           NaN         NaN         NaN         NaN         NaN         NaN
GP          100.0    NaN            NaN   NaN      1279.81    219.817909       752.0      1111.0      1257.5      1418.0      1779.0
G           100.0    NaN            NaN   NaN       491.97    132.946747       240.0       401.5       482.0      561.75       894.0
A           100.0    NaN            NaN   NaN        764.3    212.514836       491.0       616.5       719.5      855.25      1963.0
P           100.0    NaN            NaN   NaN      1256.27    281.480532       972.0     1044.75      1190.5     1378.25      2857.0
+/-         100.0    NaN            NaN   NaN       124.75    148.589352      -131.0       24.75       100.0      201.25       527.0
PIM         100.0    NaN            NaN   NaN        913.1    556.876235       117.0      530.75       825.0      1126.0      3565.0
P/GP        100.0    NaN            NaN   NaN       0.9919      0.195002        0.67        0.87        0.97        1.07        1.92
EVG         100.0    NaN            NaN   NaN       321.39     90.481528       122.0      267.25       311.5       375.0       617.0
EVP         100.0    NaN            NaN   NaN       786.35    184.790429       464.0      665.75       758.5      877.25      1818.0
PPG         100.0    NaN            NaN   NaN        154.9     48.411848        47.0       122.0       150.0       182.5       285.0
PPP         100.0    NaN            NaN   NaN       441.22     123.79876       162.0       365.5       419.5      510.75       890.0
SHG         100.0    NaN            NaN   NaN        15.68     13.173957         0.0         7.0        12.0        20.5        73.0
SHP         100.0    NaN            NaN   NaN         28.7     25.357046         0.0        10.0        23.0       40.75       149.0
OTG         100.0    NaN            NaN   NaN         5.62      5.096602         0.0         1.0         5.0         9.0        24.0
GWG         100.0    NaN            NaN   NaN        71.09     22.179295        34.0       55.75        70.5        86.0       135.0
S           100.0    NaN            NaN   NaN      3550.64    880.071181      1856.0      2956.5      3457.5     3949.75      6209.0
S%          100.0    NaN            NaN   NaN       13.382      3.330374         6.6       11.65        13.6      15.825        21.2
DOB           100     99     1980-09-26     2          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Birth City    100     82       Montréal     7          NaN           NaN         NaN         NaN         NaN         NaN         NaN
S/P           100     14             ON    31          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Ctry          100      8            CAN    72          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Ntnlty        100      8            CAN    71          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Ht          100.0    NaN            NaN   NaN        72.18      2.133807        66.0        71.0        72.0        73.0        77.0
Wt          100.0    NaN            NaN   NaN       197.84     16.140619       160.0       185.0       195.0       207.5       238.0
Draft Yr      100     35             --    20          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Round       100.0   11.0            1.0  56.0          NaN           NaN         NaN         NaN         NaN         NaN         NaN
Overall       100     41             --    20          NaN           NaN         NaN         NaN         NaN         NaN         NaN
1st Season  100.0    NaN            NaN   NaN  19826383.44  144399.72556  19461947.0  19771978.0  19821983.0  19911992.0  20082009.0
HOF           100      2              Y    63          NaN           NaN         NaN         NaN         NaN         NaN         NaN
```

### Machine Learning
As the data in the dataset is mostly numeric, it was decided to treat further analysis as a regression problem, using
supervised learning techniques. The algortithm chosen for initial analysis is the DecisionTreeRegressor provided in
`sklearn.tree`.

#### DecisionTreeRegressor
In `main.py` the variable `target` is used to define the target column of the dataset which is to be predicted by the
machine learning model. For the purpose of this analysis the column representing goals (G) is used, as this is a direct
measure of a player's performance. The `target` variable is used to build the target 1d array `y`, and the feature
matrix `X`.

```Python
# Define feature matrix X, and target (labels) y.
target = "G"

# Drop target from X.
X_all_features = df_nhl.drop(target, axis=1)

# Drop non-numeric features from X.
df_X_all_features = X_all_features.drop(["Player", "S/C", "Pos"], axis=1)

# Convert DataFrame X, and Series y to numpy arrays.
X_all_features = df_X_all_features.values
y = df_nhl[target].values

# Create single-feature array for preliminary use.
X_single_feature = X_all_features[:, 4]

print("Getting type(X_single_feature)...\n", type(X_single_feature), "\n")
print("Getting type(X_all_features)...\n", type(X_all_features), "\n")
print("Getting type(y)...\n", type(y), "\n")

# Reshape numpy arrays to unknown number of rows, 1 column.
y = y.reshape(-1, 1)
X_single_feature = X_single_feature.reshape(-1, 1)
```

```
Getting type(X_single_feature)...
 <class 'numpy.ndarray'>

Getting type(X_all_features)...
 <class 'numpy.ndarray'>

Getting type(y)...
 <class 'numpy.ndarray'>
```

The function `implement_decision_tree()` defined in `implement_decision_tree.py` is used to train a decision tree model
and predict a target in the test set. This function is first called with feature matrix containing only one feature.

```Python
implement_decision_tree(X_single_feature, y, SEED)
```

```
CV MSE: 6590.631737662596
Train MSE: 6541.544892502052
Test MSE: 5053.990206303157
RMSE_CV: 81.18270590256644
RMSE_train: 80.87981758450034
RMSE_test: 71.09142146773517
```

The function is then run again with the full feature in the feature matrix.

```Python
implement_decision_tree(X_all_features, y, SEED)
```

```
CV MSE: 2465.5218260945253
Train MSE: 2446.7869807578286
Test MSE: 1687.7888702068253
RMSE_CV: 49.654021247976736
RMSE_train: 49.46500763931841
RMSE_test: 41.08270767861857
```

#### Ensembling with RandomForestRegressor
The RandomForestRegressor is used in attempt to improve the prediction score of Decision Tree model, as measured with
root-mean-squared-error RMSE. The RandomForestRegressor model is trained in with the `implement_random_forest()`
function in `implement_random_forest.py`, called from `main.py` as follows. Two additional arguments are supplied for
the purpose of plotting feature importance: a DataFrame version of the feature matrix, and the target column name as
string.

```Python
rf = implement_random_forest(X_all_features, y, SEED, df_X_all_features, target)
```

```
RMSE_test_rf: 46.084444631038274
```

A bar plot of the feature importances is saved to file and displayed on screen.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Feature%20Importance%20in%20Prediction%20of%20G%20-%20Untuned%20Random%20Forest.png)

#### Hyperparamater Tuning on RandomForestRegressor
The RandomForestRegressor with default parameters does not offer an improvement over DecisionTreeRegressor.
Hyperparameter tuning is performed on the RandomForestRegressor model, using `GridSearchCV`, to determine the best
parameters for use with the model. This is done with the `tune_random_froest()` function defined in
`tune_random_forest.py`. The best model, with optimal parameters obtained from GridSearchCV, are used to fit and predict
on the test set.

```Python
rf_tuned = tune_random_forest(rf, X_all_features, y, SEED, df_X_all_features, target)
```

```
Getting RandomForestRegressor hyperparamters...
 {'bootstrap': True, 'ccp_alpha': 0.0, 'criterion': 'squared_error', 'max_depth': None, 'max_features': 1.0, 'max_leaf_nodes': None, 'max_samples': None, 'min_impurity_decrease': 0.0, 'min_samples_leaf': 0.12, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'n_estimators': 400, 'n_jobs': None, 'oob_score': False, 'random_state': 1, 'verbose': 0, 'warm_start': False}

Tuning hyperparameters with GridSearchCV...

Fitting 3 folds for each of 36 candidates, totalling 108 fits
Getting best hyperparameters...
 {'max_depth': 4, 'max_features': 'log2', 'min_samples_leaf': 0.1, 'n_estimators': 500}

Getting best model...
 RandomForestRegressor(max_depth=4, max_features='log2', min_samples_leaf=0.1,
                      n_estimators=500, random_state=1)

Predicting test set labels with best model...

RMSE_test_rf_tuned: 38.69701056342926
```

A bar plot of the feature importances is saved to file and displayed on screen.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Feature%20Importance%20in%20Prediction%20of%20G%20-%20Tuned%20Random%20Forest.png)

## Results
The plots provided above are included in the project directory, along with `terminal_log.txt` - a log of terminal output
for a successful execution of `main.py`.

The three plots generated during exploratory data analysis, reproduced below, give an understanding of how the player
data is distributed.

As shown by the scatter plot, there is a general trend toward higher points totals with career longevity. However, some
outliers show high points totals for relatively few games played - see Mario Lemieux, Mike Bossy annotations.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/P-G-A%20vs.%20Games%20Played%20Scatter%20Plot.png)

The box plot of points for all positions shows maximum points (100th percentile) lower than 500, and with outliers
representing a large group of elite players far exceeding the rest of the dataset. This distribution of outstanding
players is observed across all four outfield positions.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/P%20vs.%20Pos%20Box%20Plot.png)

From the histogram, it can be seen that there is an exponential distribution in points, with points totals over 500
sparsely represented. This give some context to the career of Wayne Gretzky, holding the lead in points at 2857.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Points%20Histogram.png)

The plots generated to compare operation of a non-tuned and tuned Random Forest Regression algorithm are provided
below. It can be seen that the tuned model takes into account more features in its prediction than the non-tuned model.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Feature%20Importance%20in%20Prediction%20of%20G%20-%20Untuned%20Random%20Forest.png)


![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Feature%20Importance%20in%20Prediction%20of%20G%20-%20Tuned%20Random%20Forest.png)

## Insights
* The record in points, held by Wayne Gretzky (retired) far exceeds the nearest value, and is likely to stand 
unchallenged by currently active players. Points per games played (P/GP) for Wayne Gretzky is 1.92. Mario Lemieux (1.88)
and Mike Bossy (1.50) may have come closest if career durations had been equivalent. Of active players, Connor McDavid
(1.43) has the highest point scoring pace.
* The record in goals, also held by Wayne Gretzky, is less secure, with active player Alex Ovechkin on pace to surpass
within three seasons.
* As determined by earlier analysis of +/- for Bob Stewart, the obvious metrics of points/goals/assists are not the only
determining factors of a player's success in the NHL. This is confirmed by 75th percentiles in games played (453) and
points (156).
* The presence of extreme outliers - though occurring naturally and not warranting removal - in the dataset leads to 
high variance which impacts the supervised learning model's ability to fit all data points. This can be seen in the RMSE
values of the DecisionTreeRegressor with the prediction error on test set being lower than prediction error on train
set. Methods for normalising the dataset are to be explored further, to improve the fit of the model to such a dataset.
* Hyperparmateer tuning improves performance of Random Forest regression, in this case lowering the RMSE of the
prediction on the test set, and using more features in prediction, than non-tuned Random Forest regression.

## References
National Hockey League. (2022). *Stats* [online]. 
Available from: https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100 
[accessed 15 August 2022].  

Wikipedia. (2022). *Handedness* [online].
Available from: https://en.wikipedia.org/wiki/Handedness
[accessed 15 August 2022].  

hockeyhow.com. (2022). *Why are Most Hockey Players Left-Handed?* [online].
Available from: https://hockeyhow.com/why-most-hockey-players-left-handed/
[accessed 15 August 2022].  

National Hockey League. (2022). *Stats* [online]. 
Available from: https://www.nhl.com/stats/skaters?report=bios&reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100
[accessed 15 August 2022].  

