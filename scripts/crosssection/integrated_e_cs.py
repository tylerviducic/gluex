import ROOT
import my_library.common_analysis_tools as tools
import my_library.kinematic_cuts as cuts
import my_library.constants as constants
import pandas as pd
import os
os.nice(18)
ROOT.EnableImplicitMT()

# channel = 'pipkmks'
channel = 'pimkpks'

x_min, x_max = 1.14, 1.52
n_bins = int((x_max - x_min) / 0.01)

fit_low, fit_high = 1.15, 1.51

beam_range = 'e_beam >= 7.5 && e_beam < 11.5'

data_hists = []
counts = []
cor_hists = []
funcs = []
t_bins = []
t_bin_widths = []
yields = []
yield_errors = []
cs_list = []
cs_errors = []
acceptances = []
acceptance_errors = []
t_bin_widths = []
t_bin_centers = []

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg par1', 'bkg par2', 'bkg par3']


res_df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_t_f1_mc_width.csv')

if channel == 'pipkmks' :
    v_mean = constants.F1_PIPKMKS_VOIGHT_MEAN
    v_width = constants.F1_PIPKMKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet
    f1_color = ROOT.kBlue
    # background_color = ROOT.kOrange
    background_color = total_fit_color
    hist_title = 'K^{-}K_{s}#pi^{+}'
    gaus_mean = constants.F1_PIPKMKS_GAUS_MEAN
    gaus_width = constants.F1_PIPKMKS_GAUS_WIDTH
    kstar_cut = cuts.KSTAR_ALL_CUT_PIPKMKS
elif channel == 'pimkpks' :
    v_mean = constants.F1_PIMKPKS_VOIGHT_MEAN
    v_width = constants.F1_PIMKPKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet +9
    f1_color = ROOT.kRed
    # background_color = ROOT.kTeal-5
    background_color = total_fit_color
    hist_title = 'K^{+}K_{s}#pi^{-}'
    gaus_mean = constants.F1_PIMKPKS_GAUS_MEAN
    gaus_width = constants.F1_PIMKPKS_GAUS_WIDTH
    kstar_cut = cuts.KSTAR_ALL_CUT_PIMKPKS 

guesses = {
    0: 10000, # voight amplitude
    1: v_mean, # voight mean
    3: v_width, # voight width
    4: 10000, # gaus amplitude
    5: gaus_mean, # gaus mean
    6: gaus_width, # gaus width
    7: 1, # bkg const
    8: -1, # bkg first order
    9: 1 # bkg second order
}

df_data = tools.get_dataframe(channel, 'gluex1', 'data').Filter(beam_range).Filter(kstar_cut)

df_spring = tools.get_dataframe(channel, 'spring', 'signal').Filter(beam_range)
df_fall = tools.get_dataframe(channel, 'fall', 'signal').Filter(beam_range)
df_2017 = tools.get_dataframe(channel, '2017', 'signal').Filter(beam_range)

df_spring_thrown = tools.get_dataframe(channel, 'spring', 'signal', filtered=False, thrown=True).Filter(beam_range)
df_fall_thrown = tools.get_dataframe(channel, 'fall', 'signal', filtered=False, thrown=True).Filter(beam_range)
df_2017_thrown = tools.get_dataframe(channel, '2017', 'signal', filtered=False, thrown=True).Filter(beam_range)

