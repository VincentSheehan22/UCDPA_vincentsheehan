import matplotlib.pyplot as plt
import seaborn as sns


def get_pga_scatterplot(df_nhl):
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
    axs[0].text(915, 1723, "Mario Lemieux")
    axs[0].text(752, 1126, "Mike Bossy")
    axs[0].text(1274, 1410, "Alex Ovechkin")
    axs[0].text(1108, 1409, "Sidney Crosby")

    # Plot Goals vs. Games Played on subplot 1.
    sns.scatterplot(x=df_nhl['GP'], y=df_nhl['G'], color='r', alpha=0.5, label='Goals', ax=axs[1])
    axs[1].set(xlabel='Games Played')
    axs[1].set(ylabel='Count')
    axs[1].set_yticks(range(0, 3500, 500))
    axs[1].legend(loc='upper left')
    axs[1].text(1487, 894, "Wayne Gretzky")
    axs[1].text(1767, 801, "Gordie Howe")
    axs[1].text(1274, 780, "Alex Ovechkin")

    # Plot Assists vs. Games Played on subplot 2.
    sns.scatterplot(x=df_nhl['GP'], y=df_nhl['A'], color='g', alpha=0.5, label='Assists', ax=axs[2])
    axs[2].set(xlabel='Games Played')
    axs[2].set(ylabel='Count')
    axs[2].set_yticks(range(0, 3500, 500))
    axs[2].legend(loc='upper left')
    axs[2].text(1487, 1963, "Wayne Gretzky")
    axs[2].text(1731, 1249, "Ron Francis")
    axs[2].text(1756, 1193, "Mark Messier")

    plt.show()
