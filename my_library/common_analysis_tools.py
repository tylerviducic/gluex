"""
this is almost certainly not the right way to do something like this,
but lets go ahead and see if this works out. 

writing a python file that can be imported into other python files that 
contains common analysis tools/code snippets that i use
"""

import math
import ROOT
import pandas as pd
import numpy as np

### COMMONLY USED VARIABLES ###

## KSHORT FIT PARAMETERS ##

KSHORT_FIT_WIDTH = 0.01035
KSHORT_FIT_MEAN = 0.4971

## KKPI BRANCHING FRACTION ##

F1_KKPI_BRANCHING_FRACTION = 0.091
F1_KKPI_BRANCHING_FRACTION_ERROR = 0.004

## PI- K+ KS FIT PARAMETERS ##

F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA = 0.0104626
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA_ERROR = 0.0004433
F1_PIMKPKS_VOIGHT_SIGMA = 0.01043
F1_PIMKPKS_VOIGHT_SIGMA_ERROR = 0.00032003657273967957

F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN = 1.2844
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN_ERROR = 0.0004577578618949474
F1_PIMKPKS_VOIGHT_MEAN = 1.2849
F1_PIMKPKS_VOIGHT_MEAN_ERROR = 0.0003009278967198714

F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_WIDTH = 0.028369
F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_WIDTH_ERROR = 0.004577578618949474
F1_PIMKPKS_VOIGHT_WIDTH = 0.02528
F1_PIMKPKS_VOIGHT_WIDTH_ERROR = 0.001470065522229072

## PI+ K- KS FIT PARAMETERS ##

F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA = 0.0102287
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA_ERROR = 0.000273588
F1_PIPKMKS_VOIGHT_SIGMA = 0.01043
F1_PIPKMKS_VOIGHT_SIGMA_ERROR = 0.0002837264794425809

F1_PIPKMKS_VOIGHT_MEAN = 1.2795
F1_PIPKMKS_VOIGHT_MEAN_ERROR = 0.00043425186549761463
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN = 1.2787
F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN_ERROR = 0.0005084747325606598

F1_PIPKMKS_VOIGHT_WIDTH = 0.02475
F1_PIPKMKS_VOIGHT_WIDTH_ERROR = 0.0023994451637479544
F1_PIPKMKS_ACCETPANCE_CORRECTED_VOIGHT_WIDTH = 0.02631
F1_PIPKMKS_ACCETPANCE_CORRECTED_VOIGHT_WIDTH_ERROR = 0.002782548323692978

# CUT VARIABLES # 

KS_PATHLENGTH_CUT = 'pathlength_sig > 5'
KS_COLIN_CUT = 'cos_colin > 0.99'
KS_VERTEX_CUT = ' vertex_distance > 3'
OLD_KS_MASS_CUT = 'ks_m > 0.475 && ks_m < 0.525'
KS_MASS_CUT = f'abs(ks_m - {KSHORT_FIT_MEAN}) < {2 * KSHORT_FIT_WIDTH}'
PPIP_MASS_CUT = 'ppip_m > 1.4'
KMP_MASS_CUT = 'kmp_m > 1.95'
F1_SIGNAL_REGION_PIPKMKS = 'pipkmks_m > 1.2 && pipkmks_m < 1.5'
F1_SIGNAL_REGION_PIMKPKS = 'pimkpks_m > 1.2 && pimkpks_m < 1.5'
BEAM_RANGE = 'e_beam >= 6.50000000000 && e_beam <= 11.5'
T_RANGE = 'mand_t >= 0.1 && mand_t <= 1.9'
P_P_CUT = 'p_p > 0.4'
MX2_PPIPKMKS_CUT = 'abs(mx2_ppipkmks) < 0.01'
MX2_PPIMKPKS_CUT = 'abs(mx2_ppimkpks) < 0.01'
# PPIM_MASS_CUT = 'ppim_m > 1.8'
PPIM_MASS_CUT = 'ppim_m > 1.4'
KSP_MASS_CUT = 'ksp_m > 1.95'

KSTAR_NO_CUT_PIPKMKS = 'kspip_m > 0.0'
KSTAR_PLUS_CUT = 'kspip_m < 0.8 || kspip_m > 1.0'
KSTAR_MINUS_CUT = 'kspim_m < 0.8 || kspim_m > 1.0'
KSTAR_ZERO_CUT_PIPKMKS = 'kmpip_m < 0.8 || kmpip_m > 1.0'
KSTAR_ALL_CUT_PIPKMKS = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'
KEEP_NEUTRAL_REJECT_CHARGED_PIPKMKS = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m > 0.8 && kmpip_m < 1.0)'
KEEP_CHARGED_REJECT_NEUTRAL_PIPKMKS = '(kspip_m > 0.8 && kspip_m < 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

KSTAR_NO_CUT_PIMKPKS = 'kspim_m > 0.0'
KSTAR_ZERO_CUT_PIMKPKS = 'kppim_m < 0.8 || kppim_m > 1.0'
KSTAR_ALL_CUT_PIMKPKS = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'
KEEP_NEUTRAL_REJECT_CHARGED_PIMKPKS = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m > 0.8 && kppim_m < 1.0)'
KEEP_CHARGED_REJECT_NEUTRAL_PIMKPKS = '(kspim_m > 0.8 && kspim_m < 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'

# COLORBLIND HEX CODES #
COLORBLIND_HEX_DICT = { 
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#D55E00',
    'purple': '#CC78BC',
    'brown': '#CA9161',
    'pink': '#FBAFE4',
    'gray': '#949494',
    'yellow': '#ECE133',
    'cyan': '#56B4E9'
}

# MATPLOTLIB LATEX AXIS LABEL STRING #
LATEX_AXIS_LABEL_DICT = {
    't': '$-t$ (GeV$^2$)',
    'cross_section': '$\\frac{d\\sigma}{dt}$ $\\frac{nb}{GeV^2}$',
    'yield': 'counts',
    'mean': 'mean (GeV)',
    'width': 'width (GeV)',
    'chi2ndf': '$\\chi^2$/ndf',
    'pipkmks': '$\\pi^+K^-K_s$',
    'pimkpks': '$\\pi^-K^+K_s$'
}

RUN_DICT = {
    'fall': '2018_fall',
    'spring': '2018_spring',
    '2017': '2017',
    '2019_unconstrained': '2019_unconstrained',
    '2019_constrained': '2019_constrained'
        }

KSTAR_CUT_NAME_DICT_PIPKMKS = {
    KSTAR_NO_CUT_PIPKMKS: 'no',
    KSTAR_PLUS_CUT: 'plus',
    KSTAR_ZERO_CUT_PIPKMKS: 'zero',
    KSTAR_ALL_CUT_PIPKMKS: 'all'
}

