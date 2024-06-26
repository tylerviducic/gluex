import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts
from my_library.systematics_constants import VARIED_CUTS_DICT_PIPKMKS, NOMINAL_CUTS_DICT_PIPKMKS, VARIED_CUTS_DICT_PIMKPKS, NOMINAL_CUTS_DICT_PIMKPKS
import pandas as pd

# ROOT.EnableImplicitMT(12)


def get_binned_data_hist(channel, cut, e, t_bin_index, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')

    data_filename = f'/work/halld/home/viducic/data/{channel}/systematics/hists/{channel}_data.root'
    data_file = ROOT.TFile(data_filename, 'READ')
    hist_name = f'{channel}_data_{cut}_{ltn}_e{e}_t{t_bin_index}'
    hist = data_file.Get(hist_name)
    hist.SetDirectory(0)
    data_file.Close()
    return hist


def get_binned_mc_hist(channel, run_period, cut, e, t_bin_index, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')
    mc_filename = f'/work/halld/home/viducic/data/{channel}/systematics/hists/{channel}_mc_{run_period}.root'
    mc_file = ROOT.TFile(mc_filename, 'READ')
    hist_name = f'{channel}_signal_{cut}_{ltn}_{run_period}_e{e}_t{t_bin_index}'
    hist = mc_file.Get(hist_name)
    hist.SetDirectory(0)
    mc_file.Close()
    return hist


def get_gluex1_mc_hist(channel, cut, e, t_bin_index, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')
    
    flux_spring = tools.get_luminosity('spring', e-0.5, e+0.5)
    flux_fall = tools.get_luminosity('fall', e-0.5, e+0.5)
    flux_2017 = tools.get_luminosity('2017', e-0.5, e+0.5)
    total_flux = flux_spring + flux_fall + flux_2017

    hist_spring = get_binned_mc_hist(channel, 'spring', cut, e, t_bin_index, ltn)
    hist_fall = get_binned_mc_hist(channel, 'fall', cut, e, t_bin_index, ltn)
    hist_2017 = get_binned_mc_hist(channel, '2017', cut, e, t_bin_index, ltn)

    hist_gluex = hist_spring.Clone()
    hist_gluex.Scale(flux_spring/total_flux)
    hist_gluex.Add(hist_fall, flux_fall/total_flux)
    hist_gluex.Add(hist_2017, flux_2017/total_flux)

    hist_gluex.SetDirectory(0)
    return hist_gluex


def get_acceptance_per_run_period(channel, run_period, cut, e, t_bin_index, ltn):
    if cut == 'neutral_kstar' or cut == 'charged_kstar':
        return tools.get_binned_signal_acceptance(channel, run_period, e, t_bin_index, error=False)
    signal_hist = get_binned_mc_hist(channel, run_period, cut, e, t_bin_index, ltn)
    thrown_hist = tools.get_binned_signal_thrown_hist(channel, run_period, e, t_bin_index)
    acceptance, error = tools.get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error=True)
    # print(f'channel: {channel}, run_period: {run_period}, cut: {cut}, e: {e}, t_bin_index: {t_bin_index}, ltn: {ltn}, %error: {error/acceptance*100}')
    return acceptance


def get_gluex1_acceptance(channel, cut, e, t_bin_index, ltn):
    acceptance_spring = get_acceptance_per_run_period(channel, 'spring', cut, e, t_bin_index, ltn)
    acceptance_fall = get_acceptance_per_run_period(channel, 'fall', cut, e, t_bin_index, ltn)
    acceptance_2017 = get_acceptance_per_run_period(channel, '2017', cut, e, t_bin_index, ltn)
    # print(f'spring: {acceptance_spring}, fall: {acceptance_fall}, 2017: {acceptance_2017}')

    if e == 12:
        flux_spring = tools.get_luminosity('spring', e-5.5, e-0.5)
        flux_fall = tools.get_luminosity('fall', e-5.5, e-0.5)
        flux_2017 = tools.get_luminosity('2017', e-5.5, e-0.5)
    else:
        flux_spring = tools.get_luminosity('spring', e-0.5, e+0.5)
        flux_fall = tools.get_luminosity('fall', e-0.5, e+0.5)
        flux_2017 = tools.get_luminosity('2017', e-0.5, e+0.5)
    
    # print(f'spring: {flux_spring}, fall: {flux_fall}, 2017: {flux_2017}')
    
    total_flux = flux_spring + flux_fall + flux_2017

    acceptance = (acceptance_spring * flux_spring + acceptance_fall * flux_fall + acceptance_2017 * flux_2017) / total_flux
    return acceptance


def correct_data_hist_for_varied_kstar_efficiency(hist, cut, lt):
    if lt not in ['loose', 'tight']:
        raise ValueError(f'Invalid ltn value: {lt}. Must be one of "loose", "tight"')
    
    new_hist = hist.Clone()
    new_hist.Sumw2()
    kstar_efficiency_df = pd.read_csv(
        f'/work/halld/home/viducic/systematic_errors/kstar_eff/kstar_cut_efficiency_{cut}_{lt}_10.0.csv')
    for i in range(1, hist.GetXaxis().GetNbins()+1):
        bin_ef_df = kstar_efficiency_df.loc[kstar_efficiency_df.mass_bin_center == round(
            hist.GetXaxis().GetBinCenter(i), 3)]
        if len(bin_ef_df) == 0:
            print(
                f'Bin center = {hist.GetXaxis().GetBinCenter(i)} has no efficiency value')
            continue
        bin_eff = bin_ef_df.kstar_cut_efficiency.values[0]
        hist.SetBinContent(i, hist.GetBinContent(i) / bin_eff)
        hist.SetBinError(i, hist.GetBinError(i) / bin_eff)
    hist.SetDirectory(0)
    return hist


def check_param_guess_structure(param_guesses: dict):
    if len(param_guesses) != 10:
        raise ValueError('Invalid number of parameter guesses. Must be 10')
    return True


def fit_hist(hist, param_guesses: dict, cut, e, t, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')
    
    check_param_guess_structure(param_guesses)
    
    func = ROOT.TF1(f'func_{ltn}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, 1.63)

    func.SetParameter(0, param_guesses[0]) # voigt amplitude
    func.SetParLimits(0, 0., 100000)
    func.FixParameter(1, param_guesses[1]) # voigt mean
    func.FixParameter(2, param_guesses[2]) # voigt sigma/resolution 
    func.FixParameter(3, param_guesses[3]) # voigt width
    func.SetParameter(4, param_guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0., 10000)
    func.FixParameter(5, param_guesses[5])
    func.FixParameter(6, param_guesses[6]) # gaus width
    func.SetParameter(7, param_guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, param_guesses[8]) # bkg par2
    func.SetParameter(9, param_guesses[9]) # bkg par3

    result = hist.Fit(func, 'SRBQ0')
    return result, func


def update_guesses(func):
    # new_guesses = {0: func.GetParameter(0), # voigt_amplitude
    #            1: func.GetParameter(1), # voigt_mean
    #            2: func.GetParameter(2), # voigt_sigma
    #            3: func.GetParameter(3), # voigt_width
    #            4: func.GetParameter(4), # gaus_amplitude
    #            5: func.GetParameter(5), # gaus_mean
    #            6: func.GetParameter(6), # gaus_width
    #            7: func.GetParameter(7), # bkg_par1
    #            8: func.GetParameter(8), # bkg_par2
    #            9: func.GetParameter(9)} # bkg_par3
    new_guesses = {i: func.GetParameter(i) for i in range(func.GetNpar())}
    return new_guesses


def get_func_components(func, ltn):
    voigt = ROOT.TF1(f'voigt_{ltn}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.16, 1.6)
    gaus = ROOT.TF1(f'gaus_{ltn}', 'gaus(0)', 1.16, 1.6)
    bkg = ROOT.TF1(f'bkg_{ltn}', 'pol2(0)', 1.16, 1.6)

    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))

    return voigt, gaus, bkg


def get_yield_and_error(func, hist):
    voigt = ROOT.TF1(f'voigt_dummy', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.16, 1.6)
    for i in range(4):
        voigt.SetParameter(i, func.GetParameter(i))

    f1_yield = voigt.Integral(1.16, 1.5, 1e-7)/0.01
    f1_error = f1_yield*tools.calculate_rel_bootstrap_error(hist, func)
    return f1_yield, f1_error


def calculate_dataframe_info(func, hist, channel, e, t, cut, ltn):
    if e == 12:
        e_lumi = tools.get_luminosity_gluex_1(7.5, 11.5)*1000
    else:
        e_lumi = tools.get_luminosity_gluex_1(e-0.5, e+0.5)*1000
    f1_yield, f1_yield_error = get_yield_and_error(func, hist)
    f1_acceptance = get_gluex1_acceptance(channel, cut, e, t, ltn)
    f1_acceptance_error = 0 
    cross_section = tools.calculate_crosssection(f1_yield, f1_acceptance, e_lumi, constants.T_WIDTH_DICT[t], constants.F1_KKPI_BRANCHING_FRACTION)
    cross_section_error = tools.propogate_error_multiplication(cross_section, [f1_yield], [f1_yield_error])
    return f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error


def get_row_for_df(channel, func_nominal, func_loose, func_tight, hist_nominal, hist_loose, hist_tight, e, t, cut):
    f1_yield_nominal, f1_yield_error_nominal, f1_acceptance_nominal, f1_acceptance_error_nominal, cross_section_nominal, cross_section_error_nominal = calculate_dataframe_info(func_nominal, hist_nominal, channel, e, t, cut, 'nominal')
    f1_yield_loose, f1_yield_error_loose, f1_acceptance_loose, f1_acceptance_error_loose, cross_section_loose, cross_section_error_loose = calculate_dataframe_info(func_loose, hist_loose, channel, e, t, cut, 'loose')
    f1_yield_tight, f1_yield_error_tight, f1_acceptance_tight, f1_acceptance_error_tight, cross_section_tight, cross_section_error_tight = calculate_dataframe_info(func_tight, hist_tight, channel, e, t, cut, 'tight')
    row = [channel, e, t, cut, 
           f1_yield_nominal, f1_yield_error_nominal, f1_acceptance_nominal, f1_acceptance_error_nominal, cross_section_nominal, cross_section_error_nominal,
           f1_yield_loose, f1_yield_error_loose, f1_acceptance_loose, f1_acceptance_error_loose, cross_section_loose, cross_section_error_loose,
           f1_yield_tight, f1_yield_error_tight, f1_acceptance_tight, f1_acceptance_error_tight, cross_section_tight, cross_section_error_tight]
    return row


if __name__ == '__main__':

    ROOT.gROOT.SetBatch(True)
    print('Running')

    rows = {'channel':[], 'e':[], 't':[], 'cut':[],
            'f1_yield_nominal':[], 'f1_yield_error_nominal':[], 'f1_acceptance_nominal':[], 'f1_acceptance_error_nominal':[], 'cross_section_nominal':[], 'cross_section_error_nominal':[],
            'f1_yield_loose':[], 'f1_yield_error_loose':[], 'f1_acceptance_loose':[], 'f1_acceptance_error_loose':[], 'cross_section_loose':[], 'cross_section_error_loose':[],
            'f1_yield_tight':[], 'f1_yield_error_tight':[], 'f1_acceptance_tight':[], 'f1_acceptance_error_tight':[], 'cross_section_tight':[], 'cross_section_error_tight':[]
    }

    channels = ['pipkmks', 'pimkpks']

    c = ROOT.TCanvas('c', 'c', 1000, 1000)

    for channel in channels:

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

        for cut in VARIED_CUTS_DICT_PIPKMKS:
            for e in range(8, 13):

                param_guesses = {
                    0: 5, # voigt amplitude
                    1: v_mean, # voigt mean
                    2: 0.11, # voigt sigma
                    3: v_width, # voigt width
                    4: 15, # gaus amplitude
                    5: gaus_mean, # gaus mean
                    6: gaus_width, # gaus width
                    7: -100, # bkg par1
                    8: 100, # bkg par2
                    9: 1 # bkg par3
                }

                for t in range(1, 8):

                    if e != 12:
                        param_guesses[2] = tools.get_binned_resolution(channel, e, t)
                    else:
                        res_int_df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_t_f1_mc_width.csv')
                        param_guesses[2] = res_int_df.loc[(res_int_df.t_bin == t)].sigma.values[0]

                    nominal_data_hist = get_binned_data_hist(channel, cut, e, t, 'nominal')
                    loose_data_hist = get_binned_data_hist(channel, cut, e, t, 'loose')
                    tight_data_hist = get_binned_data_hist(channel, cut, e, t, 'tight')

                    nominal_cor_hist = tools.correct_data_hist_for_kstar_efficiency(nominal_data_hist)
                    if cut not in ['neutral_kstar', 'charged_kstar']:
                        eff_cor_hist_loose = tools.correct_data_hist_for_kstar_efficiency(loose_data_hist)
                        eff_cor_hist_tight = tools.correct_data_hist_for_kstar_efficiency(tight_data_hist)
                    else: 
                        eff_cor_hist_loose = correct_data_hist_for_varied_kstar_efficiency(loose_data_hist, cut, 'loose')
                        eff_cor_hist_tight = correct_data_hist_for_varied_kstar_efficiency(tight_data_hist, cut, 'tight')

                    nominal_cor_hist = tools.remove_zero_datapoints(nominal_cor_hist)
                    eff_cor_hist_loose = tools.remove_zero_datapoints(eff_cor_hist_loose)
                    eff_cor_hist_tight = tools.remove_zero_datapoints(eff_cor_hist_tight)

                    result_nominal, func_nominal = fit_hist(nominal_cor_hist, param_guesses, cut, e, t, 'nominal')
                    result_loose, func_loose = fit_hist(eff_cor_hist_loose, param_guesses, cut, e, t, 'loose')
                    result_tight, func_tight = fit_hist(eff_cor_hist_tight, param_guesses, cut, e, t, 'tight')

                    voigt_nominal, gaus_nominal, bkg_nominal = get_func_components(func_nominal, 'nominal')
                    voigt_loose, gaus_loose, bkg_loose = get_func_components(func_loose, 'loose')
                    voigt_tight, gaus_tight, bkg_tight = get_func_components(func_tight, 'tight')

                    func_nominal.SetLineColor(total_fit_color)
                    func_loose.SetLineColor(total_fit_color)
                    func_tight.SetLineColor(total_fit_color)

                    voigt_nominal.SetLineColor(ROOT.kBlack)
                    voigt_loose.SetLineColor(ROOT.kBlack)
                    voigt_tight.SetLineColor(ROOT.kBlack)

                    voigt_nominal.SetFillColor(f1_color)
                    voigt_loose.SetFillColor(f1_color)
                    voigt_tight.SetFillColor(f1_color)
                    
                    voigt_nominal.SetFillStyle(1001)
                    voigt_loose.SetFillStyle(1001)
                    voigt_tight.SetFillStyle(1001)

                    gaus_nominal.SetLineColor(background_color)
                    gaus_loose.SetLineColor(background_color)
                    gaus_tight.SetLineColor(background_color)

                    gaus_nominal.SetLineStyle(3)
                    gaus_loose.SetLineStyle(3)
                    gaus_tight.SetLineStyle(3)

                    bkg_nominal.SetLineColor(background_color)
                    bkg_loose.SetLineColor(background_color)
                    bkg_tight.SetLineColor(background_color)

                    bkg_nominal.SetLineStyle(2)
                    bkg_loose.SetLineStyle(2)
                    bkg_tight.SetLineStyle(2)
                    
                    c.Clear()
                    c.Divide(1, 3)
                    c.cd(1)
                    eff_cor_hist_loose.Draw()
                    func_loose.Draw('same')
                    voigt_loose.Draw('same')
                    gaus_loose.Draw('same')
                    bkg_loose.Draw('same')
                    c.cd(2)
                    nominal_cor_hist.Draw()
                    func_nominal.Draw('same')
                    voigt_nominal.Draw('same')
                    gaus_nominal.Draw('same')
                    bkg_nominal.Draw('same')
                    c.cd(3)
                    eff_cor_hist_tight.Draw()
                    func_tight.Draw('same')
                    voigt_tight.Draw('same')
                    gaus_tight.Draw('same')
                    bkg_tight.Draw('same')

                    c.Update()
                    c.SaveAs(f'/work/halld/home/viducic/systematic_errors/plots/cut_sys/{channel}_{cut}_e{e}_t{t}_fit.png')

                    param_guesses = update_guesses(func_nominal)
                    row = get_row_for_df(channel, func_nominal, func_loose, func_tight, nominal_cor_hist, eff_cor_hist_loose, eff_cor_hist_tight, e, t, cut)
                    for i, key in enumerate(rows.keys()):
                        rows[key].append(row[i])                   

    df = pd.DataFrame(rows)
    df.to_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv', index=False)
    print('done')





                    

    

                    




                    


