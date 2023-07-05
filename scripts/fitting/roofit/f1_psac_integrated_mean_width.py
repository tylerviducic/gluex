# FIT KKPi INTEGRATED Distribution after phasespace acceptance correction for mean and width check

import ROOT
from common_analysis_tools import *
import os

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

channel = 'pipkmks'
# channel = 'pimkpks'

if channel == 'pipkmks' :
    all_cut = KSTAR_ALL_CUT_PIPKMKS
    voight_resoltion = F1_PIPKMKS_VOIGHT_SIGMA
elif channel == 'pimkpks' :
    all_cut = KSTAR_ALL_CUT_PIMKPKS
    voight_resoltion = F1_PIMKPKS_VOIGHT_SIGMA


def get_acceptance_corrected_kkpi(channel, run_period):

    data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data')
    data_df = ROOT.RDataFrame(data_file_and_tree[1], data_file_and_tree[0])

    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)


    recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])

    thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')

    data_df = data_df.Filter(all_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    recon_df = recon_df.Filter(all_cut).Filter(T_RANGE).Filter(BEAM_RANGE)

    data_hist = data_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', 150, 1.0, 2.5), f'{channel}_m').GetValue()
    recon_hist = recon_df.Histo1D((f'recon_hist_{run_period}', f'recon_hist_{run_period}', 150, 1.0, 2.5), f'{channel}_m').GetValue()
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

# ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

# relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
# relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.001, 0.1)

# set up a roofit voightian with a mean of 1.285, width of 0.024, and a sigma of 0.013
voight_m = ROOT.RooRealVar("voight_m", "voight_m", 1.285, 1.2, 1.3)
voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.024, 0.01, 0.075)
voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", voight_resoltion, 0.01, 0.5)
# voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", 0.0111726, 0.01, 0.5)
voight_sigma.setError(.000435994)
voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_m, voight_width, voight_sigma)

# hold the voight parameters fixed
# voight_m.setConstant(True)
# voight_width.setConstant(True)
voight_sigma.setConstant(True)

# relbw = ROOT.RelBreitWigner("relbw", "relbw", m_kkpi, relbw_m, relbw_width)

# bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.4, 1.43)
# bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.5)

# bw = ROOT.RooBreitWigner("1420", "1420", m_kkpi, bw_m, bw_width)

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

bkg = ROOT.RooChebychev("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4)) 


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

n_f1 = ROOT.RooRealVar("n_f1", "n_f1", 10000, 0.0, 1000000000)
n_bkg = ROOT.RooRealVar("n_bkg", "n_bkg", 10000, 0.0, 1000000000)

combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, bkg), ROOT.RooArgList(n_f1, n_bkg))

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
# fit_result = combined_pdf.fitTo(dh, ROOT.RooFit.Save())

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
chi2ndf = frame.chiSquare(npar)

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
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue'])))

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


print(f"f1 mass = {voight_m.getVal() * 1000} +/- {voight_m.getError() * 1000}")
print(f"f1 width = {voight_width.getVal() * 1000} +/- {voight_width.getError() * 1000}")
print(f"Fit X2/ndf = {chi2_per_ndf}")
print(f"second X2/ndf = {chi2ndf}")
print(f'f1 yield = {n_f1.getVal()} +/- {n_f1.getError()}')

input("Press enter to close")