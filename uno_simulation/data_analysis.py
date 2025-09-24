import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df_specials = pd.read_csv("results_with_specials.csv")
df_no_specials = pd.read_csv("results_no_specials.csv")

for num_players in range(1, 9):
    plt.figure(figsize=(10, 6))
    data_specials = df_specials[df_specials["num_players"] == num_players]["turns"]
    data_no_specials = df_no_specials[df_no_specials["num_players"] == num_players]["turns"]

    data_specials.hist(bins=100, alpha=0.5, label="With special cards")
    data_no_specials.hist(bins=100, alpha=0.5, label="Without special cards")

    plt.title(f'Distribution of Turns for {num_players} Players')
    plt.xlabel('Number of Turns')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.show()

# df_specials.groupby("num_players")["turns"].describe()
print(df_specials.groupby("num_players")["turns"].mean())
print(df_no_specials.groupby("num_players")["turns"].mean())
print("no specials:", max(df_no_specials.groupby("num_players")["turns"]), "with specials:",
      max(df_specials.groupby("num_players")["turns"]))
