# FIT KKPi INTEGRATED Distribution after phasespace acceptance correction for mean and width check

import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import os
import numpy as np

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks' :
    # all_cut = ct.KSTAR_ALL_CUT_PIPKMKS
    voight_resoltion = constants.F1_PIPKMKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIPKMKS_VOIGHT_SIGMA_ERROR
elif channel == 'pimkpks' :
    # all_cut = ct.KSTAR_ALL_CUT_PIMKPKS
    voight_resoltion = constants.F1_PIMKPKS_VOIGHT_SIGMA
    voight_resolution_error = constants.F1_PIMKPKS_VOIGHT_SIGMA_ERROR

file_and_tree_spring = ct.get_flat_file_and_tree(channel, 'spring', 'data')
file_and_tree_fall = ct.get_flat_file_and_tree(channel, 'fall', 'data')
file_and_tree_2017 = ct.get_flat_file_and_tree(channel, '2017', 'data')

df_spring = ROOT.RDataFrame(file_and_tree_spring[1], file_and_tree_spring[0])
df_fall = ROOT.RDataFrame(file_and_tree_fall[1], file_and_tree_fall[0])
df_2017 = ROOT.RDataFrame(file_and_tree_2017[1], file_and_tree_2017[0])

hist_spring = df_spring.Histo1D((f'hist_spring', f'hist_spring', 150, 1.0, 2.5), f'{channel}_m').GetValue()
hist_fall = df_fall.Histo1D((f'hist_fall', f'hist_fall', 150, 1.0, 2.5), f'{channel}_m').GetValue()
hist_2017 = df_2017.Histo1D((f'hist_2017', f'hist_2017', 150, 1.0, 2.5), f'{channel}_m').GetValue()

hist_spring.Sumw2()
hist_fall.Sumw2()
hist_2017.Sumw2()

data_hist = hist_spring.Clone()
data_hist.Add(hist_fall)
data_hist.Add(hist_2017)
# data_hist.Draw()
# input("Press enter to continue")

for i in range(1, data_hist.GetNbinsX() + 1):
    data_hist.SetBinError(i, np.sqrt(data_hist.GetBinContent(i)))


# data_hist = ct.get_integrated_gluex1_acceptance_corrected_data(channel, cut)
# data_hist = ct.get_integrated_gluex1_kstar_corrected_data_hist(channel)


m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.15, 1.8)
range_min = 1.19
range_max = 1.5
m_kkpi.setRange("fit_range", range_min, range_max)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), data_hist)

# ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

# relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
# relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.001, 0.1)

# set up a roofit voightian with a mean of 1.285, width of 0.024, and a sigma of 0.013
voight_m_1285 = ROOT.RooRealVar("voight_m_1285", "voight_m_1285", 1.285, 1.2, 1.3)
voight_width_1285 = ROOT.RooRealVar("voight_width_1285", "voight_width_1285", 0.023, 0.01, 0.075)
voight_sigma_1285 = ROOT.RooRealVar("voight_sigma_1285", "voight_sigma_1285", voight_resoltion, 0.01, 0.5)
voight_sigma_1285.setError(voight_resolution_error)
voight_1285 = ROOT.RooVoigtian("voight_1285", "voight_1285", m_kkpi, voight_m_1285, voight_width_1285, voight_sigma_1285)

voight_m_1420 = ROOT.RooRealVar("voight_m_1420", "voight_m_1420", 1.420, 1.35, 1.45)
voight_width_1420 = ROOT.RooRealVar("voight_width_1420", "voight_width_1420", 0.0525, 0.04, 0.075)
voight_sigma_1420 = ROOT.RooRealVar("voight_sigma_1420", "voight_sigma_1420", voight_resoltion, 0.01, 0.5)
voight_sigma_1420.setError(voight_resolution_error)
voight_1420 = ROOT.RooVoigtian("voight_1420", "voight_1420", m_kkpi, voight_m_1420, voight_width_1420, voight_sigma_1420)