KSTAR_CUT_DICT_PIPKMKS = {
    'no': KSTAR_NO_CUT_PIPKMKS,
    'plus': KSTAR_PLUS_CUT,
    'zero': KSTAR_ZERO_CUT_PIPKMKS,
    'all': KSTAR_ALL_CUT_PIPKMKS
}

KSTAR_CUT_NAME_DICT_PIMKPKS = {
    KSTAR_NO_CUT_PIMKPKS: 'no',
    KSTAR_MINUS_CUT: 'minus',
    KSTAR_ZERO_CUT_PIMKPKS: 'zero',
    KSTAR_ALL_CUT_PIMKPKS: 'all'
}

KSTAR_CUT_DICT_PIMKPKS = {
    'no': KSTAR_NO_CUT_PIMKPKS,
    'minus': KSTAR_MINUS_CUT,
    'zero': KSTAR_ZERO_CUT_PIMKPKS,
    'all': KSTAR_ALL_CUT_PIMKPKS
}

KSTAR_CUT_TITLE_DICT = {
    'no': 'No K* Rejection',
    'plus': 'K*^{+} Rejected',
    'minus': 'K*^{-} Rejected',
    'zero': 'K*^{0} Rejected',
    'all': 'Both K* Rejected'
}


ALLOWED_E_BINS = range(7, 12)
ALLOWED_T_BINS = range(1, 8)
ALLOWED_RUN_PERIODS = ['spring', 'fall', '2017']
ALLOWED_CHANNELS = ['pipkmks', 'pimkpks']
ALLOWED_DATATYPES_RECON = ['data', 'signal', 'phasespace']
ALLOWED_DATATYPES_THROWN = ['signal', 'phasespace']

T_BIN_DICT = {1: '0.1_0.2', 2: '0.2_0.3', 3: '0.3_0.4',
              4: '0.4_0.65', 5: '0.65_0.9', 
              6: '0.9_1.4', 7: '1.4_1.9'
              }

T_CUT_DICT = {0: (0.0, 0.1), 1: (0.1, 0.2), 2: (0.2, 0.3), 3: (0.3, 0.4),
              4: (0.4, 0.65), 5: (0.65, 0.9), 
              6: (0.9, 1.4), 7: (1.4, 1.9)
              }

T_WIDTH_DICT = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.25, 5: 0.25, 6: 0.5, 7: 0.5}

FLUX_DICT = {
    'fall': '50685_51768',
    'spring': '40856_42559'
        }

BEAM_DICT = {
    7: '6.5_7.5',
    8: '7.5_8.5',
    9: '8.5_9.5',
    10: '9.5_10.5',
    11: '10.5_11.5'
        }

BEAM_CUT_DICT = {
    7: (6.5, 7.5),
    8: (7.5, 8.5),
    9: (8.5, 9.5),
    10: (9.5, 10.5),
    11: (10.5, 11.5)
}

BEAM_INDEX_DICT = {
    1: (6.5, 7.5),
    2: (7.5, 8.5),
    3: (8.5, 9.5),
    4: (9.5, 10.5),
    5: (10.5, 11.5)
}

BEAM_BIN_FILTER = """
int get_beam_bin_index(double e_beam) {
        return static_cast<int>(e_beam-6.5) + 1;
}
"""

T_BIN_FILTER = """
int get_t_bin_index(double t) {
    if (t <= 0.4) {
        return static_cast<int>(t/0.1);
    }
    else if (t > 0.4 && t <= 0.9) {
        return static_cast<int>((t-0.4)/0.25)+4;
    }
    else if (t > 0.9 && t <= 1.9) {
        return static_cast<int>((t-0.9)/0.5)+6;
    }
    else {
        return -1;
    }
}
"""

F1_CUT_LIST_PIPKMKS = [KSTAR_NO_CUT_PIPKMKS, KSTAR_PLUS_CUT, KSTAR_ZERO_CUT_PIPKMKS, KSTAR_ALL_CUT_PIPKMKS]
F1_CUT_LIST_PIMKPKS = [KSTAR_NO_CUT_PIMKPKS, KSTAR_MINUS_CUT, KSTAR_ZERO_CUT_PIMKPKS, KSTAR_ALL_CUT_PIMKPKS]

###################
##### METHODS #####
###################


def get_flat_data_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/data'
    treename = ''
    if not comboloop:
        file_path += f'/bestX2/{channel}_'
        if filtered:
            file_path += f'filtered_{RUN_DICT[run_period]}.root'
            treename = f'{channel}_filtered_{RUN_DICT[run_period]}'
        else:
            if hist:
                file_path += f'flat_result_{RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{RUN_DICT[run_period]}.root'
                treename = f'{channel}__B4_M16'
    else:
        file_path += f'/comboloop/{channel}_comboloop_flat_{RUN_DICT[run_period]}.root'
        treename = f'{channel}__B4_M16'
    return (file_path, treename)


def get_flat_signal_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/mc/signal/{channel}_'
    treename = ''
    if not comboloop:
        if filtered:
            file_path += f'filtered_{RUN_DICT[run_period]}.root'
            treename = f'{channel}_filtered_{RUN_DICT[run_period]}'
        else:
            if hist:
                file_path += f'flat_result_{RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{RUN_DICT[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop signal mc file yet')
    return (file_path, treename)


def get_flat_phasespace_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/halld/home/viducic/data/{channel}/mc/phasespace/{channel}_'
    treename = ''
    if not comboloop:
        if filtered:
            file_path += f'filtered_{RUN_DICT[run_period]}.root'
            treename = f'{channel}_phasespace_filtered_{RUN_DICT[run_period]}'
        else:
            if hist:
                file_path += f'flat_result_{RUN_DICT[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{RUN_DICT[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop phasespace mc file yet')
    return (file_path, treename)


def get_flat_thrown_file_and_tree(channel, run_period, phasespace=False, hist=True):
    if not phasespace:
        if not hist:
            return (f'/volatile/halld/home/viducic/selector_output/f1_{channel}/thrown/{channel}_thrown_{RUN_DICT[run_period]}.root', f'{channel}_thrown')
        return (f'/work/halld/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_signal_flat_result_{RUN_DICT[run_period]}.root', 'pipkmks_thrown')
    elif phasespace:
        if not hist:
            return (f'/volatile/halld/home/viducic/selector_output/f1_{channel}/thrown/{channel}_phasespace_thrown_{RUN_DICT[run_period]}.root', f'{channel}_thrown')
        return(f'/work/halld/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_phasespace_flat_result_{RUN_DICT[run_period]}.root', 'pipkmks_thrown')


