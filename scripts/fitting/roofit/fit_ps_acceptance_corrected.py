# FIT KKPi Distribution after phasespace acceptance correction 

import ROOT
from common_analysis_tools import *


channel = 'pipkmks'
run_period = 'spring'
datatype = 'data'


beam = 9
kstar_cut = 'all'
t_bin = 3
beam_range = f'{beam - 0.5}_{beam+0.5}'

data_file_and_tree = get_flat_file_and_tree(channel, run_period, datatype, filtered=False, hist=True)
data_file = ROOT.TFile.Open(data_file_and_tree[0], 'READ')

recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace', filtered=False, hist=True)
thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
print(recon_phasespace_file_and_tree[0])


recon_file = ROOT.TFile.Open(recon_phasespace_file_and_tree[0], 'READ')
thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')


data_hist_name = channel + '_cut_kstar_' + kstar_cut + '_cut_beam_' + beam_range+ f'_t_{t_bin_dict[t_bin]}' +';1'
print(data_hist_name)
data_hist = data_file.Get(data_hist_name)
recon_hist = recon_file.Get(data_hist_name)

data_hist.Sumw2()
recon_hist.Sumw2()

thrown_hist_name = channel + '_beam_' + beam_range + f'_t_{t_bin_dict[t_bin]}' +';1'
thrown_hist = thrown_file.Get(thrown_hist_name)
thrown_hist.Sumw2()

acceptance_hist = recon_hist.Clone()
acceptance_hist.Divide(thrown_hist)


ac_data_hist = data_hist.Clone()
ac_data_hist.Divide(acceptance_hist)

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

m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.2, 1.5)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), ac_data_hist)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.001, 0.1)

# set up a roofit voightian with a mean of 1.285, width of 0.024, and a sigma of 0.013
voight_m = ROOT.RooRealVar("voight_m", "voight_m", 1.285, 1.2, 1.3)
voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.024, 0.01, 0.075)
voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", 0.013, 0.001, 0.5)
voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_m, voight_width, voight_sigma)

# hold the voight parameters fixed
# voight_m.setConstant(True)
# voight_width.setConstant(True)
# voight_sigma.setConstant(True)

relbw = ROOT.RelBreitWigner("relbw", "relbw", m_kkpi, relbw_m, relbw_width)

bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.4, 1.43)
bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.5)

bw = ROOT.RooBreitWigner("1420", "1420", m_kkpi, bw_m, bw_width)

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

# bkg = ROOT.RooBernstein("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

## POLYNOMIAL ##
# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -100, 100)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -100, 100)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -100, 100)
# bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -100, 100)

# bkg = ROOT.RooPolynomial("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4))


# def assemble_pdf(cut, func_1285, func_1420, func_bkg):
#     print(func_1285.getVal('voight_m'))
#     if cut == 'all':
#         sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
#         combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(func_1285, func_bkg), ROOT.RooArgList(sig_frac))
#     else:
#         bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)
#         sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
#         combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(func_1285, func_bkg, func_1420), ROOT.RooArgList(sig_frac, bkg_frac))
#     return combined_pdf

# def draw_pdf(cut, frame, combined_pdf, sig_func_name):
#     combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
#     combined_pdf.plotOn(frame, ROOT.RooFit.Components(sig_func_name), ROOT.RooFit.LineColor(ROOT.kBlue))
#     if cut != 'all':
#         combined_pdf.plotOn(frame, ROOT.RooFit.Components('1420'), ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineStyle(ROOT.kDashed))
#     combined_pdf.plotOn(frame, ROOT.RooFit.Components('bkg'), ROOT.RooFit.LineColor(ROOT.kGreen))
#     return
        
# 
# combined_pdf = assemble_pdf(kstar_cut, voight, bw, bkg)
## COMBINED PDF ##
bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.0, 1.0)
bkg_pdf = ROOT.RooAddPdf("bkg_pdf", "bkg_pdf", ROOT.RooArgList(bkg, bw), ROOT.RooArgList(bkg_frac))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)
# # combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(relbw, bkg_pdf), ROOT.RooArgList(sig_frac))
combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, bkg_pdf), ROOT.RooArgList(sig_frac))

# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
# combined_pdf.fitTo(dh)
combined_pdf.chi2FitTo(dh)

frame = m_kkpi.frame()
dh.plotOn(frame)
# draw_pdf(kstar_cut, frame, combined_pdf, '1285')
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kGreen))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineStyle(ROOT.kDashed))
# combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kBlue))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(ROOT.kBlue))

frame.Draw()

input('Press enter to continue...')