# hold the voight parameters fixed
# voight_m.setConstant(True)
# voight_width.setConstant(True)
voight_sigma_1285.setConstant(True)
voight_sigma_1420.setConstant(True)

# relbw = ROOT.RelBreitWigner("relbw", "relbw", m_kkpi, relbw_m, relbw_width)

# bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.4, 1.43)
# bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.5)

# bw = ROOT.RooBreitWigner("1420", "1420", m_kkpi, bw_m, bw_width)

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -2.0, 2.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -2.0, 2.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -2.0, 2.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -2.0, 2.0)

bkg = ROOT.RooChebychev("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))


## BERNSTEIN ##

# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
# bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

# bkg = ROOT.RooBernstein("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4))

# POLYNOMIAL ##
# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -100, 100)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -100, 100)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -100, 100)
# bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -100, 100)

# bkg = ROOT.RooPolynomial("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4))


## COMBINED PDF ##
# bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)
# bkg_pdf = ROOT.RooAddPdf("bkg_pdf", "bkg_pdf", ROOT.RooArgList(bkg, bw), ROOT.RooArgList(bkg_frac))

# sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
# # combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(relbw, bkg_pdf), ROOT.RooArgList(sig_frac))
# combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, bkg), ROOT.RooArgList(sig_frac))

n_f1_1285 = ROOT.RooRealVar("n_f1_1285", "n_f1_1285", 10000, 0.0, 1000000000)
n_f1_1420 = ROOT.RooRealVar("n_f1_1420", "n_f1_1420", 10000, 0.0, 1000000000)
n_bkg = ROOT.RooRealVar("n_bkg", "n_bkg", 10000, 0.0, 1000000000)

combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight_1285, voight_1420, bkg), ROOT.RooArgList(n_f1_1285, n_f1_1420, n_bkg))


c2 = ROOT.RooChi2Var(f"c2", f"c2", combined_pdf, dh, ROOT.RooFit.Extended(True), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Range("fit_range"))
minuit = ROOT.RooMinuit(c2)
minuit.migrad()
minuit.minos()

# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
# combined_pdf.fitTo(dh)
# fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.Save())
# fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Save())
fit_result = minuit.save()
# fit_result = combined_pdf.fitTo(dh, ROOT.RooFit.Save())

chi2_val = c2.getVal()
n_bins_ndf = data_hist.GetXaxis().FindBin(range_max) - data_hist.GetXaxis().FindBin(range_min)
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

npar = combined_pdf.getParameters(dh).selectByAttrib("Constant", False).getSize()
chi2ndf = frame.chiSquare(npar)

dh.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
# draw_pdf(kstar_cut, frame, combined_pdf, '1285')
# combined_pdf.plotOn(frame, ROOT.RooFit.VisualizeError(fit_result), ROOT.RooFit.LineColor(ROOT.kRed))
combined_pdf.plotOn(frame, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red'])))
pullHist = frame.pullHist()
npar = combined_pdf.getParameters(dh).selectByAttrib("Constant", False).getSize()
chi2ndf = frame.chiSquare(npar)
# fit_result.plotOn(frame, ROOT.RooAbsArg(voight), ROOT.RooFit.LineColor(ROOT.kRed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kGreen))
combined_pdf.plotOn(frame, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['green'])), ROOT.RooFit.LineStyle(ROOT.kDashed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kBlue))
combined_pdf.plotOn(frame, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.Components("voight_1285"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['blue'])))
combined_pdf.plotOn(frame, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.Components("voight_1420"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['purple'])))

frame.Draw()
c1.Update()
c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/{channel}_two_peak_integrated_fit.png')

pullDist = ROOT.TH1I("pullDist", "pullDist", 3, 0, 3)
for i in range(0, pullHist.GetN()):
    pullDist.Fill(abs(pullHist.GetY()[i]))

