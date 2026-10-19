# HD 110086: Chandra ObsID 9533 flare

Python scripts and plots for inspecting the X-ray flare of HD 110086 in Chandra observation 9533. The analysis includes light curves, detector coverage, soft/hard-band rates, source/background comparisons, Bayesian blocks, and an exponential decay fit.

## Scripts

| File | Purpose |
| --- | --- |
| `9533lc.py` | Plot the extracted 200-second light curve. |
| `9533energy.py` | Compare soft/hard-band count rates and their hardness ratio. |
| `9533dithering.py` | Plot the detector coverage fraction around the flare. |
| `9533plottingbackground.py` | Compare source and area-scaled background rates, using CCD 3 good-time intervals. |
| `9533bayesianblocks.py` | Find changes in the unbinned source photon rate with Bayesian blocks. |
| `9533flaremeasurements.py` | Estimate the baseline, excess counts, and exponential decay timescale. |
| `9533flaresinutc.py` | Print the brightest light-curve bin times in UTC. |
| `9533background.py` | Print peak counts, count rate, and UTC bin times. |
| `reports/sherpa_results/` | Saved full-aperture and wing-spectrum Sherpa sessions. |

Existing figures are in `plots/`.

Flux extraction logs for sources 477 and 969 in ObsIDs 1586, 9532, and 9533, together with a combined flux summary, are in `logs/`.

## Python environment

Use Python 3.11 or newer in an analysis environment:

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` records the package versions used for local verification. The saved Sherpa sessions additionally require a compatible CIAO/Sherpa environment with XSPEC support; these are separate from the plotting dependencies.

## Input data

The FITS data and original Chandra observation downloads stay local and are excluded from this repository. Place your processed files in this layout relative to the repository directory:

```text
eventinfo/
  observations/9533/repro/acisf09533_repro_evt2.fits
  products/
    lightcurves/
      hd110086_9533_200s.fits
      hd110086_soft_200s.fits
      hd110086_hard_200s.fits
    diagnostics/hd110086_dither.fits
    spectra/
      hd110086_spectra/
      hd110086_wing_spectra/
```

The light-curve scripts expect a `LIGHTCURVE` table with `TIME_MIN`, `TIME_MAX`, `COUNTS`, and `EXPOSURE` columns. The dither script reads the `AREAFRACTION` table and its `TIME` and `FRACAREA` columns. The event-based scripts read the `EVENTS` table; the background comparison uses the `GTI` extension with version 3.

The two spectral directories are needed only for the saved Sherpa sessions. Keep the spectra, background files, and ARF/RMF responses together within each directory.

## Run

From the repository directory:

```bash
python 9533lc.py
python 9533dithering.py
python 9533energy.py
python 9533plottingbackground.py
python 9533bayesianblocks.py
python 9533flaremeasurements.py
python 9533flaresinutc.py
```

Paths resolve from each script's location, so a different terminal working directory is also supported. Plotting scripts save their figures into `plots/` and display them.

The exponential decay model is the pre-flare baseline plus a decaying excess count rate. Its timescale, tau, is the time for that excess above baseline to decrease to 1/e of its initial value.
