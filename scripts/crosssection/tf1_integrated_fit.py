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

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

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

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg par1', 'bkg par2', 'bkg par3']
initial_guesses = {
    0: 100,
    1: 1.28, 
    3: 0.023,
    4: 1,
    5: 1.37,
    6: 0.033,
    7: 1000,
    8: 1000,
    9: -1000
}


data_hist = ct.get_integrated_gluex1_kstar_corrected_data_hist(channel)
data_hist.GetXaxis().SetRangeUser(1.19, 1.51)
data_hist.GetYaxis().SetRangeUser(0, data_hist.GetMaximum()*1.1)

func = ROOT.TF1(f'integrated_{channel}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.2, 1.5)

func.SetParameter(0, initial_guesses[0])
func.SetParLimits(0, 1, 1000000)
func.SetParameter(1, initial_guesses[1])
func.SetParLimits(1, 1.26, 1.3)
func.FixParameter(2, voight_resoltion)
func.SetParameter(3, initial_guesses[3])
func.SetParLimits(3, 0.005, 0.05)
func.SetParameter(4, initial_guesses[4])
func.SetParLimits(4, 0, 1000000)
func.SetParameter(5, initial_guesses[5])
# func.FixParameter(5, initial_guesses[5])
func.SetParLimits(5, 1.35, 1.4)
# func.FixParameter(6, initial_guesses[6])
func.SetParameter(6, initial_guesses[6])
func.SetParLimits(6, 0.025, 0.05)
func.SetParameter(7, initial_guesses[4])
func.SetParameter(8, initial_guesses[5])
func.SetParLimits(8, 0, 100000)
func.SetParameter(9, initial_guesses[6])
func.SetParLimits(9, -100000, 100000)

func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

result = data_hist.Fit(func, 'SRBOM')
func.SetLineColor(total_fit_color)

voight = ROOT.TF1(f'voight', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.19, 1.51)
voight.SetLineColor(ROOT.kBlack)
voight.SetFillColor(f1_color)
voight.SetFillStyle(1001)
gaus = ROOT.TF1('gaus', 'gaus(0)', 1.19, 1.51)
gaus.SetLineColor(background_color)
gaus.SetLineStyle(3)
bkg = ROOT.TF1('bkg', 'pol2(0)', 1.19, 1.51)
bkg.SetLineColor(background_color)
bkg.SetLineStyle(2)

initial_guesses[4] = func.GetParameter(4)
initial_guesses[5] = func.GetParameter(5)
initial_guesses[6] = func.GetParameter(6)
initial_guesses[7] = func.GetParameter(7)
initial_guesses[8] = func.GetParameter(8)
initial_guesses[9] = func.GetParameter(9)

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