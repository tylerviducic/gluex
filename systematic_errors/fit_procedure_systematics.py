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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_nominal_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    properties = get_properties(channel)

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


    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    gaus.SetLineColor(properties['background_color'])
    gaus.SetLineStyle(3)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)
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
    range_low, range_high = 1.18, 1.49
    properties = get_properties(channel)
    # func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', properties['range_low'], properties['range_high'])
    func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', range_low, range_high)
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

    properties = get_properties(channel)
    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    gaus.SetLineColor(properties['background_color'])
    gaus.SetLineStyle(3)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)

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

    properties = get_properties(channel)
    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    gaus.SetLineColor(properties['background_color'])
    gaus.SetLineStyle(3)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)

    return voigt, gaus, bkg


# NO GAUS
def get_nogaus_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: -100, # bkg par1
        5: 100, # bkg par2
        6: -100 # bkg par3
    }
    return initial_guesses


def get_nogaus_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_nogaus_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + pol2(4)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # bkg par1
    # func.SetParLimits(4, -100000, 0.0)
    func.SetParameter(5, guesses[5])# bkg par2
    func.SetParameter(6, guesses[6]) # bkg par3
    return func


def get_nogaus_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_nogaus_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))


    bkg = ROOT.TF1(f'bkg_nogaus_{channel}_{e}_{t}', 'pol2(0)', func.GetXmin(), func.GetXmax())
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

    properties = get_properties(channel)
    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)

    return voigt, bkg


# EXPONENTIAL POL2
def get_exppol2_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        2: properties['v_sigma'], # voight sigma
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: 0.01, # bkg par1
        8: 0.01, # bkg par2
    }
    return initial_guesses


def get_exppol2_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_exppol2_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + TMath::Exp([7] + [8]*x)', properties['range_low'], properties['range_high'])
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    return func


def get_exppol2_components(func):
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = ROOT.TF1(f'voigt_exppol2_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', func.GetXmin(), func.GetXmax())
    voigt.SetParameter(0, func.GetParameter(0))
    voigt.SetParameter(1, func.GetParameter(1))
    voigt.SetParameter(2, func.GetParameter(2))
    voigt.SetParameter(3, func.GetParameter(3))

    gaus = ROOT.TF1(f'gaus_exppol2_{channel}_{e}_{t}', 'gaus(0)', func.GetXmin(), func.GetXmax())
    gaus.SetParameter(0, func.GetParameter(4))
    gaus.SetParameter(1, func.GetParameter(5))
    gaus.SetParameter(2, func.GetParameter(6))

    bkg = ROOT.TF1(f'bkg_exppol2_{channel}_{e}_{t}', 'TMath::Exp([0] + [1]*x)', func.GetXmin(), func.GetXmax())
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

    properties = get_properties(channel)
    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    gaus.SetLineColor(properties['background_color'])
    gaus.SetLineStyle(3)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)

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
    # func.SetParLimits(7, -100000, 0.0)
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

    properties = get_properties(channel)
    voigt.SetLineColor(ROOT.kBlack)
    voigt.SetFillColor(properties['f1_color'])
    voigt.SetFillStyle(1001)
    gaus.SetLineColor(properties['background_color'])
    gaus.SetLineStyle(3)
    bkg.SetLineColor(properties['background_color'])
    bkg.SetLineStyle(2)

    return voigt, gaus, bkg


# FLOAT VOIGT MEAN
def get_voigt_mean_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_floatvoigtmean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.SetParameter(1, guesses[1]) # voight mean
    func.SetParLimits(1, 1.25, 1.35)
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_voigt_mean_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_floatvoigtmean_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_floatvoigtmean_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_floatvoigtmean_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT VOIGT WIDTH
def get_voigt_width_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_floatvoigtwidth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.SetParameter(3, guesses[3]) # voight width
    func.SetParLimits(3, 0.01, 0.045)
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_voigt_width_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_floatvoigtwidth_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_floatvoigtwidth_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_floatvoigtwidth_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT GAUS MEAN
def get_gaus_mean_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_floatgausmean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.SetParameter(5, guesses[5])# gaus mean
    func.SetParLimits(5, 1.33, 1.4)
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_gaus_mean_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_floatgausmean_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_floatgausmean_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_floatgausmean_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# FLOAT GAUS WIDTH
def get_gaus_width_float_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_floatgauswidth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.SetParameter(6, guesses[6]) # gaus width
    func.SetParLimits(6, 0.03, 0.05)
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_gaus_width_float_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_floatgauswidth_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_floatgauswidth_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_floatgauswidth_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# WIDE LEFT
def get_wideleft_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_wideleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, properties['range_high'])
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wideleft_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wideleft_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wideleft_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wideleft_{channel}_{e}_{t}')

    return voigt, gaus, bkg

