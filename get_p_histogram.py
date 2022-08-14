import matplotlib.pyplot as plt
import seaborn as sns


def get_p_histogram(df_nhl):
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

    plt.savefig("Points Histogram.png")
    plt.show()