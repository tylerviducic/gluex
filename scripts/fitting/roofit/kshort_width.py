# script to test width of kshort
# TODO: redo this. 

"""
An effective resolution is computed as σ = f σ1 + (1 − f )σ2 where f is the fraction 
of the first Gaussian contribution. The resulting effective resolutions for the LL and DD categories are 
σLL = 2.53 MeV and σDD = 6.46 MeV. The KS0 signals are selected within 
3.0σ of the fitted KS0 mass of 497.8 MeV.2
"""

import ROOT
import my_library.common_analysis_tools as ct
import my_library.thesis_plotter_library as plotter
from my_library.kinematic_cuts import KS_PATHLENGTH_CUT, MX2_PPIPKMKS_CUT, P_P_CUT
from my_library.constants import KSHORT_FIT_MEAN, KSHORT_FIT_WIDTH, COLORBLIND_HEX_DICT

df = ct.get_dataframe('pipkmks', 'spring', 'data')
df = df.Filter(KS_PATHLENGTH_CUT).Filter(MX2_PPIPKMKS_CUT).Filter(P_P_CUT)

nbins, xlow, xhigh = 1000, 0.35, 0.65
data_hist = df.Histo1D(('ks_m', 'ks_m', nbins, xlow, xhigh), 'ks_m').GetValue()


signal_yield = ROOT.RooRealVar("signal_yield", "Signal Yield", 0, 10000000)
background_yield = ROOT.RooRealVar("background_yield", "Background Yield", 0, 10000000)

m_pipi = ROOT.RooRealVar("m_pipi", "m_pipi", xlow, xhigh)
# range_min = 0.45
# range_max = 0.55
# m_pipi.setRange("fit_range", range_min, range_max)
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

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1.0, 0., 1000000.)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1.0, -10., 1000000.)
bkg = ROOT.RooPolynomial("bkg", "bkg", m_pipi, ROOT.RooArgList(bkg_par1))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)

composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(double_gaus, bkg), ROOT.RooArgList(sig_frac))
# composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(double_gaus, bkg), ROOT.RooArgList(signal_yield, background_yield))
# composite.chi2FitTo(dh)
# composite.fitTo(dh, ROOT.RooFit.Range("fit_range"))
composite.fitTo(dh)
# composite.fitTo(dh,ROOT.RooFit.SumCoefRange("signal"))

signal_integral = double_gaus.createIntegral(ROOT.RooArgSet(m_pipi), ROOT.RooFit.Range(KSHORT_FIT_MEAN - (2*KSHORT_FIT_WIDTH), KSHORT_FIT_MEAN + (2*KSHORT_FIT_WIDTH)))
background_integral = bkg.createIntegral(ROOT.RooArgSet(m_pipi), ROOT.RooFit.Range(KSHORT_FIT_MEAN - (2*KSHORT_FIT_WIDTH), KSHORT_FIT_MEAN + (2*KSHORT_FIT_WIDTH)))

signal_to_background = signal_integral.getVal() / background_integral.getVal()

frame = m_pipi.frame()
dh.plotOn(frame)
composite.plotOn(frame)
composite.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.TColor.GetColor((COLORBLIND_HEX_DICT['purple']))))
composite.plotOn(frame, ROOT.RooFit.Components("double_gaus"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor((COLORBLIND_HEX_DICT['red']))))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_1"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(COLORBLIND_HEX_DICT['blue'])))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_2"), ROOT.RooFit.LineStyle(ROOT.kDashDotted), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(COLORBLIND_HEX_DICT['cyan'])))

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
c1.cd()
frame.Draw()
title = 'Fit of M(#pi^{+}#pi^{-})'
frame.SetTitle(title)
frame.GetXaxis().SetTitle('M(#pi^{+}#pi^{-}) [GeV]')
frame.GetYaxis().SetTitle(f'Events / {(1000*(xhigh-xlow)/nbins):.2f} MeV')
frame.GetYaxis().SetTitleOffset(1.5)
c1.SaveAs('/w/halld-scshelf2101/home/viducic/plots/thesis/ks_width.png')

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