ks_test_func = combined_pdf.createHistogram("ks_test_func", m_kkpi)#, ROOT.RooFit.Binning(1000))
ks_test_data = dh.createHistogram("ks_test_data", m_kkpi)#, ROOT.RooFit.Binning(1000))
ks_test_data.Scale(1/ks_test_data.Integral())
ks_test_func.Scale(1/ks_test_func.Integral())

kstest = ks_test_data.KolmogorovTest(ks_test_func)
# latex = ROOT.TLatex(); #prepare text in LaTeX format latex->SetTextSize(0.035);
# latex.SetNDC()
# latex.DrawLatex(0.25, 0.75, ROOT.Form("K-S test = %.2f", kstest)); 
print("K-S test = " + str(kstest))

"""
K-S test = 1 means very high probability of data coming from the 
distribution described by the model
"""
ks_test_data.SetLineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red']))


c3 = ROOT.TCanvas("c2", "c2", 800, 600)
c3.cd()
c3.Divide(3, 1)
c3.cd(1)
pullHist.Draw("AP")

y = 0.0

line= ROOT.TLine(frame.GetXaxis().GetXmin(), y, frame.GetXaxis().GetXmax(), y)
line.SetLineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red']))
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw("same")
c3.cd(2)
pullDist.Draw()
c3.cd(3)
ks_test_data.Draw()
ks_test_func.Draw("same")
c3.Update()


print(f"f1 mass = {voight_m_1285.getVal() * 1000} +/- {voight_m_1285.getError() * 1000}")
print(f"f1 width = {voight_width_1285.getVal() * 1000} +/- {voight_width_1285.getError() * 1000}")
print(f"1420 mass = {voight_m_1420.getVal() * 1000} +/- {voight_m_1420.getError() * 1000}")
print(f"1420 width = {voight_width_1420.getVal() * 1000} +/- {voight_width_1420.getError() * 1000}")
# print("chi2 = " + str(chi2_val))
print("chi2 = " + str(c2.getVal()))
print("ndf = " + str(ndf))
print("chi2/ndf (manual calculation) = " + str(chi2_per_ndf))
print(f"second X2/ndf (frame method) = {chi2ndf}")
print(f'f1 yield = {n_f1_1285.getVal()} +/- {n_f1_1285.getError()}')

input("Press enter to close")



## OLD CODE ### def get_acceptance_corrected_kkpi(channel, run_period):

#     data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data')
#     data_df = ROOT.RDataFrame(data_file_and_tree[1], data_file_and_tree[0])

#     recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
#     thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)


#     recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])

#     thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')

#     data_df = data_df.Filter(all_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
#     recon_df = recon_df.Filter(all_cut).Filter(T_RANGE).Filter(BEAM_RANGE)

#     data_hist = data_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', 150, 1.0, 2.5), f'{channel}_m').GetValue()
#     recon_hist = recon_df.Histo1D((f'recon_hist_{run_period}', f'recon_hist_{run_period}', 150, 1.0, 2.5), f'{channel}_m').GetValue()
#     thrown_hist_name = channel + ';1'
#     thrown_hist = thrown_file.Get(thrown_hist_name)

#     data_hist.Sumw2()
#     recon_hist.Sumw2()
#     thrown_hist.Sumw2()

#     acceptance_hist = recon_hist.Clone()
#     acceptance_hist.Divide(thrown_hist)

#     ac_data_hist = data_hist.Clone()
#     ac_data_hist.Divide(acceptance_hist)
#     ac_data_hist.SetDirectory(0)

#     return ac_data_hist


# ac_data_hist_2017 = get_acceptance_corrected_kkpi(channel, '2017')
# ac_data_hist_spring = get_acceptance_corrected_kkpi(channel, 'spring')
# ac_data_hist_fall = get_acceptance_corrected_kkpi(channel, 'fall')


# ac_data_hist_total = ac_data_hist_spring
# ac_data_hist_total.Add(ac_data_hist_fall)
# ac_data_hist_total.Add(ac_data_hist_2017)