def get_flat_file_and_tree(channel, run_period, datatype, comboloop=False, filtered=True, hist=False, thrown=False, verbose=False):
    file_tuple = ()
    if thrown:
        if datatype == 'signal':
            file_tuple = get_flat_thrown_file_and_tree(channel, run_period, hist=hist)
        elif datatype == 'phasespace':
            file_tuple = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True, hist=hist)
        else:
            print('invalid thrown datatype')
            return
    else:
        if datatype == 'data':
            file_tuple = get_flat_data_file_and_tree(channel, run_period, comboloop, filtered, hist)
        elif datatype == 'signal':
            file_tuple = get_flat_signal_file_and_tree(channel, run_period, comboloop, filtered, hist)
        elif datatype == 'phasespace':
            file_tuple = get_flat_phasespace_file_and_tree(channel, run_period, comboloop, filtered, hist)
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
    lumi = lumi_hist.Integral(lumi_hist.FindBin(beam_low), lumi_hist.FindBin(beam_high))
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
    if t not in ALLOWED_T_BINS:
        raise ValueError('invalid t bin number')
    return True


def validate_e_bin(e):
    if e not in ALLOWED_E_BINS:
        raise ValueError('invalid e bin number')
    return True


def get_binned_kkpi_hist_title(channel, e, t_bin_index):
    validate_t_bin(t_bin_index)
    validate_e_bin(e)
    if channel == 'pipkmks':
        kkpi = 'K^{-}K_{s}#pi^{-}'
    elif channel == 'pimkpks':
        kkpi = 'K^{+}K_{s}#pi^{+}'
    else:
        return None
    return 'M({}) for E_{}={}- and t={}-{}'.format(kkpi, '{#gamma}', e-0.5, e+0.5, T_CUT_DICT[t_bin_index][0], T_CUT_DICT[t_bin_index][1])

def get_integrated_kkpi_hist_title(channel):
    if channel == 'pipkmks':
        kkpi = 'K^{-}K_{s}#pi^{-}'
    elif channel == 'pimkpks':
        kkpi = 'K^{+}K_{s}#pi^{+}'
    else:
        return None
    return 'M({}) for E_{}=6.5-11.5 and t=0.1-1.9'.format(kkpi, '{#gamma}')


def propogate_error_multiplication(target_datapoint, input_datapoints: list, input_errors: list):
    err_f2 = 0
    for i in range(len(input_datapoints)):
        err_f2 += (input_errors[i]/input_datapoints[i])**2
        return target_datapoint * math.sqrt(err_f2)


def propogate_error_addition(input_errors: list):
    err_f2 = 0
    for i in range(len(input_errors)):
        err_f2 += (input_errors[i])**2
        return math.sqrt(err_f2)


def get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index):
    hist_name = f'{channel}_cut_kstar_{cut}_cut_beam_{BEAM_DICT[e]}_t_{T_BIN_DICT[t_bin_index]};1'
    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace', filtered=False, hist=True)
    recon_phasespace_file = ROOT.TFile(recon_phasespace_file_and_tree[0])
    recon_hist = recon_phasespace_file.Get(hist_name)
    recon_hist.SetDirectory(0)
    return recon_hist


def get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index):
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
    thrown_phasespace_file = ROOT.TFile(thrown_phasespace_file_and_tree[0])
    thrown_hist_name = f'{channel}_beam_{BEAM_DICT[e]}_t_{T_BIN_DICT[t_bin_index]};1'
    thrown_hist = thrown_phasespace_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_binned_signal_thrown_hist(channel, run_period, e, t_bin_index):
    thrown_signal_file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal', filtered=False, hist=True, thrown=True)
    thrown_signal_file = ROOT.TFile(thrown_signal_file_and_tree[0])
    thrown_hist_name = f'{channel}_beam_{BEAM_DICT[e]}_t_{T_BIN_DICT[t_bin_index]};1'
    thrown_hist = thrown_signal_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_binned_data_hist(channel, run_period, cut, e, t_bin_index):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_{BEAM_DICT[e]}_t_{T_BIN_DICT[t_bin_index]};1'
    data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data', filtered=False, hist=True)
    data_hist_file = ROOT.TFile(data_file_and_tree[0])
    data_hist = data_hist_file.Get(hist_name)
    data_hist.SetDirectory(0)
    return data_hist


def get_binned_signal_mc_hist(channel, run_period, cut, e, t_bin_index):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_{BEAM_DICT[e]}_t_{T_BIN_DICT[t_bin_index]};1'
    signal_mc_file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal', filtered=False, hist=True)
    signal_mc_hist_file = ROOT.TFile(signal_mc_file_and_tree[0])
    signal_mc_hist = signal_mc_hist_file.Get(hist_name)
    signal_mc_hist.SetDirectory(0)
    return signal_mc_hist


def get_integrated_data_hist(channel, run_period, cut):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_full;1'
    data_file_and_tree = get_flat_file_and_tree(channel, run_period, 'data', filtered=False, hist=True)
    data_hist_file = ROOT.TFile(data_file_and_tree[0])
    data_hist = data_hist_file.Get(hist_name)
    data_hist.SetDirectory(0)
    return data_hist


def get_integrated_signal_mc_hist(channel, run_period, cut):
    hist_name = f'{channel}_cut_kstar_{cut}_cut_beam_full_t_full;1'
    signal_mc_file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal', filtered=False, hist=True)
    signal_mc_hist_file = ROOT.TFile(signal_mc_file_and_tree[0])
    signal_mc_hist = signal_mc_hist_file.Get(hist_name)
    signal_mc_hist.SetDirectory(0)
    return signal_mc_hist


def get_integrated_phasespace_recon_hist(channel, run_period, cut):
    hist_name = f'{channel}_kstar_{cut}_cut_beam_full_t_full;1'
    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace', filtered=False, hist=True)
    recon_phasespace_file = ROOT.TFile(recon_phasespace_file_and_tree[0])
    recon_hist = recon_phasespace_file.Get(hist_name)
    recon_hist.SetDirectory(0)
    return recon_hist


def get_integrated_phasespace_thrown_hist(channel, run_period):
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
    thrown_phasespace_file = ROOT.TFile(thrown_phasespace_file_and_tree[0])
    thrown_hist_name = f'{channel};1'
    thrown_hist = thrown_phasespace_file.Get(thrown_hist_name)
    thrown_hist.SetDirectory(0)
    return thrown_hist


def get_integrated_signal_thrown_hist(channel, run_period):
    thrown_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal', filtered=False, hist=True, thrown=True)
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
    recon_hist = get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index)

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
    hist_spring = get_binned_signal_mc_hist(channel, 'spring', cut, e, t_bin_index)
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
    acceptance_spring = get_binned_phasespace_acceptance(channel, 'spring', e, t_bin_index, cut)
    acceptance_fall = get_binned_phasespace_acceptance(channel, 'fall', e, t_bin_index, cut)
    acceptance_2017 = get_binned_phasespace_acceptance(channel, '2017', e, t_bin_index, cut)

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


