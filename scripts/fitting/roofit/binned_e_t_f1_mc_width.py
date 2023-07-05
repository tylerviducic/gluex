# fit KKPi in E and t bins for cross section to get the width used in the fits to data

import ROOT 
from common_analysis_tools import *
import numpy as np
import pandas as pd

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

beam_energy = 10

chi2_ndf_list = []
sigma_list = []
sigma_err_list = []
energy_list = []
t_bin_list = []

c1 = ROOT.TCanvas()
c1.Divide(7, 4)

for e in range(7, 11):
    for i in range(1, 8):
        c1.cd(i + 7 * (e - 7))
        ac_signal_hist_total = accepptance_correct_all_gluex1_kkpi_signal(channel, cut, e, i)

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

        frame = m_kkpi.frame()
        dh.plotOn(frame)
        func.plotOn(frame)
        npar = func.getParameters(dh).selectByAttrib("Constant", False).getSize()
        chi2ndf = frame.chiSquare(npar)
        chi2_ndf_list.append(chi2ndf)
        sigma_list.append(sigma.getVal())
        sigma_err_list.append(sigma.getError())
        energy_list.append(e)
        t_bin_list.append(i)

        frame.Draw()
        c1.Update()

# create a pandas dataframe from the lists in this script
df = pd.DataFrame({'chi2_ndf': chi2_ndf_list, 'sigma': sigma_list, 'sigma_err': sigma_err_list, 'energy': energy_list, 't_bin': t_bin_list})
#write that dataframe to a csv file without the index column
df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv', index=False)


input('Press enter to continue...')


    
