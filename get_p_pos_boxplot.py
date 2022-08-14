import  matplotlib.pyplot as plt
import seaborn as sns


def get_p_pos_boxplot(df_nhl):
    """Generate a 1 x 3 figure of box plots for Points by Position.

    Takes DataFrame object as argument, and plots for all rows. Output is saved to file and displayed on screen.
    """
    # Set up figure for multiple plots.
    fig, axs = plt.subplots(1, 3)
    fig.suptitle('Points per Position')

    # Box plot of P vs. Pos, using sns.
    sns.boxplot(data=df_nhl["P"], ax=axs[0])
    axs[0].grid(True, axis='both')
    axs[0].set(xlabel="Position")
    axs[0].set_xticklabels(["All"])
    axs[0].set(ylabel="Points")

    # Box plot of P vs. Pos, with further categorisation on S/C.
    sns.boxplot(x="Pos", y="P", data=df_nhl, ax=axs[1])
    axs[1].grid(True, axis='both')
    axs[1].set(xlabel="Position")
    axs[1].set(ylabel="Points")

    # Box plot of P vs. Pos, with further categorisation on S/C.
    sns.boxplot(x="Pos", y="P", hue="S/C", data=df_nhl, ax=axs[2])
    axs[2].grid(True, axis='both')
    axs[2].set(xlabel="Position")
    axs[2].set(ylabel="Points")

    plt.savefig("P vs. Pos Box Plot.png")
    plt.show()
