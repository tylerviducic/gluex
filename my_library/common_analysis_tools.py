"""
this is almost certainly not the right way to do something like this,
but lets go ahead and see if this works out. 

writing a python file that can be imported into other python files that 
contains common analysis tools/code snippets that i use
"""

import math

from numpy.core.umath import sqrt
import ROOT
import pandas as pd
import numpy as np

import my_library.constants as constants
import my_library.kinematic_cuts as kcuts

###################
##### METHODS #####
###################


def get_flat_data_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/data'
    treename = ''
    if not comboloop:
        file_path += f'/bestX2/{channel}_'
        if filtered:
            file_path += f'flat_filtered_{constants.RUN_DICT[run_period]}.root'
            treename = f'{channel}_filtered_data'
        else:
            if hist:
                file_path += f'flat_result_{constants.RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{constants.RUN_DICT[run_period]}.root'
                treename = f'{channel}__B4_M16'
    else:
        file_path += f'/comboloop/{channel}_comboloop_flat_{constants.RUN_DICT[run_period]}.root'
        treename = f'{channel}__B4_M16'
    return (file_path, treename)


def get_flat_signal_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/mc/signal/{channel}_'
    treename = ''
    if not comboloop:
        if filtered:
            file_path += f'flat_filtered_{constants.RUN_DICT[run_period]}.root'
            treename = f'{channel}_filtered_signal'
        else:
            if hist:
                file_path += f'flat_result_{constants.RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{constants.RUN_DICT[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop signal mc file yet')
    return (file_path, treename)


def get_flat_phasespace_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/mc/phasespace/{channel}_'
    treename = ''
    if not comboloop:
        if filtered:
            file_path += f'filtered_{constants.RUN_DICT[run_period]}.root'
            treename = f'{channel}_filtered_{constants.RUN_DICT[run_period]}'
        else:
            if hist:
                file_path += f'flat_result_{constants.RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{constants.RUN_DICT[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop phasespace mc file yet')
    return (file_path, treename)


def get_flat_nstar_file_and_tree(channel, run_period, nstar_mass, comboloop=False, filtered=True, hist=False):
    # TODO: add hist and filtered options when ready
    if channel != 'pimkpks' or run_period != 'spring':
        raise ValueError('Only pi-K+Ks for Spring 2018 is avialable for N* MC')
    if comboloop:
        raise ValueError('No comboloop N* MC')
    if nstar_mass not in constants.ALLOWED_NSTAR_MASSES:
        print(f"Valid N* masses are {constants.ALLOWED_NSTAR_MASSES}")
        raise ValueError('Invalid N* mass')
    file_path = '/work/halld/home/viducic/data/pimkpks/mc/nstar/'
    treename = ''
    if filtered:
        raise ValueError('No filtered N* MC yet')
    else:
        if hist:
            raise ValueError('No N* MC hist files yet')
        else:
            file_path += f'nstar_{nstar_mass}_flat_bestX2.root'
            treename = f'pimkpks__ks_pippim__B4_M16'
    return (file_path, treename)


def get_flat_1420_file_and_tree(channel, run_period, kstar_charge, comboloop=False, filtered=True, hist=False):
    # TODO: add filter and hist when ready
    if run_period != 'spring':
        raise ValueError('Only Spring 2018 is avialable for f1_1420 MC')
    if comboloop:
        raise ValueError('No comboloop f1_1420 MC')
    if channel == 'pipkmks' and kstar_charge not in ['zero', 'plus']:
        print(f"Valid K* charges for pipkmks are ['zero', 'plus']")
        raise ValueError('Invalid K* charge')
    elif channel == 'pimkpks' and kstar_charge not in ['zero', 'minus']:
        print(f"Valid K* charges for pimkpks are ['zero', 'minus']")
        raise ValueError('Invalid K* charge')
    filepath = f'/work/halld/home/viducic/data/{channel}/mc/f1_1420/'
    treename = ''
    if filtered:
        raise ValueError('No filtered f1_1420 MC yet')
    else:
        if hist:
            raise ValueError('No f1_1420 MC hist files yet')
        else:
            filepath += f'f1_1420_kstar_{kstar_charge}_flat_bestX2.root'
            treename += f'{channel}__ks_pippim__B4_M16'
    return (filepath, treename)


def get_flat_thrown_file_and_tree(channel, run_period, phasespace=False, hist=True):
    if not phasespace:
        if not hist:
            return (f'/w/halld-scshelf2101/home/viducic/data/{channel}/mc/thrown/{channel}_thrown_{constants.RUN_DICT[run_period]}.root', f'{channel}_thrown')
        return (f'/work/halld/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_signal_flat_result_{constants.RUN_DICT[run_period]}.root', 'pipkmks_thrown')
    elif phasespace:
        if not hist:
            return (f'/volatile/halld/home/viducic/selector_output/f1_{channel}/thrown/{channel}_phasespace_thrown_{constants.RUN_DICT[run_period]}.root', f'{channel}_thrown')
        return (f'/work/halld/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_phasespace_flat_result_{constants.RUN_DICT[run_period]}.root', 'pipkmks_thrown')


def get_flat_file_and_tree(channel, run_period, datatype, comboloop=False, filtered=True, hist=False, thrown=False, verbose=False, nstar_mass=None, kstar_charge=None):
    file_tuple = ()
    if thrown:
        if datatype == 'signal':
            file_tuple = get_flat_thrown_file_and_tree(
                channel, run_period, hist=hist)
        elif datatype == 'phasespace':
            file_tuple = get_flat_thrown_file_and_tree(
                channel, run_period, phasespace=True, hist=hist)
        else:
            print('invalid thrown datatype')
            return
    else:
        if datatype == 'data':
            file_tuple = get_flat_data_file_and_tree(
                channel, run_period, comboloop, filtered, hist)
        elif datatype == 'signal':
            file_tuple = get_flat_signal_file_and_tree(
                channel, run_period, comboloop, filtered, hist)
        elif datatype == 'phasespace':
            file_tuple = get_flat_phasespace_file_and_tree(
                channel, run_period, comboloop, filtered, hist)
        elif datatype == 'nstar':
            file_tuple = get_flat_nstar_file_and_tree(
                channel, run_period, nstar_mass, comboloop, filtered, hist)
        elif datatype == 'f1_1420':
            file_tuple = get_flat_1420_file_and_tree(
                channel, run_period, kstar_charge, comboloop, filtered, hist)
        else:
            print('invalid datatype')
            return
    if verbose:
        print(f'filepath: {file_tuple[0]} || treename: {file_tuple[1]}')
    return file_tuple


def get_luminosity(run_period, beam_low=6.5, beam_high=11.5):
    filename = '/work/halld/home/viducic/data/flux/'
    if run_period == 'fall':
        filename += 'flux_50685_51768.root'
    elif run_period == 'spring':
        filename += 'flux_40856_42559.root'
    elif run_period == '2017':
        filename += 'flux_30274_31057.root'
    else:
        return -1
    f = ROOT.TFile(filename)
    lumi_hist = f.Get('tagged_lumi')
    lumi = lumi_hist.Integral(lumi_hist.FindBin(
        beam_low), lumi_hist.FindBin(beam_high))
    f.Close()
    return lumi


def get_luminosity_gluex_1(beam_low=6.5, beam_high=11.5):
    lumi_spring = get_luminosity('spring', beam_low, beam_high)
    lumi_fall = get_luminosity('fall', beam_low, beam_high)
    lumi_2017 = get_luminosity('2017', beam_low, beam_high)

    return lumi_spring + lumi_fall + lumi_2017


def weight_histograms_by_flux(hist_spring: ROOT.TH1, hist_fall: ROOT.TH1, hist_2017: ROOT.TH1):
    hist_spring.Sumw2()
    hist_fall.Sumw2()
    hist_2017.Sumw2()

    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    combined_hist = hist_spring.Clone()
    combined_hist.Scale(lumi_spring / lumi_total)
    combined_hist.Add(hist_fall, lumi_fall / lumi_total)
    combined_hist.Add(hist_2017, lumi_2017 / lumi_total)

    combined_hist.Sumw2()
    combined_hist.SetDirectory(0)

    return combined_hist


def validate_t_bin(t):
    if t not in constants.ALLOWED_T_BINS:
        raise ValueError('invalid t bin number')
    return True


def validate_e_bin(e):
    if e not in constants.ALLOWED_E_BINS:
        raise ValueError('invalid e bin number')
    return True


def get_binned_kkpi_hist_title(channel, e, t_bin_index):
    validate_t_bin(t_bin_index)
    validate_e_bin(e)
    if channel == 'pipkmks':
        kkpi = 'K^{-}K_{s}#pi^{+}'
    elif channel == 'pimkpks':
        kkpi = 'K^{+}K_{s}#pi^{-}'
    else:
        return None
    return 'M({}) for E_{}={}-{} and t={}-{}'.format(kkpi, '{#gamma}', e-0.5, e+0.5, constants.T_CUT_DICT[t_bin_index][0], constants.T_CUT_DICT[t_bin_index][1])


def get_integrated_kkpi_hist_title(channel):
    if channel == 'pipkmks':
        kkpi = 'K^{-}K_{s}#pi^{+}'
    elif channel == 'pimkpks':
        kkpi = 'K^{+}K_{s}#pi^{-}'
    else:
        return None
    return 'M({}) for E_{}=6.5-11.5 and t=0.1-1.9'.format(kkpi, '{#gamma}')


def propogate_error_multiplication(target_datapoint, input_datapoints: list, input_errors: list):
    err_f2 = 0
    for i, datapoint in enumerate(input_datapoints):
        err_f2 += (input_errors[i]/datapoint)**2
        return target_datapoint * math.sqrt(err_f2)


def propogate_error_addition(input_errors: list):
    err_f2 = 0
    for error in input_errors:
        err_f2 += (error)**2
        return math.sqrt(err_f2)


def get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_{constants.BEAM_DICT[e]}_t_{constants.T_BIN_DICT[t_bin_index]};1'
    recon_phasespace_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'phasespace', filtered=False, hist=True)
    recon_phasespace_file = ROOT.TFile(recon_phasespace_file_and_tree[0])
    recon_hist = recon_phasespace_file.Get(hist_name)
    recon_hist.SetDirectory(0)
    return recon_hist


