import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks' :
    v_mean = constants.F1_PIPKMKS_VOIGHT_MEAN
    v_width = constants.F1_PIPKMKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet
    f1_color = ROOT.kBlue
    # background_color = ROOT.kOrange
    background_color = total_fit_color
    hist_title = 'K^{-}K_{s}#pi^{+}'
    gaus_mean = 1.371
    gaus_width = 0.0333
elif channel == 'pimkpks' :
    v_mean = constants.F1_PIMKPKS_VOIGHT_MEAN
    v_width = constants.F1_PIMKPKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet +9
    f1_color = ROOT.kRed
    # background_color = ROOT.kTeal-5
    background_color = total_fit_color
    hist_title = 'K^{+}K_{s}#pi^{-}'
    gaus_mean = 1.360
    # gaus_width = 0.0463
    gaus_width = 0.0333

df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv')

mean_list = []
mean_error_list = []
width_list = []
width_error_list = []
chi2ndf_list = []
ks_test_list = []
data_yield_list = []
yield_error_list = []
acceptance_list = []
acceptance_error_list = []
bin_width_list = []
cross_section_list = []
cross_section_error_list = []
t_bin_list = []
t_bin_width_list = []
energy_bin_list = []
luminosity_list = []

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg par1', 'bkg par2', 'bkg par3']

c = ROOT.TCanvas('c', 'c', 1000, 1000)

for e in range(8, 12):
    c.Clear()
    c.Divide(4, 2)
    luminosity = ct.get_luminosity_gluex_1(e-0.5, e+0.5)*1000
    hists=[]
    funcs = []
    bkgs = []
    voigts = []
    gauses = []

    initial_guesses = {
        0: 10,
        1: v_mean, 
        3: v_width,
        4: 1,
        5: gaus_mean,
        6: gaus_width,
        7: 1000,
        8: 1000,
        9: -1000
    }
    
    for t in range(1, 8):
        c.cd(t)
        cor_hist = ct.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist = ct.remove_zero_datapoints(cor_hist)

        hist.GetXaxis().SetRangeUser(1.18, 1.52)
        hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)

        hist.GetXaxis().SetTitle(hist_title + ' (GeV)')
        hist.GetXaxis().SetTitleSize(0.055)
        hist.GetYaxis().SetTitle('Counts/10 MeV')

        hist.SetTitle('E_{#gamma} = ' + str(e) + ' GeV || ' + f'{constants.T_CUT_DICT[t][0]} < -t < {constants.T_CUT_DICT[t][1]}' + ' GeV^{2}')
        hist.SetTitleSize(0.055)

        hists.append(hist)


        func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.2, 1.5)
        
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]

        func.SetParameter(0, initial_guesses[0])
        func.SetParLimits(0, 1, 10000)
        func.FixParameter(1, initial_guesses[1])
        # func.SetParLimits(1, 1.26, 1.3)
        func.FixParameter(2, e_t_sigma)
        func.FixParameter(3, initial_guesses[3])
        # func.SetParLimits(3, 0.005, 0.05)
        func.SetParameter(4, initial_guesses[4])
        func.SetParLimits(4, 0, 100)
        # func.SetParameter(5, initial_guesses[5])
        func.FixParameter(5, initial_guesses[5])
        # func.SetParLimits(5, 1.35, 1.4)
        func.FixParameter(6, initial_guesses[6])
        # func.SetParameter(6, initial_guesses[6])
        # func.SetParLimits(6, 0.025, 0.05)
        func.SetParameter(7, initial_guesses[4])
        func.SetParameter(8, initial_guesses[5])
        func.SetParLimits(8, 0, 100000)
        func.SetParameter(9, initial_guesses[6])
        func.SetParLimits(9, -100000, 100000)

        func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

        result = hist.Fit(func, 'SRB')
        func.SetLineColor(total_fit_color)

        voight = ROOT.TF1(f'voight_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.2, 1.5)
        voight.SetLineColor(ROOT.kBlack)
        voight.SetFillColor(f1_color)
        voight.SetFillStyle(1001)
        gaus = ROOT.TF1('gaus', 'gaus(0)', 1.2, 1.5)
        gaus.SetLineColor(background_color)
        gaus.SetLineStyle(3)
        bkg = ROOT.TF1('bkg', 'pol2(0)', 1.2, 1.5)
        bkg.SetLineColor(background_color)
        bkg.SetLineStyle(2)

        initial_guesses[4] = func.GetParameter(4)
        initial_guesses[5] = func.GetParameter(5)
        initial_guesses[6] = func.GetParameter(6)
        initial_guesses[7] = func.GetParameter(7)
        initial_guesses[8] = func.GetParameter(8)
        initial_guesses[9] = func.GetParameter(9)


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

        hists[t-1].Draw()
        funcs[t-1].Draw('same')
        voigts[t-1].Draw('same')
        bkgs[t-1].Draw('same')
        gauses[t-1].Draw('same')

        f1_yield = voight.Integral(1.2, 1.5)/0.01
        f1_yield_error = func.GetParError(0)/func.GetParameter(0) * f1_yield
        acceptance, acceptance_error = ct.get_binned_gluex1_signal_acceptance(channel, e, t)
        cross_section = ct.calculate_crosssection(f1_yield, acceptance, luminosity, constants.T_WIDTH_DICT[t], constants.F1_KKPI_BRANCHING_FRACTION)
        cross_section_error = ct.propogate_error_multiplication(cross_section, [f1_yield, acceptance, luminosity, constants.F1_KKPI_BRANCHING_FRACTION], [f1_yield_error, acceptance_error, luminosity * 0.05, constants.F1_KKPI_BRANCHING_FRACTION_ERROR])

        mean_list.append(func.GetParameter(1))
        mean_error_list.append(func.GetParError(1))
        width_list.append(func.GetParameter(3))
        width_error_list.append(func.GetParError(3))
        chi2ndf_list.append(func.GetChisquare()/func.GetNDF())
        # ks_test_list.append(func.KolmogorovTest(hist))
        data_yield_list.append(f1_yield)
        yield_error_list.append(f1_yield_error)
        acceptance_list.append(acceptance)
        acceptance_error_list.append(acceptance_error)
        cross_section_list.append(cross_section)
        cross_section_error_list.append(cross_section_error)
        t_bin_list.append((constants.T_CUT_DICT[t][0] + constants.T_CUT_DICT[t][1])/2.0)
        t_bin_width_list.append(constants.T_WIDTH_DICT[t]/2.0)
        energy_bin_list.append(e)
        luminosity_list.append(luminosity)
        

        c.Update()

    c.SaveAs(f'/work/halld/home/viducic/scripts/crosssection/plots/pol2_gaus_{channel}_e{e}_t{t}_fit.png')

value_df = pd.DataFrame({'mean': mean_list, 'mean_error': mean_error_list, 'width': width_list, 'width_error': width_error_list, 'chi2ndf': chi2ndf_list, 'yield': data_yield_list, 'yield_error': yield_error_list, 'acceptance': acceptance_list, 'acceptance_error': acceptance_error_list,'cross_section': cross_section_list, 'cross_section_error': cross_section_error_list, 't_bin_middle': t_bin_list, 't_bin_width': t_bin_width_list, 'beam_energy': energy_bin_list, 'luminosity': luminosity_list})
value_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/tf1_gaus_cross_section_values.csv', index=False)