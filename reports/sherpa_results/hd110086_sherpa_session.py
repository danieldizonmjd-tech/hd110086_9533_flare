from pathlib import Path as _DataPath

# Resolve inputs and plots from the data folder, regardless of the terminal directory.
DATA_ROOT = _DataPath(__file__).resolve().parents[2]

import numpy
from sherpa.astro.ui import *

######### Load Data Sets

load_pha(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare.pi'))

######### Data Spectral Responses

load_arf(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare.arf'), resp_id=1)
load_rmf(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare.rmf'), resp_id=1)

######### Load Background Data Sets

load_bkg(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare_bkg.pi'), bkg_id=1)

######### Background Spectral Responses

load_arf(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare.arf'), resp_id=1, bkg_id=1)
load_rmf(1, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/preflare.rmf'), resp_id=1, bkg_id=1)

######### Set Energy or Wave Units

set_analysis(1, quantity="energy", type="rate", factor=0)

######### Filter Data

notice_id(1, "0.496399998665:7.007999897003")
notice_id(1, bkg_id=1)
notice_id(1, "0.496399998665:7.007999897003", bkg_id=1)
load_pha(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak.pi'))

######### Data Spectral Responses

load_arf(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak.arf'), resp_id=1)
load_rmf(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak.rmf'), resp_id=1)

######### Load Background Data Sets

load_bkg(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak_bkg.pi'), bkg_id=1)

######### Background Spectral Responses

load_arf(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak.arf'), resp_id=1, bkg_id=1)
load_rmf(2, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/peak.rmf'), resp_id=1, bkg_id=1)

######### Set Energy or Wave Units

set_analysis(2, quantity="energy", type="rate", factor=0)

######### Filter Data

notice_id(2, "0.496399998665:7.007999897003")
notice_id(2, bkg_id=1)
notice_id(2, "0.496399998665:7.007999897003", bkg_id=1)
load_pha(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay.pi'))

######### Data Spectral Responses

load_arf(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay.arf'), resp_id=1)
load_rmf(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay.rmf'), resp_id=1)

######### Load Background Data Sets

load_bkg(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay_bkg.pi'), bkg_id=1)

######### Background Spectral Responses

load_arf(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay.arf'), resp_id=1, bkg_id=1)
load_rmf(3, str(DATA_ROOT / 'eventinfo/products/spectra/hd110086_spectra/decay.rmf'), resp_id=1, bkg_id=1)

######### Set Energy or Wave Units

set_analysis(3, quantity="energy", type="rate", factor=0)

######### Filter Data

notice_id(3, "0.496399998665:7.007999897003")
notice_id(3, bkg_id=1)
notice_id(3, "0.496399998665:7.007999897003", bkg_id=1)


######### Set Statistic

set_stat("wstat")


######### Set Fitting Method

set_method("levmar")

set_method_opt("epsfcn", 1.1920928955078125e-07)
set_method_opt("factor", 100.0)
set_method_opt("ftol", 1.1920928955078125e-07)
set_method_opt("gtol", 1.1920928955078125e-07)
set_method_opt("maxfev", None)
set_method_opt("numcores", 1)
set_method_opt("verbose", 0)
set_method_opt("xtol", 1.1920928955078125e-07)


######### Set Model Components and Parameters

create_model_component("xsapec", "pre")
pre.integrate = True

pre.kT.default_val = 1.0
pre.kT.default_min = 0.008
pre.kT.default_max = 64.0
pre.kT.val     = 0.9554028499337449
pre.kT.min     = 0.008
pre.kT.max     = 64.0
pre.kT.units   = "keV"
pre.kT.frozen  = False

pre.Abundanc.default_val = 1.0
pre.Abundanc.default_min = 0.0
pre.Abundanc.default_max = 5.0
pre.Abundanc.val     = 1.0
pre.Abundanc.min     = 0.0
pre.Abundanc.max     = 5.0
pre.Abundanc.units   = ""
pre.Abundanc.frozen  = True

pre.Redshift.default_val = 0.0
pre.Redshift.default_min = -0.999
pre.Redshift.default_max = 10.0
pre.Redshift.val     = 0.0
pre.Redshift.min     = -0.999
pre.Redshift.max     = 10.0
pre.Redshift.units   = ""
pre.Redshift.frozen  = True

pre.norm.default_val = 1.0
pre.norm.default_min = 0.0
pre.norm.default_max = 1e+24
pre.norm.val     = 3.748387691757676e-05
pre.norm.min     = 0.0
pre.norm.max     = 1e+24
pre.norm.units   = ""
pre.norm.frozen  = False

create_model_component("xsapec", "peak")
peak.integrate = True

peak.kT.default_val = 1.0
peak.kT.default_min = 0.008
peak.kT.default_max = 64.0
peak.kT.val     = 3.1441060719883946
peak.kT.min     = 0.008
peak.kT.max     = 64.0
peak.kT.units   = "keV"
peak.kT.frozen  = False

peak.Abundanc.default_val = 1.0
peak.Abundanc.default_min = 0.0
peak.Abundanc.default_max = 5.0
peak.Abundanc.val     = 1.0
peak.Abundanc.min     = 0.0
peak.Abundanc.max     = 5.0
peak.Abundanc.units   = ""
peak.Abundanc.frozen  = True

peak.Redshift.default_val = 0.0
peak.Redshift.default_min = -0.999
peak.Redshift.default_max = 10.0
peak.Redshift.val     = 0.0
peak.Redshift.min     = -0.999
peak.Redshift.max     = 10.0
peak.Redshift.units   = ""
peak.Redshift.frozen  = True

peak.norm.default_val = 1.0
peak.norm.default_min = 0.0
peak.norm.default_max = 1e+24
peak.norm.val     = 0.0017271245210935388
peak.norm.min     = 0.0
peak.norm.max     = 1e+24
peak.norm.units   = ""
peak.norm.frozen  = False

create_model_component("xsapec", "decay")
decay.integrate = True

decay.kT.default_val = 1.0
decay.kT.default_min = 0.008
decay.kT.default_max = 64.0
decay.kT.val     = 1.8054895208539024
decay.kT.min     = 0.008
decay.kT.max     = 64.0
decay.kT.units   = "keV"
decay.kT.frozen  = False

decay.Abundanc.default_val = 1.0
decay.Abundanc.default_min = 0.0
decay.Abundanc.default_max = 5.0
decay.Abundanc.val     = 1.0
decay.Abundanc.min     = 0.0
decay.Abundanc.max     = 5.0
decay.Abundanc.units   = ""
decay.Abundanc.frozen  = True

decay.Redshift.default_val = 0.0
decay.Redshift.default_min = -0.999
decay.Redshift.default_max = 10.0
decay.Redshift.val     = 0.0
decay.Redshift.min     = -0.999
decay.Redshift.max     = 10.0
decay.Redshift.units   = ""
decay.Redshift.frozen  = True

decay.norm.default_val = 1.0
decay.norm.default_min = 0.0
decay.norm.default_max = 1e+24
decay.norm.val     = 0.00036565072504742365
decay.norm.min     = 0.0
decay.norm.max     = 1e+24
decay.norm.units   = ""
decay.norm.frozen  = False



######### Set Source, Pileup and Background Models

set_source(1, xsapec.pre)

set_source(2, xsapec.peak)

set_source(3, xsapec.decay)


######### XSPEC Module Settings

set_xschatter(10)
set_xsabund("angr")
set_xscosmo(70, 0, 0.73)
set_xsxsect("vern")