def get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index):
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(
        channel, run_period, phasespace=True)
    thrown_phasespace_file = ROOT.TFile(thrown_phasespace_file_and_tree[0])
    thrown_hist_name = f'{channel}_beam_{constants.BEAM_DICT[e]}_t_{constants.T_BIN_DICT[t_bin_index]};1'
    thrown_hist = thrown_phasespace_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_binned_signal_thrown_hist(channel, run_period, e, t_bin_index):
    thrown_signal_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'signal', filtered=False, hist=True, thrown=True)
    thrown_signal_file = ROOT.TFile(thrown_signal_file_and_tree[0])
    # print(thrown_signal_file_and_tree[0])
    if e == 12:
        thrown_hist_name = f'{channel}_beam_full_t_{constants.T_BIN_DICT[t_bin_index]};1'
    else:
        thrown_hist_name = f'{channel}_beam_{constants.BEAM_DICT[e]}_t_{constants.T_BIN_DICT[t_bin_index]};1'
    thrown_hist = thrown_signal_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_binned_data_hist(channel, run_period, cut, e, t_bin_index):
    if e == 12:
        hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_{constants.T_BIN_DICT[t_bin_index]};1'
    else:
        hist_name = f'{channel}_kstar_{cut}_cut_beam_{constants.BEAM_DICT[e]}_t_{constants.T_BIN_DICT[t_bin_index]};1'
    data_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'data', filtered=False, hist=True)
    data_hist_file = ROOT.TFile(data_file_and_tree[0])
    data_hist = data_hist_file.Get(hist_name)
    data_hist.SetDirectory(0)
    return data_hist


def get_binned_signal_mc_hist(channel, run_period, cut, e, t_bin_index):
    if e == 12:
        hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_{constants.T_BIN_DICT[t_bin_index]};1'
    else:
        hist_name = f'{channel}_kstar_{cut}_cut_beam_{constants.BEAM_DICT[e]}_t_{constants.T_BIN_DICT[t_bin_index]};1'
    signal_mc_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'signal', filtered=False, hist=True)
    # print(signal_mc_file_and_tree[0])
    # print(hist_name)
    signal_mc_hist_file = ROOT.TFile(signal_mc_file_and_tree[0])
    signal_mc_hist = signal_mc_hist_file.Get(hist_name)
    signal_mc_hist.SetDirectory(0)
    return signal_mc_hist


def get_integrated_data_hist(channel, run_period, cut):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_full;1'
    data_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'data', filtered=False, hist=True)
    data_hist_file = ROOT.TFile(data_file_and_tree[0])
    print(data_file_and_tree[0])
    data_hist = data_hist_file.Get(hist_name)
    print(hist_name)
    data_hist.SetDirectory(0)
    return data_hist


def get_integrated_signal_mc_hist(channel, run_period, cut):
    hist_name = f'{channel}_cut_kstar_{cut}_cut_beam_full_t_full;1'
    signal_mc_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'signal', filtered=False, hist=True)
    signal_mc_hist_file = ROOT.TFile(signal_mc_file_and_tree[0])
    signal_mc_hist = signal_mc_hist_file.Get(hist_name)
    signal_mc_hist.SetDirectory(0)
    return signal_mc_hist


def get_integrated_phasespace_recon_hist(channel, run_period, cut):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_full;1'
    recon_phasespace_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'phasespace', filtered=False, hist=True)
    recon_phasespace_file = ROOT.TFile(recon_phasespace_file_and_tree[0])
    recon_hist = recon_phasespace_file.Get(hist_name)
    recon_hist.SetDirectory(0)
    return recon_hist


def get_integrated_phasespace_thrown_hist(channel, run_period):
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(
        channel, run_period, phasespace=True)
    thrown_phasespace_file = ROOT.TFile(thrown_phasespace_file_and_tree[0])
    thrown_hist_name = f'{channel};1'
    thrown_hist = thrown_phasespace_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_integrated_signal_thrown_hist(channel, run_period):
    thrown_phasespace_file_and_tree = get_flat_file_and_tree(
        channel, run_period, 'signal', filtered=False, hist=True, thrown=True)
    thrown_phasespace_file = ROOT.TFile(thrown_phasespace_file_and_tree[0])
    thrown_hist_name = f'{channel};1'
    thrown_hist = thrown_phasespace_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def acceptance_correct_histo(data_hist: ROOT.TH1, recon_hist: ROOT.TH1, thrown_hist: ROOT.TH1):
    data_hist.Sumw2()
    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)

    ac_data_hist = data_hist.Clone()
    ac_data_hist.Divide(acceptance_hist)
    ac_data_hist.SetDirectory(0)

    return ac_data_hist


def acceptance_correct_binned_kkpi_data(channel, run_period, cut, e, t_bin_index):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    data_hist = get_binned_data_hist(channel, run_period, cut, e, t_bin_index)
    recon_hist = get_binned_phasespace_recon_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(
        channel, run_period, e, t_bin_index)

    ac_data_hist = acceptance_correct_histo(data_hist, recon_hist, thrown_hist)
    ac_data_hist.SetDirectory(0)

    return ac_data_hist


def get_gluex1_binned_kkpi_data(channel, cut, e, t_bin_index):
    hist_spring = get_binned_data_hist(channel, 'spring', cut, e, t_bin_index)
    hist_fall = get_binned_data_hist(channel, 'fall', cut, e, t_bin_index)
    hist_2017 = get_binned_data_hist(channel, '2017', cut, e, t_bin_index)

    hist_spring.Sumw2()
    hist_fall.Sumw2()
    hist_2017.Sumw2()

    hist_total = hist_spring.Clone()
    hist_total.Add(hist_fall)
    hist_total.Add(hist_2017)

    hist_total.SetDirectory(0)

    return hist_total


def get_gluex1_binned_kkpi_signal_mc(channel, cut, e, t_bin_index):
    hist_spring = get_binned_signal_mc_hist(
        channel, 'spring', cut, e, t_bin_index)
    hist_fall = get_binned_signal_mc_hist(channel, 'fall', cut, e, t_bin_index)
    hist_2017 = get_binned_signal_mc_hist(channel, '2017', cut, e, t_bin_index)

    hist_spring.Sumw2()
    hist_fall.Sumw2()
    hist_2017.Sumw2()

    lumi_spring = get_luminosity('spring', e-0.5, e+0.5)
    lumi_fall = get_luminosity('fall', e-0.5, e+0.5)
    lumi_2017 = get_luminosity('2017', e-0.5, e+0.5)
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    hist_spring.Scale(lumi_spring/lumi_total)
    hist_fall.Scale(lumi_fall/lumi_total)
    hist_2017.Scale(lumi_2017/lumi_total)

    hist_total = hist_spring.Clone()
    hist_total.Add(hist_fall)
    hist_total.Add(hist_2017)

    hist_total.SetDirectory(0)

    return hist_total


def get_gluex1_binned_avg_phasespace_acceptance(channel, cut, e, t_bin_index):
    acceptance_spring = get_binned_phasespace_acceptance(
        channel, 'spring', e, t_bin_index, cut)
    acceptance_fall = get_binned_phasespace_acceptance(
        channel, 'fall', e, t_bin_index, cut)
    acceptance_2017 = get_binned_phasespace_acceptance(
        channel, '2017', e, t_bin_index, cut)

    acceptance_spring.Sumw2()
    acceptance_fall.Sumw2()
    acceptance_2017.Sumw2()

    lumi_spring = get_luminosity('spring', e-0.5, e+0.5)
    lumi_fall = get_luminosity('fall', e-0.5, e+0.5)
    lumi_2017 = get_luminosity('2017', e-0.5, e+0.5)
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    scaled_acceptance_spring = acceptance_spring.Clone()
    scaled_acceptance_spring.Scale(lumi_spring/lumi_total)
    scaled_acceptance_fall = acceptance_fall.Clone()
    scaled_acceptance_fall.Scale(lumi_fall/lumi_total)
    scaled_acceptance_2017 = acceptance_2017.Clone()
    scaled_acceptance_2017.Scale(lumi_2017/lumi_total)

    avg_acceptance = scaled_acceptance_spring.Clone()
    avg_acceptance.Add(scaled_acceptance_fall)
    avg_acceptance.Add(scaled_acceptance_2017)

    avg_acceptance.SetDirectory(0)

    return avg_acceptance


def acceptance_correct_all_binned_gluex1_kkpi_data_with_phasespace(channel, cut, e, t_bin_index):

    data_hist = get_gluex1_binned_kkpi_data(channel, cut, e, t_bin_index)
    acceptance_hist = get_gluex1_binned_avg_phasespace_acceptance(
        channel, cut, e, t_bin_index)

    data_hist.Sumw2()
    acceptance_hist.Sumw2()

    corrected_hist = data_hist.Clone()
    corrected_hist.Divide(acceptance_hist)

    corrected_hist.SetDirectory(0)

    return corrected_hist


def get_acceptance_corrected_signal_mc(channel, run_period, cut, e, t_bin_index, n_bins=150):

    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    signal_df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

    if channel == 'pipkmks':
        kstar_cut_dict = kcuts.KSTAR_CUT_DICT_PIPKMKS
    elif channel == 'pimkpks':
        kstar_cut_dict = kcuts.KSTAR_CUT_DICT_PIMKPKS

    signal_df = (signal_df.Filter(kstar_cut_dict[cut]).
                 Filter(f'mand_t > {constants.T_CUT_DICT[t_bin_index][0]} && mand_t < {constants.T_CUT_DICT[t_bin_index][1]}').
                 Filter(f'e_beam > {e - 0.5} && e_beam < {e + 0.5}'))
    # reduce signal_df to 0.5% of it's size for error bar handling
    signal_df = signal_df.Range(0, int(signal_df.Count().GetValue() / 10))

    signal_hist = signal_df.Histo1D(
        (f'data_hist_{run_period}', f'data_hist_{run_period}', n_bins, 1.0, 2.5), f'{channel}_m').GetValue()
    recon_hist = get_binned_phasespace_recon_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(
        channel, run_period, e, t_bin_index)

    ac_signal_hist = acceptance_correct_histo(
        signal_hist, recon_hist, thrown_hist)
    ac_signal_hist.SetDirectory(0)
    return ac_signal_hist


