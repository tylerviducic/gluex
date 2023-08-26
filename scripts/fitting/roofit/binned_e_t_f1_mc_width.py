# fit KKPi in E and t bins for cross section to get the width used in the fits to data

import ROOT 
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import numpy as np
import pandas as pd

channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks':
#     voight_mean = ct.F1_PIPKMKS_VOIGHT_MEAN
#     voight_mean_error = ct.F1_PIPKMKS_VOIGHT_MEAN_ERROR
#     voight_width = ct.F1_PIPKMKS_VOIGHT_WIDTH
#     voight_width_error = ct.F1_PIPKMKS_VOIGHT_WIDTH_ERROR
    voight_resolution = constants.F1_PIPKMKS_VOIGHT_SIGMA
elif channel == 'pimkpks':
#     voight_mean = ct.F1_PIMKPKS_VOIGHT_MEAN
#     voight_mean_error = ct.F1_PIMKPKS_VOIGHT_MEAN_ERROR
#     voight_width = ct.F1_PIMKPKS_VOIGHT_WIDTH
#     voight_width_error = ct.F1_PIMKPKS_VOIGHT_WIDTH_ERROR
    voight_resolution = constants.F1_PIMKPKS_VOIGHT_SIGMA

chi2_ndf_list = []
sigma_list = []
sigma_err_list = []
energy_list = []
t_bin_list = []

c1 = ROOT.TCanvas()
c1.Divide(4, 2)

for e in range(7, 12):
    for t in range(1, 8):
        c1.cd(t)
        signal_mc_hist = ct.get_gluex1_binned_signal_mc_hist_for_resoltion_fitting(channel, e, t)

        m_kkpi = ROOT.RooRealVar('m_kkpi', 'm_kkpi', 1.2, 1.5)
        range_min = 1.22
        range_max = 1.35
        m_kkpi.setRange("fit_range", range_min, range_max)
        mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.283, 1.287)
        width = ROOT.RooRealVar('width', 'width', 0.022, 0.001, 0.1)
        sigma = ROOT.RooRealVar('sigma', 'sigma', voight_resolution, 0.001, 0.1)

        width.setConstant(ROOT.kTRUE)
        # mean.setConstant(ROOT.kTRUE)

        dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), signal_mc_hist)

        func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
        chi2_var = func.createChi2(dh)
        # fit_result = func.chi2FitTo(dh, ROOT.RooFit.Save())
        fit_result = func.fitTo(dh, ROOT.RooFit.Save())

        chi2_val = chi2_var.getVal()
        n_bins = signal_mc_hist.GetXaxis().FindBin(range_max) - signal_mc_hist.GetXaxis().FindBin(range_min)
        ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
        chi2_per_ndf = chi2_val / ndf

        frame = m_kkpi.frame()
        title = ct.get_binned_kkpi_hist_title(channel, e, t)
        frame.SetTitle(title)
        frame.GetXaxis().SetTitle(title.split(' ')[0] + ' (GeV)')
        dh.plotOn(frame)
        func.plotOn(frame)
        chi2_ndf_list.append(chi2_per_ndf)
        sigma_list.append(sigma.getVal())
        sigma_err_list.append(sigma.getError())
        energy_list.append(e)
        t_bin_list.append(t)

        frame.Draw()
    c1.Update()
    c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/binned_resolution_fits/{channel}_binned_resolution_fits_beam_{e}.png')

# create a pandas dataframe from the lists in this script
df = pd.DataFrame({'chi2_ndf': chi2_ndf_list, 'sigma': sigma_list, 'sigma_err': sigma_err_list, 'energy': energy_list, 't_bin': t_bin_list})
#write that dataframe to a csv file without the index column
df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv', index=False)


input('Press enter to continue...')


    
