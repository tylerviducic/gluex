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

if channel == 'pipkmks' :
    voight_resoltion = constants.F1_PIPKMKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIPKMKS_VOIGHT_SIGMA_ERROR
    # data_color = ROOT.TColor.GetColor(600) # kBlue
    total_fit_color = 860
    f1_color = 860-6
    gaus_color = 880
    background_color = 616
    hist_title = 'M(K^{-}K_{s}#pi^{+}) [GeV]'
    kstar_cut = kcuts.KSTAR_ALL_CUT_PIPKMKS
    gaus_mean = constants.F1_PIPKMKS_GAUS_MEAN
    gaus_width = constants.F1_PIPKMKS_GAUS_WIDTH
elif channel == 'pimkpks' :
    voight_resoltion = constants.F1_PIMKPKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIMKPKS_VOIGHT_SIGMA_ERROR
    total_fit_color = 633
    f1_color = 634
    gaus_color = 887
    background_color = 618
    hist_title = 'M(K^{+}K_{s}#pi^{-}) [GeV]'
    kstar_cut = kcuts.KSTAR_ALL_CUT_PIMKPKS
    gaus_mean = constants.F1_PIMKPKS_GAUS_MEAN
    gaus_width = constants.F1_PIMKPKS_GAUS_WIDTH

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg const', 'bkg first order', 'bkg second order']
initial_guesses = {
    0: 170, # voight amplitude
    1: 1.28, # voight mean
    3: 0.029, # voight width
    4: 495, # gaus amplitude
    5: 1.37, # gaus mean
    6: 0.033, # gaus width
    7: 1000, # bkg const
    8: -1000, # bkg first order
    9: 10 # bkg second order
}

data = ct.get_dataframe(channel, 'gluex1', 'data').Filter('e_beam > 8.0 && e_beam < 10.0').Filter('mand_t >= 0.1 && mand_t <= 0.4').Filter(kstar_cut)
uncor_data_hist = data.Histo1D(('uncor_data_hist', hist_title, 60, 1.0, 1.6), f'{channel}_m')
uncor_data_hist.Sumw2()
data_hist = ct.correct_data_hist_for_kstar_efficiency(uncor_data_hist)
data_hist.Sumw2()

# data_hist = ct.get_integrated_gluex1_kstar_corrected_data_hist(channel)

data_hist.GetXaxis().SetRangeUser(1.17, 1.5)
data_hist.GetYaxis().SetRangeUser(0, data_hist.GetMaximum()*1.1)
data_hist.GetXaxis().SetTitle(hist_title)
data_hist.GetYaxis().SetTitle('Events / 10 MeV')
data_hist.SetMarkerStyle(20)

# fit_low, fit_high = 1.18, 1.49
fit_low, fit_high = 1.17, 1.5

func = ROOT.TF1(f'integrated_{channel}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', fit_low, fit_high)

func.FixParameter(2, voight_resoltion) # voight sigma

func.SetParameter(0, initial_guesses[0]) # voight amplitude
func.SetParLimits(0, 1, 1000000)
func.SetParameter(1, initial_guesses[1]) # voight mean
# func.SetParLimits(1, 1.26, 1.3)
func.SetParameter(3, initial_guesses[3]) # voight width
# func.SetParLimits(3, 0.005, 0.05)
func.SetParameter(4, initial_guesses[4]) # gaus amplitude
func.SetParLimits(4, 1, 1000000)
func.SetParameter(5, initial_guesses[5]) # gaus mean 
func.SetParLimits(5, 1.35, 1.4)
func.SetParameter(6, initial_guesses[6]) # gaus width
func.SetParLimits(6, 0.025, 0.05)
func.SetParameter(7, initial_guesses[7]) # bkg const
# func.SetParLimits(7, 0, 1000000)
func.SetParameter(8, initial_guesses[8]) # bkg first order
# func.SetParLimits(8, 100, 10000)
func.SetParameter(9, initial_guesses[9]) # bkg second order
# func.SetParLimits(9, -100, 100)

# func.FixParameter(0, 169.6) # voigt amplitude
# func.FixParameter(1, 1.28) # voigt mean
# func.FixParameter(3, 0.028) # voigt width
# func.FixParameter(4, 495.8) # gaus amplitude
# func.FixParameter(5, 1.37) # gaus mean
# func.FixParameter(6, 0.0368) # gaus width
# func.FixParameter(7, initial_guesses[7]) # bkg const
# func.FixParameter(8, 1000) # bkg first order
# func.FixParameter(9, 50.0) # bkg second order

func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], 
                 parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

result = data_hist.Fit(func, 'SRB0')
func.SetLineColor(total_fit_color)

voight = ROOT.TF1(f'voight', '[0]*TMath::Voigt(x-[1], [2], [3])', fit_low, fit_high)
voight.SetLineColor(ROOT.kBlack)
voight.SetFillColor(f1_color)
voight.SetFillStyle(1001)
gaus = ROOT.TF1('gaus', 'gaus(0)', fit_low, fit_high)
gaus.SetLineColor(background_color)
gaus.SetLineStyle(3)
bkg = ROOT.TF1('bkg', 'pol2(0)', fit_low, fit_high)
bkg.SetLineColor(background_color)
bkg.SetLineStyle(2)

