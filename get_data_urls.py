def get_data_urls(input_file):
    """Increment page of data source an write URL to file."""
    with open(input_file, "w") as in_file:
        i = 0
        while i < 75:
            page = f'https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page={i}&pageSize=100\n'

            in_file.write(page)
            print(page)

            i += 1

if __name__ == '__main__':
    get_data_urls("Data URLs.md")