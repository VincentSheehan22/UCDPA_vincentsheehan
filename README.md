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

## Ideas For Analysis
* Define gap to Wayne Gretzky - P/G/A.
* Players capable of matching/surpassing - P/G/A.
* Exponential distribution on Gretzky's points total being matched/beaten - P/G/A. 