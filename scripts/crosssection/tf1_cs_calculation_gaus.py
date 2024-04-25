import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd

# ROOT.Math.IntegratorOneDimOptions.SetDefaultAbsTolerance(1.E-3)
# ROOT.Math.IntegratorOneDimOptions.SetDefaultRelTolerance(1.E-3)

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

ROOT.gROOT.SetBatch(True)

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

yield_rows = {
    'e':[],
    't':[],
    'yield':[],
    'yield_err':[],
    'chi2ndf':[],
    'minuit_err': []
}

parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg par1', 'bkg par2', 'bkg par3']

fit_low, fit_high = 1.16, 1.63

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
        0: 5, # voight amplitude
        1: v_mean, # voight mean
        3: v_width, # voight width
        4: 15, # gaus amplitude
        5: gaus_mean, # gaus mean
        6: gaus_width, # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    
    for t in range(1, 8):
        c.cd(t)
        cor_hist = ct.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist = ct.remove_zero_datapoints(cor_hist)

        hist.GetXaxis().SetRangeUser(1.1, 1.65)
        hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)

        hist.GetXaxis().SetTitle(hist_title + ' (GeV)')
        hist.GetXaxis().SetTitleSize(0.055)
        hist.GetYaxis().SetTitle('Counts/10 MeV')

        hist.SetTitle('E_{#gamma} = ' + str(e) + ' GeV || ' + f'{constants.T_CUT_DICT[t][0]} < -t < {constants.T_CUT_DICT[t][1]}' + ' GeV^{2}')
        hist.SetTitleSize(0.055)

        hists.append(hist)


        func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', fit_low, fit_high)
        # func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + [7] + [8]*(x+1.15) + [9]*(x-1.15)*(x-1.15)', fit_low, fit_high)
        
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]

        func.SetParameter(0, initial_guesses[0]) # voight amplitude
        func.SetParLimits(0, 0., 100000)
        func.FixParameter(1, initial_guesses[1]) # voight mean
        func.FixParameter(2, e_t_sigma)
        func.FixParameter(3, initial_guesses[3]) # voight width
        func.SetParameter(4, initial_guesses[4]) # gaus amplitude
        func.SetParLimits(4, 0., 100000)
        func.FixParameter(5, initial_guesses[5]) # gaus mean 
        # func.SetParLimits(5, 1.34, 1.4)
        func.FixParameter(6, initial_guesses[6]) # gaus width
        # func.SetParameter(6, initial_guesses[6])
        # func.SetParLimits(6, 0.025, 0.05)
        func.SetParameter(7, initial_guesses[7]) # bkg par1
        func.SetParameter(8, initial_guesses[8]) # bkg par2
        func.SetParameter(9, initial_guesses[9]) # bkg par3
        # if t != 7:
        #     # func.SetParameter(7, 0) # bkg par1
        #     func.SetParameter(7, initial_guesses[7]) # bkg par1
        #     func.SetParameter(8, initial_guesses[8]) # bkg par2
        #     func.SetParameter(9, initial_guesses[9]) # bkg par3
        # else:
        #     func.SetParameter(7, -100)
        #     # func.SetParLimits(7, -100000, .0)
        #     # func.SetParLimits(7, -100000, 0)
        #     func.SetParameter(8, 100)
        #     # func.SetParLimits(8, 0, 1000000)
        #     func.SetParameter(9, 1)
            # func.SetParLimits(9, -100000, 0)
        # func.SetParLimits(7, -100000, 50.0)
        # func.SetParLimits(8, 0, 1000000)
        # func.SetParLimits(9, -100000, 100000)

        func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

        result = hist.Fit(func, 'SRBN')
        # result = hist.Fit(func, 'SRBEV')
        # print("\n")
        # print("==" * 20)
        # print("==" * 20)
        # print("\n")
        # print(f'V_Amp: {func1.GetParameter(0)}')
        # print(f'G_Amp: {func1.GetParameter(4)}')
        
        func.SetLineColor(total_fit_color)

        print('\n')
        print(f'++' * 10)
        print(f'++' * 10)
        print(f'E = {e} GeV, t = {t} GeV^2, AMP = {func.GetParameter(0)} +/- {func.GetParError(0)}')
        print(f'++' * 10)
        print(f'++' * 10)
        print('\n')

        voight = ROOT.TF1(f'voight_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', fit_low, fit_high)
        voight.SetLineColor(ROOT.kBlack)
        voight.SetFillColor(f1_color)
        voight.SetFillStyle(1001)
        gaus = ROOT.TF1('gaus', 'gaus(0)', fit_low, fit_high)
        gaus.SetLineColor(background_color)
        gaus.SetLineStyle(3)
        bkg = ROOT.TF1('bkg', 'pol2(0)', fit_low, fit_high)
        bkg.SetLineColor(background_color)
        bkg.SetLineStyle(2)

        initial_guesses[0] = func.GetParameter(0)
        initial_guesses[4] = func.GetParameter(4)
        initial_guesses[5] = func.GetParameter(5)
        initial_guesses[6] = func.GetParameter(6)
        initial_guesses[7] = func.GetParameter(7)
        initial_guesses[8] = func.GetParameter(8)
        initial_guesses[9] = func.GetParameter(9)


        voight.SetParameter(0, func.GetParameter(0))
        voight.SetParError(0, func.GetParError(0))
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

        f1_yield = voight.Integral(1.16, 1.5, 1e-7)/0.01
        f1_yield_error = ct.calculate_rel_bootstrap_error(hist, func, n_trials=10000) * f1_yield
        acceptance, acceptance_error = ct.get_binned_gluex1_signal_acceptance(channel, e, t)
        cross_section = ct.calculate_crosssection(f1_yield, acceptance, luminosity, constants.T_WIDTH_DICT[t], constants.F1_KKPI_BRANCHING_FRACTION)
        cross_section_error = ct.propogate_error_multiplication(cross_section, [f1_yield], [f1_yield_error])
        chi2ndf = func.GetChisquare()/func.GetNDF()

        yield_rows['t'].append(t)
        yield_rows['e'].append(e)
        yield_rows['yield'].append(f1_yield)
        yield_rows['yield_err'].append(f1_yield_error)
        yield_rows['chi2ndf'].append(chi2ndf)
        yield_rows['minuit_err'].append(func.GetParError(0)/func.GetParameter(0))

        mean_list.append(func.GetParameter(1))
        mean_error_list.append(func.GetParError(1))
        width_list.append(func.GetParameter(3))
        width_error_list.append(func.GetParError(3))
        chi2ndf_list.append(chi2ndf)
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
        # print("\n")
        # print("++++++++" * 5)
        # print("++++++++" * 5)
        # print("++++++++" * 5)
        # print("\n")

    c.SaveAs(f'/work/halld/home/viducic/scripts/crosssection/plots/pol2_gaus_{channel}_e{e}_fit.png')

value_df = pd.DataFrame({'mean': mean_list, 'mean_error': mean_error_list, 'width': width_list, 'width_error': width_error_list, 'chi2ndf': chi2ndf_list, 'yield': data_yield_list, 'yield_error': yield_error_list, 'acceptance': acceptance_list, 'acceptance_error': acceptance_error_list,'cross_section': cross_section_list, 'cross_section_error': cross_section_error_list, 't_bin_middle': t_bin_list, 't_bin_width': t_bin_width_list, 'beam_energy': energy_bin_list, 'luminosity': luminosity_list})
value_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/tf1_gaus_cross_section_values.csv', index=False)

yield_df = pd.DataFrame(yield_rows)
yield_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/tf1_gaus_yield_values.csv', index=False)