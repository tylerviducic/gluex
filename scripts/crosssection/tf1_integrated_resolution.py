import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import os

os.nice(18)
ROOT.EnableImplicitMT()

channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'


signal_mc = ct.get_integrated_gluex1_signal_mc_hist_for_resolution_fitting('pipkmks', scale_factor=50, nbins = 500)
ct.set_sqrtN_error(signal_mc)

func = ROOT.TF1('func', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.15, 1.4)
func.FixParameter(1, 1.285)
func.FixParameter(3, 0.022)

signal_mc.Fit(func, 'R0')

chi2_per_ndf = func.GetChisquare() / func.GetNDF()

res_fit_latex = ROOT.TLatex()
res_fit_latex.SetTextSize(0.03)
res_fit_latex.DrawLatexNDC(0.65, 0.8, '#chi^2/ndf = ' + '{:.2f}'.format(chi2_per_ndf))
res_fit_latex.DrawLatexNDC(0.65, 0.75, '#sigma = ' + '{:.2f}'.format(func.GetParameter(2) * 1000) + ' MeV')


c = ROOT.TCanvas('c', 'c', 800, 600)
signal_mc.Draw()
func.Draw('same')
c.Draw()

# print(f'resoltuion = {func.GetParameter(2)}')
# print(f'chi2/ndf = {chi2_per_ndf}')

# input('Press enter to continue...')