def acceptance_correcst_all_binned_gluex1_kkpi_data_with_phasespace(channel, cut, e, t_bin_index):

    data_hist = get_gluex1_binned_kkpi_data(channel, cut, e, t_bin_index)
    acceptance_hist = get_gluex1_binned_avg_phasespace_acceptance(channel, cut, e, t_bin_index)

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
        kstar_cut_dict = KSTAR_CUT_DICT_PIPKMKS
    elif channel == 'pimkpks':
        kstar_cut_dict = KSTAR_CUT_DICT_PIMKPKS

    signal_df = (signal_df.Filter(kstar_cut_dict[cut]).
                 Filter(f'mand_t > {T_CUT_DICT[t_bin_index][0]} && mand_t < {T_CUT_DICT[t_bin_index][1]}').
                 Filter(f'e_beam > {e - 0.5} && e_beam < {e + 0.5}'))
    # reduce signal_df to 0.5% of it's size for error bar handling
    signal_df = signal_df.Range(0, int(signal_df.Count().GetValue() / 10))

    signal_hist = signal_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', n_bins, 1.0, 2.5), f'{channel}_m').GetValue()
    recon_hist = get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index)

    ac_signal_hist = acceptance_correct_histo(signal_hist, recon_hist, thrown_hist)
    ac_signal_hist.SetDirectory(0)
    return ac_signal_hist


def accepptance_correct_all_gluex1_kkpi_signal_mc_with_phasespace(channel, cut, e, t_bin_index, n_bins=30):
    hist_spring = get_acceptance_corrected_signal_mc(channel, 'spring', cut, e, t_bin_index)
    hist_fall = get_acceptance_corrected_signal_mc(channel, 'fall', cut, e, t_bin_index)
    hist_2017 = get_acceptance_corrected_signal_mc(channel, '2017', cut, e, t_bin_index)

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
    """returns cross section for kkpi with multiplicity of 6"""
    return (data_yield / (acceptance *luminosity * bin_width * branching_fraction * 6))

def get_binned_integrated_phasespace_acceptance(channel, run_period, e, t_bin_index, cut='all', range_lower=1.0, range_upper=2.5):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)
    
    recon_hist = get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index)

    acceptance = recon_hist.Integral(recon_hist.FindBin(range_lower), recon_hist.FindBin(range_upper)) / thrown_hist.Integral(thrown_hist.FindBin(range_lower), thrown_hist.FindBin(range_upper))
    return acceptance


def get_binned_phasespace_acceptance(channel, run_period, e, t_bin_index, cut):
    """
    e should be an integer between 7 and 10 inclusive
    cut should be either "no_cut, plus, zero, or all
    """
    validate_e_bin(e)
    validate_t_bin(t_bin_index)
    
    recon_hist = get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index)

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
    
    recon_hist = get_binned_phasespace_recon_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_phasespace_thrown_hist(channel, run_period, e, t_bin_index)

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
    acceptance_spring = get_integrated_phasespace_acceptance(channel, 'spring', cut)
    acceptance_fall = get_integrated_phasespace_acceptance(channel, 'fall', cut)
    acceptance_2017 = get_integrated_phasespace_acceptance(channel, '2017', cut)

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


def get_integrated_gluex1_phaasespace_acceptance_corrected_data(channel, cut):
    data_hist = get_integrated_gluex1_data(channel, cut)
    acceptance = get_integrated_gluex1_avg_phasespace_acceptance(channel, cut)

    data_hist.Sumw2()
    acceptance.Sumw2()

    acceptance_corrected_data_hist = data_hist.Clone()
    acceptance_corrected_data_hist.Divide(acceptance)

    acceptance_corrected_data_hist.SetDirectory(0)

    return acceptance_corrected_data_hist


def get_integrated_gluex1_signal_mc(channel, cut):   
    signal_mc_hist_spring = get_integrated_signal_mc_hist(channel, 'spring', cut)
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

    signal_mc_hist = get_gluex1_binned_kkpi_signal_mc(channel, cut, e, t_bin_index)
    acceptance_hist = get_gluex1_binned_avg_phasespace_acceptance(channel, cut, e, t_bin_index)

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
    kstar_efficiency_df = pd.read_csv('/work/halld/home/viducic/data/ps_dalitz/kstar_cut_efficiency_stepsize_10.csv')
    for i in range(1, hist.GetXaxis().GetNbins()+1):
        bin_ef_df = kstar_efficiency_df.loc[kstar_efficiency_df.mass_bin_center == round(hist.GetXaxis().GetBinCenter(i), 3)]
        if len(bin_ef_df) == 0:
            print(f'Bin center = {hist.GetXaxis().GetBinCenter(i)} has no efficiency value')
            continue
        bin_eff = bin_ef_df.kstar_cut_efficiency.values[0]
        hist.SetBinContent(i, hist.GetBinContent(i) / bin_eff)
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
    df = df.Filter(T_RANGE).Filter(BEAM_RANGE)#.Filter(KSTAR_CUT_DICT_PIPKMKS[cut])
    hist = df.Histo1D((f'{channel}_m', f'{channel}_m', nbins, 1.0, 2.5), f'{channel}_m')
    hist.Sumw2()
    hist.SetDirectory(0)
    return hist.GetValue()


