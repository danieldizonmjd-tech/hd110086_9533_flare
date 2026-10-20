# HD 110086 flare: Chandra ObsID 9533

Python scripts and figures used to study the X-ray flare of HD 110086. The analysis includes light curves, source/background comparisons, detector coverage, soft and hard energy bands, Bayesian blocks, and a decay fit.

## Contents

- `scripts/9533*.py`: plotting and timing analysis scripts.
- `plots/`: generated figures.
- `eventinfo/regions/`: source, background, and spectral extraction regions.
- `reports/sherpa_results/`: saved spectral fitting sessions.
- `logs/`: flux extraction results.

## Setup

Use a separate Python 3.11+ environment for plotting:

```bash
python -m pip install -r requirements.txt
python scripts/9533plottingbackground.py
```

Observational FITS files and extracted data stay local under `eventinfo/` and are excluded from the repository. Spectral fitting also requires CIAO/Sherpa with XSPEC support and the local spectra and response files.
