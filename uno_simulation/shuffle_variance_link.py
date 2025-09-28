import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df_specials_low = pd.read_csv("results_with_specials_low_16n6c.csv")
df_specials_medium = pd.read_csv("results_with_specials_medium_16n6c.csv")
df_specials_high = pd.read_csv("results_with_specials_high_16n6c.csv")

df_no_specials_low = pd.read_csv("results_no_specials_low_16n6c.csv")
df_no_specials_medium = pd.read_csv("results_no_specials_medium_16n6c.csv")
df_no_specials_high = pd.read_csv("results_no_specials_high_16n6c.csv")

for df, specials, shuffle in [
    (df_specials_low, True, "low"),
    (df_specials_medium, True, "medium"),
    (df_specials_high, True, "high"),
    (df_no_specials_low, False, "low"),
    (df_no_specials_medium, False, "medium"),
    (df_no_specials_high, False, "high"),
]:
    df["specials"] = specials
    df["shuffle_level"] = shuffle

df_all = pd.concat([
    df_specials_low, df_specials_medium, df_specials_high,
    df_no_specials_low, df_no_specials_medium, df_no_specials_high
])

summary = (
    df_all
    .groupby(["specials", "shuffle_level", "num_players"])["turns"]
    .agg(["mean", "std"])
    .reset_index()
)

print(summary.head())

plt.figure(figsize=(8, 6))

for (specials_flag, shuffle_level), subset in summary.groupby(["specials", "shuffle_level"]):
    label = f"{'Specials' if specials_flag else 'No Specials'}, shuffle={shuffle_level}"
    plt.plot(
        subset["num_players"],
        subset["std"],
        marker="o",
        label=label
    )

plt.title("Std Dev of Turns vs Players")
plt.xlabel("Number of Players")
plt.ylabel("Standard Deviation of Turns")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
