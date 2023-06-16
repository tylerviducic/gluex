# script for fitting kkpi distribution with eta as part of the function to "test" contribution

import ROOT
from common_analysis_tools import *
import os

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

channel = 'pipkmks'
cut = 'all'


def get_acceptance_corrected_kkpi(channel, run_period):

    data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data')
    data_df = ROOT.RDataFrame(data_file_and_tree[1], data_file_and_tree[0])

    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)


    recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])

    thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')

    data_df = data_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)
    recon_df = recon_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)

    data_hist = data_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', 30, 1.2, 1.5), 'pipkmks_m').GetValue()
    recon_hist = recon_df.Histo1D((f'recon_hist_{run_period}', f'recon_hist_{run_period}', 30, 1.2, 1.5), 'pipkmks_m').GetValue()
    thrown_hist_name = channel + ';1'
    thrown_hist = thrown_file.Get(thrown_hist_name)

    data_hist.Sumw2()
    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)

    ac_data_hist = data_hist.Clone()
    ac_data_hist.Divide(acceptance_hist)
    ac_data_hist.SetDirectory(0)

    return ac_data_hist


ac_data_hist_2017 = get_acceptance_corrected_kkpi(channel, '2017')
ac_data_hist_spring = get_acceptance_corrected_kkpi(channel, 'spring')
ac_data_hist_fall = get_acceptance_corrected_kkpi(channel, 'fall')


ac_data_hist_total = ac_data_hist_spring
ac_data_hist_total.Add(ac_data_hist_fall)
ac_data_hist_total.Add(ac_data_hist_2017)


m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.2, 1.5)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), ac_data_hist_total)

# set up two roofit voightian with a mean of 1.285/1.295, width of 0.024/0.055, and a sigma of 0.013
voight_m_f1 = ROOT.RooRealVar("voight_m_f1", "voight_m_f1", 1.285, 1.2, 1.3)
voight_width_f1 = ROOT.RooRealVar("voight_width_f1", "voight_width_f1", 0.024, 0.01, 0.075)
voight_sigma_f1 = ROOT.RooRealVar("voight_sigma_f1", "voight_sigma_f1", 0.0111726, 0.01, 0.5)
voight_sigma_f1.setError(.000435994)
voight_f1 = ROOT.RooVoigtian("voight_f1", "voight_f1", m_kkpi, voight_m_f1, voight_width_f1, voight_sigma_f1)

# hold the f1 voight parameters fixed
# voight_m.setConstant(True)
# voight_width.setConstant(True)
voight_sigma_f1.setConstant(True)

voight_m_eta = ROOT.RooRealVar("voight_m_eta", "voight_m_eta", 1.294, 1.28, 1.3)
voight_width_eta = ROOT.RooRealVar("voight_width_eta", "voight_width_eta", 0.055, 0.01, 0.075)
voight_sigma_eta = ROOT.RooRealVar("voight_sigma_eta", "voight_sigma_eta", 0.0111726, 0.01, 0.5)
voight_sigma_eta.setError(.000435994)
voight_eta = ROOT.RooVoigtian("voight_eta", "voight_eta", m_kkpi, voight_m_eta, voight_width_eta, voight_sigma_eta)

# hold the eta voight parameters fixed
voight_m_eta.setConstant(True)
voight_width_eta.setConstant(True)
voight_sigma_eta.setConstant(True)

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

