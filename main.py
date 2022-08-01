# Main file for implementation of data analytics on NHL player dataset - 0001-7461.csv.

import pandas as pd
import matplotlib.pyplot as plt


# Don't suppress columns in terminal output.
pd.options.display.width = 0

if __name__ == '__main__':
    df_nhl = pd.read_csv("0001-7461_corrected.csv")

    # Sort dataframe by Points ('P') and Games Played ('GP') columns.
    df_nhl = df_nhl.sort_values(by=['P', 'GP'], ascending=False)

    # Summarise dataset.
    print(df_nhl.head())
    print(df_nhl.tail())
    print(df_nhl.describe())
    print(df_nhl.info())

    # Define features of interest.
    games_played = df_nhl['GP']
    points = df_nhl['P']

    # Explore dataset with scatter plots of points/goals/assists vs. games played.
    fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
    fig.suptitle('Career Points/Goals/Assists vs. Games Played - Regular Season')

    ax0.plot(games_played, points, 'o', color='b', alpha=0.5, label='Points')
    ax0.set_xlabel('Games Played')
    ax0.set_ylabel('Count')
    ax0.set_yticks(range(0, 3500, 500))
    ax0.legend(loc='upper left')

    ax1.plot(games_played, df_nhl['G'], 'o', color='r', alpha=0.5, label='Goals')
    ax1.set_xlabel('Games Played')
    ax1.set_ylabel('Count')
    ax1.set_yticks(range(0, 3500, 500))
    ax1.legend(loc='upper left')

    ax2.plot(games_played, df_nhl['A'], 'o', color='g', alpha=0.5, label='Assists')
    ax2.set_xlabel('Games Played')
    ax2.set_ylabel('Count')
    ax2.set_yticks(range(0, 3500, 500))
    ax2.legend(loc='upper left')

    plt.show()