def accepptance_correct_all_gluex1_kkpi_signal_mc_with_phasespace(channel, cut, e, t_bin_index, n_bins=30):
    hist_spring = get_acceptance_corrected_signal_mc(
        channel, 'spring', cut, e, t_bin_index)
    hist_fall = get_acceptance_corrected_signal_mc(
        channel, 'fall', cut, e, t_bin_index)
    hist_2017 = get_acceptance_corrected_signal_mc(
        channel, '2017', cut, e, t_bin_index)

    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    ac_signal_hist_total = hist_spring.Clone()
    ac_signal_hist_total.Scale(lumi_spring / lumi_total)
    ac_signal_hist_total.Add(hist_fall, lumi_fall / lumi_total)
    ac_signal_hist_total.Add(hist_2017, lumi_2017 / lumi_total)

    ac_signal_hist_total.SetDirectory(0)
    return ac_signal_hist_total


def calculate_crosssection_from_acceptance_corrected_yield(ac_yield, luminosity, bin_width, branching_fraction):
    """returns cross section for kkpi with multiplicity of 6"""
    return (ac_yield / (luminosity * bin_width * branching_fraction * 6))


def calculate_crosssection(data_yield, acceptance, luminosity, bin_width, branching_fraction):
    """returns cross section for kkpi with multiplicity of 6 in nb"""
    return (6 * data_yield / (acceptance * luminosity * bin_width * branching_fraction))


def get_binned_integrated_phasespace_acceptance(channel, run_period, e, t_bin_index, cut='all', range_lower=1.0, range_upper=2.5):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    recon_hist = get_binned_phasespace_recon_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(
        channel, run_period, e, t_bin_index)

    acceptance = recon_hist.Integral(recon_hist.FindBin(range_lower), recon_hist.FindBin(
        range_upper)) / thrown_hist.Integral(thrown_hist.FindBin(range_lower), thrown_hist.FindBin(range_upper))
    return acceptance


def get_binned_phasespace_acceptance(channel, run_period, e, t_bin_index, cut):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    recon_hist = get_binned_phasespace_recon_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(
        channel, run_period, e, t_bin_index)

    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)
    return acceptance_hist


def get_integrated_phasespace_acceptance(channel, run_period, cut):
    recon_hist = get_integrated_phasespace_recon_hist(channel, run_period, cut)
    thrown_hist = get_integrated_phasespace_thrown_hist(channel, run_period)

    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)

    acceptance_hist.SetDirectory(0)

    return acceptance_hist


def get_phasespace_acceptance(channel, run_period, cut, e, t_bin_index):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    recon_hist = get_binned_phasespace_recon_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(
        channel, run_period, e, t_bin_index)

    acceptance = recon_hist.Integral() / thrown_hist.Integral()
    return acceptance


def get_integrated_gluex1_data(channel, cut):
    data_hist_spring = get_integrated_data_hist(channel, 'spring', cut)
    data_hist_fall = get_integrated_data_hist(channel, 'fall', cut)
    data_hist_2017 = get_integrated_data_hist(channel, '2017', cut)

    data_hist_spring.Sumw2()
    data_hist_fall.Sumw2()
    data_hist_2017.Sumw2()

    data_hist_total = data_hist_spring.Clone()
    data_hist_total.Add(data_hist_fall)
    data_hist_total.Add(data_hist_2017)

    data_hist_total.SetDirectory(0)
    return data_hist_total


def get_integrated_gluex1_avg_phasespace_acceptance(channel, cut):
    acceptance_spring = get_integrated_phasespace_acceptance(
        channel, 'spring', cut)
    acceptance_fall = get_integrated_phasespace_acceptance(
        channel, 'fall', cut)
    acceptance_2017 = get_integrated_phasespace_acceptance(
        channel, '2017', cut)

    acceptance_spring.Sumw2()
    acceptance_fall.Sumw2()
    acceptance_2017.Sumw2()

    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    acceptance_spring.Scale(lumi_spring / lumi_total)
    acceptance_fall.Scale(lumi_fall / lumi_total)
    acceptance_2017.Scale(lumi_2017 / lumi_total)

    acceptance_total = acceptance_spring.Clone()
    acceptance_total.Add(acceptance_fall)
    acceptance_total.Add(acceptance_2017)

    acceptance_total.SetDirectory(0)

    return acceptance_total


def get_integrated_gluex1_phasespace_acceptance_corrected_data(channel, cut):
    data_hist = get_integrated_gluex1_data(channel, cut)
    acceptance = get_integrated_gluex1_avg_phasespace_acceptance(channel, cut)

    data_hist.Sumw2()
    acceptance.Sumw2()

    acceptance_corrected_data_hist = data_hist.Clone()
    acceptance_corrected_data_hist.Divide(acceptance)

    acceptance_corrected_data_hist.SetDirectory(0)

    return acceptance_corrected_data_hist


def get_integrated_gluex1_signal_mc(channel, cut):
    signal_mc_hist_spring = get_integrated_signal_mc_hist(
        channel, 'spring', cut)
    signal_mc_hist_fall = get_integrated_signal_mc_hist(channel, 'fall', cut)
    signal_mc_hist_2017 = get_integrated_signal_mc_hist(channel, '2017', cut)

    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    signal_mc_hist_spring.Sumw2()
    signal_mc_hist_fall.Sumw2()
    signal_mc_hist_2017.Sumw2()

    signal_mc_hist_spring.Scale(lumi_spring / lumi_total)
    signal_mc_hist_fall.Scale(lumi_fall / lumi_total)
    signal_mc_hist_2017.Scale(lumi_2017 / lumi_total)

    signal_mc_hist_total = signal_mc_hist_spring.Clone()
    signal_mc_hist_total.Add(signal_mc_hist_fall)
    signal_mc_hist_total.Add(signal_mc_hist_2017)

    signal_mc_hist_total.SetDirectory(0)
    return signal_mc_hist_total


def acceptance_correct_all_binned_gluex1_kkpi_signal_mc_with_phasespace(channel, cut, e, t_bin_index):
    signal_mc_hist = get_gluex1_binned_kkpi_signal_mc(
        channel, cut, e, t_bin_index)
    acceptance_hist = get_gluex1_binned_avg_phasespace_acceptance(
        channel, cut, e, t_bin_index)

    signal_mc_hist.Sumw2()
    acceptance_hist.Sumw2()

    corrected_hist = signal_mc_hist.Clone()
    corrected_hist.Divide(acceptance_hist)

    corrected_hist.SetDirectory(0)

    return corrected_hist


def get_integrated_gluex1_acceptance_corrected_signal_mc_with_phasespace(channel, cut):
    signal_mc_hist = get_integrated_gluex1_signal_mc(channel, cut)
    acceptance = get_integrated_gluex1_avg_phasespace_acceptance(channel, cut)

    signal_mc_hist.Sumw2()
    acceptance.Sumw2()

    acceptance_corrected_data_signal_mc = signal_mc_hist.Clone()
    acceptance_corrected_data_signal_mc.Divide(acceptance)

    acceptance_corrected_data_signal_mc.SetDirectory(0)

    return acceptance_corrected_data_signal_mc


def correct_data_hist_for_kstar_efficiency(hist):
    new_hist = hist.Clone()
    new_hist.Sumw2()
    kstar_efficiency_df = pd.read_csv(
        '/work/halld/home/viducic/data/ps_dalitz/kstar_cut_efficiency_10.0.csv')
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


def get_integrated_gluex1_kstar_corrected_data_hist(channel):
    data_hist = get_integrated_gluex1_data(channel, 'all')
    data_hist.Sumw2()
    corrected_hist = correct_data_hist_for_kstar_efficiency(data_hist)
    corrected_hist.Sumw2()
    corrected_hist.SetDirectory(0)
    return corrected_hist


def get_binned_kstar_corrected_data(channel, run_period, e, t_bin_index, cut='all'):
    validate_e_bin(e)
    validate_t_bin(t_bin_index)
    data_hist = get_binned_data_hist(channel, run_period, cut, e, t_bin_index)
    data_hist.Sumw2()
    corrected_hist = correct_data_hist_for_kstar_efficiency(data_hist)
    corrected_hist.Sumw2()
    corrected_hist.SetDirectory(0)
    return corrected_hist


def get_binned_gluex1_kstar_corrected_data(channel, e, t_bin_index, cut='all'):
    data_hist = get_gluex1_binned_kkpi_data(channel, cut, e, t_bin_index)
    data_hist.Sumw2()
    corrected_hist = correct_data_hist_for_kstar_efficiency(data_hist)
    corrected_hist.Sumw2()
    corrected_hist.SetDirectory(0)
    return corrected_hist


