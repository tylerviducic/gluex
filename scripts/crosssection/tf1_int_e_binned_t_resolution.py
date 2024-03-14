import ROOT 
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as cuts
import pandas as pd
import os

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

voight_resolution = constants.F1_PIPKMKS_VOIGHT_SIGMA

ROOT.EnableImplicitMT()
os.nice(18)

chi2_ndf_list = []
sigma_list = []
sigma_err_list = []
t_bin_list = []
func_list = []
hist_list = []

c1 = ROOT.TCanvas()
c1.Divide(4, 2)

df_spring = tools.get_dataframe(channel, 'spring', 'signal').Filter(cuts.BEAM_RANGE)
df_fall = tools.get_dataframe(channel, 'fall', 'signal').Filter(cuts.BEAM_RANGE)
df_2017 = tools.get_dataframe(channel, '2017', 'signal').Filter(cuts.BEAM_RANGE)

hists = []

for t in range(1, 8):
    hist_spring = df_spring.Filter(cuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_spring_{channel}_{t}', ';M(KK#Pi) [GeV];Counts/10 MeV', 500, 1.15, 1.4), f'{channel}_m')
    hist_fall = df_fall.Filter(cuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_fall_{channel}_{t}', ';M(KK#Pi) [GeV];Counts/10 MeV', 500, 1.15, 1.4), f'{channel}_m')
    hist_2017 = df_2017.Filter(cuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_2017_{channel}_{t}', ';M(KK#Pi) [GeV];Counts/10 MeV', 500, 1.15, 1.4), f'{channel}_m')

    hists.append((hist_spring, hist_fall, hist_2017))

for i, hist in enumerate(hists):
    c1.cd(i + 1)
    hist_total = tools.weight_histograms_by_flux(hist[0].GetValue(), hist[1].GetValue(), hist[2].GetValue())
    func = ROOT.TF1(f'func_{i+1}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.15, 1.4)
    func.FixParameter(1, 1.285)
    func.SetParameter(2, voight_resolution)
    func.FixParameter(3, 0.022)

    hist_total.Fit(func, 'RQ')

    chi2_per_ndf = func.GetChisquare() / func.GetNDF()
    resolution = func.GetParameter(2)
    resolution_error = func.GetParError(2)

    chi2_ndf_list.append(chi2_per_ndf)
    sigma_list.append(resolution)
    sigma_err_list.append(resolution_error)
    t_bin_list.append(i + 1)
    hist_list.append(hist_total)
    func_list.append(func)

    hist_list[-1].Draw()
    func_list[-1].Draw('same')

    c1.Update()

df = pd.DataFrame({'chi2_ndf': chi2_ndf_list, 'sigma': sigma_list, 'sigma_err': sigma_err_list, 't_bin': t_bin_list})
df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_t_f1_mc_width.csv', index=False)

input('Press enter to continue...')
    


