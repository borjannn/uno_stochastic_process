import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats import gamma

df_specials = pd.read_csv("results_with_specials_high.csv")
df_no_specials = pd.read_csv("results_no_specials_high.csv")

fitted_params = []
for n in range(2, 7):
    data = df_specials[df_specials["num_players"] == n]["turns"]
    shape, loc, scale = gamma.fit(data)
    fitted_params.append({"num_players": n, "shape": shape, "scale": scale})

print(fitted_params)
df_params = pd.DataFrame(fitted_params)


coeff_shape = np.polyfit(df_params["num_players"], df_params["shape"], 1)
coeff_scale = np.polyfit(df_params["num_players"], df_params["scale"], 1)

predicted_params = {}

for n in [8, 9]:
    shape_pred = np.polyval(coeff_shape, n)
    scale_pred = np.polyval(coeff_scale, n)
    predicted_params[n] = {"shape": shape_pred, "scale": scale_pred}
    print(f"Predicted gamma params for {n} players: shape={shape_pred}, scale={scale_pred}")

for n in [8, 9]:
    data = df_specials[df_specials["num_players"] == n]["turns"]

    plt.hist(data, bins=50, density=True, alpha=0.5, label=f"Observed (n={n})")

    x = np.linspace(0, data.max(), 500)
    shape = predicted_params[n]["shape"]
    scale = predicted_params[n]["scale"]
    y = gamma.pdf(x, a=shape, scale=scale)

    plt.plot(x, y, "r-", lw=2, label=f"Predicted Gamma (n={n})")

    plt.title(f"Game Length Distribution (Players={n})")
    plt.xlabel("Number of Turns")
    plt.ylabel("Density")
    plt.legend()
    plt.show()
