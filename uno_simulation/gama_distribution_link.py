import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats import gamma

df_specials = pd.read_csv("results_with_specials_high.csv")
df_no_specials = pd.read_csv("results_no_specials_high.csv")

fitted_params = []
for n in range(2, 8):
    data = df_specials[df_specials["num_players"] == n]["turns"]
    shape, loc, scale = gamma.fit(data, floc=0)
    fitted_params.append({"num_players": n, "shape": shape, "scale": scale})

print(fitted_params)
df_params = pd.DataFrame(fitted_params)

coeff_shape = np.polyfit(df_params["num_players"], df_params["shape"], 1)
coeff_scale = np.polyfit(df_params["num_players"], df_params["scale"], 1)

predicted_params = {}
# ---------- Subplots for 2–7 ----------
fig, axes = plt.subplots(2, 3, figsize=(15, 8))  # 6 subplots (2 rows × 3 cols)
axes = axes.flatten()

for i, n in enumerate(range(2, 8)):
    ax = axes[i]
    data = df_specials[df_specials["num_players"] == n]["turns"]

    # Histogram of observed data
    ax.hist(data, bins=50, density=True, alpha=0.3, label=f"Observed (n={n})")

    # Fitted gamma
    shape = df_params[df_params["num_players"] == n]["shape"].values[0]
    scale = df_params[df_params["num_players"] == n]["scale"].values[0]
    x = np.linspace(0, data.max(), 500)
    y = gamma.pdf(x, a=shape, scale=scale)
    ax.plot(x, y, lw=2, label=f"Fitted Gamma (n={n})")

    ax.set_title(f"Players={n}")
    ax.set_xlabel("Turns")
    ax.set_ylabel("Density")
    ax.legend()

plt.suptitle("Observed vs Fitted Gamma (Players 2–7)", fontsize=14)
plt.tight_layout()
plt.show()

for n in [8, 9]:
    shape_pred = np.polyval(coeff_shape, n)
    scale_pred = np.polyval(coeff_scale, n)
    predicted_params[n] = {"shape": shape_pred, "scale": scale_pred}
    print(f"Predicted gamma params for {n} players: shape={shape_pred}, scale={scale_pred}")

fig, axes = plt.subplots(1, 2, figsize=(15, 8))  # 6 subplots (2 rows × 3 cols)
axes = axes.flatten()

for i, n in enumerate(range(8, 10)):
    ax = axes[i]
    data = df_specials[df_specials["num_players"] == n]["turns"]

    # Histogram of observed data
    ax.hist(data, bins=50, density=True, alpha=0.3, label=f"Observed (n={n})")

    # Fitted gamma
    shape = predicted_params[n]["shape"]
    scale = predicted_params[n]["scale"]

    x = np.linspace(0, data.max(), 500)
    y = gamma.pdf(x, a=shape, scale=scale)
    ax.plot(x, y, lw=2, label=f"Fitted Gamma (n={n})")

    ax.set_title(f"Players={n}")
    ax.set_xlabel("Turns")
    ax.set_ylabel("Density")
    ax.legend()

plt.suptitle("Observed vs Fitted Gamma (Players 2–7)", fontsize=14)
plt.tight_layout()
plt.show()
