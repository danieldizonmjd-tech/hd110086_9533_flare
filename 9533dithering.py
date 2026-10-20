from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

root = Path(__file__).resolve().parent

with fits.open(root / 'eventinfo/products/diagnostics/hd110086_dither.fits') as f:
    d = f["AREAFRACTION"].data
    time = np.asarray(d["TIME"], dtype=float)
    frac = np.asarray(d["FRACAREA"], dtype=float)

t0 = 344609527.309310   # same ref time as the light curve
time_ks = (time - t0) / 1000

plt.figure(figsize=(10, 4))
plt.plot(time_ks, frac, ".", color="black", markersize=2)
plt.axvspan(70, 75, color="orange", alpha=0.2, label="X-ray flare")
plt.xlim(65, 80)
plt.ylim(0, 1.05)
plt.xlabel("Time since observation start ~ ks")
plt.ylabel("FRACAREA")
plt.title("HD110086_9533 Detector Coverage")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.grid(False)
plt.savefig(root / 'plots/OBS_9533_dither_check.png', dpi=300)
plt.show()
