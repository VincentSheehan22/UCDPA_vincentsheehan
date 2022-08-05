# UCDPA Project Assignment - Analysing NHL Regular Season Career Statistics

## Data Source
The National Hockey League, a North American ice-hockey league, operating since 1917 maintains on its website - 
https://www.nhl.com - a record of player statistics dating back to the inaugural 1917-18 season. This dataset includes
entries for over 7000 players to have played a regular season game in the NHL, and offers player-by-player comparison
in areas such as Games Played, Goals, Assists (primary and secondary passes leading to goals), and Points (goals +
assists).

The website provides filtering of stats by season, team, player position and game type, among others. Data is available
in several reports, with different statistics tracked in each. For the scope of this project, analysis will be performed
on the Skaters/All-Time/Regular Season/Summary report, the first page of which is available at the link below. 

NHL all-time player statistics for regular season games - summary report:  
https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100

Analysis of other available reports in combination with the summary report is left as an exercise, beyond the scope of
this project.

## Implementation
### Data Import
Multiple methods of data import were explored.

#### NHL Stats API
Dataset collection via API was explored. An API was found to be available, but not well documented.

Team and season data can be found at below links, but a useful API for the player career stats dataset was not found. 
* https://statsapi.web.nhl.com/api/v1/teams
* https://statsapi.web.nhl.com/api/v1/seasons

#### Web Scraping
Dataset collection via web scraping was explored, but the tabular data on NHL.com was found to be implemented as
ReactTable objects, and not parsable with the BeautifulSoup library.

#### Pandas File Reading
NHL.com provides the stats data for download in Excel format. This was found to be the most direct approach to acquiring
the dataset. However, the table view, and thus export, is limited to 100 rows per page.

A script - `get_data_urls.py` - was created for pagination of the tabular data by incrementing the page number within
the URL, writing all page URLs to file for future reference. It is left as an exercise, beyond the scope of this
project, to utilise page URLs for browser automation of the Excel file export.

The dataset was manually downloaded as a set of 75 Excel files (~100 entries apiece), containing 7461 records - player
career statistics from 1917-18 to 2021-2022 seasons.

With the data collected and stored in the `Raw Data Files` directory, the `pandas.read_excel()` method was used to
compile the Excel file into a DataFrame, within the `get_dataset_excel()` function defined in `get_dataset.py`.

### Data Cleaning
#### Regex Replacement
The dataset contains text and numeric data. Numeric values greater than 3 digits are represented as `"1,234"`. Regex
used to convert to `1234` format:  
* Find: `(\d),(\d)(\d)(\d)`  
* Replace: `\1\2\3\4`

The above regex strings were provided as parameters to the `find_and replace()` function defined in
`find_and_replace.py`, along with the dataframe `df_nhl`. The regex strings use capture groups (parenthesis) to capture
and return the 1st, 2nd, 3rd and 4th digit characters, eliminating the ',' characters.

```
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
Dataframe sorted by 'P' (points), 'G' (goals), and 'A' (assists) columns, with index reset.
```
df_nhl = df_nhl.sort_values(by=['P', 'G', 'A'], ascending=False).reset_index()
```

`df.head()`:
```
   index         Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP  EVG   EVP  PPG  PPP SHG  SHP  OTG  GWG     S    S% TOI/GP  FOW%
0      0  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617  1818  204  890  73  149    2   91  5088  17.6     --    49
1      1   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538  1296  217  610  11   15   19  135  5637  13.6     --  24.5
2      2   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452  1162  179  581  63  144    8   92  4221  16.4     --  54.7
3      3    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566  1250  211  564  24   36    0  121  3803    --     --    --
4      4    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349  1040  188  727  12   31    4   79  3756  14.6     --  54.8 
```

#### Type Conversion
The dataframe contains numeric columns stored as object type, as shown by `df.info()`. As such, these columns are not
represented with `df.describe()` Conversion to int and float types is required.

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7461 entries, 0 to 7460
Data columns (total 23 columns):
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
 11  EVG     7461 non-null   object 
 12  EVP     7461 non-null   object 
 13  PPG     7461 non-null   object 
 14  PPP     7461 non-null   object 
 15  SHG     7461 non-null   object 
 16  SHP     7461 non-null   object 
 17  OTG     7461 non-null   int64  
 18  GWG     7461 non-null   int64  
 19  S       7461 non-null   object 
 20  S%      7461 non-null   object 
 21  TOI/GP  7461 non-null   object 
 22  FOW%    7461 non-null   object 
dtypes: float64(1), int64(5), object(17)
memory usage: 1.3+ MB
None 
```

