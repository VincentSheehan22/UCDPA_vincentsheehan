# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
import matplotlib.pyplot as plt


# Don't suppress columns in terminal output.
pd.options.display.width = 0

if __name__ == '__main__':
    df_nhl = pd.read_csv("0001-7461_corrected.csv")

    df_nhl = df_nhl.sort_values(by=['P', 'GP'], ascending=False)

    print(df_nhl.head())
    print(df_nhl.tail())
    print(df_nhl.describe())
    print(df_nhl.info())

    games_played = df_nhl['GP']
    print(games_played)
    points = df_nhl['P']
    print(points)

    plt.plot(games_played, points, 'o', alpha=0.5)
    plt.title('Career Points vs. Games Played - Regular Season')
    plt.xlabel('Games Played')
    plt.ylabel('Points')
    plt.xticks(rotation=90)

    plt.show()
