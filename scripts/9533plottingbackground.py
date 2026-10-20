from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

root = Path(__file__).resolve().parents[1]
filename = root / 'eventinfo/observations/9533/repro/acisf09533_repro_evt2.fits'

with fits.open(filename) as f:
    data = f["EVENTS"].data
    gti = f["GTI", 3].data  # Good-time intervals for CCD 3.
    x = np.asarray(data["X"], dtype=float)
    y = np.asarray(data["Y"], dtype=float)
    energy = np.asarray(data["ENERGY"], dtype=float)
    time = np.asarray(data["TIME"], dtype=float)
    gti_start = np.asarray(gti["START"], dtype=float)
    gti_stop = np.asarray(gti["STOP"], dtype=float)

xc, yc = 4646.8904, 3699.1736   # HD 110086 in sky pixels
src_r = 7.32
bkg_in, bkg_out = 14.63, 29.27

r2 = (x - xc)**2 + (y - yc)**2
band = (energy >= 500) & (energy <= 7000)   # 0.5-7 keV

source_times = time[(r2 <= src_r**2) & band]
background_times = time[(r2 >= bkg_in**2) & (r2 <= bkg_out**2) & band]

print("Source photons:", len(source_times))
print("Background photons:", len(background_times))

# 200 s bins
t0 = 344609527.309310
bin_size = 200
edges = np.arange(t0, np.max(gti_stop) + bin_size, bin_size)
centers = (edges[:-1] + edges[1:]) / 2
time_ks = (centers - t0) / 1000

source_counts, _ = np.histogram(source_times, bins=edges)
background_counts, _ = np.histogram(background_times, bins=edges)

# usable exposure per bin from the GTIs
exposure = np.zeros(len(centers))
for start, stop in zip(gti_start, gti_stop):
    overlap = np.minimum(edges[1:], stop) - np.maximum(edges[:-1], start)
    exposure += np.maximum(overlap, 0)

# rates, nan where there's no exposure
good = exposure > 0
source_rate = np.full(len(centers), np.nan)
background_rate = np.full(len(centers), np.nan)
source_rate[good] = source_counts[good] / exposure[good]
background_rate[good] = background_counts[good] / exposure[good]

# scale the annulus to the source aperture area
scale = (np.pi * src_r**2) / (np.pi * (bkg_out**2 - bkg_in**2))
scaled_background = background_rate * scale
net_rate = source_rate - scaled_background

print("Background scaling factor:", scale)
print("Maximum source rate:", np.nanmax(source_rate))
print("Maximum net rate:", np.nanmax(net_rate))

# plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

ax1.plot(time_ks, source_rate, color="black", lw=1.2, drawstyle="steps-mid")
ax1.plot(time_ks, scaled_background, color="red", linestyle="--", lw=1.2, drawstyle="steps-mid")
ax1.set_title("HD110086_9533 Source vs Background")
ax1.set_ylabel("Count rate ~ counts/s")
ax1.grid(alpha=0.25)
ax1.legend(loc="upper left", frameon=False)

ax2.plot(time_ks, net_rate, color="blue", lw=1.2, drawstyle="steps-mid")
ax2.set_xlabel("Time since reference time ~ ks")
ax2.set_ylabel("Net count rate ~ counts/s")
ax2.grid(alpha=0.25)

flare_start, flare_end = 69.639, 74.009
for ax in (ax1, ax2):
    ax.axvspan(flare_start, flare_end, color="orange", alpha=0.15)

plt.tight_layout()
for ax in plt.gcf().axes:
    ax.grid(False)
plt.savefig(root / 'plots/OBS_9533_source_background.png', dpi=300, bbox_inches="tight")
plt.show()