def get_binned_signal_mc_hist_for_resolution_fitting(channel, run_period, e, t_bin_index, n_bins = 200, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    validate_e_bin(e)
    validate_t_bin(t_bin_index)

    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    e_cut = f'e_beam > {BEAM_CUT_DICT[e][0]} && e_beam < {BEAM_CUT_DICT[e][1]}'
    df = df.Filter(f't_bin == {t_bin_index}').Filter(e_cut)#.Filter(KSTAR_CUT_DICT_PIPKMKS[cut])
    hist = df.Histo1D((f'{channel}_m', f'{channel}_m', n_bins, xmin, xmax), f'{channel}_m')
    hist.Sumw2()
    hist.SetDirectory(0)
    return hist.GetValue()


def get_gluex1_binned_signal_mc_hist_for_resoltion_fitting(channel, e, t_bin_index, n_bins = 200, xmin=1.0, xmax=2.5, cut='all', scale_factor=1):
    hist_spring = get_binned_signal_mc_hist_for_resolution_fitting(channel, 'spring', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)
    hist_fall = get_binned_signal_mc_hist_for_resolution_fitting(channel, 'fall', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)
    hist_2017 = get_binned_signal_mc_hist_for_resolution_fitting(channel, '2017', e, t_bin_index, n_bins, xmin, xmax, cut, scale_factor)

    hist_spring.Sumw2()
    hist_fall.Sumw2()
    hist_2017.Sumw2()

    hist_total = weight_histograms_by_flux(hist_spring, hist_fall, hist_2017)
    hist_total.Sumw2()
    hist_total.SetLineColor(ROOT.TColor.GetColor(COLORBLIND_HEX_DICT['blue']))
    hist_total.SetTitle(get_binned_kkpi_hist_title(channel, e, t_bin_index))
    hist_total.GetXaxis().SetTitle('M(K^{+}K^{-}#pi^{+}) [GeV]')
    hist_total.GetYaxis().SetTitle(f'Events / {(xmax - xmin)/n_bins:.3f} GeV')

    hist_total.SetDirectory(0)
    return hist_total


def get_integrated_gluex1_signal_mc_hist_for_resolution_fitting(channel, nbins=500, xmin = 1.0, xmax = 2.5, cut='all', scale_factor=1):
    hist_spring = get_integrated_signal_mc_hist_for_resolution_fitting(channel, 'spring', nbins, xmin, xmax, cut)
    hist_fall = get_integrated_signal_mc_hist_for_resolution_fitting(channel, 'fall', nbins, xmin, xmax, cut)
    hist_2017 = get_integrated_signal_mc_hist_for_resolution_fitting(channel, '2017', nbins, xmin, xmax, cut)
    combined_weighted_hist = weight_histograms_by_flux(hist_spring, hist_fall, hist_2017)
    combined_weighted_hist.Scale(1/scale_factor)
    combined_weighted_hist.Sumw2()
    combined_weighted_hist.SetDirectory(0)
    return combined_weighted_hist


def get_acceptance(nrecon, nthrown, error=True):
    if not error:
        return nrecon/nthrown
    else:
        error_recon = 0.0
        error_thrown = 0.0
        acceptance = nrecon/nthrown
        error = propogate_error_multiplication(acceptance, [nrecon, nthrown], [error_recon, error_thrown])
        return acceptance, error


def get_binned_signal_acceptance(channel, run_period, e, t_bin_index, cut='no', error=True):
    signal_hist = get_binned_signal_mc_hist(channel, run_period, cut, e, t_bin_index)
    thrown_hist = get_binned_signal_thrown_hist(channel, run_period, e, t_bin_index)
    return get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error)


def get_integrated_signal_acceptance(channel, run_period, cut='no', error=True):
    signal_hist = get_integrated_signal_mc_hist(channel, run_period, cut)
    thrown_hist = get_integrated_signal_mc_hist(channel, run_period)
    return get_acceptance(signal_hist.Integral(), thrown_hist.Integral(), error)


