from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

root = Path(__file__).resolve().parent


def read_lc(name):
    with fits.open(root / 'eventinfo/products/lightcurves' / name) as hdul:
        d = hdul["LIGHTCURVE"].data
        return (np.array(d["TIME_MIN"], dtype=float),
                np.array(d["COUNTS"], dtype=float),
                np.array(d["EXPOSURE"], dtype=float))


t_soft, s, exp_s = read_lc('hd110086_soft_200s.fits')
t_hard, h, exp_h = read_lc('hd110086_hard_200s.fits')

if not np.allclose(t_soft, t_hard, rtol=0, atol=0.001):
    raise ValueError("Soft and hard time bins do not match.")

time_ks = (t_soft - t_soft[0]) / 1000

# rates, nan where there's no exposure
soft = np.full_like(s, np.nan)
hard = np.full_like(h, np.nan)
soft[exp_s > 0] = s[exp_s > 0] / exp_s[exp_s > 0]
hard[exp_h > 0] = h[exp_h > 0] / exp_h[exp_h > 0]

# hardness ratio
total = hard + soft
ok = (total > 0) & (exp_s > 0) & (exp_h > 0)
hr = np.full_like(total, np.nan)
hr[ok] = (hard[ok] - soft[ok]) / total[ok]

fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

axes[0].step(time_ks, soft, where="post", color="blue")
axes[0].set_ylabel("Soft ~ counts/s")
axes[0].set_title("HDD110086_9533 Energy Analysis\nSoft: 0.5–1.2 keV, Hard: 1.2–7 keV")

axes[1].step(time_ks, hard, where="post", color="red")
axes[1].set_ylabel("Hard ~ counts/s")

axes[2].plot(time_ks, hr, ".", color="black", markersize=3)
axes[2].set_ylabel("Hardness ratio")
axes[2].set_xlabel("Time since observation start ~ ks")
axes[2].set_ylim(-1.1, 1.1)

for ax in axes:
    ax.axvspan(70, 75, color="orange", alpha=0.15)
    ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(root / 'plots/OBS_9533_energy_analysis.png', dpi=300)
plt.show()