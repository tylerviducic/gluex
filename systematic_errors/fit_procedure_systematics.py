"""script to vary the fitting procedure to estimate the systematic errors"""

"""This actually may be the worst code i've ever written but deadlines yaknow
   do not, in any circumstances, write code like this. also, please dont judge me"""

import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import pandas as pd

def get_data(channel, e, t):
    if channel == 'pipkmks':
        hist_title = 'K^{-}K_{s}#pi^{+}'
    elif channel == 'pimkpks':
        hist_title = 'K^{+}K_{s}#pi^{-}'

    cor_hist = tools.get_binned_gluex1_kstar_corrected_data(channel, e, t)
    hist = tools.remove_zero_datapoints(cor_hist)
    hist.GetXaxis().SetRangeUser(1.13, 1.53)
    hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)

    hist.GetXaxis().SetTitle(hist_title + ' (GeV)')
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetTitle('Counts/10 MeV')

    hist.SetTitle('E_{#gamma} = ' + str(e) + ' GeV || ' + f'{constants.T_CUT_DICT[t][0]} < -t < {constants.T_CUT_DICT[t][1]}' + ' GeV^{2}')
    hist.SetTitleSize(0.055)
    hist.SetDirectory(0)
    return hist

# TODO: draw functions with correct colors
def get_properties(channel):
    if channel == 'pipkmks':
        properties = {
            'v_mean': constants.F1_PIPKMKS_VOIGHT_MEAN,
            'v_width': constants.F1_PIPKMKS_VOIGHT_WIDTH,
            'v_sigma': tools.get_binned_resolution('pipkmks', 8, 1),
            'total_fit_color': ROOT.kViolet,
            'f1_color': ROOT.kBlue,
            'background_color': ROOT.kViolet,
            'hist_title': 'K^{-}K_{s}#pi^{+}',
            'gaus_mean': constants.F1_PIPKMKS_GAUS_MEAN,
            'gaus_width': constants.F1_PIPKMKS_GAUS_WIDTH,
            'range_low': 1.15,
            'range_high': 1.51
        }
    elif channel == 'pimkpks':
        properties = {
            'v_mean': constants.F1_PIMKPKS_VOIGHT_MEAN,
            'v_width': constants.F1_PIMKPKS_VOIGHT_WIDTH,
            'v_sigma': tools.get_binned_resolution('pimkpks', 8, 1),
            'total_fit_color': ROOT.kViolet +9,
            'f1_color': ROOT.kRed,
            'background_color': ROOT.kViolet +9,
            'hist_title': 'K^{+}K_{s}#pi^{-}',
            'gaus_mean': constants.F1_PIMKPKS_GAUS_MEAN,
            'gaus_width': constants.F1_PIMKPKS_GAUS_WIDTH,
            'range_low': 1.15,
            'range_high': 1.51
        }
    return properties


# NOMINAL FIT
def get_nominal_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_nominal_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_nominal_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_nominal_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_nominal_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))


    gaus = ROOT.TF1(f'gaus_nominal_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_nominal_{channel}_{e}_{t}', 'pol2(0)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    gaus.SetParError(0, func.GetParError(4))
    gaus.SetParError(1, func.GetParError(5))
    gaus.SetParError(2, func.GetParError(6))

    bkg.SetParError(0, func.GetParError(7))
    bkg.SetParError(1, func.GetParError(8))
    bkg.SetParError(2, func.GetParError(9))


    return voigt, gaus, bkg


# POL1
def get_pol1_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
    }
    return initial_guesses


def get_pol1_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParameter(8, guesses[8]) # bkg par2
    return func


def get_pol1_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus = ROOT.TF1(f'gaus_pol1_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_pol1_{channel}_{e}_{t}', 'pol1(0)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    gaus.SetParError(0, func.GetParError(4))
    gaus.SetParError(1, func.GetParError(5))
    gaus.SetParError(2, func.GetParError(6))

    bkg.SetParError(0, func.GetParError(7))
    bkg.SetParError(1, func.GetParError(8))

    return voigt, gaus, bkg


# POL3
def get_pol3_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1, # bkg par3
        10: 1, # bkg par4
    }
    return initial_guesses


