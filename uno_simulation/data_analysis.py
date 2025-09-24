import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df_specials = pd.read_csv("results_with_specials.csv")
df_no_specials = pd.read_csv("results_no_specials.csv")

print(df_specials.head())
print(df_specials.columns)

# df_specials.groupby("num_players")["turns"].describe()
print(df_specials.groupby("num_players")["turns"].mean())
print(df_no_specials.groupby("num_players")["turns"].mean())

df_specials[df_specials["num_players"] == 4]["turns"].hist(bins=100, alpha=0.5, label="with specials")
df_no_specials[df_no_specials["num_players"] == 4]["turns"].hist(bins=100, alpha=0.5, label="no specials")
plt.legend()
plt.show()
print("no specials:", max(df_no_specials.groupby("num_players")["turns"]), "with specials:",
      max(df_specials.groupby("num_players")["turns"]))

