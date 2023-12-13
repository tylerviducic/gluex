"""
fit the kkpi corrected distributinos with "two peaks" to describe the bumps for the
tails of the f1(1420) peak per klaus's suggestoin 
"""

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

data_hist = ct.get_integrated_gluex1_kstar_corrected_data_hist(channel)

kkpi_low, kkpi_high = 1.2, 1.5
m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", kkpi_low, kkpi_high)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), data_hist)

voight_m = ROOT.RooRealVar("voight_m", "voight_m", 1.285, 1.2, 1.3)
voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.0227, 0.01, 0.075)
voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", voight_resoltion, 0.01, 0.5)
voight_sigma.setError(voight_resolution_error)
voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_m, voight_width, voight_sigma)
voight_sigma.setConstant(True)
# voight_m.setConstant(True)
# voight_width.setConstant(True)

gaus_m = ROOT.RooRealVar("gaus_m", "gaus_m", 1.36, 1.35, 1.43)
gaus_width = ROOT.RooRealVar("gaus_width", "gaus_width", 0.034, 0.025, 0.05)
gaus = ROOT.RooGaussian("gaus", "gaus", m_kkpi, gaus_m, gaus_width)
# gaus_m.setConstant(True)
# gaus_width.setConstant(True)

## CHEBYCHEV ##
bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 0.0, 2.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 0.0, 2.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", 0.0, 2.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", 0.0, 2.0)

bkg = ROOT.RooChebychev("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1))
# bkg_par1.setConstant(True)

n_f1 = ROOT.RooRealVar("n_f1", "n_f1", 10000, 0.0, 1000000000)
n_gaus = ROOT.RooRealVar("n_gaus", "n_gaus", 10000, 0.0, 1000000000)
n_bkg = ROOT.RooRealVar("n_bkg", "n_bkg", 10000, 0.0, 1000000000)

combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, gaus, bkg), ROOT.RooArgList(n_f1, n_gaus, n_bkg))

c2 = ROOT.RooChi2Var(f"c2", f"c2", combined_pdf, dh, ROOT.RooFit.Extended(True), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
minuit = ROOT.RooMinuit(c2)
minuit.migrad()
minuit.minos()

fit_result = minuit.save()

chi2_val = c2.getVal()
n_bins_ndf = data_hist.GetXaxis().FindBin(kkpi_high) - data_hist.GetXaxis().FindBin(kkpi_low)
# n_bins = 29
ndf = n_bins_ndf - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
chi2_per_ndf = chi2_val / ndf

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
c1.cd()
frame = m_kkpi.frame()
title = ct.get_integrated_kkpi_hist_title(channel)
frame.SetTitle(title)
frame.GetXaxis().SetTitle(f'{title.split(" ")[0]} GeV') 
frame.GetYaxis().SetTitle(f'Counts/10MeV')

dh.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
# dh.plotOn(frame, DataError="SumW2", LineColor="b", MarkerColor="b")
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(total_fit_color), ROOT.RooFit.Name("full_fit"))
pullHist = frame.pullHist()
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(f1_color), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(f1_color), ROOT.RooFit.LineWidth(5), ROOT.RooFit.Name("f1_signal"))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("gaus"), ROOT.RooFit.LineColor(gaus_color), ROOT.RooFit.LineWidth(4), ROOT.RooFit.Name("1420_tail"))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(background_color), ROOT.RooFit.MarkerColor(background_color), ROOT.RooFit.LineWidth(4), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name("bkg"))

frame.Draw()

legend = ROOT.TLegend(0.7, 0.2, 0.95, 0.5)
legend.AddEntry(frame.findObject("full_fit"), "Total Fit", "lpf")
legend.AddEntry(frame.findObject("f1_signal"), "f_{1}(1285) Signal", "lpf")
legend.AddEntry(frame.findObject("1420_tail"), "f_{1}(1420) Tail", "lpf")
legend.AddEntry(frame.findObject("bkg"), "Background", "l")
legend.Draw()

