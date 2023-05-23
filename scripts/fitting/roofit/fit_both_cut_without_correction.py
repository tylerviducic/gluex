# FIT KKPi INTEGRATED Distribution without corrections

import ROOT
from common_analysis_tools import *
import os

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

channel = 'pipkmks'
run_period = 'spring'

data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data')
data_df = ROOT.RDataFrame(data_file_and_tree[1], data_file_and_tree[0])


kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'
data_df = data_df.Filter(kstar_all_cut)


data_hist = data_df.Histo1D(('data_hist', 'data_hist', 50, 1.2, 1.7), 'pipkmks_m').GetValue()


data_hist.Sumw2()


# c = ROOT.TCanvas()
# c.Divide(2,2)
# c.cd(1)
# data_hist.Draw()
# c.cd(2)
# ac_data_hist.Draw()
# c.cd(3)
# thrown_hist.SetLineColor(ROOT.kRed)
# thrown_hist.Draw('hist')
# recon_hist.Draw('same hist')
# c.cd(4)
# acceptance_hist.Draw('hist')
# c.Update()

# input('Press enter to continue...')

m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.2, 1.7)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), data_hist)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.001, 0.1)

# set up a roofit voightian with a mean of 1.285, width of 0.024, and a sigma of 0.013
voight_m = ROOT.RooRealVar("voight_m", "voight_m", 1.285, 1.2, 1.3)
voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.024, 0.01, 0.075)
voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", 0.012456, 0.01, 0.5)
voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_m, voight_width, voight_sigma)

# hold the voight parameters fixed
# voight_m.setConstant(True)
# voight_width.setConstant(True)
voight_sigma.setConstant(True)

relbw = ROOT.RelBreitWigner("relbw", "relbw", m_kkpi, relbw_m, relbw_width)

# bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.4, 1.43)
# bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.5)

# bw = ROOT.RooBreitWigner("1420", "1420", m_kkpi, bw_m, bw_width)

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

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

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
# # combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(relbw, bkg_pdf), ROOT.RooArgList(sig_frac))
combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, bkg), ROOT.RooArgList(sig_frac))

chi2_var = combined_pdf.createChi2(dh)


# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
# combined_pdf.fitTo(dh)
fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Save())

chi2_val = chi2_var.getVal()
n_bins = data_hist.GetNbinsX()
ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
chi2_per_ndf = chi2_val / ndf
print("chi2 = " + str(chi2_val))
print("ndf = " + str(ndf))
print("chi2/ndf = " + str(chi2_per_ndf))

frame = m_kkpi.frame()
dh.plotOn(frame)
# draw_pdf(kstar_cut, frame, combined_pdf, '1285')
# combined_pdf.plotOn(frame, ROOT.RooFit.VisualizeError(fit_result), ROOT.RooFit.LineColor(ROOT.kRed))
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red'])))
# fit_result.plotOn(frame, ROOT.RooAbsArg(voight), ROOT.RooFit.LineColor(ROOT.kRed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kGreen))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green'])), ROOT.RooFit.LineStyle(ROOT.kDashed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kBlue))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue'])))

frame.Draw()

input('Press enter to continue...')