import ROOT 
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd

channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'

voight_resolution = constants.F1_PIPKMKS_VOIGHT_SIGMA

chi2_ndf_list = []
sigma_list = []
sigma_err_list = []
energy_list = []
t_bin_list = []
func_list = []
hist_list = []

c1 = ROOT.TCanvas()
c1.Divide(4, 2)

for e in range(7, 12):
    for t in range(1,8):
        c1.cd(t)
        t_bin_list.append(t)
        energy_list.append(e)
        signal_mc_hist = ct.get_gluex1_binned_signal_mc_hist_for_resoltion_fitting(channel, e, t)

        func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.15, 1.4)
        func.FixParameter(1, 1.285)
        func.SetParameter(2, voight_resolution)
        func.FixParameter(3, 0.022)

        signal_mc_hist.Fit(func, 'RQ')

        chi2_per_ndf = func.GetChisquare() / func.GetNDF()
        resolution = func.GetParameter(2)
        resolution_error = func.GetParError(2)

        chi2_ndf_list.append(chi2_per_ndf)
        sigma_list.append(resolution)
        sigma_err_list.append(resolution_error)

        hist_list.append(signal_mc_hist)
        func_list.append(func)

        hist_list[-1].Draw()
        func_list[-1].Draw('same')

    c1.Update()
    c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/binned_resolution_fits/{channel}_binned_resolution_fits_beam_{e}.png')

    df = pd.DataFrame({'chi2_ndf': chi2_ndf_list, 'sigma': sigma_list, 'sigma_err': sigma_err_list, 'energy': energy_list, 't_bin': t_bin_list})
    # write that dataframe to a csv file without the index column
    df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv', index=False)
        
        
