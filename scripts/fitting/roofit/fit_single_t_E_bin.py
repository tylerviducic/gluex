# fit single t/E bin for moskov 

import ROOT

data_filename = "/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_result_2018_spring.root"
data_file = ROOT.TFile.Open(data_filename)

data_hist = data_file.Get("pipkmks_beam_8_t_0.4_kstar_all_cut;1")

x = ROOT.RooRealVar("x", "x", 1.0, 1.7)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)

x.setRange("signal", 1.19, 1.45)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

m = ROOT.RooRealVar("m", "m", 1.285, 1.2, 1.325)
width = ROOT.RooRealVar("width", "width", 0.026, 0.02, 0.04)
# amplitude = ROOT.RooRealVar("amplitude", "amplitude", 0.0, 10000.0)

# relbw = ROOT.RelBW("relbw", "relbw", x, amplitude, m, width)
# bw = ROOT.RooBreitWigner("bw", "bw", x, m, width)
bw = ROOT.RelBreitWigner("bw", "bw", x, m, width)

## ROO POLYNOMIAL ##
bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

# bkg = ROOT.RooPolynomial("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4))
bkg = ROOT.RooChebychev("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4))

## ROO BERSTEIN ##
# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1, -0.10, 10.0)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1, -0.10, 10.0)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", 1, -0.10, 10.0)
# bkg_par4 = ROOT.RooRealVar("bkg_par3", "bkg_par3", 1, -0.10, 10.0)

# bkg = ROOT.RooBernstein("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)

composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(bw, bkg), ROOT.RooArgList(sig_frac))
composite.fitTo(dh, ROOT.RooFit.Range("signal"))

frame = x.frame()
dh.plotOn(frame)
composite.plotOn(frame)
composite.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kGreen))
composite.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kRed))

frame.Draw()
input("Press enter to continue...")
