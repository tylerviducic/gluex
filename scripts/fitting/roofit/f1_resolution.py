# script to get resolution of f1 to evaluate effectiveness of potential Ks constraint

import ROOT
from common_analysis_tools import *


#TODO apply all cuts to MC annd fit f1 signal to get width. it (should???) will be a breit-wigner

file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'signal')

energy_cut = 'e_beam >= 6.5 && e_beam <= 10.5'
t_cut = 'mand_t >= 0.1 && mand_t <= 1.9'

df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

hist = df.Filter(energy_cut).Filter(t_cut).Histo1D(('pipkmks', 'pipkmks', 200, 1.15, 1.45), 'pipkmks_m').GetValue()

m_kkpi = ROOT.RooRealVar('m_kkpi', 'm_kkpi', 1.0, 1.8)
mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.2, 1.3)
width = ROOT.RooRealVar('width', 'width', 0.025, 0.001, 0.1)
sigma = ROOT.RooRealVar('sigma', 'sigma', 0.025, 0.001, 0.1)

dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), hist)

func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
func.fitTo(dh)

frame = m_kkpi.frame()
dh.plotOn(frame)
func.plotOn(frame)

frame.Draw()

input('press enter to continue')
