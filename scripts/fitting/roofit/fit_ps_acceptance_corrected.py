# FIT KKPi Distribution after phasespace acceptance correction 

import ROOT
from common_analysis_tools import *


channel = 'pipkmks'
run_period = 'spring'
datatype = 'data'


beam = 9
kstar_cut = 'plus'
t_bin = 3
beam_range = f'{beam - 0.5}_{beam+0.5}'

data_file_and_tree = get_flat_file_and_tree(channel, run_period, datatype, filtered=False, hist=True)
data_file = ROOT.TFile.Open(data_file_and_tree[0], 'READ')

recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace', filtered=False, hist=True)
thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
print(recon_phasespace_file_and_tree[0])
input('please exit now')

recon_file = ROOT.TFile.Open(recon_phasespace_file_and_tree[0], 'READ')
thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')


data_hist_name = channel + '_cut_kstar_' + kstar_cut + '_cut_beam_' + beam_range+ f'_t_{t_bin_dict[t_bin]}' +';1'
data_hist = data_file.Get(data_hist_name)
recon_hist = recon_file.Get(data_hist_name)

thrown_hist_name = channel + '_beam_' + beam_range + f'_t_{t_bin_dict[t_bin]}' +';1'
thrown_hist = thrown_file.Get(thrown_hist_name)

acceptance_hist = recon_hist.Clone()
acceptance_hist.Divide(thrown_hist)

ac_data_hist = data_hist.Clone()
ac_data_hist.Divide(acceptance_hist)

c = ROOT.TCanvas()
c.Divide(2,1)
c.cd(1)
# data_hist.Draw()
recon_hist.Draw()
c.cd(2)
# ac_data_hist.Draw()
thrown_hist.Draw()
c.Update()

input('Press enter to continue...')

x = ROOT.RooRealVar("x", "x", 1.2, 1.8)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), ac_data_hist)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.01, 0.03)

relbw = ROOT.RelBreitWigner("relbw", "relbw", x, relbw_m, relbw_width)

bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.35, 1.5)
bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.1)

bw = ROOT.RooBreitWigner("bw", "bw", x, bw_m, bw_width)

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

bkg = ROOT.RooChebychev("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

## COMBINED PDF ##
bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.1, 0.9)
sig_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.1, 0.9)
bkg_pdf = ROOT.RooAddPdf("bkg_pdf", "bkg_pdf", ROOT.RooArgList(bkg, bw), ROOT.RooArgList(bkg_frac))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.1, 0.9)
combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(relbw, bkg_pdf), ROOT.RooArgList(sig_frac))

# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
combined_pdf.fitTo(dh)

frame = x.frame()
dh.plotOn(frame)
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))

frame.Draw()

input('Press enter to continue...')