def get_binned_gluex1_signal_acceptance(channel, e, t_bin_index, cut='no', error=True):
    lumi_spring = get_luminosity('spring', e-0.5, e+0.5)
    lumi_fall = get_luminosity('fall', e-0.5, e+0.5)
    lumi_2017 = get_luminosity('2017', e-0.5, e+0.5)
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    if not error:
        weighted_acceptance_spring = get_binned_signal_acceptance(channel, 'spring', e, t_bin_index, cut, error) * lumi_spring
        weighted_acceptance_fall = get_binned_signal_acceptance(channel, 'fall', e, t_bin_index, cut, error) * lumi_fall
        weighted_acceptance_2017 = get_binned_signal_acceptance(channel, '2017', e, t_bin_index, cut, error) * lumi_2017

        return (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total
    else:
        error_spring = 0.0
        error_fall = 0.0
        error_2017 = 0.0
        acceptance_spring, error_spring = get_binned_signal_acceptance(channel, 'spring', e, t_bin_index, cut)
        acceptance_fall, error_fall = get_binned_signal_acceptance(channel, 'fall', e, t_bin_index, cut)
        acceptance_2017, error_2017 = get_binned_signal_acceptance(channel, '2017', e, t_bin_index, cut)

        weighted_acceptance_spring = acceptance_spring * lumi_spring
        weighted_acceptance_fall = acceptance_fall * lumi_fall
        weighted_acceptance_2017 = acceptance_2017 * lumi_2017
        total_acceptance = (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total

        weighted_error_spring = error_spring * lumi_spring
        weighted_error_fall = error_fall * lumi_fall
        weighted_error_2017 = error_2017 * lumi_2017
        total_error = (weighted_error_spring + weighted_error_fall + weighted_error_2017)/lumi_total

        return total_acceptance, total_error


def get_integrated_gluex1_signal_acceptance(channel, cut='no', error=True):
    lumi_spring = get_luminosity('spring')
    lumi_fall = get_luminosity('fall')
    lumi_2017 = get_luminosity('2017')
    lumi_total = lumi_spring + lumi_fall + lumi_2017

    if not error:
        weighted_acceptance_spring = get_integrated_signal_acceptance(channel, 'spring', cut) * lumi_spring
        weighted_acceptance_fall = get_integrated_signal_acceptance(channel, 'fall', cut) * lumi_fall
        weighted_acceptance_2017 = get_integrated_signal_acceptance(channel, '2017', cut) * lumi_2017
        return (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total
    else:
        error_spring = 0.0
        error_fall = 0.0
        error_2017 = 0.0
        acceptance_spring, error_spring = get_integrated_signal_acceptance(channel, 'spring', cut)
        acceptance_fall, error_fall = get_integrated_signal_acceptance(channel, 'fall', cut)
        acceptance_2017, error_2017 = get_integrated_signal_acceptance(channel, '2017', cut)

        weighted_acceptance_spring = acceptance_spring * lumi_spring
        weighted_acceptance_fall = acceptance_fall * lumi_fall
        weighted_acceptance_2017 = acceptance_2017 * lumi_2017
        total_acceptance = (weighted_acceptance_spring + weighted_acceptance_fall + weighted_acceptance_2017)/lumi_total

        weighted_error_spring = error_spring * lumi_spring
        weighted_error_fall = error_fall * lumi_fall
        weighted_error_2017 = error_2017 * lumi_2017
        total_error = (weighted_error_spring + weighted_error_fall + weighted_error_2017)/lumi_total
        return total_acceptance, total_error


def set_sqrtN_error(hist):
    for i in range(1, hist.GetNbinsX()+1):
        error = np.sqrt(hist.GetBinContent(i))
        hist.SetBinError(i, error)


# this is legit awful code. im sorry if anyone in the future needs to use this
def get_integrated_acceptance_corrected_signal_mc_for_resolution_fitting(channel, n_bins, cut, scale_factor=1):
    if channel == 'pipkmks':
        kstar_cut = KSTAR_CUT_DICT_PIPKMKS[cut]
    elif channel == 'pimkpks':
        kstar_cut = KSTAR_CUT_DICT_PIMKPKS[cut]

    file_and_tree_spring = get_flat_file_and_tree(channel, "spring", 'signal')
    file_and_tree_fall = get_flat_file_and_tree(channel, "fall", 'signal')
    file_and_tree_2017 = get_flat_file_and_tree(channel, "2017", 'signal')


    signal_df_spring = ROOT.RDataFrame(file_and_tree_spring[1], file_and_tree_spring[0]) 
    signal_df_fall = ROOT.RDataFrame(file_and_tree_fall[1], file_and_tree_fall[0]) 
    signal_df_2017 = ROOT.RDataFrame(file_and_tree_2017[1], file_and_tree_2017[0]) 

    recon_phasespace_file_and_tree_spring = get_flat_file_and_tree(channel, "spring", 'phasespace')
    recon_phasespace_file_and_tree_fall = get_flat_file_and_tree(channel, "fall", 'phasespace')
    recon_phasespace_file_and_tree_2017 = get_flat_file_and_tree(channel, "2017", 'phasespace')

    thrown_phasespace_file_and_tree_spring = get_flat_thrown_file_and_tree(channel, "spring", phasespace=True)
    thrown_phasespace_file_and_tree_fall = get_flat_thrown_file_and_tree(channel, "fall", phasespace=True)
    thrown_phasespace_file_and_tree_2017 = get_flat_thrown_file_and_tree(channel, "2017", phasespace=True)

    recon_df_spring = ROOT.RDataFrame(recon_phasespace_file_and_tree_spring[1], recon_phasespace_file_and_tree_spring[0])
    recon_df_fall = ROOT.RDataFrame(recon_phasespace_file_and_tree_fall[1], recon_phasespace_file_and_tree_fall[0])
    recon_df_2017 = ROOT.RDataFrame(recon_phasespace_file_and_tree_2017[1], recon_phasespace_file_and_tree_2017[0])

    thrown_file_spring = ROOT.TFile.Open(thrown_phasespace_file_and_tree_spring[0], 'READ')
    thrown_file_fall = ROOT.TFile.Open(thrown_phasespace_file_and_tree_fall[0], 'READ')
    thrown_file_2017 = ROOT.TFile.Open(thrown_phasespace_file_and_tree_2017[0], 'READ')
    # print(thrown_phasespace_file_and_tree[0])

    signal_df_spring = signal_df_spring.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    signal_df_fall = signal_df_fall.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    signal_df_2017 = signal_df_2017.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    # reduce signal_df size

    signal_df_spring = signal_df_spring.Range(0, int(signal_df_spring.Count().GetValue() / scale_factor))
    signal_df_fall = signal_df_fall.Range(0, int(signal_df_fall.Count().GetValue() / scale_factor))
    signal_df_2017 = signal_df_2017.Range(0, int(signal_df_2017.Count().GetValue() / scale_factor))

    recon_df_spring = recon_df_spring.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    recon_df_fall = recon_df_fall.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)
    recon_df_2017 = recon_df_2017.Filter(kstar_cut).Filter(T_RANGE).Filter(BEAM_RANGE)

    signal_hist_spring = signal_df_spring.Histo1D(('data_hist_"spring"', 'data_hist_"spring"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    signal_hist_fall = signal_df_fall.Histo1D(('data_hist_"fall"', 'data_hist_"fall"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    signal_hist_2017 = signal_df_2017.Histo1D(('data_hist_"2017"', 'data_hist_"2017"', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()


    recon_hist_spring = recon_df_spring.Histo1D(('recon_hist_spring', 'recon_hist_spring', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    recon_hist_fall = recon_df_fall.Histo1D(('recon_hist_fall', 'recon_hist_fall', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()
    recon_hist_2017 = recon_df_2017.Histo1D(('recon_hist_2017', 'recon_hist_2017', n_bins, 1.2, 1.5), f'{channel}_m').GetValue()


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
    if run_period not in ALLOWED_RUN_PERIODS:
        error_message = f"Run period {run_period} not allowed. Allowed run periods are: {ALLOWED_RUN_PERIODS}"
        raise ValueError(error_message)
    return True 


def check_channel(channel):
    if channel not in ALLOWED_CHANNELS:
        error_message = f"Channel {channel} not allowed. Allowed channels are: {ALLOWED_CHANNELS}"
        raise ValueError(error_message)


def check_datatype_recon(datatype):
    if datatype not in ALLOWED_DATATYPES_RECON:
        error_message = f"Datatype {datatype} not allowed. Allowed datatypes are: {ALLOWED_DATATYPES_RECON}"
        raise ValueError(error_message)


def check_datatype_thrown(datatype):
    if datatype not in ALLOWED_DATATYPES_THROWN:
        error_message = f"Datatype {datatype} not allowed. Allowed datatypes are: {ALLOWED_DATATYPES_THROWN}"
        raise ValueError(error_message)


def verify_args(channel, run_period, datatype):
    check_run_period(run_period)
    check_channel(channel)
    check_datatype_recon(datatype)
    return True


def verify_thrown_args(channel, run_period, datatype):
    check_run_period(run_period)
    check_channel(channel)
    check_datatype_thrown(datatype)
    return True


def define_pimkpks_columns(df):
    ROOT.gInterpreter.Declare(T_BIN_FILTER)
    ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)
    new_df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
    new_df = new_df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

    new_df = new_df.Define('ks_px', "pim2_px + pip_px")
    new_df = new_df.Define('ks_py', "pim2_py + pip_py")
    new_df = new_df.Define('ks_pz', "pim2_pz + pip_pz")
    new_df = new_df.Define('ks_E', "pim2_E + pip_E")
    new_df = new_df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

    new_df = new_df.Define('ks_px_measured', "pim2_px_measured + pip_px_measured")
    new_df = new_df.Define('ks_py_measured', "pim2_py_measured + pip_py_measured")
    new_df = new_df.Define('ks_pz_measured', "pim2_pz_measured + pip_pz_measured")
    new_df = new_df.Define('ks_E_measured', "pim2_E_measured + pip_E_measured")
    new_df = new_df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

    new_df = new_df.Define('mxpx_ppimkpks', '-p_px_measured - pim1_px_measured - kp_px_measured - ks_px_measured')
    new_df = new_df.Define('mxpy_ppimkpks', '-p_py_measured - pim1_py_measured - kp_py_measured - ks_py_measured')
    new_df = new_df.Define('mxpz_ppimkpks', 'e_beam - p_pz_measured - pim1_pz_measured - kp_pz_measured - ks_pz_measured')
    new_df = new_df.Define('mxe_ppimkpks', 'e_beam + 0.938272088 - p_E_measured - pim1_E_measured - kp_E_measured - ks_E_measured')
    new_df = new_df.Define('mx2_ppimkpks', 'mxe_ppimkpks*mxe_ppimkpks - mxpx_ppimkpks*mxpx_ppimkpks - mxpy_ppimkpks*mxpy_ppimkpks - mxpz_ppimkpks*mxpz_ppimkpks')

    new_df = new_df.Define('ppim_px', 'pim1_px + p_px')
    new_df = new_df.Define('ppim_py', 'pim1_py + p_py')
    new_df = new_df.Define('ppim_pz', 'pim1_pz + p_pz')
    new_df = new_df.Define('ppim_E', 'pim1_E + p_E')
    new_df = new_df.Define('ppim_m', 'sqrt(ppim_E*ppim_E - ppim_px*ppim_px - ppim_py*ppim_py - ppim_pz*ppim_pz)')


    new_df = new_df.Define('missing_px', '-p_px - pim1_px - ks_px - kp_px')
    new_df = new_df.Define('missing_py', '-p_py - pim1_py - ks_py - kp_py')
    new_df = new_df.Define('missing_pz', 'e_beam - p_pz - pim1_pz - ks_pz - kp_pz')
    new_df = new_df.Define('missing_E', 'e_beam + 0.938 - p_E - pim1_E - ks_E - kp_E')

    new_df = new_df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

    new_df = new_df.Define('kpp_px', 'p_px + kp_px')
    new_df = new_df.Define('kpp_py', 'p_py + kp_py')
    new_df = new_df.Define('kpp_pz', 'p_pz + kp_pz')
    new_df = new_df.Define('kpp_E', 'p_E + kp_E')

    new_df = new_df.Define('kpp_m', 'sqrt(kpp_E*kpp_E - kpp_px*kpp_px - kpp_py*kpp_py - kpp_pz*kpp_pz)')

    new_df = new_df.Define('ksp_px', 'p_px + ks_px')
    new_df = new_df.Define('ksp_py', 'p_py + ks_py')
    new_df = new_df.Define('ksp_pz', 'p_pz + ks_pz')
    new_df = new_df.Define('ksp_E', 'p_E + ks_E')

    new_df = new_df.Define('ksp_m', 'sqrt(ksp_E*ksp_E - ksp_px*ksp_px - ksp_py*ksp_py - ksp_pz*ksp_pz)')

    new_df = new_df.Define('kspim_px', 'pim1_px + ks_px')
    new_df = new_df.Define('kspim_py', 'pim1_py + ks_py')
    new_df = new_df.Define('kspim_pz', 'pim1_pz + ks_pz')
    new_df = new_df.Define('kspim_E', 'pim1_E + ks_E')

    new_df = new_df.Define('kspim_m', 'sqrt(kspim_E*kspim_E - kspim_px*kspim_px - kspim_py*kspim_py - kspim_pz*kspim_pz)')

    new_df = new_df.Define('kppim_px', 'pim1_px + kp_px')
    new_df = new_df.Define('kppim_py', 'pim1_py + kp_py')
    new_df = new_df.Define('kppim_pz', 'pim1_pz + kp_pz')
    new_df = new_df.Define('kppim_E', 'pim1_E + kp_E')

    new_df = new_df.Define('kppim_m', 'sqrt(kppim_E*kppim_E - kppim_px*kppim_px - kppim_py*kppim_py - kppim_pz*kppim_pz)')

    new_df = new_df.Define('pimkpks_px', 'pim1_px + kp_px + ks_px')
    new_df = new_df.Define('pimkpks_py', 'pim1_py + kp_py + ks_py')
    new_df = new_df.Define('pimkpks_pz', 'pim1_pz + kp_pz + ks_pz')
    new_df = new_df.Define('pimkpks_E', 'pim1_E + kp_E + ks_E')

    new_df = new_df.Define('pimkpks_px_measured', "pim1_px_measured + kp_px_measured + ks_px_measured")
    new_df = new_df.Define('pimkpks_py_measured', "pim1_py_measured + kp_py_measured + ks_py_measured")
    new_df = new_df.Define('pimkpks_pz_measured', "pim1_pz_measured + kp_pz_measured + ks_pz_measured")
    new_df = new_df.Define('pimkpks_pt', 'sqrt(pimkpks_px_measured*pimkpks_px_measured + pimkpks_py_measured*pimkpks_py_measured)')

    new_df = new_df.Define('pimkpks_p_pt_diff', 'pimkpks_pt - p_pt')

    new_df = new_df.Define('pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')

    new_df = new_df.Define('kpks_px', 'kp_px + ks_px')
    new_df = new_df.Define('kpks_py', 'kp_py + ks_py')
    new_df = new_df.Define('kpks_pz', 'kp_pz + ks_pz')
    new_df = new_df.Define('kpks_E', 'kp_E + ks_E')
    new_df = new_df.Define('kpks_m', 'sqrt(kpks_E*kpks_E - kpks_px*kpks_px - kpks_py*kpks_py - kpks_pz*kpks_pz)')

    new_df = new_df.Define('e_bin', 'get_beam_bin_index(e_beam)')
    new_df = new_df.Define('t_bin', 'get_t_bin_index(mand_t)')

    new_df = new_df.Define('ppip_px', 'p_px + pip_px')
    new_df = new_df.Define('ppip_py', 'p_py + pip_py')
    new_df = new_df.Define('ppip_pz', 'p_pz + pip_pz')
    new_df = new_df.Define('ppip_E', 'p_E + pip_E')
    new_df = new_df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')
    return new_df


def define_pipkmks_columns(df):
    ROOT.gInterpreter.Declare(T_BIN_FILTER)
    ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)
    new_df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
    new_df = new_df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

    new_df = new_df.Define('ks_px', "pip2_px + pim_px")
    new_df = new_df.Define('ks_py', "pip2_py + pim_py")
    new_df = new_df.Define('ks_pz', "pip2_pz + pim_pz")
    new_df = new_df.Define('ks_E', "pip2_E + pim_E")
    new_df = new_df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

    new_df = new_df.Define('ks_px_measured', "pip2_px_measured + pim_px_measured")
    new_df = new_df.Define('ks_py_measured', "pip2_py_measured + pim_py_measured")
    new_df = new_df.Define('ks_pz_measured', "pip2_pz_measured + pim_pz_measured")
    new_df = new_df.Define('ks_E_measured', "pip2_E_measured + pim_E_measured")
    new_df = new_df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

    new_df = new_df.Define('mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
    new_df = new_df.Define('mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
    new_df = new_df.Define('mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
    new_df = new_df.Define('mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
    new_df = new_df.Define('mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')

    new_df = new_df.Define('ppip_px', 'pip1_px + p_px')
    new_df = new_df.Define('ppip_py', 'pip1_py + p_py')
    new_df = new_df.Define('ppip_pz', 'pip1_pz + p_pz')
    new_df = new_df.Define('ppip_E', 'pip1_E + p_E')
    new_df = new_df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')


    new_df = new_df.Define('missing_px', '-p_px - pip1_px - ks_px - km_px')
    new_df = new_df.Define('missing_py', '-p_py - pip1_py - ks_py - km_py')
    new_df = new_df.Define('missing_pz', 'e_beam - p_pz - pip1_pz - ks_pz - km_pz')
    new_df = new_df.Define('missing_E', 'e_beam + 0.938 - p_E - pip1_E - ks_E - km_E')

    new_df = new_df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

    new_df = new_df.Define('kmp_px', 'p_px + km_px')
    new_df = new_df.Define('kmp_py', 'p_py + km_py')
    new_df = new_df.Define('kmp_pz', 'p_pz + km_pz')
    new_df = new_df.Define('kmp_E', 'p_E + km_E')

    new_df = new_df.Define('kmp_m', 'sqrt(kmp_E*kmp_E - kmp_px*kmp_px - kmp_py*kmp_py - kmp_pz*kmp_pz)')

    new_df = new_df.Define('ksp_px', 'p_px + ks_px')
    new_df = new_df.Define('ksp_py', 'p_py + ks_py')
    new_df = new_df.Define('ksp_pz', 'p_pz + ks_pz')
    new_df = new_df.Define('ksp_E', 'p_E + ks_E')

    new_df = new_df.Define('ksp_m', 'sqrt(ksp_E*ksp_E - ksp_px*ksp_px - ksp_py*ksp_py - ksp_pz*ksp_pz)')

    new_df = new_df.Define('kspip_px', 'pip1_px + ks_px')
    new_df = new_df.Define('kspip_py', 'pip1_py + ks_py')
    new_df = new_df.Define('kspip_pz', 'pip1_pz + ks_pz')
    new_df = new_df.Define('kspip_E', 'pip1_E + ks_E')

    new_df = new_df.Define('kspip_m', 'sqrt(kspip_E*kspip_E - kspip_px*kspip_px - kspip_py*kspip_py - kspip_pz*kspip_pz)')

    new_df = new_df.Define('kmpip_px', 'pip1_px + km_px')
    new_df = new_df.Define('kmpip_py', 'pip1_py + km_py')
    new_df = new_df.Define('kmpip_pz', 'pip1_pz + km_pz')
    new_df = new_df.Define('kmpip_E', 'pip1_E + km_E')

    new_df = new_df.Define('kmpip_m', 'sqrt(kmpip_E*kmpip_E - kmpip_px*kmpip_px - kmpip_py*kmpip_py - kmpip_pz*kmpip_pz)')

    new_df = new_df.Define('pipkmks_px', 'pip1_px + km_px + ks_px')
    new_df = new_df.Define('pipkmks_py', 'pip1_py + km_py + ks_py')
    new_df = new_df.Define('pipkmks_pz', 'pip1_pz + km_pz + ks_pz')
    new_df = new_df.Define('pipkmks_E', 'pip1_E + km_E + ks_E')

    new_df = new_df.Define('pipkmks_px_measured', "pip1_px_measured + km_px_measured + ks_px_measured")
    new_df = new_df.Define('pipkmks_py_measured', "pip1_py_measured + km_py_measured + ks_py_measured")
    new_df = new_df.Define('pipkmks_pz_measured', "pip1_pz_measured + km_pz_measured + ks_pz_measured")
    new_df = new_df.Define('pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')

    new_df = new_df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')

    new_df = new_df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

    new_df = new_df.Define('kmks_px', 'km_px + ks_px')
    new_df = new_df.Define('kmks_py', 'km_py + ks_py')
    new_df = new_df.Define('kmks_pz', 'km_pz + ks_pz')
    new_df = new_df.Define('kmks_E', 'km_E + ks_E')
    new_df = new_df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')

    new_df = new_df.Define('e_bin', 'get_beam_bin_index(e_beam)')
    new_df = new_df.Define('t_bin', 'get_t_bin_index(mand_t)')
    return new_df


def define_pipkmks_thrown_columns(df):
    ROOT.gInterpreter.Declare(T_BIN_FILTER)
    ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)
    new_df = df.Define('pipkmks_px', 'PiPlus1_px + KMinus_px + Ks_px')
    new_df = new_df.Define('pipkmks_py', 'PiPlus1_py + KMinus_py + Ks_py')
    new_df = new_df.Define('pipkmks_pz', 'PiPlus1_pz + KMinus_pz + Ks_pz')
    new_df = new_df.Define('pipkmks_E', 'PiPlus1_E + KMinus_E + Ks_E')
    new_df = new_df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')
    new_df = new_df.Define('e_bin', 'get_beam_bin_index(Beam_E)')
    new_df = new_df.Define('t_bin', 'get_t_bin_index(men_t)')
    return new_df


def define_pimkpks_thrown_columns(df):
    ROOT.gInterpreter.Declare(T_BIN_FILTER)
    ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)
    new_df = df.Define('pimkpks_px', 'PiMinus1_px + KPlus_px + Ks_px')
    new_df = new_df.Define('pimkpks_py', 'PiMinus1_py + KPlus_py + Ks_py')
    new_df = new_df.Define('pimkpks_pz', 'PiMinus1_pz + KPlus_pz + Ks_pz')
    new_df = new_df.Define('pimkpks_E', 'PiMinus1_E + KPlus_E + Ks_E')
    new_df = new_df.Define('pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')
    new_df = new_df.Define('e_bin', 'get_beam_bin_index(Beam_E)')
    new_df = new_df.Define('t_bin', 'get_t_bin_index(men_t)')
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
        return df.Filter(MX2_PPIPKMKS_CUT).Filter(KS_PATHLENGTH_CUT).Filter(KS_MASS_CUT).Filter(PPIP_MASS_CUT).Filter(KMP_MASS_CUT).Filter(P_P_CUT)
    elif channel == 'pimkpks':
        return df.Filter(MX2_PPIMKPKS_CUT).Filter(KS_PATHLENGTH_CUT).Filter(KS_MASS_CUT).Filter(PPIM_MASS_CUT).Filter(KSP_MASS_CUT).Filter(P_P_CUT)
    else:
        raise ValueError('Unknown channel: {}'.format(channel))


def get_dataframe(channel, run_period, datatype, filtered=True):
    if filtered:
        file_and_tree = get_flat_file_and_tree(channel, run_period, datatype)
        return ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    else:
        file_and_tree = get_flat_file_and_tree(channel, run_period, datatype, filtered=False)
        return define_columns(ROOT.RDataFrame(file_and_tree[1], file_and_tree[0]), channel)


def get_path_for_output_file(channel, datatype, thrown=False):
    if thrown:
        return f'/work/halld/home/viducic/data/{channel}/mc/thrown'
    if datatype == 'data':
        return f'/work/halld/home/viducic/data/{channel}/data/bestX2'
    elif datatype == 'signal' or datatype == 'phasespace':
        return f'/work/halld/home/viducic/data/{channel}/mc/{datatype}'
    else:
        raise ValueError('Unknown datatype: {}'.format(datatype))
    
