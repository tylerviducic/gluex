import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts
import os
from my_library.systematics_constants import VARIED_CUTS_DICT_PIPKMKS, NOMINAL_CUTS_DICT_PIPKMKS, VARIED_CUTS_DICT_PIMKPKS, NOMINAL_CUTS_DICT_PIMKPKS

ROOT.EnableImplicitMT(12)

# TODO: write fitting pipeline. calculate cross section for each energy and t bin

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
    acceptance = signal_hist.Integral()/thrown_hist.Integral()
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



if __name__ == '__main__':
    print('Running')
    channels = ['pipkmks', 'pimkpks']
    for channel in channels:
        for cut in VARIED_CUTS_DICT_PIPKMKS:
            for e in range(8, 12):
                for t in range(1, 8):
                    nominal_data_hist = get_binned_data_hist(channel, cut, e, t, 'nominal')
                    loose_data_hist = get_binned_data_hist(channel, cut, e, t, 'loose')
                    tight_data_hist = get_binned_data_hist(channel, cut, e, t, 'tight')


