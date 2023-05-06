# script to test width of kshort

import ROOT

data_filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_result_2018_spring.root'

data_file = ROOT.TFile.Open(data_filename, "READ")

data_hist = data_file.Get('ks_m')

x = ROOT.RooRealVar("x", "x", 0.3, 0.7)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)

x.setRange("signal", 0.45, 0.55)

ks_mean = ROOT.RooRealVar("mean", "mean", 0.5, 0.475, 0.515)
ks_sigma = ROOT.RooRealVar("sigma", "sigma", 0.01, 0.004, 0.02)

# ks_mean.setConstant(1)
# ks_sigma.setConstant(1)
gaus = ROOT.RooGaussian("gaus", "gaus", x, ks_mean, ks_sigma)
# gaus.fitTo(dh, ROOT.RooFit.Range("signal"))
# gaus.fitTo(dh, ROOT.RooFit.SumCoefRange("signal"))

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 0.0, -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 0.0, -1.0, 1.0)
bkg = ROOT.RooPolynomial("bkg", "bkg", x, ROOT.RooArgList(bkg_par1))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)

composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(gaus, bkg), ROOT.RooArgList(sig_frac))
composite.fitTo(dh)

frame = x.frame()
dh.plotOn(frame)
composite.plotOn(frame)

frame.Draw()