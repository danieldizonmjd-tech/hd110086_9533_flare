from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from astropy.io import fits
from scipy.optimize import curve_fit

root = Path(__file__).resolve().parent

with fits.open(root / 'eventinfo/products/lightcurves/hd110086_9533_200s.fits') as hdul:
    data = hdul["LIGHTCURVE"].data
    time = np.array(data["TIME_MIN"], dtype=float)
    counts = np.array(data["COUNTS"], dtype=float)
    exposure = np.array(data["EXPOSURE"], dtype=float)

time_ks = (time - time[0]) / 1000

good = exposure > 0
rate = np.full(len(counts), np.nan)
rate[good] = counts[good] / exposure[good]

# baseline from the quiet part before the flare
pre = good & (time_ks >= 10) & (time_ks < 65)
baseline = counts[pre].sum() / exposure[pre].sum()

# flare window
flare = good & (time_ks >= 69) & (time_ks <= 92)
peak_idx = np.nanargmax(rate[flare])
peak_time = time_ks[flare][peak_idx]
peak_rate = rate[flare][peak_idx]

excess_counts = np.sum(counts[flare] - baseline * exposure[flare])


def decay(t, amp, tau):
    return baseline + amp * np.exp(-(t - peak_time) / tau)


# fit from the peak onward
after = good & (time_ks >= peak_time) & (time_ks <= 92)

params, cov = curve_fit(
    decay, time_ks[after], rate[after],
    p0=[peak_rate - baseline, 5],
    bounds=([0, 0.01], [np.inf, 100]),
    maxfev=10000,
)
amp, tau = params

print("\n HD110086_9533 Flare Measurements")
print(f"Baseline rate: {baseline:.5f} counts/s")
print(f"Peak time: {peak_time:.2f} ks")
print(f"Peak rate: {peak_rate:.5f} counts/s")
print(f"Peak/baseline: {peak_rate / baseline:.1f}x")
print(f"Excess counts (69-92 ks): {excess_counts:.1f}")
print(f"Decay timescale: {tau:.2f} ks")

# plot
plt.figure(figsize=(10, 5))
plt.step(time_ks, rate, where="post", color="black", label="Observed X-rays")
plt.axhline(baseline, color="blue", linestyle="--", label="Pre-flare baseline")

t_model = np.linspace(peak_time, 92, 300)
plt.plot(t_model, decay(t_model, *params), color="red", linewidth=2,
         label=f"Decay fit (tau={tau:.2f} ks)")

# Label the curves directly; the white outline keeps text readable without a box.
label_style = dict( fontsize=9,path_effects=[path_effects.withStroke(linewidth=3, foreground="white")])
fit_label_time = 77.5
plt.annotate(rf"$\tau = {tau:.2f}$ ks", xy=(fit_label_time, decay(fit_label_time, *params)), xytext=(4, 36), textcoords="offset points", color="red", rotation=-15, rotation_mode="anchor", ha="left", va="bottom", **label_style,)
# tau represents the time it takes for the flare to decrease by a factor of e (~2.718).
plt.annotate("Pre-flare baseline", xy=(91, baseline), xytext=(0, -8), textcoords="offset points", color="blue", ha="right", va="top", **label_style,)

plt.xlim(65, 92)
plt.xlabel("Time ~ ks")
plt.ylabel("Count rate ~ counts/s")
plt.title("HD110086_9533 Flare Measurements")
plt.grid(alpha=0.25)
plt.tight_layout()
for ax in plt.gcf().axes:
    ax.grid(False)
plt.savefig(root / 'plots/OBS_9533_flare_measurements.png', dpi=300)
plt.show()