bkg = ROOT.RooChebychev("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3)) 

# bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)
# f1_frac = ROOT.RooRealVar("f1_frac", "f1_frac", 0.5, 0.0, 1.0)

n_bkg = ROOT.RooRealVar("n_bkg", "n_bkg", 10000, 0, 100000000)
n_eta = ROOT.RooRealVar("n_eta", "n_eta", 10000, 0, 100000000)
n_f1 = ROOT.RooRealVar("n_f1", "n_f1", 10000, 0, 100000000)

# combined_voight = ROOT.RooAddPdf("combined_voight", "combined_voight", ROOT.RooArgList(voight_f1, voight_eta), ROOT.RooArgList(f1_frac))
# combined_pdf = ROOT.RooAddPdf("combined_pdf", "combined_pdf", ROOT.RooArgList(combined_voight, bkg), ROOT.RooArgList(bkg_frac))

combined_pdf = ROOT.RooAddPdf("combined_pdf", "comined_pdf", ROOT.RooArgList(voight_f1, voight_eta, bkg), ROOT.RooArgList(n_f1, n_eta, n_bkg))

chi2_var = combined_pdf.createChi2(dh)

c2 = ROOT.RooChi2Var(f"c2", f"c2", combined_pdf, dh, ROOT.RooFit.Extended(True), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
minuit = ROOT.RooMinuit(c2)
minuit.migrad()
minuit.minos()


# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
# combined_pdf.fitTo(dh)
# fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Range("fit_range"), ROOT.RooFit.Save())
# fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Save())
fit_result = minuit.save()

chi2_val = chi2_var.getVal()
n_bins = ac_data_hist_total.GetNbinsX()
# n_bins = 29
ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
chi2_per_ndf = chi2_val / ndf
print("chi2 = " + str(chi2_val))
print("ndf = " + str(ndf))
print("chi2/ndf = " + str(chi2_per_ndf))

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
c1.cd()
frame = m_kkpi.frame()

npar = combined_pdf.getParameters(dh).selectByAttrib("Constant", False).getSize()
# chi2ndf = frame.chiSquare(npar)

dh.plotOn(frame)
# draw_pdf(kstar_cut, frame, combined_pdf, '1285')
# combined_pdf.plotOn(frame, ROOT.RooFit.VisualizeError(fit_result), ROOT.RooFit.LineColor(ROOT.kRed))
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red'])))
pullHist = frame.pullHist()
npar = combined_pdf.getParameters(dh).selectByAttrib("Constant", False).getSize()
chi2ndf = frame.chiSquare(npar)
# fit_result.plotOn(frame, ROOT.RooAbsArg(voight), ROOT.RooFit.LineColor(ROOT.kRed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kGreen))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green'])), ROOT.RooFit.LineStyle(ROOT.kDashed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kBlue))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight_f1"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue'])))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight_eta"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['cyan'])))

frame.Draw()
c1.Update()

pullDist = ROOT.TH1I("pullDist", "pullDist", 3, 0, 3)
for i in range(0, pullHist.GetN()):
    pullDist.Fill(abs(pullHist.GetY()[i]))

ks_test_func = combined_pdf.createHistogram("ks_test_func", m_kkpi, ROOT.RooFit.Binning(1000))
ks_test_data = dh.createHistogram("ks_test_data", m_kkpi, ROOT.RooFit.Binning(1000))

kstest = ks_test_data.KolmogorovTest(ks_test_func)
# latex = ROOT.TLatex(); #prepare text in LaTeX format latex->SetTextSize(0.035);
# latex.SetNDC()
# latex.DrawLatex(0.25, 0.75, ROOT.Form("K-S test = %.2f", kstest)); 
print("K-S test = " + str(kstest))

"""
K-S test = 1 means very high probability of data coming from the 
distribution described by the model
"""
ks_test_data.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))


c2 = ROOT.TCanvas("c2", "c2", 800, 600)
c2.cd()
c2.Divide(3, 1)
c2.cd(1)
pullHist.Draw("AP")

y = 0.0

line= ROOT.TLine(frame.GetXaxis().GetXmin(), y, frame.GetXaxis().GetXmax(), y)
line.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw("same")
c2.cd(2)
pullDist.Draw()
c2.cd(3)
ks_test_data.Draw()
ks_test_func.Draw("same")
c2.Update()


print(f"f1 mass = {voight_m_f1.getVal() * 1000} +/- {voight_m_f1.getError() * 1000}")
print(f"f1 width = {voight_width_f1.getVal() * 1000} +/- {voight_width_f1.getError() * 1000}")
print(f"Fit X2/ndf = {chi2_per_ndf}")
print(f"second X2/ndf = {chi2ndf}")
print(f"f1 yield = {n_f1.getVal()} +/- {n_f1.getError()}")

input("Press enter to close")