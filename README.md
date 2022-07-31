## Data Source
NHL all-time player statistics for regular season games - summary report.

https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100

Data downloaded as set of 75 Excel files (~100 entries apiece), containing 7461 records - player career statistics from
1917-18 to 2021-2022 seasons.

Excel files saved as CSV, and then CSV files combined using `combine-csv-files.py`. Full dataset saved as `0001-7461.csv`. 

Dataset contains text and numeric data. Numeric values greater than 3 digits are represented as "1,234". Regex used to
convert to 1234 format:  
* Find: `\"(\d),(\d)(\d)(\d)"`  
* Replace: `$1$2$3$4`

```
# Dataset includes 4-digit numbers represented as strings with ','. Use regex to replace string with 4-digit integer
# equivalent without ',', using capture groups:
#     Find: \"(\d),(\d)(\d)(\d)\"
#     Replace: $1$2$3$4
# df_nhl = df_nhl.replace(r'\"(\d),(\d)(\d)(\d)\"', r'$1$2$3$4', regex=True)
#   CSV corrected manually with IDE find/replace tool for brevity.
```

`df.head()`:
```
             Player S/C Pos    GP    G     A     P  +/-   PIM  P/GP  EVG   EVP  PPG  PPP SHG  SHP  OTG  GWG     S    S% TOI/GP  FOW%
5861  Wayne Gretzky   L   C  1487  894  1963  2857  520   577  1.92  617  1818  204  890  73  149    2   91  5088  17.6     --    49
5862   Jaromir Jagr   L   R  1733  766  1155  1921  322  1167  1.11  538  1296  217  610  11   15   19  135  5637  13.6     --  24.5
5863   Mark Messier   L   C  1756  694  1193  1887  211  1912  1.07  452  1162  179  581  63  144    8   92  4221  16.4     --  54.7
5864    Gordie Howe   R   R  1767  801  1049  1850  160  1685  1.05  566  1250  211  564  24   36    0  121  3803    --     --    --
5865    Ron Francis   L   C  1731  549  1249  1798  -18   977  1.04  349  1040  188  727  12   31    4   79  3756  14.6     --  54.8
```

## NHL Stats API
Dataset collection via API was explored. An API was found to be available, but not well documented.

* https://statsapi.web.nhl.com/api/v1/
* https://statsapi.web.nhl.com/api/v1/teams
* https://statsapi.web.nhl.com/api/v1/seasons

## Web Scraping
Dataset collection via web scraping was explored, but the tabular data on NHL.com was found to be implemented as ReactTable, not supported by BeautifulSoup library.

## Pandas
* pd.readcsv()

## NHL Player Stats EDA
* Scatter plot of points vs. games played.
    * Show retired vs. active.

![](https://github.com/VincentSheehan22/UCDPA_vincentsheehan/blob/main/Career%20Points%20vs%20Games%20Played_Regular%20Season.png)

## Ideas For Analysis
* Define gap to Wayne Gretzky - P/G/A.
* Players capable of matching/surpassing - P/G/A.
* Exponential distribution on Gretzky's points total being matched/beaten - P/G/A. 