# fit_params = ROOT.TPaveText(0.6, 0.5, 0.9, 0.8, "NDC")
# fit_params.AddText(f"Mean = {voight_m.getVal() * 1000} +/- {voight_m.getError() * 1000}")
# fit_params.AddText(f"Width = {voight_width.getVal() * 1000} +/- {voight_width.getError() * 1000}")
# fit_params.AddText(f"#Chi^{2}/n.d.f = " + str(round(chi2_per_ndf, 2)))
# fit_params.Draw()

fit_params = ROOT.TLatex()
fit_params.SetTextSize(0.055)
# fit_params.DrawLatexNDC(0.425, 0.875, f"Mean = {voight_m.getVal() * 1000:.2f} #pm {voight_m.getError() * 1000:.2f} MeV")
# fit_params.DrawLatexNDC(0.425, 0.825, f"Width = {voight_width.getVal() * 1000:.2f} #pm {voight_width.getError() * 1000:.2f} MeV")
fit_params.DrawLatexNDC(0.45, 0.8, "#chi^{2}/ndf = " + '{:.2f}'.format(chi2_per_ndf))
fit_params.DrawLatexNDC(0.45, 0.85, 'Width = ' + '{:.2f}'.format(voight_width.getVal() * 1000) + ' #pm ' + '{:.2f}'.format(voight_width.getError() * 1000) + ' MeV')
fit_params.DrawLatexNDC(0.45, 0.9, 'Mass = ' + '{:.2f}'.format(voight_m.getVal() * 1000) + ' #pm ' + '{:.2f}'.format(voight_m.getError() * 1000) + ' MeV')




c1.Update()
c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/{channel}_integrated_fit_two_bumps.png')
c1.SaveAs(f'/work/halld/home/viducic/scripts/plotting/dnp_maui/plots/{channel}_integrated_fit_two_bumps.png')

pullDist = ROOT.TH1I("pullDist", "pullDist", 5, 0, 5)
for i in range(0, pullHist.GetN()):
    pullDist.Fill(abs(pullHist.GetY()[i]))

ks_test_func = combined_pdf.createHistogram("ks_test_func", m_kkpi)#, ROOT.RooFit.Binning(1000))
ks_test_data = dh.createHistogram("ks_test_data", m_kkpi)#, ROOT.RooFit.Binning(1000))
# ks_test_data.Scale(1/ks_test_data.Integral())
# ks_test_func.Scale(1/ks_test_func.Integral())

kstest = ks_test_data.KolmogorovTest(ks_test_func)
print("K-S test = " + str(kstest))

"""
K-S test = 1 means very high probability of data coming from the 
distribution described by the model
"""

# c3 = ROOT.TCanvas("c2", "c2", 800, 600)
# c3.cd()
# c3.Divide(3, 1)
# c3.cd(1)
# pullHist.Draw("AP")

# y = 0.0

# line= ROOT.TLine(frame.GetXaxis().GetXmin(), y, frame.GetXaxis().GetXmax(), y)
# line.SetLineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red']))
# line.SetLineStyle(2)
# line.SetLineWidth(2)
# line.Draw("same")
# c3.cd(2)
# pullDist.Draw()
# c3.cd(3)
# ks_test_data.Draw()
# ks_test_func.Draw("same")
# c3.Update()

print(f"f1 mass = {voight_m.getVal() * 1000} +/- {voight_m.getError() * 1000}")
print(f"f1 width = {voight_width.getVal() * 1000} +/- {voight_width.getError() * 1000}")
print(f'gaus mean = {gaus_m.getVal() * 1000} +/- {gaus_m.getError() * 1000}')
print(f'gaus width = {gaus_width.getVal() * 1000} +/- {gaus_width.getError() * 1000}')
print(f'bkg par1 = {bkg_par1.getVal()} +/- {bkg_par1.getError()}')
print("chi2 = " + str(c2.getVal()))
print("ndf = " + str(ndf))
print("chi2/ndf (manual calculation) = " + str(chi2_per_ndf))
print(f'f1 yield = {n_f1.getVal()} +/- {n_f1.getError()}')

input("Press enter to close")