def get_pol3_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_pol3_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol3(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    func.SetParameter(10, guesses[10]) # bkg par4
    return func


def get_pol3_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_pol3_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus = ROOT.TF1(f'gaus_pol3_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_pol3_{channel}_{e}_{t}', 'pol3(0)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))
    bkg.SetParameter(3, func.GetParameter(10))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    gaus.SetParError(0, func.GetParError(4))
    gaus.SetParError(1, func.GetParError(5))
    gaus.SetParError(2, func.GetParError(6))

    bkg.SetParError(0, func.GetParError(7))
    bkg.SetParError(1, func.GetParError(8))
    bkg.SetParError(2, func.GetParError(9))
    bkg.SetParError(3, func.GetParError(10))

    return voigt, gaus, bkg


# NO GAUS
def get_no_gaus_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: -100, # bkg par1
        5: 100, # bkg par2
        6: 1 # bkg par3
    }
    return initial_guesses


def get_no_gaus_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_nominal_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + pol2(4)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # bkg par1
    func.SetParLimits(4, -100000, 0.0)
    func.FixParameter(5, guesses[5])# bkg par2
    func.FixParameter(6, guesses[6]) # bkg par3
    return func


def get_no_gaus_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_no_gaus_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))


    bkg = ROOT.TF1(f'bkg_no_gaus_{channel}_{e}_{t}', 'pol2(0)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(4))
    bkg.SetParameter(1, func.GetParameter(5))
    bkg.SetParameter(2, func.GetParameter(6))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    bkg.SetParError(0, func.GetParError(4))
    bkg.SetParError(1, func.GetParError(5))
    bkg.SetParError(2, func.GetParError(6))

    return voigt, bkg


# EXPONENTIAL POL2
def get_exp_pol2_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: 1, # bkg par1
        8: 1, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_exp_pol2_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_exp_pol2_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + ROOT.TMath.Exp(par[6] + par[7]*x + par[8]*x*x)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_exp_pol2_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_exp_pol2_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus = ROOT.TF1(f'gaus_exp_pol2_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_exp_pol2_{channel}_{e}_{t}', 'ROOT.TMath.Exp(par[0] + par[1]*x + par[2]*x*x)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    gaus.SetParError(0, func.GetParError(4))
    gaus.SetParError(1, func.GetParError(5))
    gaus.SetParError(2, func.GetParError(6))

    bkg.SetParError(0, func.GetParError(7))
    bkg.SetParError(1, func.GetParError(8))
    bkg.SetParError(2, func.GetParError(9))

    return voigt, gaus, bkg


# CHEBYSHEV
def get_chebyshev_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_chebyshev_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_chebyshev_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + cheb2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_chebyshev_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_chebyshev_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus = ROOT.TF1(f'gaus_chebyshev_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_chebyshev_{channel}_{e}_{t}', 'cheb2(0)', func.GetXmin(), func.GetXmax())
    bkg.SetParameter(0, func.GetParameter(7))
    bkg.SetParameter(1, func.GetParameter(8))
    bkg.SetParameter(2, func.GetParameter(9))

    voigt.SetParError(0, func.GetParError(0))
    voigt.SetParError(1, func.GetParError(1))
    voigt.SetParError(2, func.GetParError(2))
    voigt.SetParError(3, func.GetParError(3))

    gaus.SetParError(0, func.GetParError(4))
    gaus.SetParError(1, func.GetParError(5))
    gaus.SetParError(2, func.GetParError(6))

    bkg.SetParError(0, func.GetParError(7))
    bkg.SetParError(1, func.GetParError(8))
    bkg.SetParError(2, func.GetParError(9))

    return voigt, gaus, bkg


# FLOAT VOIGT MEAN
def get_voigt_mean_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_float_voigt_mean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.SetParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_voigt_mean_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_float_voigt_mean_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_float_voigt_mean_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_float_voigt_mean_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT VOIGT WIDTH
def get_voigt_width_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_float_voigt_width_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.SetParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_voigt_width_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_float_voigt_width_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_float_voigt_width_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_float_voigt_width_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT GAUS MEAN
def get_gaus_mean_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_float_gaus_mean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.SetParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_gaus_mean_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_float_gaus_mean_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_float_gaus_mean_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_float_gaus_mean_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT GAUS WIDTH
def get_gaus_width_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_float_gaus_width_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.SetParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_gaus_width_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_float_gaus_width_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_float_gaus_width_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_float_gaus_width_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# WIDE LEFT
def get_wider_left_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_wider_left_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wider_left_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wider_left_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wider_left_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wider_left_{channel}_{e}_{t}')

    return voigt, gaus, bkg

# WIDE RIGHT
def get_wider_right_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_wider_right_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.52)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wider_right_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wider_right_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wider_right_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wider_right_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# WIDE BOTH
def get_wider_both_func(channel, guesses, e, t):
    func = ROOT.TF1(f'func_wider_both_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, 1.52)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wider_both_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wider_both_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wider_both_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wider_both_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW LEFT
def get_narrow_left_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_narrow_left_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrow_left_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrow_left_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrow_left_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrow_left_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW RIGHT
def get_narrow_right_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_narrow_right_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.5)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrow_right_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrow_right_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrow_right_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrow_right_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW BOTH
def get_narrow_both_func(channel, guesses, e, t):
    func = ROOT.TF1(f'func_narrow_both_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, 1.5)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrow_both_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrow_both_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrow_both_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrow_both_{channel}_{e}_{t}')

    return voigt, gaus, bkg


def update_guesses(func):
    n_params = func.GetNpar()
    guesses = {i: func.GetParameter(i) for i in range(n_params)}
    return guesses


def get_dataframe_row(channel, e, t, fit_variation, func_voigt):
    # get dataframe row info from common_analysis_tools
    f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error = tools.calculate_dataframe_info(func_voigt, channel, e, t)
    row = [channel, e, t, fit_variation, f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error]
    return row


def main():
    ROOT.gROOT.SetBatch(True)
    print('Running')

    df = pd.DataFrame(columns=['channel', 'e', 't', 'fit_variation', 'f1_yield', 'f1_yield_error', 'f1_acceptance', 'f1_acceptance_error', 'cross_section', 'cross_section_error'])

    c_nominal = ROOT.TCanvas('c_nominal', 'c_nominal', 800, 600)
    c_pol1 = ROOT.TCanvas('c_pol1', 'c_pol1', 800, 600)
    c_pol3 = ROOT.TCanvas('c_pol3', 'c_pol3', 800, 600)
    c_no_gaus = ROOT.TCanvas('c_no_gaus', 'c_no_gaus', 800, 600)
    c_exp_pol2 = ROOT.TCanvas('c_exp_pol2', 'c_exp_pol2', 800, 600)
    c_chebyshev = ROOT.TCanvas('c_chebyshev', 'c_chebyshev', 800, 600)
    c_wider_left = ROOT.TCanvas('c_wider_left', 'c_wider_left', 800, 600)
    c_wider_right = ROOT.TCanvas('c_wider_right', 'c_wider_right', 800, 600)
    c_wider_both = ROOT.TCanvas('c_wider_both', 'c_wider_both', 800, 600)
    c_narrow_left = ROOT.TCanvas('c_narrow_left', 'c_narrow_left', 800, 600)
    c_narrow_right = ROOT.TCanvas('c_narrow_right', 'c_narrow_right', 800, 600)
    c_narrow_both = ROOT.TCanvas('c_narrow_both', 'c_narrow_both', 800, 600)
    c_float_voigt_mean = ROOT.TCanvas('c_float_voigt_mean', 'c_float_voigt_mean', 800, 600)
    c_float_voigt_width = ROOT.TCanvas('c_float_voigt_width', 'c_float_voigt_width', 800, 600)
    c_float_gaus_mean = ROOT.TCanvas('c_float_gaus_mean', 'c_float_gaus_mean', 800, 600)
    c_float_gaus_width = ROOT.TCanvas('c_float_gaus_width', 'c_float_gaus_width', 800, 600)

    for channel in ['pipkmks', 'pimkpks']:
        properties = get_properties(channel)
        for e in range(8, 12):
            guesses_nominal = get_nominal_guesses(properties)
            guesses_pol1 = get_pol1_guesses(properties)
            guesses_pol3 = get_pol3_guesses(properties)
            guesses_no_gaus = get_no_gaus_guesses(properties)
            guesses_exp_pol2 = get_exp_pol2_guesses(properties)
            guesses_chebyshev = get_chebyshev_guesses(properties)
            guesses_wider_left = get_nominal_guesses(properties)
            guesses_wider_right = get_nominal_guesses(properties)
            guesses_wider_both = get_nominal_guesses(properties)
            guesses_narrow_left = get_nominal_guesses(properties)
            guesses_narrow_right = get_nominal_guesses(properties)
            guesses_narrow_both = get_nominal_guesses(properties)
            guesses_float_voigt_mean = get_nominal_guesses(properties)
            guesses_float_voigt_width = get_nominal_guesses(properties)
            guesses_float_gaus_mean = get_nominal_guesses(properties)
            guesses_float_gaus_width = get_nominal_guesses(properties)

            c_nominal.Clear()
            c_pol1.Clear()
            c_pol3.Clear()
            c_no_gaus.Clear()
            c_exp_pol2.Clear()
            c_chebyshev.Clear()
            c_wider_left.Clear()
            c_wider_right.Clear()
            c_wider_both.Clear()
            c_narrow_left.Clear()
            c_narrow_right.Clear()
            c_narrow_both.Clear()
            c_float_voigt_mean.Clear()
            c_float_voigt_width.Clear()
            c_float_gaus_mean.Clear()
            c_float_gaus_width.Clear()

            c_nominal.Divide(4, 2)
            c_pol1.Divide(4, 2)
            c_pol3.Divide(4, 2)
            c_no_gaus.Divide(4, 2)
            c_exp_pol2.Divide(4, 2)
            c_chebyshev.Divide(4, 2)
            c_wider_left.Divide(4, 2)
            c_wider_right.Divide(4, 2)
            c_wider_both.Divide(4, 2)
            c_narrow_left.Divide(4, 2)
            c_narrow_right.Divide(4, 2)
            c_narrow_both.Divide(4, 2)
            c_float_voigt_mean.Divide(4, 2)
            c_float_voigt_width.Divide(4, 2)
            c_float_gaus_mean.Divide(4, 2)
            c_float_gaus_width.Divide(4, 2)

            for t in range(1, 8):
                hist = get_data(channel, e, t)

                func_nominal = get_nominal_func(channel, guesses_nominal, e, t)
                func_pol1 = get_pol1_func(channel, guesses_pol1, e, t)
                func_pol3 = get_pol3_func(channel, guesses_pol3, e, t)
                func_no_gaus = get_no_gaus_func(channel, guesses_no_gaus, e, t)
                func_exp_pol2 = get_exp_pol2_func(channel, guesses_exp_pol2, e, t)
                func_chebyshev = get_chebyshev_func(channel, guesses_chebyshev, e, t)
                func_wider_left = get_wider_left_func(channel, guesses_wider_left, e, t)
                func_wider_right = get_wider_right_func(channel, guesses_wider_right, e, t)
                func_wider_both = get_wider_both_func(channel, guesses_wider_both, e, t)
                func_narrow_left = get_narrow_left_func(channel, guesses_narrow_left, e, t)
                func_narrow_right = get_narrow_right_func(channel, guesses_narrow_right, e, t)
                func_narrow_both = get_narrow_both_func(channel, guesses_narrow_both, e, t)
                func_float_voigt_mean = get_voigt_mean_float_func(channel, guesses_float_voigt_mean, e, t)
                func_float_voigt_width = get_voigt_width_float_func(channel, guesses_float_voigt_width, e, t)
                func_float_gaus_mean = get_gaus_mean_float_func(channel, guesses_float_gaus_mean, e, t)
                func_float_gaus_width = get_gaus_width_float_func(channel, guesses_float_gaus_width, e, t)

                result_nominal = hist.Fit(func_nominal, 'SRBEQ0')
                result_pol1 = hist.Fit(func_pol1, 'SRBEQ0')
                result_pol3 = hist.Fit(func_pol3, 'SRBEQ0')
                result_no_gaus = hist.Fit(func_no_gaus, 'SRBEQ0')
                result_exp_pol2 = hist.Fit(func_exp_pol2, 'SRBEQ0')
                result_chebyshev = hist.Fit(func_chebyshev, 'SRBEQ0')
                result_wider_left = hist.Fit(func_wider_left, 'SRBEQ0')
                result_wider_right = hist.Fit(func_wider_right, 'SRBEQ0')
                result_wider_both = hist.Fit(func_wider_both, 'SRBEQ0')
                result_narrow_left = hist.Fit(func_narrow_left, 'SRBEQ0')
                result_narrow_right = hist.Fit(func_narrow_right, 'SRBEQ0')
                result_narrow_both = hist.Fit(func_narrow_both, 'SRBEQ0')
                result_float_voigt_mean = hist.Fit(func_float_voigt_mean, 'SRBEQ0')
                result_float_voigt_width = hist.Fit(func_float_voigt_width, 'SRBEQ0')
                result_float_gaus_mean = hist.Fit(func_float_gaus_mean, 'SRBEQ0')
                result_float_gaus_width = hist.Fit(func_float_gaus_width, 'SRBEQ0')

                voit_nominal, gaus_nominal, bkg_nominal = get_nominal_components(func_nominal)
                voit_pol1, gaus_pol1, bkg_pol1 = get_pol1_components(func_pol1)
                voit_pol3, gaus_pol3, bkg_pol3 = get_pol3_components(func_pol3)
                voit_no_gaus, bkg_no_gaus = get_no_gaus_components(func_no_gaus)
                voit_exp_pol2, gaus_exp_pol2, bkg_exp_pol2 = get_exp_pol2_components(func_exp_pol2)
                voit_chebyshev, gaus_chebyshev, bkg_chebyshev = get_chebyshev_components(func_chebyshev)
                voit_wider_left, gaus_wider_left, bkg_wider_left = get_wider_left_components(func_wider_left)
                voit_wider_right, gaus_wider_right, bkg_wider_right = get_wider_right_components(func_wider_right)
                voit_wider_both, gaus_wider_both, bkg_wider_both = get_wider_both_components(func_wider_both)
                voit_narrow_left, gaus_narrow_left, bkg_narrow_left = get_narrow_left_components(func_narrow_left)
                voit_narrow_right, gaus_narrow_right, bkg_narrow_right = get_narrow_right_components(func_narrow_right)
                voit_narrow_both, gaus_narrow_both, bkg_narrow_both = get_narrow_both_components(func_narrow_both)
                voit_float_voigt_mean, gaus_float_voigt_mean, bkg_float_voigt_mean = get_voigt_mean_float_components(func_float_voigt_mean)
                voit_float_voigt_width, gaus_float_voigt_width, bkg_float_voigt_width = get_voigt_width_float_components(func_float_voigt_width)
                voit_float_gaus_mean, gaus_float_gaus_mean, bkg_float_gaus_mean = get_gaus_mean_float_components(func_float_gaus_mean)
                voit_float_gaus_width, gaus_float_gaus_width, bkg_float_gaus_width = get_gaus_width_float_components(func_float_gaus_width)


                guesses_nominal = update_guesses(func_nominal)
                guesses_pol1 = update_guesses(func_pol1)
                guesses_pol3 = update_guesses(func_pol3)
                guesses_no_gaus = update_guesses(func_no_gaus)
                guesses_exp_pol2 = update_guesses(func_exp_pol2)
                guesses_chebyshev = update_guesses(func_chebyshev)
                guesses_wider_left = update_guesses(func_wider_left)
                guesses_wider_right = update_guesses(func_wider_right)
                guesses_wider_both = update_guesses(func_wider_both)
                guesses_narrow_left = update_guesses(func_narrow_left)
                guesses_narrow_right = update_guesses(func_narrow_right)
                guesses_narrow_both = update_guesses(func_narrow_both)
                guesses_float_voigt_mean = update_guesses(func_float_voigt_mean)
                guesses_float_voigt_width = update_guesses(func_float_voigt_width)
                guesses_float_gaus_mean = update_guesses(func_float_gaus_mean)
                guesses_float_gaus_width = update_guesses(func_float_gaus_width)

                row_nominal = get_dataframe_row(channel, e, t, 'nominal', func_nominal)
                row_pol1 = get_dataframe_row(channel, e, t, 'pol1', func_pol1)
                row_pol3 = get_dataframe_row(channel, e, t, 'pol3', func_pol3)
                row_no_gaus = get_dataframe_row(channel, e, t, 'no_gaus', func_no_gaus)
                row_exp_pol2 = get_dataframe_row(channel, e, t, 'exp_pol2', func_exp_pol2)
                row_chebyshev = get_dataframe_row(channel, e, t, 'chebyshev', func_chebyshev)
                row_wider_left = get_dataframe_row(channel, e, t, 'wider_left', func_wider_left)
                row_wider_right = get_dataframe_row(channel, e, t, 'wider_right', func_wider_right)
                row_wider_both = get_dataframe_row(channel, e, t, 'wider_both', func_wider_both)
                row_narrow_left = get_dataframe_row(channel, e, t, 'narrow_left', func_narrow_left)
                row_narrow_right = get_dataframe_row(channel, e, t, 'narrow_right', func_narrow_right)
                row_narrow_both = get_dataframe_row(channel, e, t, 'narrow_both', func_narrow_both)
                row_float_voigt_mean = get_dataframe_row(channel, e, t, 'float_voigt_mean', func_float_voigt_mean)
                row_float_voigt_width = get_dataframe_row(channel, e, t, 'float_voigt_width', func_float_voigt_width)
                row_float_gaus_mean = get_dataframe_row(channel, e, t, 'float_gaus_mean', func_float_gaus_mean)
                row_float_gaus_width = get_dataframe_row(channel, e, t, 'float_gaus_width', func_float_gaus_width)

                df = df.append(pd.Series(row_nominal, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_pol1, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_pol3, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_no_gaus, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_exp_pol2, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_chebyshev, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_wider_left, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_wider_right, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_wider_both, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_narrow_left, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_narrow_right, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_narrow_both, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_float_voigt_mean, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_float_voigt_width, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_float_gaus_mean, index=df.columns), ignore_index=True)
                df = df.append(pd.Series(row_float_gaus_width, index=df.columns), ignore_index=True)

                c_nominal.cd(t)
                hist.Draw()
                func_nominal.Draw('SAME')
                voit_nominal.Draw('SAME')
                gaus_nominal.Draw('SAME')
                bkg_nominal.Draw('SAME')

                c_pol1.cd(t)
                hist.Draw()
                func_pol1.Draw('SAME')
                voit_pol1.Draw('SAME')
                gaus_pol1.Draw('SAME')
                bkg_pol1.Draw('SAME')

                c_pol3.cd(t)
                hist.Draw()
                func_pol3.Draw('SAME')

                c_no_gaus.cd(t)
                hist.Draw()
                func_no_gaus.Draw('SAME')
                voit_no_gaus.Draw('SAME')
                bkg_no_gaus.Draw('SAME')

                c_exp_pol2.cd(t)
                hist.Draw()
                func_exp_pol2.Draw('SAME')
                voit_exp_pol2.Draw('SAME')
                gaus_exp_pol2.Draw('SAME')
                bkg_exp_pol2.Draw('SAME')

                c_chebyshev.cd(t)
                hist.Draw()
                func_chebyshev.Draw('SAME')
                voit_chebyshev.Draw('SAME')
                gaus_chebyshev.Draw('SAME')
                bkg_chebyshev.Draw('SAME')

                c_wider_left.cd(t)
                hist.Draw()
                func_wider_left.Draw('SAME')
                voit_wider_left.Draw('SAME')
                gaus_wider_left.Draw('SAME')
                bkg_wider_left.Draw('SAME')

                c_wider_right.cd(t)
                hist.Draw()
                func_wider_right.Draw('SAME')
                voit_wider_right.Draw('SAME')
                gaus_wider_right.Draw('SAME')
                bkg_wider_right.Draw('SAME')

                c_wider_both.cd(t)
                hist.Draw()
                func_wider_both.Draw('SAME')
                voit_wider_both.Draw('SAME')
                gaus_wider_both.Draw('SAME')
                bkg_wider_both.Draw('SAME')

                c_narrow_left.cd(t)
                hist.Draw()
                func_narrow_left.Draw('SAME')
                voit_narrow_left.Draw('SAME')
                gaus_narrow_left.Draw('SAME')
                bkg_narrow_left.Draw('SAME')

                c_narrow_right.cd(t)
                hist.Draw()
                func_narrow_right.Draw('SAME')
                voit_narrow_right.Draw('SAME')
                gaus_narrow_right.Draw('SAME')
                bkg_narrow_right.Draw('SAME')

                c_narrow_both.cd(t)
                hist.Draw()
                func_narrow_both.Draw('SAME')
                voit_narrow_both.Draw('SAME')
                gaus_narrow_both.Draw('SAME')
                bkg_narrow_both.Draw('SAME')

                c_float_voigt_mean.cd(t)
                hist.Draw()
                func_float_voigt_mean.Draw('SAME')
                voit_float_voigt_mean.Draw('SAME')
                gaus_float_voigt_mean.Draw('SAME')
                bkg_float_voigt_mean.Draw('SAME')

                c_float_voigt_width.cd(t)
                hist.Draw()
                func_float_voigt_width.Draw('SAME')
                voit_float_voigt_width.Draw('SAME')
                gaus_float_voigt_width.Draw('SAME')
                bkg_float_voigt_width.Draw('SAME')

                c_float_gaus_mean.cd(t)
                hist.Draw()
                func_float_gaus_mean.Draw('SAME')
                voit_float_gaus_mean.Draw('SAME')
                gaus_float_gaus_mean.Draw('SAME')
                bkg_float_gaus_mean.Draw('SAME')
                
                c_float_gaus_width.cd(t)
                hist.Draw()
                func_float_gaus_width.Draw('SAME')
                voit_float_gaus_width.Draw('SAME')
                gaus_float_gaus_width.Draw('SAME')
                bkg_float_gaus_width.Draw('SAME')

            c_nominal.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_nominal_e{e}.pdf')
            c_pol1.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol1_e{e}.pdf')
            c_pol3.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol3_e{e}.pdf')
            c_no_gaus.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_no_gaus_e{e}.pdf')
            c_exp_pol2.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_exp_pol2_e{e}.pdf')
            c_chebyshev.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_chebyshev_e{e}.pdf')
            c_wider_left.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wider_left_e{e}.pdf')
            c_wider_right.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wider_right_e{e}.pdf')
            c_wider_both.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wider_both_e{e}.pdf')
            c_narrow_left.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrow_left_e{e}.pdf')
            c_narrow_right.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrow_right_e{e}.pdf')
            c_narrow_both.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrow_both_e{e}.pdf')
            c_float_voigt_mean.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_float_voigt_mean_e{e}.pdf')
            c_float_voigt_width.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_float_voigt_width_e{e}.pdf')
            c_float_gaus_mean.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_float_gaus_mean_e{e}.pdf')
            c_float_gaus_width.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_float_gaus_width_e{e}.pdf')

    df.to_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv')
    return


if __name__ == '__main__':
    main()