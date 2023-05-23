# script to get resolution of f1 to evaluate effectiveness of potential Ks constraint

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'
run_period = 'spring'

file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'signal')

# energy_cut = 'e_beam >= 8.0 && e_beam <= 10'
# t_cut = 'mand_t >= 0.1 && mand_t <= 0.5'
energy_cut = 'e_beam >= 6.5 && e_beam <= 10.5'
t_cut = 'mand_t >= 0.1 && mand_t <= 1.9'

df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)

recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])

thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')

hist = df.Filter(energy_cut).Filter(t_cut).Filter(KSTAR_ALL_CUT).Histo1D(('pipkmks', 'pipkmks', 30, 1.2, 1.5), 'pipkmks_m').GetValue()
hist.Sumw2()
recon_hist = recon_df.Histo1D(('recon_hist', 'recon_hist', 30, 1.2, 1.5), 'pipkmks_m')
recon_hist.Sumw2()

thrown_hist_name = channel + ';1'
thrown_hist = thrown_file.Get(thrown_hist_name)

thrown_hist.Sumw2()

acceptance_hist = recon_hist.Clone()
acceptance_hist.Divide(thrown_hist)

ac_data_hist = hist.Clone()
ac_data_hist.Divide(acceptance_hist)

m_kkpi = ROOT.RooRealVar('m_kkpi', 'm_kkpi', 1.0, 1.8)
mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.2, 1.3)
width = ROOT.RooRealVar('width', 'width', 0.023, 0.001, 0.1)
sigma = ROOT.RooRealVar('sigma', 'sigma', 0.025, 0.001, 0.1)

width.setConstant(ROOT.kTRUE)
mean.setConstant(ROOT.kTRUE)


dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), ac_data_hist)

func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
func.fitTo(dh)

frame = m_kkpi.frame()
dh.plotOn(frame)
func.plotOn(frame)

frame.Draw()

input('press enter to continue')
