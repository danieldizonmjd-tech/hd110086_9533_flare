from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.time import Time

root = Path(__file__).resolve().parent

with fits.open(root / 'eventinfo/products/lightcurves/hd110086_9533_200s.fits') as f:
    data = f["LIGHTCURVE"].data
    counts = np.array(data["COUNTS"])
    exposure = np.array(data["EXPOSURE"])
    tmin = np.array(data["TIME_MIN"])
    tmax = np.array(data["TIME_MAX"])

# rate, skipping bins with no exposure
rate = np.full(len(counts), np.nan)
good = exposure > 0
rate[good] = counts[good] / exposure[good]

peak = np.nanargmax(rate)

print(" HD110086_9533 Flare in UTC ")

times = {
    "Peak bin start": tmin[peak],
    "Peak bin midpoint": (tmin[peak] + tmax[peak]) / 2,
    "Peak bin end": tmax[peak],
}

for label, t in times.items():
    utc = Time(t, format="cxcsec", scale="tt").utc
    print(label, utc.isot, "UTC")

print("Peak counts:", counts[peak])
print("Peak rate:", rate[peak], "counts/s")