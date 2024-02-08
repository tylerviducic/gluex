from typing import Dict
from unittest import result
import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts
import os
from my_library.systematics_constants import VARIED_CUTS_DICT_PIPKMKS, NOMINAL_CUTS_DICT_PIPKMKS, VARIED_CUTS_DICT_PIMKPKS, NOMINAL_CUTS_DICT_PIMKPKS
import pandas as pd

ROOT.EnableImplicitMT(12)

# TODO: write fitting pipeline. calculate cross section for each energy and t bin

def get_binned_data_hist(channel, cut, e, t_bin_index, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')

    data_filename = f'/work/halld/home/viducic/data/{channel}/systematics/hists/{channel}_data.root'
    data_file = ROOT.TFile(data_filename, 'READ')
    hist_name = f'{channel}_data_{cut}_{ltn}_e{e}_t{t_bin_index}'
    print(data_filename)
    print(hist_name)
    hist = data_file.Get(hist_name)
    print(type(hist))
    hist.SetDirectory(0)
    data_file.Close()
    return hist


def get_binned_mc_hist(channel, run_period, cut, e, t_bin_index, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')
    mc_filename = f'/work/halld/home/viducic/data/{channel}/systematics/hists/{channel}_mc_{run_period}.root'
    mc_file = ROOT.TFile(mc_filename, 'READ')
    hist_name = f'{channel}_signal_{cut}_{ltn}_e{e}_t{t_bin_index}'
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
    signal_hist = get_binned_mc_hist(channel, run_period, cut, e, t_bin_index, ltn)
    thrown_hist = tools.get_binned_signal_thrown_hist(channel, run_period, e, t_bin_index)
    acceptance, error = tools.get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error=True)
    print(f'channel: {channel}, run_period: {run_period}, cut: {cut}, e: {e}, t_bin_index: {t_bin_index}, ltn: {ltn}, %error: {error/acceptance*100}')
    return acceptance
    

def get_gluex1_acceptance(channel, cut, e, t_bin_index, ltn):
    acceptance_spring = get_acceptance_per_run_period(channel, 'spring', cut, e, t_bin_index, ltn)
    acceptance_fall = get_acceptance_per_run_period(channel, 'fall', cut, e, t_bin_index, ltn)
    acceptance_2017 = get_acceptance_per_run_period(channel, '2017', cut, e, t_bin_index, ltn)

    flux_spring = tools.get_luminosity('spring', e-0.5, e+0.5)
    flux_fall = tools.get_luminosity('fall', e-0.5, e+0.5)
    flux_2017 = tools.get_luminosity('2017', e-0.5, e+0.5)
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
    param_keys = ['voigt_amplitude', 'voigt_mean', 'voigt_sigma', 'voigt_width', 'gaus_amplitude', 'gaus_mean', 'gaus_width', 'bkg_par1', 'bkg_par2', 'bkg_par3']
    if len(param_guesses) != 10:
        raise ValueError('Invalid number of parameter guesses. Must be 10')
    for guess_key, correct_key in zip(param_guesses.keys(), param_keys):
        if guess_key != correct_key:
            raise ValueError(f'Invalid parameter guess key: {guess_key}. was expecting {correct_key}')
    return True


# TODO: write function to fit histograms
def fit_hist(hist, param_guesses: dict, cut, e, t, ltn):
    if ltn not in ['loose', 'tight', 'nominal']:
        raise ValueError(f'Invalid ltn value: {ltn}. Must be one of "loose", "tight", "nominal"')
    
    check_param_guess_structure(param_guesses)
    
    func = ROOT.TF1(f'func_{cut}_{e}_{t}_{ltn}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.15, 1.51)

    for par_name in param_guesses.keys():
        func.SetParameter(par_name, param_guesses[par_name])

    func.SetParameter('voigt_amplitude', param_guesses['voigt_amplitude']) # voigt amplitude
    func.SetParLimits('voigt_amplitude', 0.1, 100000)
    func.FixParameter('voigt_mean', param_guesses['voigt_mean']) # voigt mean
    func.FixParameter('voigt_sigma', param_guesses['voigt_sigma']) # voigt sigma/resolution 
    func.FixParameter('voigt_width', param_guesses['voigt_width']) # voigt width
    func.SetParameter('voigt_amplitude', param_guesses['gaus_amplitude']) # gaus amplitude
    func.SetParLimits('voigt_amplitude', 0.1, 10000)
    func.FixParameter('gaus_mean', param_guesses['gaus_mean'])
    func.FixParameter('gaus_width', param_guesses['gaus_width']) # gaus width
    func.SetParameter('bkg_par1', param_guesses['bkg_par1']) # bkg par1
    func.SetParLimits('bkg_par1', -100000, 0.0)
    func.SetParameter('bkg_par2', param_guesses['bkg_par2']) # bkg par2
    func.SetParameter('bkg_par3', param_guesses['bkg_par3']) # bkg par3

    result = hist.Fit(func, 'SRBE0')
    func.SetDirectory(0)
    return result, func


def update_guesses(func):
    new_guesses = {'voigt_amplitude': func.GetParameter(0), 
               'voigt_mean': func.GetParameter(1), 
               'voigt_sigma': func.GetParameter(2),
               'voigt_width': func.GetParameter(3), 
               'gaus_amplitude': func.GetParameter(4), 
               'gaus_mean': func.GetParameter(5), 
               'gaus_width': func.GetParameter(6), 
               'bkg_par1': func.GetParameter(7), 
               'bkg_par2': func.GetParameter(8), 
               'bkg_par3': func.GetParameter(9)}
    return new_guesses


def get_func_components(func, e, t, cut, ltn):
    voigt = ROOT.TF1(f'voigt_{cut}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.15, 1.51)
    gaus = ROOT.TF1(f'gaus_{cut}_{e}_{t}', 'gaus(0)', 1.15, 1.51)
    bkg = ROOT.TF1(f'bkg_{cut}_{e}_{t}', 'pol2(0)', 1.15, 1.51)

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

    voigt.SetDirectory(0)
    gaus.SetDirectory(0)
    bkg.SetDirectory(0)

    return voigt, gaus, bkg


def get_yield_and_error(voigt_func):
    f1_yield = voigt_func.Integral(1.2, 1.5)
    f1_error = voigt_func.GetParError(0)/voigt_func.GetParameter(0) * f1_yield
    return f1_yield, f1_error


# TODO: write function to store fit results in CSV file
def store_dataframe_info(voigt_loose, voigt_nominal, voigt_tight, luminosity, e, t, cut):

    return

if __name__ == '__main__':

    print('Running')
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
            for e in range(8, 12):

                param_guesses = {
                    'voigt_amplitude': 5, # voigt amplitude
                    'voigt_mean': v_mean, # voigt mean
                    'voigt_width': v_width, # voigt width
                    'gaus_amplitude': 15, # gaus amplitude
                    'gaus_mean': gaus_mean, # gaus mean
                    'gaus_width': gaus_width, # gaus width
                    'bkg_par1': -100, # bkg par1
                    'bkg_par2': 100, # bkg par2
                    'bkg_par3': 1 # bkg par3
                }

                e_flux = tools.get_luminosity_gluex_1(e-0.5, e+0.5)*1000

                for t in range(1, 8):
                    nominal_data_hist = get_binned_data_hist(channel, cut, e, t, 'nominal')
                    loose_data_hist = get_binned_data_hist(channel, cut, e, t, 'loose')
                    tight_data_hist = get_binned_data_hist(channel, cut, e, t, 'tight')

                    nominal_cor_hist = tools.correct_data_hist_for_kstar_efficiency(nominal_data_hist)
                    if cut not in ['neutral_kstar', 'charged_kstar']:
                        eff_cor_hist_loose = correct_data_hist_for_varied_kstar_efficiency(loose_data_hist, cut, 'loose')
                        eff_cor_hist_tight = correct_data_hist_for_varied_kstar_efficiency(tight_data_hist, cut, 'tight')
                    else: 
                        eff_cor_hist_loose = tools.correct_data_hist_for_kstar_efficiency(loose_data_hist)
                        eff_cor_hist_tight = tools.correct_data_hist_for_kstar_efficiency(tight_data_hist)

                    result_nominal, func_nominal = fit_hist(nominal_cor_hist, param_guesses, cut, e, t, 'nominal')
                    result_loose, func_loose = fit_hist(eff_cor_hist_loose, param_guesses, cut, e, t, 'loose')
                    result_tight, func_tight = fit_hist(eff_cor_hist_tight, param_guesses, cut, e, t, 'tight')

                    voigt_nominal, gaus_nominal, bkg_nominal = get_func_components(func_nominal, e, t, cut, 'nominal')
                    voigt_loose, gaus_loose, bkg_loose = get_func_components(func_loose, e, t, cut, 'loose')
                    voigt_tight, gaus_tight, bkg_tight = get_func_components(func_tight, e, t, cut, 'tight')

                    func_nominal.SetLineColor(total_fit_color)
                    func_loose.SetLineColor(total_fit_color)
                    func_tight.SetLineColor(total_fit_color)

                    voigt_nominal.SetLineColor(ROOT.kBlack)
                    voigt_loose.SetLineColor(ROOT.kBlack)
                    voigt_tight.SetLineColor(ROOT.kBlack)

                    voigt_nominal.SetFillColor(f1_color)
                    voigt_loose.SetFillColor(f1_color)
                    voigt_tight.SetFillColor(f1_color)

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
                    func_loose.Draw()
                    voigt_loose.Draw('same')
                    gaus_loose.Draw('same')
                    bkg_loose.Draw('same')
                    c.cd(2)
                    func_nominal.Draw()
                    voigt_nominal.Draw('same')
                    gaus_nominal.Draw('same')
                    bkg_nominal.Draw('same')
                    c.cd(3)
                    func_tight.Draw()
                    voigt_tight.Draw('same')
                    gaus_tight.Draw('same')
                    bkg_tight.Draw('same')

                    c.Update()
                    c.SaveAs(f'/work/halld/home/viducic/systematic_errors/kstar_eff/plots/{channel}_{cut}_e{e}_t{t}_fit.png')

                    nominal_yield, nominal_yield_error = get_yield_and_error(voigt_nominal)
                    nominal_acceptance = get_gluex1_acceptance(channel, cut, e, t, 'nominal')





                    



                    




                    


