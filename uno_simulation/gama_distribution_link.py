import pandas as pd
import numpy as np
import matplotlib
from scipy.interpolate import UnivariateSpline

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats import gamma

df_specials = pd.read_csv("results_with_specials_high_16n6c.csv")
df_no_specials = pd.read_csv("results_no_specials_high_16n6c.csv")

fitted_params = []
for n in range(2, 12):
    data = df_specials[df_specials["num_players"] == n]["turns"]
    shape, loc, scale = gamma.fit(data)
    fitted_params.append({"num_players": n, "shape": shape, "scale": scale})

print(fitted_params)
df_params = pd.DataFrame(fitted_params)

spline_shape = UnivariateSpline(df_params["num_players"], df_params["shape"], k=2, s=0)
spline_scale = UnivariateSpline(df_params["num_players"], np.log(df_params["scale"]), k=2, s=0)

predicted_params = {}

for n in [12, 13, 14]:
    shape_pred = spline_shape(n)
    log_scale_pred = spline_scale(n)
    scale_pred = np.exp(log_scale_pred)
    predicted_params[n] = {"shape": shape_pred, "scale": scale_pred}
    print(f"Predicted gamma params for {n} players: shape={shape_pred}, scale={scale_pred}")

for n in [12, 13, 14]:
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
