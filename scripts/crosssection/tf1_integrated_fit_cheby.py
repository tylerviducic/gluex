"""
fit the kkpi corrected distributinos with "two peaks" to describe the bumps for the
tails of the f1(1420) peak per klaus's suggestoin 
"""

from numpy.lib.npyio import re
import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts 
import my_library.gluex_style as gxstyle
import os

os.nice(18)
ROOT.EnableImplicitMT(8)
ROOT.gStyle.SetOptStat(0)

channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'

ROOT.TF1.InitStandardFunctions()
f = ROOT.gROOT.GetListOfFunctions()
print(f.FindObject('chebyshev2'))

if channel == 'pipkmks' :
    voight_resoltion = constants.F1_PIPKMKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIPKMKS_VOIGHT_SIGMA_ERROR
    # data_color = ROOT.TColor.GetColor(600) # kBlue
    total_fit_color = 860
    f1_color = 860-6
    gaus_color = 880
    background_color = 616
elif channel == 'pimkpks' :
    voight_resoltion = constants.F1_PIMKPKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIMKPKS_VOIGHT_SIGMA_ERROR
    total_fit_color = 633
    f1_color = 634
    gaus_color = 887
    background_color = 618

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg norm', 'bkg const', 'bkg first order', 'bkg second order']
initial_guesses = {
    0: 170, # voight amplitude
    1: 1.28, # voight mean
    3: 0.029, # voight width
    4: 495, # gaus amplitude
    5: 1.37, # gaus mean
    6: 0.033, # gaus width
    7: -1500, # bkg norm
    9: -0.8, # bkg first order
    10: 0.3
      # bkg second order
}


data_hist = ct.get_integrated_gluex1_kstar_corrected_data_hist(channel)
data_hist.GetXaxis().SetRangeUser(1.15, 1.55)
data_hist.GetYaxis().SetRangeUser(0, data_hist.GetMaximum()*1.1)

func = ROOT.TF1(f'integrated_{channel}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + [7]*cheb2(8)', 1.16, 1.54)

func.FixParameter(2, voight_resoltion) # voight sigma
func.FixParameter(8, 1) # bkg const

func.SetParameter(0, initial_guesses[0]) # voight amplitude
func.SetParLimits(0, 1, 1000000)
func.SetParameter(1, initial_guesses[1]) # voight mean
# func.SetParLimits(1, 1.26, 1.3)
func.SetParameter(3, initial_guesses[3]) # voight width
# func.SetParLimits(3, 0.005, 0.05)
func.SetParameter(4, initial_guesses[4]) # gaus amplitude
func.SetParLimits(4, 1, 1000000)
func.SetParameter(5, initial_guesses[5]) # gaus mean 
# func.SetParLimits(5, 1.35, 1.4)
func.SetParameter(6, initial_guesses[6]) # gaus width
func.SetParLimits(6, 0.025, 0.05)
func.SetParameter(7, initial_guesses[7]) # bkg norm
func.SetParameter(9, initial_guesses[9]) # bkg first order
func.SetParLimits(9, -100, 0.0)
func.SetParameter(10, initial_guesses[10]) # bkg second order
# func.SetParLimits(10, -1, 1)

func.FixParameter(0, 169.6) # voigt amplitude
func.FixParameter(1, 1.28) # voigt mean
func.FixParameter(3, 0.028) # voigt width
func.FixParameter(4, 495.8) # gaus amplitude
func.FixParameter(5, 1.37) # gaus mean
func.FixParameter(6, 0.0368) # gaus width
# func.FixParameter(7, initial_guesses[7]) # bkg norm
func.FixParameter(9, 0.8) # bkg first order
# func.FixParameter(10, 0.0) # bkg second order

func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], 
                 parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9], parameter_names[10])

result = data_hist.Fit(func, 'SRB0E')
func.SetLineColor(total_fit_color)

voight = ROOT.TF1(f'voight', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.18, 1.55)
voight.SetLineColor(ROOT.kBlack)
voight.SetFillColor(f1_color)
voight.SetFillStyle(1001)
gaus = ROOT.TF1('gaus', 'gaus(0)', 1.18, 1.55)
gaus.SetLineColor(background_color)
gaus.SetLineStyle(3)
bkg = ROOT.TF1('bkg', '[0]*cheb2(1)', 1.18, 1.55)
bkg.SetLineColor(background_color)
bkg.SetLineStyle(2)

voight.SetParameter(0, func.GetParameter(0))
voight.SetParError(0, func.GetParError(0))
voight.SetParameter(1, func.GetParameter(1))
voight.SetParError(1, func.GetParError(1))
voight.SetParameter(2, func.GetParameter(2))
voight.SetParError(2, func.GetParError(2))
voight.SetParameter(3, func.GetParameter(3))
voight.SetParError(3, func.GetParError(3))
gaus.SetParameter(0, func.GetParameter(4))
gaus.SetParError(0, func.GetParError(4))
gaus.SetParameter(1, func.GetParameter(5))
gaus.SetParError(1, func.GetParError(5))
gaus.SetParameter(2, func.GetParameter(6))
gaus.SetParError(2, func.GetParError(6))
bkg.SetParameter(0, func.GetParameter(7))
bkg.SetParError(0, func.GetParError(7))
bkg.SetParameter(1, func.GetParameter(8))
bkg.SetParError(1, func.GetParError(8))
bkg.SetParameter(2, func.GetParameter(9))
bkg.SetParError(2, func.GetParError(9))
bkg.SetParameter(3, func.GetParameter(10))
bkg.SetParError(3, func.GetParError(10))

print(f'Voight Mass: {voight.GetParameter(1)} +/- {voight.GetParError(1)}')
print(f'Voight Width: {voight.GetParameter(3)} +/- {voight.GetParError(3)}')
print(f'Gaus mean: {gaus.GetParameter(1)} +/- {gaus.GetParError(1)}')
print(f'Gaus width: {gaus.GetParameter(2)} +/- {gaus.GetParError(2)}')
print(f'chi^2/ndf = {func.GetChisquare()/func.GetNDF()}')


c = ROOT.TCanvas('c', 'c', 1000, 1000)
data_hist.Draw()
func.Draw('same')
voight.Draw('same')
gaus.Draw('same')
bkg.Draw('same')
c.Update()

input('press enter to continue')