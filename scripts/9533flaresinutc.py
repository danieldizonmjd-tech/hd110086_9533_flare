from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.time import Time

# folder above this script, so it works from any terminal directory
root = Path(__file__).resolve().parents[1]

hdul = fits.open(root / 'eventinfo/products/lightcurves/hd110086_9533_200s.fits')
data = hdul['LIGHTCURVE'].data

counts = np.array(data['COUNTS'])
exposure = np.array(data['EXPOSURE'])
tmin = np.array(data['TIME_MIN'])
tmax = np.array(data['TIME_MAX'])
hdul.close()

# only divide where exposure is nonzero, leave the rest as nan
rate = np.full(len(counts), np.nan)
good = exposure > 0
rate[good] = counts[good] / exposure[good]

peak = np.nanargmax(rate)

print("Brightest bin:")

start = Time(tmin[peak], format='cxcsec', scale='tt').utc
mid = Time((tmin[peak] + tmax[peak]) / 2, format='cxcsec', scale='tt').utc
end = Time(tmax[peak], format='cxcsec', scale='tt').utc

print(f"Start: {start.isot} UTC")
print(f"Midpoint: {mid.isot} UTC")
print(f"End: {end.isot} UTC")
print("Counts:", counts[peak])
print("Count rate:", rate[peak], "counts/s")