```
             index            G          +/-         P/GP          OTG          GWG
count  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000  7461.000000
mean     49.340571    48.807935    -2.009382     0.300495     0.593486     6.973596
std      28.847304    90.376002    50.052797     0.240286     1.702940    13.465574
min       0.000000     0.000000  -257.000000     0.000000     0.000000     0.000000
25%      24.000000     1.000000   -14.000000     0.130000     0.000000     0.000000
50%      49.000000    10.000000    -1.000000     0.250000     0.000000     1.000000
75%      74.000000    53.000000     0.000000     0.430000     0.000000     7.000000
max      99.000000   894.000000   722.000000     1.920000    24.000000   135.000000 
```

Columns requiring type conversion:
* GP: int64
* A: int64
* P: int64
* PIM: int64
* EVG: int64  
* EVP: int64  
* PPG: int64  
* PPP: int64  
* SHG: int64
* SHP: int64
* S: int64
* S%: float64
* TOI/GP: time (mm:ss)
* FOW%: float64

Type conversion:
```
df_nhl['GP'] = df_nhl['GP'].astype('int64')
```

#### Missing Data
The dataset contains entries for players who played prior to modern record keeping. Some columns such as 'EVG' contain
missing data, represented as '--'. These require replacement in order to complete type conversion.

Replacement options:
1. Replace '--' with `NaN`, and use `.dropna()`.
    * Excludes notable players from analysis.
2. Replace '--' with 0.
    * May under-represent actual value.
    * Lowers mean of the series.
3. Replace '--' with league mean.
   * May over- or under-represent actual value.
   * Preserves mean of the series.
4. Remove columns containing '--'.
   * Excludes features from further analysis.

Missing data was explored to determine how best to handle. A function `handle_missing_data.py` was created to take
dataframe as input, convert entries with value "--" - representing missing in the NHL dataset - to `NaN`. With NaNs
populated in the dataframe, the function then obtains a count of missing data per column. The modified data frame and
missing data counts are then returned.

``` Python
# Explore missing data to determine how best to handle.
df_nhl, missing_count = handle_missing_data.handle_missing_data(df_nhl)
print(df_nhl.head(), "\n")
print(missing_count, "\n")
```

Passing `df_nhl` to `handle_missing_data()`, conversion of missing data to `NaN` was successful, as shown with
`df_nhl.head()`:
```
   index         Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP    EVG   EVP    PPG    PPP   SHG    SHP  OTG  GWG     S    S% TOI/GP  FOW%
0      0  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617.0  1818  204.0  890.0  73.0  149.0    2   91  5088  17.6    NaN  49.0
1      1   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538.0  1296  217.0  610.0  11.0   15.0   19  135  5637  13.6    NaN  24.5
2      2   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452.0  1162  179.0  581.0  63.0  144.0    8   92  4221  16.4    NaN  54.7
3      3    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566.0  1250  211.0  564.0  24.0   36.0    0  121  3803   NaN    NaN   NaN
4      4    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349.0  1040  188.0  727.0  12.0   31.0    4   79  3756  14.6    NaN  54.8 
```

The missing data counts provide some insight on how to handle missing values for each column.
```
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
* **FOW%**: Face-off win percentage. Game scenario in which two players contest possession of the puck. Typically taken
by players in the centre position.
  * As data is not available for over 50% of players in the dataset, this column will be dropped.

#### Duplicate Data
Checked dataframe for duplicate entries with `df_nhl.duplicated()`. No duplicate entries found.


### Exploratory Data Analysis
* Scatter plot of points vs. games played.
    * Show retired vs. active.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Career%20Points%20vs%20Games%20Played_Regular%20Season.png)
![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Career%20Points-Goals-Assists%20vs%20Games%20Played_Regular%20Season.png)

## Ideas For Analysis
* Define gap to Wayne Gretzky - P/G/A.
* Players capable of matching/surpassing - P/G/A.
* Exponential distribution on Gretzky's points total being matched/beaten - P/G/A. 