# WIDE RIGHT
def get_wideright_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_wideright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.52)
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wideright_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wideright_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wideright_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wideright_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# WIDE BOTH
def get_wideboth_func(channel, guesses, e, t):
    func = ROOT.TF1(f'func_wideboth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, 1.52)
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_wideboth_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_wideboth_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_wideboth_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_wideboth_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW LEFT
def get_narrowleft_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_narrowleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, properties['range_high'])
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrowleft_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrowleft_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrowleft_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrowleft_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW RIGHT
def get_narrowright_func(channel, guesses, e, t):
    properties = get_properties(channel)
    func = ROOT.TF1(f'func_narrowright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.5)
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
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrowright_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrowright_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrowright_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrowright_{channel}_{e}_{t}')

    return voigt, gaus, bkg


# NARROW BOTH
def get_narrowboth_func(channel, guesses, e, t):
    func = ROOT.TF1(f'func_narrowboth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, 1.5)
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
    # func.SetcooParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


def get_narrowboth_components(func):
    voigt_nom, gaus_nom, bkg_nom = get_nominal_components(func)
    name_root = func.GetName().split('_')
    channel = name_root[2]
    e = name_root[3]
    t = name_root[4]
    voigt = voigt_nom.Clone(f'voigt_narrowboth_{channel}_{e}_{t}')
    gaus = gaus_nom.Clone(f'gaus_narrowboth_{channel}_{e}_{t}')
    bkg = bkg_nom.Clone(f'bkg_narrowboth_{channel}_{e}_{t}')

    return voigt, gaus, bkg


def update_guesses(func):
    n_params = func.GetNpar()
    guesses = {i: func.GetParameter(i) for i in range(n_params)}
    return guesses


def get_dataframe_row(channel, e, t, func_voigt):
    # get dataframe row info from common_analysis_tools
    f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error = tools.calculate_dataframe_info(func_voigt, channel, e, t)
    row = [f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error]
    return row


def main():
    ROOT.gROOT.SetBatch(True)
    print('Running')

    column_headers = [
                    'channel', 'e', 't', 
                    'nominal_yield', 'nominal_yield_error', 'nominal_acceptance', 'nominal_acceptance_error', 'nominal_cross_section', 'nominal_cross_section_error',
                    'pol1_yield', 'pol1_yield_error', 'pol1_acceptance', 'pol1_acceptance_error', 'pol1_cross_section', 'pol1_cross_section_error',
                    'pol3_yield', 'pol3_yield_error', 'pol3_acceptance', 'pol3_acceptance_error', 'pol3_cross_section', 'pol3_cross_section_error',
                    'nogaus_yield', 'nogaus_yield_error', 'nogaus_acceptance', 'nogaus_acceptance_error', 'nogaus_cross_section', 'nogaus_cross_section_error',
                    'exppol2_yield', 'exppol2_yield_error', 'exppol2_acceptance', 'exppol2_acceptance_error', 'exppol2_cross_section', 'exppol2_cross_section_error',
                    'chebyshev_yield', 'chebyshev_yield_error', 'chebyshev_acceptance', 'chebyshev_acceptance_error', 'chebyshev_cross_section', 'chebyshev_cross_section_error',
                    'wideleft_yield', 'wideleft_yield_error', 'wideleft_acceptance', 'wideleft_acceptance_error', 'wideleft_cross_section', 'wideleft_cross_section_error',
                    'wideright_yield', 'wideright_yield_error', 'wideright_acceptance', 'wideright_acceptance_error', 'wideright_cross_section', 'wideright_cross_section_error',
                    'wideboth_yield', 'wideboth_yield_error', 'wideboth_acceptance', 'wideboth_acceptance_error', 'wideboth_cross_section', 'wideboth_cross_section_error',
                    'narrowleft_yield', 'narrowleft_yield_error', 'narrowleft_acceptance', 'narrowleft_acceptance_error', 'narrowleft_cross_section', 'narrowleft_cross_section_error',
                    'narrowright_yield', 'narrowright_yield_error', 'narrowright_acceptance', 'narrowright_acceptance_error', 'narrowright_cross_section', 'narrowright_cross_section_error',
                    'narrowboth_yield', 'narrowboth_yield_error', 'narrowboth_acceptance', 'narrowboth_acceptance_error', 'narrowboth_cross_section', 'narrowboth_cross_section_error',
                    'floatvoigtmean_yield', 'floatvoigtmean_yield_error', 'floatvoigtmean_acceptance', 'floatvoigtmean_acceptance_error', 'floatvoigtmean_cross_section', 'floatvoigtmean_cross_section_error',
                    'floatvoigtwidth_yield', 'floatvoigtwidth_yield_error', 'floatvoigtwidth_acceptance', 'floatvoigtwidth_acceptance_error', 'floatvoigtwidth_cross_section', 'floatvoigtwidth_cross_section_error',
                    'floatgausmean_yield', 'floatgausmean_yield_error', 'floatgausmean_acceptance', 'floatgausmean_acceptance_error', 'floatgausmean_cross_section', 'floatgausmean_cross_section_error',
                    'floatgauswidth_yield', 'floatgauswidth_yield_error', 'floatgauswidth_acceptance', 'floatgauswidth_acceptance_error', 'floatgauswidth_cross_section', 'floatgauswidth_cross_section_error'
                      ]
    
    df = pd.DataFrame(columns=column_headers)

    c_nominal = ROOT.TCanvas('c_nominal', 'c_nominal', 800, 600)
    c_pol1 = ROOT.TCanvas('c_pol1', 'c_pol1', 800, 600)
    c_pol3 = ROOT.TCanvas('c_pol3', 'c_pol3', 800, 600)
    c_nogaus = ROOT.TCanvas('c_nogaus', 'c_nogaus', 800, 600)
    c_exppol2 = ROOT.TCanvas('c_exppol2', 'c_exppol2', 800, 600)
    c_chebyshev = ROOT.TCanvas('c_chebyshev', 'c_chebyshev', 800, 600)
    c_wideleft = ROOT.TCanvas('c_wideleft', 'c_wideleft', 800, 600)
    c_wideright = ROOT.TCanvas('c_wideright', 'c_wideright', 800, 600)
    c_wideboth = ROOT.TCanvas('c_wideboth', 'c_wideboth', 800, 600)
    c_narrowleft = ROOT.TCanvas('c_narrowleft', 'c_narrowleft', 800, 600)
    c_narrowright = ROOT.TCanvas('c_narrowright', 'c_narrowright', 800, 600)
    c_narrowboth = ROOT.TCanvas('c_narrowboth', 'c_narrowboth', 800, 600)
    c_floatvoigtmean = ROOT.TCanvas('c_floatvoigtmean', 'c_floatvoigtmean', 800, 600)
    c_floatvoigtwidth = ROOT.TCanvas('c_floatvoigtwidth', 'c_floatvoigtwidth', 800, 600)
    c_floatgausmean = ROOT.TCanvas('c_floatgausmean', 'c_floatgausmean', 800, 600)
    c_floatgauswidth = ROOT.TCanvas('c_floatgauswidth', 'c_floatgauswidth', 800, 600)

    funcs_nominal = []
    funcs_pol1 = []
    funcs_pol3 = []
    funcs_nogaus = []
    funcs_exppol2 = []
    funcs_chebyshev = []
    funcs_wideleft = []
    funcs_wideright = []
    funcs_wideboth = []
    funcs_narrowleft = []
    funcs_narrowright = []
    funcs_narrowboth = []
    funcs_floatvoigtmean = []
    funcs_floatvoigtwidth = []
    funcs_floatgausmean = []
    funcs_floatgauswidth = []
    hists = []

    for channel in ['pipkmks', 'pimkpks']:
        properties = get_properties(channel)
        for e in range(8, 13):
            guesses_nominal = get_nominal_guesses(properties)
            guesses_pol1 = get_pol1_guesses(properties)
            guesses_pol3 = get_pol3_guesses(properties)
            guesses_nogaus = get_nogaus_guesses(properties)
            guesses_exppol2 = get_exppol2_guesses(properties)
            guesses_chebyshev = get_chebyshev_guesses(properties)
            guesses_wideleft = get_nominal_guesses(properties)
            guesses_wideright = get_nominal_guesses(properties)
            guesses_wideboth = get_nominal_guesses(properties)
            guesses_narrowleft = get_nominal_guesses(properties)
            guesses_narrowright = get_nominal_guesses(properties)
            guesses_narrowboth = get_nominal_guesses(properties)
            guesses_floatvoigtmean = get_nominal_guesses(properties)
            guesses_floatvoigtwidth = get_nominal_guesses(properties)
            guesses_floatgausmean = get_nominal_guesses(properties)
            guesses_floatgauswidth = get_nominal_guesses(properties)

            c_nominal.Clear()
            c_pol1.Clear()
            c_pol3.Clear()
            c_nogaus.Clear()
            c_exppol2.Clear()
            c_chebyshev.Clear()
            c_wideleft.Clear()
            c_wideright.Clear()
            c_wideboth.Clear()
            c_narrowleft.Clear()
            c_narrowright.Clear()
            c_narrowboth.Clear()
            c_floatvoigtmean.Clear()
            c_floatvoigtwidth.Clear()
            c_floatgausmean.Clear()
            c_floatgauswidth.Clear()

            c_nominal.Divide(4, 2)
            c_pol1.Divide(4, 2)
            c_pol3.Divide(4, 2)
            c_nogaus.Divide(4, 2)
            c_exppol2.Divide(4, 2)
            c_chebyshev.Divide(4, 2)
            c_wideleft.Divide(4, 2)
            c_wideright.Divide(4, 2)
            c_wideboth.Divide(4, 2)
            c_narrowleft.Divide(4, 2)
            c_narrowright.Divide(4, 2)
            c_narrowboth.Divide(4, 2)
            c_floatvoigtmean.Divide(4, 2)
            c_floatvoigtwidth.Divide(4, 2)
            c_floatgausmean.Divide(4, 2)
            c_floatgauswidth.Divide(4, 2)

            for t in range(1, 8):
                hist = get_data(channel, e, t)
                hists.append(hist)

                func_nominal = get_nominal_func(channel, guesses_nominal, e, t)
                func_pol1 = get_pol1_func(channel, guesses_pol1, e, t)
                func_pol3 = get_pol3_func(channel, guesses_pol3, e, t)
                func_nogaus = get_nogaus_func(channel, guesses_nogaus, e, t)
                func_exppol2 = get_exppol2_func(channel, guesses_exppol2, e, t)
                func_chebyshev = get_chebyshev_func(channel, guesses_chebyshev, e, t)
                func_wideleft = get_wideleft_func(channel, guesses_wideleft, e, t)
                func_wideright = get_wideright_func(channel, guesses_wideright, e, t)
                func_wideboth = get_wideboth_func(channel, guesses_wideboth, e, t)
                func_narrowleft = get_narrowleft_func(channel, guesses_narrowleft, e, t)
                func_narrowright = get_narrowright_func(channel, guesses_narrowright, e, t)
                func_narrowboth = get_narrowboth_func(channel, guesses_narrowboth, e, t)
                func_floatvoigtmean = get_voigt_mean_float_func(channel, guesses_floatvoigtmean, e, t)
                func_floatvoigtwidth = get_voigt_width_float_func(channel, guesses_floatvoigtwidth, e, t)
                func_floatgausmean = get_gaus_mean_float_func(channel, guesses_floatgausmean, e, t)
                func_floatgauswidth = get_gaus_width_float_func(channel, guesses_floatgauswidth, e, t)

                result_nominal = hist.Fit(func_nominal, 'SRBEQ0')
                result_pol1 = hist.Fit(func_pol1, 'SRBEQ0')
                result_pol3 = hist.Fit(func_pol3, 'SRBEQ0')
                result_nogaus = hist.Fit(func_nogaus, 'SRBEQ0')
                result_exppol2 = hist.Fit(func_exppol2, 'SRBEQ0')
                result_chebyshev = hist.Fit(func_chebyshev, 'SRBEQ0')
                result_wideleft = hist.Fit(func_wideleft, 'SRBEQ0')
                result_wideright = hist.Fit(func_wideright, 'SRBEQ0')
                result_wideboth = hist.Fit(func_wideboth, 'SRBEQ0')
                result_narrowleft = hist.Fit(func_narrowleft, 'SRBEQ0')
                result_narrowright = hist.Fit(func_narrowright, 'SRBEQ0')
                result_narrowboth = hist.Fit(func_narrowboth, 'SRBEQ0')
                result_floatvoigtmean = hist.Fit(func_floatvoigtmean, 'SRBEQ0')
                result_floatvoigtwidth = hist.Fit(func_floatvoigtwidth, 'SRBEQ0')
                result_floatgausmean = hist.Fit(func_floatgausmean, 'SRBEQ0')
                result_floatgauswidth = hist.Fit(func_floatgauswidth, 'SRBEQ0')

                voit_nominal, gaus_nominal, bkg_nominal = get_nominal_components(func_nominal)
                voit_pol1, gaus_pol1, bkg_pol1 = get_pol1_components(func_pol1)
                voit_pol3, gaus_pol3, bkg_pol3 = get_pol3_components(func_pol3)
                voit_nogaus, bkg_nogaus = get_nogaus_components(func_nogaus)
                voit_exppol2, gaus_exppol2, bkg_exppol2 = get_exppol2_components(func_exppol2)
                voit_chebyshev, gaus_chebyshev, bkg_chebyshev = get_chebyshev_components(func_chebyshev)
                voit_wideleft, gaus_wideleft, bkg_wideleft = get_wideleft_components(func_wideleft)
                voit_wideright, gaus_wideright, bkg_wideright = get_wideright_components(func_wideright)
                voit_wideboth, gaus_wideboth, bkg_wideboth = get_wideboth_components(func_wideboth)
                voit_narrowleft, gaus_narrowleft, bkg_narrowleft = get_narrowleft_components(func_narrowleft)
                voit_narrowright, gaus_narrowright, bkg_narrowright = get_narrowright_components(func_narrowright)
                voit_narrowboth, gaus_narrowboth, bkg_narrowboth = get_narrowboth_components(func_narrowboth)
                voit_floatvoigtmean, gaus_floatvoigtmean, bkg_floatvoigtmean = get_voigt_mean_float_components(func_floatvoigtmean)
                voit_floatvoigtwidth, gaus_floatvoigtwidth, bkg_floatvoigtwidth = get_voigt_width_float_components(func_floatvoigtwidth)
                voit_floatgausmean, gaus_floatgausmean, bkg_floatgausmean = get_gaus_mean_float_components(func_floatgausmean)
                voit_floatgauswidth, gaus_floatgauswidth, bkg_floatgauswidth = get_gaus_width_float_components(func_floatgauswidth)

                funcs_nominal.append((func_nominal, voit_nominal, gaus_nominal, bkg_nominal))
                funcs_pol1.append((func_pol1, voit_pol1, gaus_pol1, bkg_pol1))
                funcs_pol3.append((func_pol3, voit_pol3, gaus_pol3, bkg_pol3))
                funcs_nogaus.append((func_nogaus, voit_nogaus, bkg_nogaus))
                funcs_exppol2.append((func_exppol2, voit_exppol2, gaus_exppol2, bkg_exppol2))
                funcs_chebyshev.append((func_chebyshev, voit_chebyshev, gaus_chebyshev, bkg_chebyshev))
                funcs_wideleft.append((func_wideleft, voit_wideleft, gaus_wideleft, bkg_wideleft))
                funcs_wideright.append((func_wideright, voit_wideright, gaus_wideright, bkg_wideright))
                funcs_wideboth.append((func_wideboth, voit_wideboth, gaus_wideboth, bkg_wideboth))
                funcs_narrowleft.append((func_narrowleft, voit_narrowleft, gaus_narrowleft, bkg_narrowleft))
                funcs_narrowright.append((func_narrowright, voit_narrowright, gaus_narrowright, bkg_narrowright))
                funcs_narrowboth.append((func_narrowboth, voit_narrowboth, gaus_narrowboth, bkg_narrowboth))
                funcs_floatvoigtmean.append((func_floatvoigtmean, voit_floatvoigtmean, gaus_floatvoigtmean, bkg_floatvoigtmean))
                funcs_floatvoigtwidth.append((func_floatvoigtwidth, voit_floatvoigtwidth, gaus_floatvoigtwidth, bkg_floatvoigtwidth))
                funcs_floatgausmean.append((func_floatgausmean, voit_floatgausmean, gaus_floatgausmean, bkg_floatgausmean))
                funcs_floatgauswidth.append((func_floatgauswidth, voit_floatgauswidth, gaus_floatgauswidth, bkg_floatgauswidth))


                guesses_nominal = update_guesses(func_nominal)
                guesses_pol1 = update_guesses(func_pol1)
                guesses_pol3 = update_guesses(func_pol3)
                guesses_nogaus = update_guesses(func_nogaus)
                guesses_exppol2 = update_guesses(func_exppol2)
                guesses_chebyshev = update_guesses(func_chebyshev)
                guesses_wideleft = update_guesses(func_wideleft)
                guesses_wideright = update_guesses(func_wideright)
                guesses_wideboth = update_guesses(func_wideboth)
                guesses_narrowleft = update_guesses(func_narrowleft)
                guesses_narrowright = update_guesses(func_narrowright)
                guesses_narrowboth = update_guesses(func_narrowboth)
                guesses_floatvoigtmean = update_guesses(func_floatvoigtmean)
                guesses_floatvoigtwidth = update_guesses(func_floatvoigtwidth)
                guesses_floatgausmean = update_guesses(func_floatgausmean)
                guesses_floatgauswidth = update_guesses(func_floatgauswidth)

                row_nominal = get_dataframe_row(channel, e, t, func_nominal)
                row_pol1 = get_dataframe_row(channel, e, t, func_pol1)
                row_pol3 = get_dataframe_row(channel, e, t, func_pol3)
                row_nogaus = get_dataframe_row(channel, e, t, func_nogaus)
                row_exppol2 = get_dataframe_row(channel, e, t, func_exppol2)
                row_chebyshev = get_dataframe_row(channel, e, t, func_chebyshev)
                row_wideleft = get_dataframe_row(channel, e, t, func_wideleft)
                row_wideright = get_dataframe_row(channel, e, t, func_wideright)
                row_wideboth = get_dataframe_row(channel, e, t, func_wideboth)
                row_narrowleft = get_dataframe_row(channel, e, t, func_narrowleft)
                row_narrowright = get_dataframe_row(channel, e, t, func_narrowright)
                row_narrowboth = get_dataframe_row(channel, e, t, func_narrowboth)
                row_floatvoigtmean = get_dataframe_row(channel, e, t, func_floatvoigtmean)
                row_floatvoigtwidth = get_dataframe_row(channel, e, t, func_floatvoigtwidth)
                row_floatgausmean = get_dataframe_row(channel, e, t, func_floatgausmean)
                row_floatgauswidth = get_dataframe_row(channel, e, t, func_floatgauswidth)

                row = [channel, e, t]
                full_row = row + row_nominal + row_pol1 + row_pol3 + row_nogaus + row_exppol2 + row_chebyshev + row_wideleft + row_wideright + row_wideboth + row_narrowleft + row_narrowright + row_narrowboth + row_floatvoigtmean + row_floatvoigtwidth + row_floatgausmean + row_floatgauswidth
                
                df = df.append(pd.Series(full_row, index=df.columns), ignore_index=True)

                # df = df.append(pd.Series(row_nominal, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_pol1, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_pol3, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_nogaus, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_exppol2, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_chebyshev, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_wideleft, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_wideright, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_wideboth, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_narrowleft, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_narrowright, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_narrowboth, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_floatvoigtmean, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_floatvoigtwidth, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_floatgausmean, index=df.columns), ignore_index=True)
                # df = df.append(pd.Series(row_floatgauswidth, index=df.columns), ignore_index=True)

                c_nominal.cd(t)
                hists[-1].Draw()
                funcs_nominal[-1][0].Draw('SAME')
                funcs_nominal[-1][1].Draw('SAME')
                funcs_nominal[-1][2].Draw('SAME')
                funcs_nominal[-1][3].Draw('SAME')


                c_pol1.cd(t)
                hists[-1].Draw()
                funcs_pol1[-1][0].Draw('SAME')
                funcs_pol1[-1][1].Draw('SAME')
                funcs_pol1[-1][2].Draw('SAME')
                funcs_pol1[-1][3].Draw('SAME')

                c_pol3.cd(t)
                hists[-1].Draw()
                funcs_pol3[-1][0].Draw('SAME')
                funcs_pol3[-1][1].Draw('SAME')
                funcs_pol3[-1][2].Draw('SAME')
                funcs_pol3[-1][3].Draw('SAME')

                c_nogaus.cd(t)
                hists[-1].Draw()
                funcs_nogaus[-1][0].Draw('SAME')
                funcs_nogaus[-1][1].Draw('SAME')
                funcs_nogaus[-1][2].Draw('SAME')

                c_exppol2.cd(t)
                hists[-1].Draw()
                funcs_exppol2[-1][0].Draw('SAME')
                funcs_exppol2[-1][1].Draw('SAME')
                funcs_exppol2[-1][2].Draw('SAME')
                funcs_exppol2[-1][3].Draw('SAME')

                c_chebyshev.cd(t)
                hists[-1].Draw()
                funcs_chebyshev[-1][0].Draw('SAME')
                funcs_chebyshev[-1][1].Draw('SAME')
                funcs_chebyshev[-1][2].Draw('SAME')
                funcs_chebyshev[-1][3].Draw('SAME')

                c_wideleft.cd(t)
                hists[-1].Draw()
                funcs_wideleft[-1][0].Draw('SAME')
                funcs_wideleft[-1][1].Draw('SAME')
                funcs_wideleft[-1][2].Draw('SAME')
                funcs_wideleft[-1][3].Draw('SAME')

                c_wideright.cd(t)
                hists[-1].Draw()
                funcs_wideright[-1][0].Draw('SAME')
                funcs_wideright[-1][1].Draw('SAME')
                funcs_wideright[-1][2].Draw('SAME')
                funcs_wideright[-1][3].Draw('SAME')

                c_wideboth.cd(t)
                hists[-1].Draw()
                funcs_wideboth[-1][0].Draw('SAME')
                funcs_wideboth[-1][1].Draw('SAME')
                funcs_wideboth[-1][2].Draw('SAME')
                funcs_wideboth[-1][3].Draw('SAME')

                c_narrowleft.cd(t)
                hists[-1].Draw()
                funcs_narrowleft[-1][0].Draw('SAME')
                funcs_narrowleft[-1][1].Draw('SAME')
                funcs_narrowleft[-1][2].Draw('SAME')
                funcs_narrowleft[-1][3].Draw('SAME')

                c_narrowright.cd(t)
                hists[-1].Draw()
                funcs_narrowright[-1][0].Draw('SAME')
                funcs_narrowright[-1][1].Draw('SAME')
                funcs_narrowright[-1][2].Draw('SAME')
                funcs_narrowright[-1][3].Draw('SAME')

                c_narrowboth.cd(t)
                hists[-1].Draw()
                funcs_narrowboth[-1][0].Draw('SAME')
                funcs_narrowboth[-1][1].Draw('SAME')
                funcs_narrowboth[-1][2].Draw('SAME')
                funcs_narrowboth[-1][3].Draw('SAME')

                c_floatvoigtmean.cd(t)
                hists[-1].Draw()
                funcs_floatvoigtmean[-1][0].Draw('SAME')
                funcs_floatvoigtmean[-1][1].Draw('SAME')
                funcs_floatvoigtmean[-1][2].Draw('SAME')
                funcs_floatvoigtmean[-1][3].Draw('SAME')

                c_floatvoigtwidth.cd(t)
                hists[-1].Draw()
                funcs_floatvoigtwidth[-1][0].Draw('SAME')
                funcs_floatvoigtwidth[-1][1].Draw('SAME')
                funcs_floatvoigtwidth[-1][2].Draw('SAME')
                funcs_floatvoigtwidth[-1][3].Draw('SAME')

                c_floatgausmean.cd(t)
                hists[-1].Draw()
                funcs_floatgausmean[-1][0].Draw('SAME')
                funcs_floatgausmean[-1][1].Draw('SAME')
                funcs_floatgausmean[-1][2].Draw('SAME')
                funcs_floatgausmean[-1][3].Draw('SAME')
                
                c_floatgauswidth.cd(t)
                hists[-1].Draw()
                funcs_floatgauswidth[-1][0].Draw('SAME')
                funcs_floatgauswidth[-1][1].Draw('SAME')
                funcs_floatgauswidth[-1][2].Draw('SAME')
                funcs_floatgauswidth[-1][3].Draw('SAME')

                c_nominal.Update()
                c_pol1.Update()
                c_pol3.Update()
                c_nogaus.Update()
                c_exppol2.Update()
                c_chebyshev.Update()
                c_wideleft.Update()
                c_wideright.Update()
                c_wideboth.Update()
                c_narrowleft.Update()
                c_narrowright.Update()
                c_narrowboth.Update()
                c_floatvoigtmean.Update()
                c_floatvoigtwidth.Update()
                c_floatgausmean.Update()
                c_floatgauswidth.Update()

            c_nominal.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_nominal_e{e}.pdf')
            c_pol1.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol1_e{e}.pdf')
            c_pol3.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol3_e{e}.pdf')
            c_nogaus.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_nogaus_e{e}.pdf')
            c_exppol2.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_exppol2_e{e}.pdf')
            c_chebyshev.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_chebyshev_e{e}.pdf')
            c_wideleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideleft_e{e}.pdf')
            c_wideright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideright_e{e}.pdf')
            c_wideboth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideboth_e{e}.pdf')
            c_narrowleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowleft_e{e}.pdf')
            c_narrowright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowright_e{e}.pdf')
            c_narrowboth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowboth_e{e}.pdf')
            c_floatvoigtmean.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatvoigtmean_e{e}.pdf')
            c_floatvoigtwidth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatvoigtwidth_e{e}.pdf')
            c_floatgausmean.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgausmean_e{e}.pdf')
            c_floatgauswidth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgauswidth_e{e}.pdf')

    df.to_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv')
    return


if __name__ == '__main__':
    # TODO: solve the problems

    """problems
    [DONE] pimkpks exp 8, 9, 10, 11 (params probably)
    [DONE] pimkpks float gaus mean 9, 11
    [DONE] pimkpks float gaus width 8, 10, 
    [DONE] pimkpks float voigt width 8, 9, 10, 11
    [DONE] pimkpks no gaus 8, 9, 10, 11
    [ALL GOOD] pimkpks pol1 11

    [DONE] pipkmks exp 8, 9, 10, 11 (params probably)
    [DONE] pipkmks float gaus mean 11 
    [DONE] pipkmks float gaus width 8, 9
    [DONE] pipkmks float voigt mean 11
    [DONE] pipkmks float voigt width 8, 9, 10, 11
    [DONE] pipkmks no gaus 8, 9, 10, 11
    [ALL GOOD] pipkmks pol3 fit range might be wrong

    """
    main()