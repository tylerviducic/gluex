# script to test width of kshort


"""
An effective resolution is computed as σ = f σ1 + (1 − f )σ2 where f is the fraction 
of the first Gaussian contribution. The resulting effective resolutions for the LL and DD categories are 
σLL = 2.53 MeV and σDD = 6.46 MeV. The KS0 signals are selected within 
3.0σ of the fitted KS0 mass of 497.8 MeV.2
"""

import ROOT
from common_analysis_tools import *

data_filename = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
data_treename = 'pipkmks__B4_M16'

df = ROOT.RDataFrame(data_treename, data_filename)

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

ks_pathlength_cut = 'pathlength_sig > 5'

data_hist = df.Filter(ks_pathlength_cut).Histo1D(('ks_m', 'ks_m', 500, 0.35, 0.65), 'ks_m').GetValue()


signal_yield = ROOT.RooRealVar("signal_yield", "Signal Yield", 0, 10000000)
background_yield = ROOT.RooRealVar("background_yield", "Background Yield", 0, 10000000)

m_pipi = ROOT.RooRealVar("m_pipi", "m_pipi", 0.35, 0.65)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_pipi), data_hist)

# m_pipi.setRange("signal", KSHORT_FIT_MEAN - (2*KSHORT_FIT_WIDTH), KSHORT_FIT_MEAN + (2*KSHORT_FIT_WIDTH))

ks_mean_1 = ROOT.RooRealVar("mean_1", "mean_1", 0.5, 0.475, 0.515)
ks_sigma_1 = ROOT.RooRealVar("sigma_1", "sigma_1", 0.01, 0.002, 0.02)

# ks_mean.setConstant(1)
# ks_sigma.setConstant(1)
gaus_1 = ROOT.RooGaussian("gaus_1", "gaus_1", m_pipi, ks_mean_1, ks_sigma_1)

ks_mean_2 = ROOT.RooRealVar("mean_2", "mean_2", 0.5, 0.475, 0.515)
ks_sigma_2 = ROOT.RooRealVar("sigma_2", "sigma_2", 0.01, 0.002, 0.02)

gaus_2 = ROOT.RooGaussian("gaus_2", "gaus_2", m_pipi, ks_mean_2, ks_sigma_2)

gaus_frac = ROOT.RooRealVar("gaus_frac", "gaus_frac", 0.05, 0.0, 1.0)
double_gaus = ROOT.RooAddPdf("double_gaus", "double_gaus", ROOT.RooArgList(gaus_1, gaus_2), ROOT.RooArgList(gaus_frac))


## FIT IN DIFFERENT RANGE ##
# gaus.fitTo(dh, ROOT.RooFit.Range("signal"))
# gaus.fitTo(dh, ROOT.RooFit.SumCoefRange("signal"))

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1.0, -10., 100000.)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1.0, -10., 100000.)
bkg = ROOT.RooPolynomial("bkg", "bkg", m_pipi, ROOT.RooArgList(bkg_par1))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)

composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(double_gaus, bkg), ROOT.RooArgList(sig_frac))
# composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(double_gaus, bkg), ROOT.RooArgList(signal_yield, background_yield))
# composite.chi2FitTo(dh)
composite.fitTo(dh)
# composite.fitTo(dh,ROOT.RooFit.SumCoefRange("signal"))

signal_integral = double_gaus.createIntegral(ROOT.RooArgSet(m_pipi), ROOT.RooFit.Range(KSHORT_FIT_MEAN - (2*KSHORT_FIT_WIDTH), KSHORT_FIT_MEAN + (2*KSHORT_FIT_WIDTH)))
background_integral = bkg.createIntegral(ROOT.RooArgSet(m_pipi), ROOT.RooFit.Range(KSHORT_FIT_MEAN - (2*KSHORT_FIT_WIDTH), KSHORT_FIT_MEAN + (2*KSHORT_FIT_WIDTH)))

signal_to_background = signal_integral.getVal() / background_integral.getVal()

frame = m_pipi.frame()
dh.plotOn(frame)
composite.plotOn(frame)
composite.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kBlack))
composite.plotOn(frame, ROOT.RooFit.Components("double_gaus"), ROOT.RooFit.LineColor(ROOT.kRed))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_1"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_2"), ROOT.RooFit.LineStyle(ROOT.kDashDotted), ROOT.RooFit.LineColor(ROOT.kRed))

frame.Draw()

def get_composite_width(sig1, sig2, frac):
    return sig1 * frac + sig2 * (1.0 - frac)

def get_composite_mean(mean1, mean2, frac):
    return mean1 * frac + mean2 * (1.0 - frac)
    
composite_width = get_composite_width(ks_sigma_1.getVal(), ks_sigma_2.getVal(), gaus_frac.getVal())
composite_width_error = get_composite_width(ks_sigma_1.getError(), ks_sigma_2.getError(), gaus_frac.getVal())
composite_mean = get_composite_mean(ks_mean_1.getVal(), ks_mean_2.getVal(), gaus_frac.getVal())
print(f'Width of first gaussian is: {ks_sigma_1.getVal()} +/- {ks_sigma_1.getError()}')
print(f'Width of second gaussian is: {ks_sigma_2.getVal()} +/- {ks_sigma_2.getError()}')
print(f'Fraction of first gaussian is: {gaus_frac.getVal()}')
print(f'Width of double gaussian is: {composite_width} +/- {composite_width_error}')
print(f'Mean of first gaussian is: {ks_mean_1.getVal()}')
print(f'Mean of second gaussian is: {ks_mean_2.getVal()}')
print(f'Fraction of first gaussian is: {gaus_frac.getVal()}')
print(f'Mean of double gaussian is: {composite_mean}')
print(f'signal integral is: {signal_integral.getVal()}')
print(f'background integral is: {background_integral.getVal()}')
input("Press enter to exit")