def get_integrated_signal_mc_hist_for_resolution_fitting(channel, run_period, nbins=500, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    # .Filter(KSTAR_CUT_DICT_PIPKMKS[cut])
    df = df.Filter(kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    hist = df.Histo1D((f'{channel}_m', f'{channel}_m',
                      nbins, 1.0, 2.5), f'{channel}_m')
    hist.Sumw2()
    hist.SetDirectory(0)
    return hist.GetValue()


def get_binned_signal_mc_hist_for_resolution_fitting(channel, run_period, e, t_bin_index, n_bins=200, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    e_cut = f'e_beam > {constants.BEAM_CUT_DICT[e][0]} && e_beam < {constants.BEAM_CUT_DICT[e][1]}'
    df = df.Filter(f't_bin == {t_bin_index}').Filter(
        e_cut)  # .Filter(KSTAR_CUT_DICT_PIPKMKS[cut])
    hist = df.Histo1D((f'{channel}_m', f'{channel}_m',
                      n_bins, xmin, xmax), f'{channel}_m')
    hist.Sumw2()
    hist.SetDirectory(0)
    return hist.GetValue()


def get_gluex1_binned_signal_mc_hist_for_resoltion_fitting(channel, e, t_bin_index, n_bins=200, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    hist_spring = get_binned_signal_mc_hist_for_resolution_fitting(
        channel, 'spring', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)
    hist_fall = get_binned_signal_mc_hist_for_resolution_fitting(
        channel, 'fall', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)
    hist_2017 = get_binned_signal_mc_hist_for_resolution_fitting(
        channel, '2017', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)

    hist_spring.Sumw2()
    hist_fall.Sumw2()
    hist_2017.Sumw2()

    hist_total = weight_histograms_by_flux(hist_spring, hist_fall, hist_2017)
    hist_total.Sumw2()
    hist_total.SetLineColor(ROOT.TColor.GetColor(
        constants.COLORBLIND_HEX_DICT['blue']))
    hist_total.SetTitle(get_binned_kkpi_hist_title(channel, e, t_bin_index))
    hist_total.GetXaxis().SetTitle('M(K^{+}K^{-}#pi^{+}) [GeV]')
    hist_total.GetYaxis().SetTitle(f'Events / {(xmax - xmin)/n_bins:.3f} GeV')

    hist_total.SetDirectory(0)
    return hist_total


def get_integrated_gluex1_signal_mc_hist_for_resolution_fitting(channel, nbins=500, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    hist_spring = get_integrated_signal_mc_hist_for_resolution_fitting(
        channel, 'spring', nbins, xmin, xmax, cut)
    hist_fall = get_integrated_signal_mc_hist_for_resolution_fitting(
        channel, 'fall', nbins, xmin, xmax, cut)
    hist_2017 = get_integrated_signal_mc_hist_for_resolution_fitting(
        channel, '2017', nbins, xmin, xmax, cut)
    combined_weighted_hist = weight_histograms_by_flux(
        hist_spring, hist_fall, hist_2017)
    combined_weighted_hist.Scale(1/scale_factor)
    combined_weighted_hist.Sumw2()
    combined_weighted_hist.SetDirectory(0)
    return combined_weighted_hist


def get_acceptance(nrecon, nthrown, error=True):
    if not error:
        return nrecon/nthrown
    else:
        error_recon = sqrt(nrecon)
        error_thrown = sqrt(nthrown)
        acceptance = nrecon/nthrown
        error = propogate_error_multiplication(
            acceptance, [nrecon, nthrown], [error_recon, error_thrown])
        return acceptance, error


def get_binned_signal_acceptance(channel, run_period, e, t_bin_index, cut='no', error=True):
    signal_hist = get_binned_signal_mc_hist(
        channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_signal_thrown_hist(
        channel, run_period, e, t_bin_index)
    return get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error)


def get_integrated_signal_acceptance(channel, run_period, cut='no', error=True):
    signal_hist = get_integrated_signal_mc_hist(channel, run_period, cut)
    thrown_hist = get_integrated_signal_mc_hist(channel, run_period)
    return get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error)


def get_binned_gluex1_signal_acceptance(channel, e, t_bin_index, cut='no', error=True):
    if e!=12:
        lumi_spring = get_luminosity('spring', e-0.5, e+0.5)
        lumi_fall = get_luminosity('fall', e-0.5, e+0.5)
        lumi_2017 = get_luminosity('2017', e-0.5, e+0.5)
    else:
        lumi_spring = get_luminosity('spring', e-5.5, e-0.5)
        lumi_fall = get_luminosity('fall', e-5.5, e-0.5)
        lumi_2017 = get_luminosity('2017', e-5.5, e-0.5)
        
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    if not error:
        weighted_acceptance_spring = get_binned_signal_acceptance(
            channel, 'spring', e, t_bin_index, cut, error) * lumi_spring
        weighted_acceptance_fall = get_binned_signal_acceptance(
            channel, 'fall', e, t_bin_index, cut, error) * lumi_fall
        weighted_acceptance_2017 = get_binned_signal_acceptance(
            channel, '2017', e, t_bin_index, cut, error) * lumi_2017

        return (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total
    else:
        error_spring = 0.0
        error_fall = 0.0
        error_2017 = 0.0
        acceptance_spring, error_spring = get_binned_signal_acceptance(
            channel, 'spring', e, t_bin_index, cut)
        acceptance_fall, error_fall = get_binned_signal_acceptance(
            channel, 'fall', e, t_bin_index, cut)
        acceptance_2017, error_2017 = get_binned_signal_acceptance(
            channel, '2017', e, t_bin_index, cut)

        weighted_acceptance_spring = acceptance_spring * lumi_spring
        weighted_acceptance_fall = acceptance_fall * lumi_fall
        weighted_acceptance_2017 = acceptance_2017 * lumi_2017
        total_acceptance = (weighted_acceptance_spring +
                            weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total

        weighted_error_spring = error_spring * lumi_spring
        weighted_error_fall = error_fall * lumi_fall
        weighted_error_2017 = error_2017 * lumi_2017
        total_error = (weighted_error_spring +
                       weighted_error_fall + weighted_error_2017)/lumi_total

        return total_acceptance, total_error


def get_integrated_gluex1_signal_acceptance(channel, cut='no', error=True):
    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    if not error:
        weighted_acceptance_spring = get_integrated_signal_acceptance(
            channel, 'spring', cut) * lumi_spring
        weighted_acceptance_fall = get_integrated_signal_acceptance(
            channel, 'fall', cut) * lumi_fall
        weighted_acceptance_2017 = get_integrated_signal_acceptance(
            channel, '2017', cut) * lumi_2017
        return (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total
    else:
        error_spring = 0.0
        error_fall = 0.0
        error_2017 = 0.0
        acceptance_spring, error_spring = get_integrated_signal_acceptance(
            channel, 'spring', cut)
        acceptance_fall, error_fall = get_integrated_signal_acceptance(
            channel, 'fall', cut)
        acceptance_2017, error_2017 = get_integrated_signal_acceptance(
            channel, '2017', cut)

        weighted_acceptance_spring = acceptance_spring * lumi_spring
        weighted_acceptance_fall = acceptance_fall * lumi_fall
        weighted_acceptance_2017 = acceptance_2017 * lumi_2017
        total_acceptance = (weighted_acceptance_spring +
                            weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total

        weighted_error_spring = error_spring * lumi_spring
        weighted_error_fall = error_fall * lumi_fall
        weighted_error_2017 = error_2017 * lumi_2017
        total_error = (weighted_error_spring +
                       weighted_error_fall + weighted_error_2017)/lumi_total
        return total_acceptance, total_error


def set_sqrtN_error(hist):
    for i in range(1, hist.GetNbinsX()+1):
        error = np.sqrt(hist.GetBinContent(i))
        hist.SetBinError(i, error)


# this is legit awful code. im sorry if anyone in the future needs to use this
def get_integrated_acceptance_corrected_signal_mc_for_resolution_fitting(channel, n_bins, cut, scale_factor=1):
    if channel == 'pipkmks':
        kstar_cut = kcuts.KSTAR_CUT_DICT_PIPKMKS[cut]
    elif channel == 'pimkpks':
        kstar_cut = kcuts.KSTAR_CUT_DICT_PIMKPKS[cut]

    file_and_tree_spring = get_flat_file_and_tree(channel, "spring", 'signal')
    file_and_tree_fall = get_flat_file_and_tree(channel, "fall", 'signal')
    file_and_tree_2017 = get_flat_file_and_tree(channel, "2017", 'signal')

    signal_df_spring = ROOT.RDataFrame(
        file_and_tree_spring[1], file_and_tree_spring[0])
    signal_df_fall = ROOT.RDataFrame(
        file_and_tree_fall[1], file_and_tree_fall[0])
    signal_df_2017 = ROOT.RDataFrame(
        file_and_tree_2017[1], file_and_tree_2017[0])

    recon_phasespace_file_and_tree_spring = get_flat_file_and_tree(
        channel, "spring", 'phasespace')
    recon_phasespace_file_and_tree_fall = get_flat_file_and_tree(
        channel, "fall", 'phasespace')
    recon_phasespace_file_and_tree_2017 = get_flat_file_and_tree(
        channel, "2017", 'phasespace')

    thrown_phasespace_file_and_tree_spring = get_flat_thrown_file_and_tree(
        channel, "spring", phasespace=True)
    thrown_phasespace_file_and_tree_fall = get_flat_thrown_file_and_tree(
        channel, "fall", phasespace=True)
    thrown_phasespace_file_and_tree_2017 = get_flat_thrown_file_and_tree(
        channel, "2017", phasespace=True)

    recon_df_spring = ROOT.RDataFrame(
        recon_phasespace_file_and_tree_spring[1], recon_phasespace_file_and_tree_spring[0])
    recon_df_fall = ROOT.RDataFrame(
        recon_phasespace_file_and_tree_fall[1], recon_phasespace_file_and_tree_fall[0])
    recon_df_2017 = ROOT.RDataFrame(
        recon_phasespace_file_and_tree_2017[1], recon_phasespace_file_and_tree_2017[0])

    thrown_file_spring = ROOT.TFile.Open(
        thrown_phasespace_file_and_tree_spring[0], 'READ')
    thrown_file_fall = ROOT.TFile.Open(
        thrown_phasespace_file_and_tree_fall[0], 'READ')
    thrown_file_2017 = ROOT.TFile.Open(
        thrown_phasespace_file_and_tree_2017[0], 'READ')
    # print(thrown_phasespace_file_and_tree[0])

    signal_df_spring = signal_df_spring.Filter(
        kstar_cut).Filter(kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    signal_df_fall = signal_df_fall.Filter(kstar_cut).Filter(
        kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    signal_df_2017 = signal_df_2017.Filter(kstar_cut).Filter(
        kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    # reduce signal_df size

    signal_df_spring = signal_df_spring.Range(
        0, int(signal_df_spring.Count().GetValue() / scale_factor))
    signal_df_fall = signal_df_fall.Range(
        0, int(signal_df_fall.Count().GetValue() / scale_factor))
    signal_df_2017 = signal_df_2017.Range(
        0, int(signal_df_2017.Count().GetValue() / scale_factor))

    recon_df_spring = recon_df_spring.Filter(kstar_cut).Filter(
        kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    recon_df_fall = recon_df_fall.Filter(kstar_cut).Filter(
        kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)
    recon_df_2017 = recon_df_2017.Filter(kstar_cut).Filter(
        kcuts.T_RANGE).Filter(kcuts.BEAM_RANGE)

    signal_hist_spring = signal_df_spring.Histo1D(
        ('data_hist_"spring"', 'data_hist_"spring"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    signal_hist_fall = signal_df_fall.Histo1D(
        ('data_hist_"fall"', 'data_hist_"fall"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    signal_hist_2017 = signal_df_2017.Histo1D(
        ('data_hist_"2017"', 'data_hist_"2017"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()

    recon_hist_spring = recon_df_spring.Histo1D(
        ('recon_hist_spring', 'recon_hist_spring', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    recon_hist_fall = recon_df_fall.Histo1D(
        ('recon_hist_fall', 'recon_hist_fall', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    recon_hist_2017 = recon_df_2017.Histo1D(
        ('recon_hist_2017', 'recon_hist_2017', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()

    thrown_hist_name = channel + f'_f1_res_{n_bins};1'
    thrown_hist_spring = thrown_file_spring.Get(thrown_hist_name)
    thrown_hist_fall = thrown_file_fall.Get(thrown_hist_name)
    thrown_hist_2017 = thrown_file_2017.Get(thrown_hist_name)

    signal_hist_spring.Sumw2()
    recon_hist_spring.Sumw2()
    thrown_hist_spring.Sumw2()
    signal_hist_fall.Sumw2()
    recon_hist_fall.Sumw2()
    thrown_hist_fall.Sumw2()
    signal_hist_2017.Sumw2()
    recon_hist_2017.Sumw2()
    thrown_hist_2017.Sumw2()

    lumi_spring = get_luminosity("spring")
    lumi_fall = get_luminosity("fall")
    lumi_2017 = get_luminosity("2017")
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    signal_hist_spring.Scale(lumi_spring / lumi_total)
    signal_hist_fall.Scale(lumi_fall / lumi_total)
    signal_hist_2017.Scale(lumi_2017 / lumi_total)

    signal_hist_total = signal_hist_spring.Clone()
    signal_hist_total.Add(signal_hist_fall)
    signal_hist_total.Add(signal_hist_2017)

    acceptance_spring = recon_hist_spring.Clone()
    acceptance_spring.Divide(thrown_hist_spring)
    acceptance_spring.Scale(lumi_spring / lumi_total)
    acceptance_fall = recon_hist_fall.Clone()
    acceptance_fall.Divide(thrown_hist_fall)
    acceptance_fall.Scale(lumi_fall / lumi_total)
    acceptance_2017 = recon_hist_2017.Clone()
    acceptance_2017.Divide(thrown_hist_2017)
    acceptance_2017.Scale(lumi_2017 / lumi_total)

    acceptance_total = acceptance_spring.Clone()
    acceptance_total.Add(acceptance_fall)
    acceptance_total.Add(acceptance_2017)

    acceptance_corrected_signal_mc_hist = signal_hist_total.Clone()
    acceptance_corrected_signal_mc_hist.Divide(acceptance_total)

    acceptance_corrected_signal_mc_hist.SetDirectory(0)
    return acceptance_corrected_signal_mc_hist


def check_run_period(run_period):
    if run_period not in constants.ALLOWED_RUN_PERIODS:
        error_message = f"Run period {run_period} not allowed. Allowed run periods are: {constants.ALLOWED_RUN_PERIODS}"
        raise ValueError(error_message)
    return True


def check_channel(channel):
    if channel not in constants.ALLOWED_CHANNELS:
        error_message = f"Channel {channel} not allowed. Allowed channels are: {constants.ALLOWED_CHANNELS}"
        raise ValueError(error_message)


def check_datatype_recon(datatype):
    if datatype not in constants.ALLOWED_DATATYPES_RECON:
        error_message = f"Datatype {datatype} not allowed. Allowed datatypes are: {constants.ALLOWED_DATATYPES_RECON}"
        raise ValueError(error_message)


def check_nstar_mass(nstar_mass):
    if nstar_mass not in constants.ALLOWED_NSTAR_MASSES:
        error_message = f"Nstar mass {nstar_mass} not allowed. Allowed nstar masses are: {constants.ALLOWED_NSTAR_MASSES}"
        raise ValueError(error_message)


def check_kstar_charge(channel, kstar_charge):
    if channel == 'pipkmks' and kstar_charge not in ['zero', 'plus']:
        error_message = f'Kstar charge {kstar_charge} not allowed for channel {channel}. Allowed kstar charges are: ["zero", "plus"]'
        raise ValueError(error_message)
    elif channel == 'pimkpks' and kstar_charge not in ['zero', 'minus']:
        error_message = f'Kstar charge {kstar_charge} not allowed for channel {channel}. Allowed kstar charges are: ["zero", "minus"]'
        raise ValueError(error_message)


def check_datatype_thrown(datatype):
    if datatype not in constants.ALLOWED_DATATYPES_THROWN:
        error_message = f"Datatype {datatype} not allowed. Allowed datatypes are: {constants.ALLOWED_DATATYPES_THROWN}"
        raise ValueError(error_message)


def verify_args(channel, run_period, datatype, nstar_mass=None, kstar_charge=None):
    check_run_period(run_period)
    check_channel(channel)
    check_datatype_recon(datatype)
    if datatype == 'nstar':
        check_nstar_mass(nstar_mass)
    if datatype == 'f1_1420':
        check_kstar_charge(channel, kstar_charge)
    return True


def verify_thrown_args(channel, run_period, datatype):
    check_run_period(run_period)
    check_channel(channel)
    check_datatype_thrown(datatype)
    return True


@ROOT.Numba.Declare(['float', 'float', 'float'], 'float')
def get_theta(px, py, pz):
    return np.degrees(np.arctan2(np.sqrt(px**2 + py**2), pz))


@ROOT.Numba.Declare(['float', 'float'], 'float')
def get_phi(px, py):
    return np.degrees(np.arctan2(py, px))


@ROOT.Numba.Declare(['float', 'float', 'float'], 'float')
def get_p(px, py, pz):
    return np.sqrt(px*px + py*py + pz*pz)


@ROOT.Numba.Declare(['float', 'float', 'float', 'float'], 'float')
def get_m(px, py, pz, E):
    return np.sqrt(E*E - px*px - py*py - pz*pz)


def define_pimkpks_columns(df):
    new_df = df.Define('chi2ndf', 'kin_chisq/kin_ndf')

    new_df = new_df.Define('p_p', 'Numba::get_p(p_px, p_py, p_pz)')
    new_df = new_df.Define('pim1_p', 'Numba::get_p(pim1_px, pim1_py, pim1_pz)')
    new_df = new_df.Define('pim2_p', 'Numba::get_p(pim2_px, pim2_py, pim2_pz)')
    new_df = new_df.Define('pip_p', 'Numba::get_p(pip_px, pip_py, pip_pz)')
    new_df = new_df.Define('kp_p', 'Numba::get_p(kp_px, kp_py, kp_pz)')

    new_df = new_df.Define('p_theta', 'Numba::get_theta(p_px, p_py, p_pz)')
    new_df = new_df.Define(
        'pim1_theta', 'Numba::get_theta(pim1_px, pim1_py, pim1_pz)')
    new_df = new_df.Define(
        'pim2_theta', 'Numba::get_theta(pim2_px, pim2_py, pim2_pz)')
    new_df = new_df.Define(
        'pip_theta', 'Numba::get_theta(pip_px, pip_py, pip_pz)')
    new_df = new_df.Define('kp_theta', 'Numba::get_theta(kp_px, kp_py, kp_pz)')

    new_df = new_df.Define('p_phi', 'Numba::get_phi(p_px, p_py)')
    new_df = new_df.Define('pim1_phi', 'Numba::get_phi(pim1_px, pim1_py)')
    new_df = new_df.Define('pim2_phi', 'Numba::get_phi(pim2_px, pim2_py)')
    new_df = new_df.Define('pip_phi', 'Numba::get_phi(pip_px, pip_py)')
    new_df = new_df.Define('kp_phi', 'Numba::get_phi(kp_px, kp_py)')

    new_df = new_df.Define(
        'p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')

    new_df = new_df.Define('ks_px', "pim2_px + pip_px")
    new_df = new_df.Define('ks_py', "pim2_py + pip_py")
    new_df = new_df.Define('ks_pz', "pim2_pz + pip_pz")
    new_df = new_df.Define('ks_E', "pim2_E + pip_E")
    new_df = new_df.Define('ks_p', 'Numba::get_p(ks_px, ks_py, ks_pz)')
    new_df = new_df.Define('ks_theta', 'Numba::get_theta(ks_px, ks_py, ks_pz)')
    new_df = new_df.Define('ks_phi', 'Numba::get_phi(ks_px, ks_py)')
    new_df = new_df.Define('ks_m', "Numba::get_m(ks_px, ks_py, ks_pz, ks_E)")

    new_df = new_df.Define(
        'ks_px_measured', "pim2_px_measured + pip_px_measured")
    new_df = new_df.Define(
        'ks_py_measured', "pim2_py_measured + pip_py_measured")
    new_df = new_df.Define(
        'ks_pz_measured', "pim2_pz_measured + pip_pz_measured")
    new_df = new_df.Define('ks_E_measured', "pim2_E_measured + pip_E_measured")
    new_df = new_df.Define(
        'ks_m_measured', "Numba::get_m(ks_px_measured, ks_py_measured, ks_pz_measured, ks_E_measured)")

    new_df = new_df.Define(
        'mxpx_ppimkpks', '-p_px_measured - pim1_px_measured - kp_px_measured - ks_px_measured')
    new_df = new_df.Define(
        'mxpy_ppimkpks', '-p_py_measured - pim1_py_measured - kp_py_measured - ks_py_measured')
    new_df = new_df.Define(
        'mxpz_ppimkpks', 'e_beam - p_pz_measured - pim1_pz_measured - kp_pz_measured - ks_pz_measured')
    new_df = new_df.Define(
        'mxe_ppimkpks', 'e_beam + 0.938272088 - p_E_measured - pim1_E_measured - kp_E_measured - ks_E_measured')
    new_df = new_df.Define(
        'mx2_ppimkpks', 'mxe_ppimkpks*mxe_ppimkpks - mxpx_ppimkpks*mxpx_ppimkpks - mxpy_ppimkpks*mxpy_ppimkpks - mxpz_ppimkpks*mxpz_ppimkpks')

    new_df = new_df.Define('ppim_px', 'pim1_px + p_px')
    new_df = new_df.Define('ppim_py', 'pim1_py + p_py')
    new_df = new_df.Define('ppim_pz', 'pim1_pz + p_pz')
    new_df = new_df.Define('ppim_E', 'pim1_E + p_E')
    new_df = new_df.Define(
        'ppim_m', 'Numba::get_m(ppim_px, ppim_py, ppim_pz, ppim_E)')

    new_df = new_df.Define('missing_px', '-p_px - pim1_px - ks_px - kp_px')
    new_df = new_df.Define('missing_py', '-p_py - pim1_py - ks_py - kp_py')
    new_df = new_df.Define(
        'missing_pz', 'e_beam - p_pz - pim1_pz - ks_pz - kp_pz')
    new_df = new_df.Define(
        'missing_E', 'e_beam + 0.938 - p_E - pim1_E - ks_E - kp_E')

    new_df = new_df.Define(
        'missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

    new_df = new_df.Define('kpp_px', 'p_px + kp_px')
    new_df = new_df.Define('kpp_py', 'p_py + kp_py')
    new_df = new_df.Define('kpp_pz', 'p_pz + kp_pz')
    new_df = new_df.Define('kpp_E', 'p_E + kp_E')
    new_df = new_df.Define(
        'kpp_m', 'Numba::get_m(kpp_px, kpp_py, kpp_pz, kpp_E)')

    new_df = new_df.Define('ksp_px', 'p_px + ks_px')
    new_df = new_df.Define('ksp_py', 'p_py + ks_py')
    new_df = new_df.Define('ksp_pz', 'p_pz + ks_pz')
    new_df = new_df.Define('ksp_E', 'p_E + ks_E')
    new_df = new_df.Define(
        'ksp_m', 'Numba::get_m(ksp_px, ksp_py, ksp_pz, ksp_E)')

    new_df = new_df.Define('kspim_px', 'pim1_px + ks_px')
    new_df = new_df.Define('kspim_py', 'pim1_py + ks_py')
    new_df = new_df.Define('kspim_pz', 'pim1_pz + ks_pz')
    new_df = new_df.Define('kspim_E', 'pim1_E + ks_E')
    new_df = new_df.Define(
        'kspim_m', 'Numba::get_m(kspim_px, kspim_py, kspim_pz, kspim_E)')

    new_df = new_df.Define('kppim_px', 'pim1_px + kp_px')
    new_df = new_df.Define('kppim_py', 'pim1_py + kp_py')
    new_df = new_df.Define('kppim_pz', 'pim1_pz + kp_pz')
    new_df = new_df.Define('kppim_E', 'pim1_E + kp_E')
    new_df = new_df.Define(
        'kppim_m', 'Numba::get_m(kppim_px, kppim_py, kppim_pz, kppim_E)')

    new_df = new_df.Define('pimkpks_px', 'pim1_px + kp_px + ks_px')
    new_df = new_df.Define('pimkpks_py', 'pim1_py + kp_py + ks_py')
    new_df = new_df.Define('pimkpks_pz', 'pim1_pz + kp_pz + ks_pz')
    new_df = new_df.Define('pimkpks_E', 'pim1_E + kp_E + ks_E')

    new_df = new_df.Define('pimkpks_px_measured',
                           "pim1_px_measured + kp_px_measured + ks_px_measured")
    new_df = new_df.Define('pimkpks_py_measured',
                           "pim1_py_measured + kp_py_measured + ks_py_measured")
    new_df = new_df.Define('pimkpks_pz_measured',
                           "pim1_pz_measured + kp_pz_measured + ks_pz_measured")
    new_df = new_df.Define(
        'pimkpks_pt', 'sqrt(pimkpks_px_measured*pimkpks_px_measured + pimkpks_py_measured*pimkpks_py_measured)')
    new_df = new_df.Define('pimkpks_p_pt_diff', 'pimkpks_pt - p_pt')
    new_df = new_df.Define(
        'pimkpks_m', 'Numba::get_m(pimkpks_px, pimkpks_py, pimkpks_pz, pimkpks_E)')

    new_df = new_df.Define('kpks_px', 'kp_px + ks_px')
    new_df = new_df.Define('kpks_py', 'kp_py + ks_py')
    new_df = new_df.Define('kpks_pz', 'kp_pz + ks_pz')
    new_df = new_df.Define('kpks_E', 'kp_E + ks_E')
    new_df = new_df.Define(
        'kpks_m', 'Numba::get_m(kpks_px, kpks_py, kpks_pz, kpks_E)')

    new_df = new_df.Define('e_bin', kcuts.BEAM_BIN_FILTER)
    new_df = new_df.Define('t_bin', kcuts.T_BIN_FILTER)

    new_df = new_df.Define('ppip_px', 'p_px + pip_px')
    new_df = new_df.Define('ppip_py', 'p_py + pip_py')
    new_df = new_df.Define('ppip_pz', 'p_pz + pip_pz')
    new_df = new_df.Define('ppip_E', 'p_E + pip_E')
    new_df = new_df.Define(
        'ppip_m', 'Numba::get_m(ppip_px, ppip_py, ppip_pz, ppip_E)')
    return new_df


def define_pipkmks_columns(df):
    new_df = df.Define('chi2ndf', 'kin_chisq/kin_ndf')

    new_df = new_df.Define('p_p', 'Numba::get_p(p_px, p_py, p_pz)')
    new_df = new_df.Define('pip1_p', 'Numba::get_p(pip1_px, pip1_py, pip1_pz)')
    new_df = new_df.Define('pip2_p', 'Numba::get_p(pip2_px, pip2_py, pip2_pz)')
    new_df = new_df.Define('pim_p', 'Numba::get_p(pim_px, pim_py, pim_pz)')
    new_df = new_df.Define('km_p', 'Numba::get_p(km_px, km_py, km_pz)')

    new_df = new_df.Define('p_theta', 'Numba::get_theta(p_px, p_py, p_pz)')
    new_df = new_df.Define(
        'pip1_theta', 'Numba::get_theta(pip1_px, pip1_py, pip1_pz)')
    new_df = new_df.Define(
        'pip2_theta', 'Numba::get_theta(pip2_px, pip2_py, pip2_pz)')
    new_df = new_df.Define(
        'pim_theta', 'Numba::get_theta(pim_px, pim_py, pim_pz)')
    new_df = new_df.Define('km_theta', 'Numba::get_theta(km_px, km_py, km_pz)')

    new_df = new_df.Define('p_phi', 'Numba::get_phi(p_px, p_py)')
    new_df = new_df.Define('pip1_phi', 'Numba::get_phi(pip1_px, pip1_py)')
    new_df = new_df.Define('pip2_phi', 'Numba::get_phi(pip2_px, pip2_py)')
    new_df = new_df.Define('pim_phi', 'Numba::get_phi(pim_px, pim_py)')
    new_df = new_df.Define('km_phi', 'Numba::get_phi(km_px, km_py)')

    new_df = new_df.Define(
        'p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')

    new_df = new_df.Define('ks_px', "pip2_px + pim_px")
    new_df = new_df.Define('ks_py', "pip2_py + pim_py")
    new_df = new_df.Define('ks_pz', "pip2_pz + pim_pz")
    new_df = new_df.Define('ks_E', "pip2_E + pim_E")
    new_df = new_df.Define('ks_p', 'Numba::get_p(ks_px, ks_py, ks_pz)')
    new_df = new_df.Define('ks_theta', 'Numba::get_theta(ks_px, ks_py, ks_pz)')
    new_df = new_df.Define('ks_phi', 'Numba::get_phi(ks_px, ks_py)')
    new_df = new_df.Define('ks_m', "Numba::get_m(ks_px, ks_py, ks_pz, ks_E)")

    new_df = new_df.Define(
        'ks_px_measured', "pip2_px_measured + pim_px_measured")
    new_df = new_df.Define(
        'ks_py_measured', "pip2_py_measured + pim_py_measured")
    new_df = new_df.Define(
        'ks_pz_measured', "pip2_pz_measured + pim_pz_measured")
    new_df = new_df.Define('ks_E_measured', "pip2_E_measured + pim_E_measured")
    new_df = new_df.Define(
        'ks_m_measured', "Numba::get_m(ks_px_measured, ks_py_measured, ks_pz_measured, ks_E_measured)")

    new_df = new_df.Define(
        'mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
    new_df = new_df.Define(
        'mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
    new_df = new_df.Define(
        'mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
    new_df = new_df.Define(
        'mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
    new_df = new_df.Define(
        'mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')

    new_df = new_df.Define('ppip_px', 'pip1_px + p_px')
    new_df = new_df.Define('ppip_py', 'pip1_py + p_py')
    new_df = new_df.Define('ppip_pz', 'pip1_pz + p_pz')
    new_df = new_df.Define('ppip_E', 'pip1_E + p_E')
    new_df = new_df.Define(
        'ppip_m', 'Numba::get_m(ppip_px, ppip_py, ppip_pz, ppip_E)')

    new_df = new_df.Define('missing_px', '-p_px - pip1_px - ks_px - km_px')
    new_df = new_df.Define('missing_py', '-p_py - pip1_py - ks_py - km_py')
    new_df = new_df.Define(
        'missing_pz', 'e_beam - p_pz - pip1_pz - ks_pz - km_pz')
    new_df = new_df.Define(
        'missing_E', 'e_beam + 0.938 - p_E - pip1_E - ks_E - km_E')
    new_df = new_df.Define(
        'missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

    new_df = new_df.Define('kmp_px', 'p_px + km_px')
    new_df = new_df.Define('kmp_py', 'p_py + km_py')
    new_df = new_df.Define('kmp_pz', 'p_pz + km_pz')
    new_df = new_df.Define('kmp_E', 'p_E + km_E')
    new_df = new_df.Define(
        'kmp_m', 'Numba::get_m(kmp_px, kmp_py, kmp_pz, kmp_E)')

    new_df = new_df.Define('ksp_px', 'p_px + ks_px')
    new_df = new_df.Define('ksp_py', 'p_py + ks_py')
    new_df = new_df.Define('ksp_pz', 'p_pz + ks_pz')
    new_df = new_df.Define('ksp_E', 'p_E + ks_E')
    new_df = new_df.Define(
        'ksp_m', 'Numba::get_m(ksp_px, ksp_py, ksp_pz, ksp_E)')

    new_df = new_df.Define('kspip_px', 'pip1_px + ks_px')
    new_df = new_df.Define('kspip_py', 'pip1_py + ks_py')
    new_df = new_df.Define('kspip_pz', 'pip1_pz + ks_pz')
    new_df = new_df.Define('kspip_E', 'pip1_E + ks_E')
    new_df = new_df.Define(
        'kspip_m', 'Numba::get_m(kspip_px, kspip_py, kspip_pz, kspip_E)')

    new_df = new_df.Define('kmpip_px', 'pip1_px + km_px')
    new_df = new_df.Define('kmpip_py', 'pip1_py + km_py')
    new_df = new_df.Define('kmpip_pz', 'pip1_pz + km_pz')
    new_df = new_df.Define('kmpip_E', 'pip1_E + km_E')
    new_df = new_df.Define(
        'kmpip_m', 'Numba::get_m(kmpip_px, kmpip_py, kmpip_pz, kmpip_E)')

    new_df = new_df.Define('pipkmks_px', 'pip1_px + km_px + ks_px')
    new_df = new_df.Define('pipkmks_py', 'pip1_py + km_py + ks_py')
    new_df = new_df.Define('pipkmks_pz', 'pip1_pz + km_pz + ks_pz')
    new_df = new_df.Define('pipkmks_E', 'pip1_E + km_E + ks_E')

    new_df = new_df.Define('pipkmks_px_measured',
                           "pip1_px_measured + km_px_measured + ks_px_measured")
    new_df = new_df.Define('pipkmks_py_measured',
                           "pip1_py_measured + km_py_measured + ks_py_measured")
    new_df = new_df.Define('pipkmks_pz_measured',
                           "pip1_pz_measured + km_pz_measured + ks_pz_measured")
    new_df = new_df.Define(
        'pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')
    new_df = new_df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')
    new_df = new_df.Define(
        'pipkmks_m', 'Numba::get_m(pipkmks_px, pipkmks_py, pipkmks_pz, pipkmks_E)')

    new_df = new_df.Define('kmks_px', 'km_px + ks_px')
    new_df = new_df.Define('kmks_py', 'km_py + ks_py')
    new_df = new_df.Define('kmks_pz', 'km_pz + ks_pz')
    new_df = new_df.Define('kmks_E', 'km_E + ks_E')
    new_df = new_df.Define(
        'kmks_m', 'Numba::get_m(kmks_px, kmks_py, kmks_pz, kmks_E)')

    new_df = new_df.Define('e_bin', kcuts.BEAM_BIN_FILTER)
    new_df = new_df.Define('t_bin', kcuts.T_BIN_FILTER)
    return new_df


def define_pipkmks_thrown_columns(df):
    new_df = df.Define('pipkmks_px', 'PiPlus1_px + KMinus_px + Ks_px')
    new_df = new_df.Define('pipkmks_py', 'PiPlus1_py + KMinus_py + Ks_py')
    new_df = new_df.Define('pipkmks_pz', 'PiPlus1_pz + KMinus_pz + Ks_pz')
    new_df = new_df.Define('pipkmks_E', 'PiPlus1_E + KMinus_E + Ks_E')
    new_df = new_df.Define(
        'pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')
    new_df = new_df.Alias('e_beam', 'Beam_E')
    new_df = new_df.Alias('mand_t', 'men_t')
    new_df = new_df.Define('e_bin', kcuts.BEAM_BIN_FILTER)
    new_df = new_df.Define('t_bin', kcuts.T_BIN_FILTER)
    return new_df


def define_pimkpks_thrown_columns(df):
    new_df = df.Define('pimkpks_px', 'PiMinus1_px + KPlus_px + Ks_px')
    new_df = new_df.Define('pimkpks_py', 'PiMinus1_py + KPlus_py + Ks_py')
    new_df = new_df.Define('pimkpks_pz', 'PiMinus1_pz + KPlus_pz + Ks_pz')
    new_df = new_df.Define('pimkpks_E', 'PiMinus1_E + KPlus_E + Ks_E')
    new_df = new_df.Define(
        'pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')
    new_df = new_df.Alias('e_beam', 'Beam_E')
    new_df = new_df.Alias('mand_t', 'men_t')
    new_df = new_df.Define('e_bin', kcuts.BEAM_BIN_FILTER)
    new_df = new_df.Define('t_bin', kcuts.T_BIN_FILTER)
    return new_df


def define_columns(df, channel, thrown=False):
    if channel == 'pipkmks':
        if thrown:
            new_df = define_pipkmks_thrown_columns(df)
        else:
            new_df = define_pipkmks_columns(df)
    elif channel == 'pimkpks':
        if thrown:
            new_df = define_pimkpks_thrown_columns(df)
        else:
            new_df = define_pimkpks_columns(df)
    else:
        raise ValueError('Unknown channel: {}'.format(channel))
    return new_df


def filter_dataframe(df, channel):
    if channel == 'pipkmks':
        return df.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIPKMKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.P_P_CUT)
    elif channel == 'pimkpks':
        return df.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIMKPKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.P_P_CUT)
    else:
        raise ValueError('Unknown channel: {}'.format(channel))


def get_dataframe(channel, run_period, datatype, filtered=True, thrown=False, nstar_mass=None, kstar_charge=None):
    if datatype == 'nstar' and not nstar_mass:
        raise ValueError('N* mass not provided')
    if not thrown:
        if filtered:
            if run_period == 'gluex1':
                file_and_trees = [get_flat_file_and_tree(channel, 'spring', datatype), get_flat_file_and_tree(
                    channel, 'fall', datatype), get_flat_file_and_tree(channel, '2017', datatype)]
                files = ROOT.std.vector('string')()
                for file_and_tree in file_and_trees:
                    files.push_back(file_and_tree[0])
                return ROOT.RDataFrame(file_and_trees[0][1], files)
            file_and_tree = get_flat_file_and_tree(
                channel, run_period, datatype)
            return ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
        else:
            if run_period == 'gluex1':
                file_and_trees = [get_flat_file_and_tree(channel, 'spring', datatype, filtered=False), get_flat_file_and_tree(
                    channel, 'fall', datatype, filtered=False), get_flat_file_and_tree(channel, '2017', datatype, filtered=False)]
                files = ROOT.std.vector('string')()
                for file_and_tree in file_and_trees:
                    files.push_back(file_and_tree[0])
                return define_columns(ROOT.RDataFrame(file_and_trees[0][1], files), channel)
            else:
                file_and_tree = get_flat_file_and_tree(
                    channel, run_period, datatype, filtered=False, nstar_mass=nstar_mass, kstar_charge=kstar_charge)
                return define_columns(ROOT.RDataFrame(file_and_tree[1], file_and_tree[0]), channel)
    elif thrown and datatype != 'data' and not filtered:
        file_and_tree = get_flat_file_and_tree(
            channel, run_period, datatype, filtered=False, thrown=True)
        return define_columns(ROOT.RDataFrame(file_and_tree[1], file_and_tree[0]), channel, thrown=True)


def get_path_for_output_file(channel, datatype, thrown=False):
    if thrown:
        return f'/work/halld/home/viducic/data/{channel}/mc/thrown'
    if datatype == 'data':
        return f'/work/halld/home/viducic/data/{channel}/data/bestX2'
    elif datatype in ['signal', 'phasespace', 'nstar', 'f1_1420']:
        return f'/work/halld/home/viducic/data/{channel}/mc/{datatype}'
    else:
        raise ValueError('Unknown datatype: {}'.format(datatype))


def get_filename_for_output_file(channel, run_period, datatype, thrown=False, nstar_mass=None, kstar_charge=None):
    if thrown:
        return f'mc_{channel}_thrown_{datatype}_flat_results_{constants.RUN_DICT[run_period]}.root'
    output = f'{channel}'
    if datatype == 'nstar':
        check_nstar_mass(nstar_mass)
        output += f'_nstar_{nstar_mass}'
    if datatype == 'f1_1420':
        check_kstar_charge(channel, kstar_charge)
        output += f'_f1_1420_{kstar_charge}'
    output += f'_flat_result_{constants.RUN_DICT[run_period]}.root'
    return output


def get_filtered_file_output_name(channel, run_period, datatype, nstar_mass=None, kstar_charge=None):
    output_file = f'{channel}_'
    if datatype == 'nstar':
        output_file += f'nstar_{nstar_mass}_'
    if datatype == 'f1_1420':
        output_file += f'f1_1420_{kstar_charge}_'
    output_file += f'flat_filtered_{constants.RUN_DICT[run_period]}.root'
    return output_file


def get_filtered_tree_output_name(channel, datatype):
    output_tree = f'{channel}_filtered_{datatype}'
    return output_tree


def get_graph_filename(channel, run_period, datatype, nstar_mass=None, kstar_charge=None):
    output_dir = '/work/halld/home/viducic/plots/analysis_graphs/'
    filename = f'{channel}_{datatype}_'
    if datatype == 'nstar':
        filename += f'{nstar_mass}_'
    if datatype == 'f1_1420':
        filename += f'{kstar_charge}_'
    filename += f'{constants.RUN_DICT[run_period]}.dot'
    return output_dir + filename


def get_hist_name_for_flat_analysis(channel, cut=None, beam_index=0, t_index=0, thrown=False):
    if not thrown:
        if channel == 'pipkmks':
            cut_name = cut
        elif channel == 'pimkpks':
            cut_name = cut
        hist_name = f'{channel}_kstar_{cut_name}_cut_'
    else:
        hist_name = f'{channel}_'
    beam_name = 'beam_full_'
    t_name = 't_full'
    if beam_index > 0:
        beam_low = constants.BEAM_INDEX_DICT[beam_index][0]
        beam_high = constants.BEAM_INDEX_DICT[beam_index][1]
        beam_name = f'beam_{beam_low}_{beam_high}_'
    if t_index > 0:
        t_low = constants.T_CUT_DICT[t_index][0]
        t_high = constants.T_CUT_DICT[t_index][1]
        t_name = f't_{t_low}_{t_high}'
    hist_name += beam_name + t_name
    return hist_name


def fill_histos(cut_df, histo_array, channel, cut=None, beam_index=0, t_index=0, thrown=False):
    hist_name = get_hist_name_for_flat_analysis(
        channel, cut, beam_index, t_index, thrown)
    histo_array.append(cut_df.Histo1D(
        (hist_name, hist_name, 150, 1.0, 2.5), f'{channel}_m'))


def get_reduced_2d_chi2_hists(df_pipkmks, df_pimkpks, particle):
    particles = {
        'pion': ('pip1', 'pim1'),
        'kaon': ('km', 'kp'),
        'proton': ('p', 'p')
    }

    hist_pipkmks_track = df_pipkmks.Define(f'{particles[particle][0]}_chi2ndf_trk', f'{particles[particle][0]}_chisq_trk/{particles[particle][0]}_ndf_trk') \
        .Histo2D((f'pipkmks_{particles[particle][0]}_chi2ndf_trk', 'Track #Chi^{2}/ndf vs M(K^{-}K_{s}#pi^{+}) for ' + particles[particle][0], 40, 1.1, 1.5, 200, 0.0, 20.0), 'pipkmks_m',  f'{particles[particle][0]}_chi2ndf_trk')
    hist_pimkpks_track = df_pimkpks.Define(f'{particles[particle][1]}_chi2ndf_trk', f'{particles[particle][1]}_chisq_trk/{particles[particle][1]}_ndf_trk') \
        .Histo2D((f'pimkpks_{particles[particle][1]}_chi2ndf_trk', 'Track #Chi^{2}/ndf vs M(#pi^{-}K_{s}K^{+}) for ' + particles[particle][1], 40, 1.1, 1.5, 200, 0.0, 20.0), 'pimkpks_m',  f'{particles[particle][1]}_chi2ndf_trk')
    hist_pipkmks_time = df_pipkmks.Define(f'{particles[particle][0]}_chi2ndf_time', f'{particles[particle][0]}_chisq_time/{particles[particle][0]}_ndf_time') \
        .Histo2D((f'pipkmks_{particles[particle][0]}_chi2ndf_trk', 'Time #Chi^{2}/ndf vs M(K^{-}K_{s}#pi^{+}) for ' + particles[particle][0], 40, 1.1, 1.5, 200, 0.0, 20.0),  'pipkmks_m', f'{particles[particle][0]}_chi2ndf_time')
    hist_pimkpks_time = df_pimkpks.Define(f'{particles[particle][1]}_chi2ndf_time', f'{particles[particle][1]}_chisq_time/{particles[particle][1]}_ndf_time') \
        .Histo2D((f'pimkpks_{particles[particle][1]}_chi2ndf_trk', 'Time #Chi^{2}/ndf vs M(#pi^{-}K_{s}K^{+}) for ' + particles[particle][1], 40, 1.1, 1.5, 200, 0.0, 20.0),  'pimkpks_m', f'{particles[particle][1]}_chi2ndf_time')

    return hist_pipkmks_track, hist_pimkpks_track, hist_pipkmks_time, hist_pimkpks_time


def get_reduced_1d_chi2_hists(df_pipkmks, df_pimkpks, particle):
    particles = {
        'pion': ('pip1', 'pim1'),
        'kaon': ('km', 'kp'),
        'proton': ('p', 'p')
    }

    hist_pipkmks_track = df_pipkmks.Define(f'{particles[particle][0]}_chi2ndf_trk', f'{particles[particle][0]}_chisq_trk/{particles[particle][0]}_ndf_trk') \
        .Histo1D((f'pipkmks_{particles[particle][0]}_chi2ndf_trk', 'Track #Chi^{2}/ndf vs M(K^{-}K_{s}#pi^{+}) for ' + particles[particle][0], 200, 0.0, 8.0), f'{particles[particle][0]}_chi2ndf_trk')
    hist_pimkpks_track = df_pimkpks.Define(f'{particles[particle][1]}_chi2ndf_trk', f'{particles[particle][1]}_chisq_trk/{particles[particle][1]}_ndf_trk') \
        .Histo1D((f'pimkpks_{particles[particle][1]}_chi2ndf_trk', 'Track #Chi^{2}/ndf vs M(#pi^{-}K_{s}K^{+}) for ' + particles[particle][1], 200, 0.0, 8.0), f'{particles[particle][1]}_chi2ndf_trk')
    hist_pipkmks_time = df_pipkmks.Define(f'{particles[particle][0]}_chi2ndf_time', f'{particles[particle][0]}_chisq_time/{particles[particle][0]}_ndf_time') \
        .Histo1D((f'pipkmks_{particles[particle][0]}_chi2ndf_trk', 'Time #Chi^{2}/ndf vs M(K^{-}K_{s}#pi^{+}) for ' + particles[particle][0], 200, 0.0, 8.0), f'{particles[particle][0]}_chi2ndf_time')
    hist_pimkpks_time = df_pimkpks.Define(f'{particles[particle][1]}_chi2ndf_time', f'{particles[particle][1]}_chisq_time/{particles[particle][1]}_ndf_time') \
        .Histo1D((f'pimkpks_{particles[particle][1]}_chi2ndf_trk', 'Time #Chi^{2}/ndf vs M(#pi^{-}K_{s}K^{+}) for ' + particles[particle][1], 200, 0.0, 8.0), f'{particles[particle][1]}_chi2ndf_time')

    hist_pipkmks_track.SetLineColor(ROOT.TColor.GetColor(
        constants.COLORBLIND_HEX_DICT['blue']))
    hist_pipkmks_time.SetLineColor(ROOT.TColor.GetColor(
        constants.COLORBLIND_HEX_DICT['blue']))
    hist_pimkpks_track.SetLineColor(
        ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red']))
    hist_pimkpks_time.SetLineColor(ROOT.TColor.GetColor(
        constants.COLORBLIND_HEX_DICT['red']))

    return hist_pipkmks_track, hist_pimkpks_track, hist_pipkmks_time, hist_pimkpks_time


def get_tallest(hist_list: list):
    if len(hist_list) < 2:
        return 0
    tallest_index = -1
    tallest = -1
    for i in range(len(hist_list)):
        if hist_list[i].GetMaximum() > tallest:
            tallest = hist_list[i].GetMaximum()
            tallest_index = i
    return tallest_index


def sort_hists_by_max(hists: list):
    sorted_hists = []
    sorted_index = []
    while len(hists) > 0:
        tallest = get_tallest(hists)
        sorted_index.append(tallest)
        sorted_hists.append(hists.pop(tallest))
    return sorted_hists


def remove_zero_datapoints(og_hist: ROOT.TH1):
    hist = og_hist.Clone()
    for i in reversed(range(hist.GetNbinsX())):
        if hist.GetBinContent(i) == 0:
            hist_above = hist.GetBinContent(i+1)
            hist_below = hist.GetBinContent(i-1)
            error_above = hist.GetBinError(i+1)
            error_below = hist.GetBinError(i-1)
            hist_avg = (hist_above + hist_below)/2
            hist.SetBinContent(i, hist_avg)
            hist.SetBinError(i, (error_above + error_below)/2)
    hist.SetDirectory(0)
    return hist


def get_binned_resolution(channel, e, tbin):
    if e!= 12:
        df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv')
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==tbin)]['sigma'].values[0]
    else:
        df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_t_f1_mc_width.csv')
        e_t_sigma = df.loc[(df['t_bin']==tbin)]['sigma'].values[0]
    return e_t_sigma


def get_yield_and_error(hist: ROOT.TH1, func: ROOT.TF1, fitsys=False):
    voigt = ROOT.TF1(f'voigt', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetMinimumX(), func.GetMaximumX())
    for i in range(4):
        voigt.SetParameter(i, func.GetParameter(i))
    f1_yield = voigt.Integral(1.16, 1.5, 1e-7)/0.01
    if not fitsys:
        f1_error = f1_yield * calculate_rel_bootstrap_error(hist, func)
    else:
        f1_error = func.GetParError(0)
    return f1_yield, f1_error


def calculate_dataframe_info(func, hist, channel, e, t, fitsys=False):
    if e!= 12:
        e_lumi = get_luminosity_gluex_1(e-0.5, e+0.5)*1000
    else:
        e_lumi = get_luminosity_gluex_1(7.5, 11.5)*1000
    f1_yield, f1_yield_error = get_yield_and_error(hist, func, fitsys=fitsys)
    f1_acceptance = get_binned_gluex1_signal_acceptance(channel, e, t, error=False)
    f1_acceptance_error = 0 
    cross_section = calculate_crosssection(f1_yield, f1_acceptance, e_lumi, constants.T_WIDTH_DICT[t], constants.F1_KKPI_BRANCHING_FRACTION)
    cross_section_error = propogate_error_multiplication(cross_section, [f1_yield], [f1_yield_error])
    return f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error
    

def calculate_rel_bootstrap_error(hist: ROOT.TH1, f: ROOT.TF1, n_trials: int = 1000)->float:
    """
    Calculates the relative error of the amplitude of the fit function f
    It is reccomended to set batch mode to true
    """
    # print(f"performing {n_trials} boostraps")
    rng = np.random.default_rng()
    amps = []
    f_trial = f.Clone(f'ftrial')
    initial_pars = [f_trial.GetParameter(i) for i in range(f_trial.GetNpar())]
    for _ in range(n_trials):
        trial_hist = hist.Clone(f"trial")
        trial_hist.SetTitle(f"trial")
        for p in range(len(initial_pars)):
            f_trial.SetParameter(p, initial_pars[p])
        for bin in range(1, trial_hist.GetNbinsX()+1):
            val = trial_hist.GetBinContent(bin)
            std = trial_hist.GetBinError(bin)
            if val > 0:
                rel_error = std/val
            else:
                rel_error = 0
            new_val = rng.normal(val, std)
            trial_hist.SetBinContent(bin, new_val)
            trial_hist.SetBinError(bin, rel_error*new_val)
        trial_hist_cor = remove_zero_datapoints(trial_hist)
        r = trial_hist_cor.Fit(f_trial, 'SRBNQ')
        amp = f_trial.GetParameter(0)
        amps.append(amp)
    amps = np.array(amps)
    mean = amps.mean()
    var = np.where(True, (amps-mean)*(amps-mean), 0).sum()/(n_trials-1)
    return np.sqrt(var)/mean

############################
#### CONDUCT TESTS HERE ####
############################


if __name__ == '__main__':
    print('testing:')
    # df = get_dataframe('pimkpks', 'spring', 'nstar', filtered=False, nstar_mass=1440)
    # print(df.GetColumnNames())
    # print(get_path_for_output_file('pimkpks', 'nstar'))
    # df_pipkmks = get_dataframe('pipkmks', 'spring', 'data', filtered=False)
    # df_pimkpks = get_dataframe('pimkpks', 'spring', 'data')
    # hist = df_pipkmks.Histo1D('km_theta')
    # c = ROOT.TCanvas()
    # hist.Draw()
    # c.Update()
    # c.Draw()
    # input('')
    df = get_dataframe('pipkmks', 'gluex1', 'data', filtered=False)
