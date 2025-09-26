import pandas as pd
import matplotlib
from main import max_num_players

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df_specials_high = pd.read_csv("results_with_specials_high.csv")
df_no_specials_high = pd.read_csv("results_no_specials_high.csv")

df_specials_medium = pd.read_csv("results_with_specials_medium.csv")
df_no_specials_medium = pd.read_csv("results_no_specials_medium.csv")

df_specials_low = pd.read_csv("results_with_specials_low.csv")
# df_no_specials_low = pd.read_csv("results_no_specials_low.csv")

num_plots = max_num_players
num_cols = 2
num_rows = 4

fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 6, num_rows * 4),
                         sharex=True, sharey=True)
axes = axes.flatten()

for i, num_players in enumerate(range(2, max_num_players + 1)):
    ax = axes[i]

    data_specials_high = df_specials_high[df_specials_high["num_players"] == num_players]["turns"]
#     data_no_specials_high = df_no_specials_high[df_no_specials_high["num_players"] == num_players]["turns"]
    data_specials_high.hist(bins=50, alpha=0.5, label="Specials high", ax=ax)
#     data_no_specials_high.hist(bins=50, alpha=0.5, label="No Specials high", ax=ax)

    data_specials_medium = df_specials_medium[df_specials_medium["num_players"] == num_players]["turns"]
#     data_no_specials_medium = df_no_specials_medium[df_no_specials_medium["num_players"] == num_players]["turns"]
    data_specials_medium.hist(bins=50, alpha=0.5, label="Specials medium", ax=ax)
#     data_no_specials_medium.hist(bins=50, alpha=0.5, label="No Specials medium", ax=ax)

    data_specials_low = df_specials_low[df_specials_low["num_players"] == num_players]["turns"]
#     data_no_specials_low = df_no_specials_low[df_no_specials_low["num_players"] == num_players]["turns"]
    data_specials_low.hist(bins=50, alpha=0.5, label="Specials low", ax=ax)
#     data_no_specials_low.hist(bins=50, alpha=0.5, label="No Specials low", ax=ax)

    ax.set_title(f'Players: {num_players}')
    ax.set_xlabel('Number of Turns')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(axis='y', alpha=0.75)

for j in range(num_plots, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

print("\nMean turns with specials:")
print(df_specials_high.groupby("num_players")["turns"].mean())
print("\nMean turns without specials:")
# print(df_no_specials_high.groupby("num_players")["turns"].mean())
