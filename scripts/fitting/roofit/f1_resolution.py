# script to get resolution of f1 to evaluate effectiveness of potential Ks constraint

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'

def get_acceptance_corrected_signal_mc(channel, run_period):
    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    signal_df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
    recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])
    thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')

    signal_df = signal_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)
    recon_df = recon_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)

    signal_hist = signal_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', 90, 1.2, 1.5), 'pipkmks_m').GetValue()
    recon_hist = recon_df.Histo1D((f'recon_hist_{run_period}', f'recon_hist_{run_period}', 90, 1.2, 1.5), 'pipkmks_m').GetValue()
    thrown_hist_name = channel + '_f1_res;1'
    thrown_hist = thrown_file.Get(thrown_hist_name)

    signal_hist.Sumw2()
    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)

    ac_signal_hist = signal_hist.Clone()
    ac_signal_hist.Divide(acceptance_hist)
    ac_signal_hist.SetDirectory(0)

    c = ROOT.TCanvas()
    c.Divide(2, 2)
    c.cd(1)
    signal_hist.Draw()
    c.cd(2)
    recon_hist.Draw()
    c.cd(3)
    acceptance_hist.Draw()
    c.cd(4)
    ac_signal_hist.Draw()
    c.Update()
    input('press enter to continue')
    c.Clear()
    return ac_signal_hist

ac_signal_hist_spring = get_acceptance_corrected_signal_mc(channel, 'spring')
ac_signal_hist_fall = get_acceptance_corrected_signal_mc(channel, 'fall')
ac_signal_hist_2017 = get_acceptance_corrected_signal_mc(channel, '2017')

ac_signal_hist_total = ac_signal_hist_spring.Clone()
ac_signal_hist_total.Add(ac_signal_hist_fall)
ac_signal_hist_total.Add(ac_signal_hist_2017)


m_kkpi = ROOT.RooRealVar('m_kkpi', 'm_kkpi', 1.2, 1.5)
mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.2, 1.3)
width = ROOT.RooRealVar('width', 'width', 0.023, 0.001, 0.1)
sigma = ROOT.RooRealVar('sigma', 'sigma', 0.025, 0.001, 0.1)

width.setConstant(ROOT.kTRUE)
mean.setConstant(ROOT.kTRUE)


dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), ac_signal_hist_total)

func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
chi2_var = func.createChi2(dh)
fit_result = func.chi2FitTo(dh, ROOT.RooFit.Save())

chi2_val = chi2_var.getVal()
n_bins = ac_signal_hist_total.GetNbinsX()
print("n_bins = " + str(n_bins))
ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
chi2_per_ndf = chi2_val / ndf
print("chi2 = " + str(chi2_val))
print("ndf = " + str(ndf))
print("chi2/ndf = " + str(chi2_per_ndf))


frame = m_kkpi.frame()
dh.plotOn(frame)
func.plotOn(frame)
npar = func.getParameters(dh).selectByAttrib("Constant", False).getSize()
chi2ndf = frame.chiSquare(npar)


frame.Draw()

input('press enter to continue')

print(f'chi2ndf: {chi2ndf}')
