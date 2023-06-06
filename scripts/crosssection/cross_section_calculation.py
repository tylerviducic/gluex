# calculation of f1(1285) cross section using pyroot

import ROOT
from common_analysis_tools import *
import pandas as pd


channel = 'pipkmks'
cut = 'all'

df = pd.read_csv('/work/halld/home/viducic/data/fit_params/pipkmks/binned_e_t_f1_mc_width.csv')
print(df)


for e in range(7, 11):
    for t in range(1, 8):
        hist = acceptance_correct_all_gluex_1_kkpi_data(channel, cut, e, t)

        m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.2, 1.5)
        dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), hist)

        voight_mean = ROOT.RooRealVar("voight_mean", "voight_mean", 1.281, 1.2, 1.3)
        voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.022, 0.01, 0.075)
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]
        print(e_t_sigma)
        voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", e_t_sigma, 0.001, 0.1)
        voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_mean, voight_width, voight_sigma)