for t in range(1, 8):

    t_bin_centers.append((constants.T_CUT_DICT[t][1] - constants.T_WIDTH_DICT[t]/2))
    t_bin_widths.append(constants.T_WIDTH_DICT[t])

    e_t_sigma = res_df.loc[(res_df['t_bin']==t)]['sigma'].values[0]
    
    data_hists.append(df_data.Filter(cuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_{channel}_{t}', ';M(KK#Pi) [GeV];Counts/10 MeV', n_bins, x_min, x_max), f'{channel}_m'))
    counts.append(((df_spring.Filter(cuts.SELECT_T_BIN.format(t)).Count(), df_spring_thrown.Filter(cuts.SELECT_T_BIN.format(t)).Count()), \
                    (df_fall.Filter(cuts.SELECT_T_BIN.format(t)).Count(), df_fall_thrown.Filter(cuts.SELECT_T_BIN.format(t)).Count()), \
                    (df_2017.Filter(cuts.SELECT_T_BIN.format(t)).Count(), df_2017_thrown.Filter(cuts.SELECT_T_BIN.format(t)).Count())))

# for hist in data_hists:
#     hist.GetValue()
# for count in counts:
#     count[0][0].GetValue()
#     count[0][1].GetValue()
#     count[1][0].GetValue()
#     count[1][1].GetValue()
#     count[2][0].GetValue()
#     count[2][1].GetValue()
        

voigts = []
gauses = []
bkgs = []
chi2s = []

c = ROOT.TCanvas()
c.Divide(4, 2)

luminosity = tools.get_luminosity_gluex_1(7.5, 11.5)*1000
lum_spring = tools.get_luminosity('spring', 7.5, 11.5)*1000
lum_fall = tools.get_luminosity('fall', 7.5, 11.5)*1000
lum_2017 = tools.get_luminosity('2017', 7.5, 11.5)*1000

print(df_data.Count().GetValue())
print(df_spring.Count().GetValue())
print(df_fall.Count().GetValue())
print(df_2017.Count().GetValue())
print(df_spring_thrown.Count().GetValue())
print(df_fall_thrown.Count().GetValue())
print(df_2017_thrown.Count().GetValue())

for i, hist in enumerate(data_hists):
    c.cd(i + 1)
    # cor_hist = tools.correct_data_hist_for_kstar_efficiency(hist.GetValue())
    cor_hist = tools.correct_data_hist_for_kstar_efficiency(hist)
    cor_hists.append(cor_hist)

    func = ROOT.TF1(f'func_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', fit_low, fit_high)
    func.SetParameter(0, guesses[0])
    func.SetParLimits(0, 1, 10000000)
    func.FixParameter(1, guesses[1])
    func.FixParameter(2, e_t_sigma)
    func.FixParameter(3, guesses[3])
    func.SetParameter(4, guesses[4])
    func.SetParLimits(4, 1, 10000000) 
    func.FixParameter(5, guesses[5])
    func.FixParameter(6, guesses[6])
    func.SetParameter(7, guesses[7])
    func.SetParameter(8, guesses[8])
    func.SetParameter(9, guesses[9])
    func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

    result = hist.Fit(func, 'SRBE')
    func.SetLineColor(total_fit_color)
    funcs.append(func)

    chi2s.append(func.GetChisquare()/func.GetNDF())

    voight = ROOT.TF1(f'voight_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', fit_low, fit_high)
    voight.SetLineColor(ROOT.kBlack)
    voight.SetFillColor(f1_color)
    voight.SetFillStyle(1001)
    gaus = ROOT.TF1(f'gaus_{t}', 'gaus(0)', fit_low, fit_high)
    gaus.SetLineColor(background_color)
    gaus.SetLineStyle(3)
    bkg = ROOT.TF1(f'bkg_{t}', 'pol2(0)', fit_low, fit_high)
    # bkg = ROOT.TF1('bkg', '[0] + [1]*(x+1.15) + [2]*(x-1.15)*(x-1.15)', fit_low, fit_high)
    bkg.SetLineColor(background_color)
    bkg.SetLineStyle(2)

    guesses[4] = func.GetParameter(4)
    guesses[5] = func.GetParameter(5)
    guesses[6] = func.GetParameter(6)
    guesses[7] = func.GetParameter(7)
    guesses[8] = func.GetParameter(8)
    guesses[9] = func.GetParameter(9)

    voight.SetParameter(0, func.GetParameter(0))
    voight.SetParameter(1, func.GetParameter(1))
    voight.SetParameter(2, func.GetParameter(2))
    voight.SetParameter(3, func.GetParameter(3))
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))

    funcs.append(func)
    voigts.append(voight)
    gauses.append(gaus)
    bkgs.append(bkg)

    cor_hists[-1].Draw()
    funcs[-1].Draw('same')
    voigts[-1].Draw('same')
    bkgs[-1].Draw('same')
    gauses[-1].Draw('same')

    recon = (counts[i][0][0].GetValue() * lum_spring + counts[i][1][0].GetValue() * lum_fall + counts[i][2][0].GetValue() * lum_2017) / luminosity
    thrown = (counts[i][0][1].GetValue() * lum_spring + counts[i][1][1].GetValue() * lum_fall + counts[i][2][1].GetValue() * lum_2017) / luminosity

    acceptance = recon / thrown
    acceptance_error = 0

    f1_yield = voight.Integral(1.2, 1.5)/0.01
    # f1_yield_error = func.GetParError(0)/func.GetParameter(0) * f1_yield
    f1_yield_error = tools.calculate_rel_bootstrap_error(cor_hist, func, n_trials=1000) * f1_yield
    
    cross_section = tools.calculate_crosssection(f1_yield, acceptance, luminosity, constants.T_WIDTH_DICT[i+1], constants.F1_KKPI_BRANCHING_FRACTION)
    cross_section_error = tools.propogate_error_multiplication(cross_section, [f1_yield], [f1_yield_error])

    yields.append(f1_yield)
    yield_errors.append(f1_yield_error)
    cs_list.append(cross_section)
    cs_errors.append(cross_section_error)
    acceptances.append(acceptance)
    acceptance_errors.append(acceptance_error)

    c.Update()
    c.Draw()

    c.SaveAs(f'/work/halld/home/viducic/scripts/crosssection/plots/pol2_gaus_{channel}_all_e_t{i+1}_fit.png')
value_df = pd.DataFrame({'chi2ndf': chi2s, 'yield': yields, 'yield_error': yield_errors, 'acceptance': acceptances, 'acceptance_error': acceptance_errors,'cross_section': cs_list, 'cross_section_error': cs_errors, 't_bin_middle': t_bin_centers, 't_bin_width': t_bin_widths})
value_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/tf1_all_e_binned_t_values.csv', index=False)

input('Press Enter to continue...')

