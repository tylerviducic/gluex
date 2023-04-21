# to fit kkpi distributions with phasespace efficiency corrections for the K* cuts

import ROOT

data_filename = "/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_result_2018_spring.root"
flat_mc_filename = "/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_flat_result_flat_mass.root"

data_file = ROOT.TFile.Open(data_filename)
flat_mc_file = ROOT.TFile.Open(flat_mc_filename)

data_hist = data_file.Get("f1_kstar_all_cut")
# flat_mc_hist = flat_mc_file.Get("f1_kstar_all_cut")
efficiency_hist = flat_mc_file.Get("efficiency")

x = ROOT.RooRealVar("x", "x", 1.0, 1.7)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)
mch = ROOT.RooDataHist("mch", "mch", ROOT.RooArgList(x), efficiency_hist)
corrected_hist = data_hist.Clone()
corrected_hist.Divide(efficiency_hist.Clone())
ech = ROOT.RooDataHist("ech", "ech", ROOT.RooArgList(x), corrected_hist)
# corrected_hist.Draw()


# efficiency_pdf = ROOT.RooHistPdf("efficiency_pdf", "efficiency_pdf", ROOT.RooArgList(x), mch, 0)

# set up reletivistic breit-wigner with roofit
ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

m = ROOT.RooRealVar("m", "m", 1.285, 1.2, 1.325)
width = ROOT.RooRealVar("width", "width", 0.026, 0.01, 0.1)
# amplitude = ROOT.RooRealVar("amplitude", "amplitude", 0.0, 10000.0)

relbw = ROOT.RelBreitWigner("relbw", "relbw", x, m, width)

# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
# bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

# bkg = ROOT.RooChebychev("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1, 0.0, 10.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1, 0.0, 10.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", 1, 0.0, 10.0)

bkg = ROOT.RooBernstein("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

# mass_offse_var = ROOT.RooRealVar("mass_offset_var", "mass_offset_var", -1.1, -1.7)
# arg_par_mass_offset = ROOT.RooFormulaVar("arg_par_mass_offset", "mass_offset_var + x", ROOT.RooArgSet(mass_offse_var, x))
# arg_par_m0 = ROOT.RooRealVar("arg_par_m0", "arg_par_m0", 3.7)
# arg_par_c = ROOT.RooRealVar("arg_par_c", "arg_par_c", 3.0, 0.0, 10.0)
# arg_par_p = ROOT.RooRealVar("arg_par_p", "arg_par_p", 0.5, 0.0, 2.0)

# bkg = ROOT.RooArgusBG("bkg", "bkg", arg_par_mass_offset, arg_par_m0, arg_par_c, arg_par_p)

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.1, 0.9)
combined_pdf = ROOT.RooAddPdf("combined_pdf", "combined_pdf", ROOT.RooArgList(relbw, bkg), ROOT.RooArgList(sig_frac))
combined_pdf.fitTo(ech)
# eff_pdf = ROOT.RooEffProd("eff_pdf", "eff_pdf", combined_pdf, efficiency_pdf)
# eff_pdf.fitTo(dh)


frame = x.frame()
ech.plotOn(frame)
# mch.plotOn(frame, MarkerColor='b')
# mch.plotOn(frame, ROOT.RooFit.MarkerColor(ROOT.kRed))
combined_pdf.plotOn(frame)
combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kRed))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kGreen))

# eff_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
# eff_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kGreen))
# eff_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kBlue))
# efficiency_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kBlue))

frame.Draw()