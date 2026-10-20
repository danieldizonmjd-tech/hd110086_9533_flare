from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

root = Path(__file__).resolve().parent

with fits.open(root / 'eventinfo/products/lightcurves/hd110086_9533_200s.fits') as hdul:
    data = hdul["LIGHTCURVE"].data
    time = np.asarray(data["TIME_MIN"], dtype=float)
    counts = np.asarray(data["COUNTS"], dtype=float)
    exposure = np.asarray(data["EXPOSURE"], dtype=float)

time_ks = (time - time[0]) / 1000

rate = np.full(len(counts), np.nan)
good = exposure > 0
rate[good] = counts[good] / exposure[good]

plt.figure(figsize=(11, 5))
plt.step(time_ks, rate, where="post", color="black")
plt.xlabel("Time since observation start ~ ks")
plt.ylabel("Count rate ~ counts/s")
plt.title("HD110086_9533 Light Curve")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.grid(False)
plt.savefig(root / 'plots/OBS_9533_light_curve.png', dpi=300)
plt.show()