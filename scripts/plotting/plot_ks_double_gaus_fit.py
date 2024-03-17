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

df = ct.get_dataframe('pipkmks', 'gluex1', 'data', filtered=False)
df = df.Filter(KS_PATHLENGTH_CUT).Filter(MX2_PPIPKMKS_CUT).Filter(P_P_CUT)
n_bins, xlow, xhigh = 10000, 0.35, 0.7
hist_ks_pipkmks = df.Histo1D(('hist_ks_pipkmks', 'hist_ks_pipkmks', n_bins, xlow, xhigh), 'ks_m').GetValue()


ks_fit = ROOT.TF1('ks_fit', 'gaus[0] + gaus[3] + pol1(6)', 0.45, 0.55)
ks_fit.SetParameter(0, 60000)
ks_fit.SetParameter(1, 0.5)
ks_fit.SetParameter(2, 0.01)
ks_fit.SetParameter(3, 10000)
ks_fit.SetParameter(4, 0.5)
ks_fit.SetParameter(5, 0.01)
ks_fit.SetParameter(6, 10)
ks_fit.SetParameter(7, 5000)

hist_ks_pipkmks.Fit(ks_fit, 'LR0')

gaus1 = ROOT.TF1('gaus1', 'gaus', 0.4, 0.6)
gaus2 = ROOT.TF1('gaus2', 'gaus', 0.4, 0.6)
pol1 = ROOT.TF1('pol1', 'pol1', 0.4, 0.6)

gaus1.SetParameters(ks_fit.GetParameter(0), ks_fit.GetParameter(1), ks_fit.GetParameter(2))
gaus2.SetParameters(ks_fit.GetParameter(3), ks_fit.GetParameter(4), ks_fit.GetParameter(5))
pol1.SetParameters(ks_fit.GetParameter(6), ks_fit.GetParameter(7))

ks_fit.SetLineColor(ROOT.kBlue)

gaus1.SetLineColor(ROOT.kGreen)
gaus2.SetLineColor(ROOT.kRed)
pol1.SetLineColor(ROOT.kOrange)
pol1.SetLineStyle(2)

c = ROOT.TCanvas('c', 'c', 800, 800)
hist_ks_pipkmks.Draw()
ks_fit.Draw('same')
gaus1.Draw('same')
gaus2.Draw('same')
pol1.Draw('same')
c.Update()
c.Draw()
input('Press enter to continue')