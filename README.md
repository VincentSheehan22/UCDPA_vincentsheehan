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

Dataframe contains numeric columns stored as object type, as shown by `df.info()`. As such, these columns are not
represented with `df.describe()` Conversion to int and float types required.

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



## NHL Player Stats EDA
* Scatter plot of points vs. games played.
    * Show retired vs. active.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Career%20Points%20vs%20Games%20Played_Regular%20Season.png)
![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Career%20Points-Goals-Assists%20vs%20Games%20Played_Regular%20Season.png)

## Ideas For Analysis
* Define gap to Wayne Gretzky - P/G/A.
* Players capable of matching/surpassing - P/G/A.
* Exponential distribution on Gretzky's points total being matched/beaten - P/G/A. 