voight.SetParameter(0, func.GetParameter('voight amplitude'))
voight.SetParError(0, func.GetParError(0))
voight.SetParameter(1, func.GetParameter('voight mean'))
voight.SetParError(1, func.GetParError(1))
voight.SetParameter(2, func.GetParameter('voight sigma'))
voight.SetParError(2, func.GetParError(2))
voight.SetParameter(3, func.GetParameter('voight width'))
voight.SetParError(3, func.GetParError(3))
gaus.SetParameter(0, func.GetParameter('gaus amplitude'))
gaus.SetParError(0, func.GetParError(4))
gaus.SetParameter(1, func.GetParameter('gaus mean'))
gaus.SetParError(1, func.GetParError(5))
gaus.SetParameter(2, func.GetParameter('gaus width'))
gaus.SetParError(2, func.GetParError(6))
bkg.SetParameter(0, func.GetParameter('bkg const'))
bkg.SetParError(0, func.GetParError(7))
bkg.SetParameter(1, func.GetParameter('bkg first order'))
bkg.SetParError(1, func.GetParError(8))
bkg.SetParameter(2, func.GetParameter('bkg second order'))
bkg.SetParError(2, func.GetParError(9))

chi2_per_ndf = func.GetChisquare()/func.GetNDF()
voigt_mass = voight.GetParameter(1)
voigt_width = voight.GetParameter(3)
voigt_mass_err = voight.GetParError(1)
voigt_width_err = voight.GetParError(3)

print(f'Voight Mass: {voigt_mass} +/- {voigt_mass_err}')
print(f'Voight Width: {voigt_width} +/- {voigt_width_err}')
print(f'Gaus mean: {gaus.GetParameter(1)} +/- {gaus.GetParError(1)}')
print(f'Gaus width: {gaus.GetParameter(2)} +/- {gaus.GetParError(2)}')
print(f'chi^2/ndf = {chi2_per_ndf}')


c = ROOT.TCanvas('c', 'c', 1000, 1000)
data_hist.GetYaxis().SetTitleOffset(1.4)
data_hist.Draw("E1")
func.Draw('same')
voight.Draw('same')
gaus.Draw('same')
bkg.Draw('same')
data_hist.Draw("E1 same")


legend = ROOT.TLegend(0.725, 0.2, 0.945, 0.5)
legend.AddEntry(func, "Total Fit", "lpf")
legend.AddEntry(voight, "f_{1}(1285) Signal", "lpf")
legend.AddEntry(gaus, "f_{1}(1420) Tail", "lpf")
legend.AddEntry(bkg, "Background", "l")
legend.Draw()

fit_params = ROOT.TLatex()
fit_params.SetTextSize(0.0425)
fit_params.DrawLatexNDC(0.475, 0.75, "#chi^{2}/ndf = " + '{:.2f}'.format(chi2_per_ndf))
fit_params.DrawLatexNDC(0.475, 0.8, 'Width = ' + '{:.2f}'.format(voigt_width * 1000) + ' #pm ' + '{:.2f}'.format(voigt_width_err * 1000) + ' MeV')
fit_params.DrawLatexNDC(0.475, 0.85, 'Mass = ' + '{:.2f}'.format(voigt_mass * 1000) + ' #pm ' + '{:.2f}'.format(voigt_mass_err * 1000) + ' MeV')

c.Update()
c.SaveAs(f'/work/halld/home/viducic/plots/thesis/cross_section_fits/will_comparison_{channel}_fit.png')

f1_yield = voight.Integral(fit_low, fit_high)/0.01

flux = ct.get_luminosity_gluex_1(8, 10)*1000
flux_spring = ct.get_luminosity('spring', 8, 10)
flux_fall = ct.get_luminosity('fall', 8, 10)
flux_2017 = ct.get_luminosity('2017', 8, 10)

lumis = [flux_spring, flux_fall, flux_2017]
lumi = flux_spring + flux_fall + flux_2017

acceptance = 0
for i, run in enumerate(['spring', 'fall', '2017']):
    df_recon = ct.get_dataframe(channel, run, 'signal').Filter('e_beam > 8.0 && e_beam < 10.0').Filter('mand_t >= 0.1 && mand_t <= 0.4')
    df_thrown = ct.get_dataframe(channel, run, 'signal', filtered=False, thrown=True).Filter('e_beam > 8.0 && e_beam < 10.0').Filter('mand_t >= 0.1 && mand_t <= 0.4')
    acceptance += (df_recon.Count().GetValue()/df_thrown.Count().GetValue())*(lumis[i]/lumi)


cross_section = ct.calculate_crosssection(f1_yield, acceptance, flux, 0.4, 0.091)
print(f'Cross section for {channel}: {cross_section} nb/0.4 GeV^2')


input('press enter to continue')