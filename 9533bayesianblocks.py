from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy.stats import bayesian_blocks

root = Path(__file__).resolve().parent
filename = root / 'eventinfo/observations/9533/repro/acisf09533_repro_evt2.fits'

t0 = 344609527.309310           # ref time from the light curve
xc, yc = 4646.8904, 3699.1736   # HD 110086 position in sky pixels
radius = 7.32                   # 3.6 arcsec in sky pixels

with fits.open(filename) as f:
    data = f["EVENTS"].data
    x = np.asarray(data["X"], dtype=float)
    y = np.asarray(data["Y"], dtype=float)
    energy = np.asarray(data["ENERGY"], dtype=float)
    time = np.asarray(data["TIME"], dtype=float)
    gti_names = [h.name for h in f if h.name.upper().startswith("GTI")]

print("GTI extensions:", gti_names)

# photons inside the circle, 0.5-7 keV
r2 = (x - xc)**2 + (y - yc)**2
source = (r2 <= radius**2) & (energy >= 500) & (energy <= 7000)
arrival_times = np.sort(time[source])
print("Source photons:", len(arrival_times))

if len(arrival_times) < 2:
    raise RuntimeError("Not enough source photons.")

# bayesian blocks
edges = bayesian_blocks(arrival_times, fitness="events", p0=0.01)
counts, _ = np.histogram(arrival_times, bins=edges)
rates = counts / np.diff(edges)

print("\nNumber of Bayesian Blocks:", len(rates), "\n")


def to_utc(sec):
    return Time(sec, format="cxcsec", scale="tt").utc.isot

print("Results for each block:")
for i in range(len(rates)):
    start, end = edges[i], edges[i + 1]
    print(f"\nBlock {i + 1}")
    print("Start:", to_utc(start), "UTC")
    print("End:  ", to_utc(end), "UTC")
    print("Start (ks):", round((start - t0) / 1000, 3))
    print("End (ks):", round((end - t0) / 1000, 3))
    print("Photons:", counts[i])
    print("Count rate:", round(rates[i], 5), "counts/s")

# plot
edges_ks = (edges - t0) / 1000

fig, ax = plt.subplots(figsize=(11, 5))
ax.stairs(rates, edges_ks, linewidth=2, color="black", label="Bayesian Blocks")
ax.set_xlabel("Time since light-curve reference ~ ks")
ax.set_ylabel("Count rate ~ counts/s")
ax.set_title("HD110086_9533 Bayesian Blocks\n0.5–7 keV")
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(root / 'plots/OBS_9533_bayesian_blocks.png', dpi=300)
plt.show()

# does the result change with p0?
print("\n Bayesian Blocks with different p0 values ")
for p0 in [0.05, 0.01, 0.001]:
    test_edges = bayesian_blocks(arrival_times, fitness="events", p0=p0)
    print(f"\np0 = {p0}")
    print("Number of blocks:", len(test_edges) - 1)
    print("Change points near the flare:")
    for edge in test_edges[1:-1]:
        ks = (edge - t0) / 1000
        if 55 <= ks <= 82:   # flare window
            print(f"{ks:.3f} ks | {to_utc(edge)} UTC")