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
    hist.GetXaxis().SetRangeUser(1.1, 1.65)
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
            'range_low': 1.16,
            'range_high': 1.63
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
            'range_low': 1.16,
            'range_high': 1.63
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
    func.SetParLimits(4, 0.1, 100000)
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
    range_low, range_high = 1.18, 1.5
    properties = get_properties(channel)
    # func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', properties['range_low'], properties['range_high'])
    func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', range_low, range_high)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func.SetParLimits(4, 0.1, 100000)
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
    func.SetParLimits(4, 0.1, 100000)
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




# FLOAT VOIGT WIDTH
# LEFT 
def get_voigt_width_float_left_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        width = constants.F1_PIPKMKS_VOIGHT_WIDTH - constants.F1_PIPKMKS_VOIGHT_WIDTH_ERROR
    else:
        width = constants.F1_PIMKPKS_VOIGHT_WIDTH - constants.F1_PIMKPKS_VOIGHT_WIDTH_ERROR
    func = ROOT.TF1(f'func_floatvoigtwidthleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, width) # voight width
    # func.SetParLimits(3, 0.01, 0.045)
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func

# RIGHT
def get_voigt_width_float_right_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        width = constants.F1_PIPKMKS_VOIGHT_WIDTH + constants.F1_PIPKMKS_VOIGHT_WIDTH_ERROR
    else:
        width = constants.F1_PIMKPKS_VOIGHT_WIDTH + constants.F1_PIMKPKS_VOIGHT_WIDTH_ERROR
    func = ROOT.TF1(f'func_floatvoigtwidthright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, width) # voight width
    # func.SetParLimits(3, 0.01, 0.045)
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
#LEFT
def get_gaus_mean_float_left_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        mean = constants.F1_PIPKMKS_GAUS_MEAN - constants.F1_PIPKMKS_GAUS_MEAN_ERROR
    else:
        mean = constants.F1_PIMKPKS_GAUS_MEAN - constants.F1_PIMKPKS_GAUS_MEAN_ERROR
    func = ROOT.TF1(f'func_floatgausmeanleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
    func.FixParameter(5, mean) # gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


#RIGHT
def get_gaus_mean_float_right_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        mean = constants.F1_PIPKMKS_GAUS_MEAN + constants.F1_PIPKMKS_GAUS_MEAN_ERROR
    else:
        mean = constants.F1_PIMKPKS_GAUS_MEAN + constants.F1_PIMKPKS_GAUS_MEAN_ERROR
    func = ROOT.TF1(f'func_floatgausmeanright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
    func.FixParameter(5, mean) # gaus mean
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
#LEFT
def get_gaus_width_float_left_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        width = constants.F1_PIPKMKS_GAUS_WIDTH - constants.F1_PIPKMKS_GAUS_WIDTH_ERROR
    else:
        width = constants.F1_PIMKPKS_GAUS_WIDTH - constants.F1_PIMKPKS_GAUS_WIDTH_ERROR
    func = ROOT.TF1(f'func_floatgauswidthleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, width) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    # func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


#RIGHT
def get_gaus_width_float_right_func(channel, guesses, e, t):
    properties = get_properties(channel)
    if channel == 'pipkmks':
        width = constants.F1_PIPKMKS_GAUS_WIDTH + constants.F1_PIPKMKS_GAUS_WIDTH_ERROR
    else:
        width = constants.F1_PIMKPKS_GAUS_WIDTH + constants.F1_PIMKPKS_GAUS_WIDTH_ERROR
    func = ROOT.TF1(f'func_floatgauswidthright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, width) # gaus width
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
    func = ROOT.TF1(f'func_wideleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.15, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func = ROOT.TF1(f'func_wideright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.64)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func = ROOT.TF1(f'func_wideboth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.15, 1.64)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func = ROOT.TF1(f'func_narrowleft_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.17, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func = ROOT.TF1(f'func_narrowright_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.62)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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
    func = ROOT.TF1(f'func_narrowboth_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.17, 1.62)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, tools.get_binned_resolution(channel, e, t)) # voight sigma
    func.FixParameter(3, guesses[3]) # voigt width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 100000)
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


def get_dataframe_row(channel, e, t, func, hist):
    # get dataframe row info from common_analysis_tools
    f1_yield, f1_yield_error, f1_acceptance, f1_acceptance_error, cross_section, cross_section_error = tools.calculate_dataframe_info(func, hist, channel, e, t, fitsys=True)
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
                    'wideleft_yield', 'wideleft_yield_error', 'wideleft_acceptance', 'wideleft_acceptance_error', 'wideleft_cross_section', 'wideleft_cross_section_error',
                    'wideright_yield', 'wideright_yield_error', 'wideright_acceptance', 'wideright_acceptance_error', 'wideright_cross_section', 'wideright_cross_section_error',
                    'wideboth_yield', 'wideboth_yield_error', 'wideboth_acceptance', 'wideboth_acceptance_error', 'wideboth_cross_section', 'wideboth_cross_section_error',
                    'narrowleft_yield', 'narrowleft_yield_error', 'narrowleft_acceptance', 'narrowleft_acceptance_error', 'narrowleft_cross_section', 'narrowleft_cross_section_error',
                    'narrowright_yield', 'narrowright_yield_error', 'narrowright_acceptance', 'narrowright_acceptance_error', 'narrowright_cross_section', 'narrowright_cross_section_error',
                    'narrowboth_yield', 'narrowboth_yield_error', 'narrowboth_acceptance', 'narrowboth_acceptance_error', 'narrowboth_cross_section', 'narrowboth_cross_section_error',
                    'floatvoigtwidthleft_yield', 'floatvoigtwidthleft_yield_error', 'floatvoigtwidthleft_acceptance', 'floatvoigtwidthleft_acceptance_error', 'floatvoigtwidthleft_cross_section', 'floatvoigtwidthleft_cross_section_error',
                    'floatvoigtwidthright_yield', 'floatvoigtwidthright_yield_error', 'floatvoigtwidthright_acceptance', 'floatvoigtwidthright_acceptance_error', 'floatvoigtwidthright_cross_section', 'floatvoigtwidthright_cross_section_error',
                    'floatgausmeanleft_yield', 'floatgausmeanleft_yield_error', 'floatgausmeanleft_acceptance', 'floatgausmeanleft_acceptance_error', 'floatgausmeanleft_cross_section', 'floatgausmeanleft_cross_section_error',
                    'floatgausmeanright_yield', 'floatgausmeanright_yield_error', 'floatgausmeanright_acceptance', 'floatgausmeanright_acceptance_error', 'floatgausmeanright_cross_section', 'floatgausmeanright_cross_section_error',
                    'floatgauswidthleft_yield', 'floatgauswidthleft_yield_error', 'floatgauswidthleft_acceptance', 'floatgauswidthleft_acceptance_error', 'floatgauswidthleft_cross_section', 'floatgauswidthleft_cross_section_error',
                    'floatgauswidthright_yield', 'floatgauswidthright_yield_error', 'floatgauswidthright_acceptance', 'floatgauswidthright_acceptance_error', 'floatgauswidthright_cross_section', 'floatgauswidthright_cross_section_error'
                      ]
    
    rows = {header: [] for header in column_headers}
    # df = pd.DataFrame(columns=column_headers)

    c_nominal = ROOT.TCanvas('c_nominal', 'c_nominal', 800, 600)
    c_pol1 = ROOT.TCanvas('c_pol1', 'c_pol1', 800, 600)
    c_pol3 = ROOT.TCanvas('c_pol3', 'c_pol3', 800, 600)
    c_nogaus = ROOT.TCanvas('c_nogaus', 'c_nogaus', 800, 600)
    c_wideleft = ROOT.TCanvas('c_wideleft', 'c_wideleft', 800, 600)
    c_wideright = ROOT.TCanvas('c_wideright', 'c_wideright', 800, 600)
    c_wideboth = ROOT.TCanvas('c_wideboth', 'c_wideboth', 800, 600)
    c_narrowleft = ROOT.TCanvas('c_narrowleft', 'c_narrowleft', 800, 600)
    c_narrowright = ROOT.TCanvas('c_narrowright', 'c_narrowright', 800, 600)
    c_narrowboth = ROOT.TCanvas('c_narrowboth', 'c_narrowboth', 800, 600)
    c_floatvoigtwidthleft = ROOT.TCanvas('c_floatvoigtwidthleft', 'c_floatvoigtwidthleft', 800, 600)
    c_floatvoigtwidthright = ROOT.TCanvas('c_floatvoigtwidthright', 'c_floatvoigtwidthright', 800, 600)
    c_floatgausmeanleft = ROOT.TCanvas('c_floatgausmeanleft', 'c_floatgausmeanleft', 800, 600)
    c_floatgausmeanright = ROOT.TCanvas('c_floatgausmeanright', 'c_floatgausmeanright', 800, 600)
    c_floatgauswidthleft = ROOT.TCanvas('c_floatgauswidthleft', 'c_floatgauswidthleft', 800, 600)
    c_floatgauswidthright = ROOT.TCanvas('c_floatgauswidthright', 'c_floatgauswidthright', 800, 600)

    funcs_nominal = []
    funcs_pol1 = []
    funcs_pol3 = []
    funcs_nogaus = []
    funcs_wideleft = []
    funcs_wideright = []
    funcs_wideboth = []
    funcs_narrowleft = []
    funcs_narrowright = []
    funcs_narrowboth = []
    funcs_floatvoigtwidthleft = []
    funcs_floatvoigtwidthright = []
    funcs_floatgausmeanleft = []
    funcs_floatgausmeanright = []
    funcs_floatgauswidthleft = []
    funcs_floatgauswidthright = []
    hists = []

    for channel in ['pipkmks', 'pimkpks']:
        properties = get_properties(channel)
        for e in range(8, 13):
            guesses_nominal = get_nominal_guesses(properties)
            guesses_pol1 = get_pol1_guesses(properties)
            guesses_pol3 = get_pol3_guesses(properties)
            guesses_nogaus = get_nogaus_guesses(properties)
            guesses_wideleft = get_nominal_guesses(properties)
            guesses_wideright = get_nominal_guesses(properties)
            guesses_wideboth = get_nominal_guesses(properties)
            guesses_narrowleft = get_nominal_guesses(properties)
            guesses_narrowright = get_nominal_guesses(properties)
            guesses_narrowboth = get_nominal_guesses(properties)
            guesses_floatvoigtwidthleft = get_nominal_guesses(properties)
            guesses_floatvoigtwidthright = get_nominal_guesses(properties)
            guesses_floatgausmeanleft = get_nominal_guesses(properties)
            guesses_floatgausmeanright = get_nominal_guesses(properties)
            guesses_floatgauswidthleft = get_nominal_guesses(properties)
            guesses_floatgauswidthright = get_nominal_guesses(properties)

            c_nominal.Clear()
            c_pol1.Clear()
            c_pol3.Clear()
            c_nogaus.Clear()
            c_wideleft.Clear()
            c_wideright.Clear()
            c_wideboth.Clear()
            c_narrowleft.Clear()
            c_narrowright.Clear()
            c_narrowboth.Clear()
            c_floatvoigtwidthleft.Clear()
            c_floatvoigtwidthright.Clear()
            c_floatgausmeanleft.Clear()
            c_floatgausmeanright.Clear()
            c_floatgauswidthleft.Clear()
            c_floatgauswidthright.Clear()

            c_nominal.Divide(4, 2)
            c_pol1.Divide(4, 2)
            c_pol3.Divide(4, 2)
            c_nogaus.Divide(4, 2)
            c_wideleft.Divide(4, 2)
            c_wideright.Divide(4, 2)
            c_wideboth.Divide(4, 2)
            c_narrowleft.Divide(4, 2)
            c_narrowright.Divide(4, 2)
            c_narrowboth.Divide(4, 2)
            c_floatvoigtwidthleft.Divide(4, 2)
            c_floatvoigtwidthright.Divide(4, 2)
            c_floatgausmeanleft.Divide(4, 2)
            c_floatgausmeanright.Divide(4, 2)
            c_floatgauswidthleft.Divide(4, 2)
            c_floatgauswidthright.Divide(4, 2)

            for t in range(1, 8):
                hist = get_data(channel, e, t)
                hists.append(hist)

                func_nominal = get_nominal_func(channel, guesses_nominal, e, t)
                func_pol1 = get_pol1_func(channel, guesses_pol1, e, t)
                func_pol3 = get_pol3_func(channel, guesses_pol3, e, t)
                func_nogaus = get_nogaus_func(channel, guesses_nogaus, e, t)
                func_wideleft = get_wideleft_func(channel, guesses_wideleft, e, t)
                func_wideright = get_wideright_func(channel, guesses_wideright, e, t)
                func_wideboth = get_wideboth_func(channel, guesses_wideboth, e, t)
                func_narrowleft = get_narrowleft_func(channel, guesses_narrowleft, e, t)
                func_narrowright = get_narrowright_func(channel, guesses_narrowright, e, t)
                func_narrowboth = get_narrowboth_func(channel, guesses_narrowboth, e, t)
                func_floatvoigtwidthleft = get_voigt_width_float_left_func(channel, guesses_floatvoigtwidthleft, e, t)
                func_floatvoigtwidthright = get_voigt_width_float_right_func(channel, guesses_floatvoigtwidthright, e, t)
                func_floatgausmeanleft = get_gaus_mean_float_left_func(channel, guesses_floatgausmeanleft, e, t)
                func_floatgausmeanright = get_gaus_mean_float_right_func(channel, guesses_floatgausmeanright, e, t)
                func_floatgauswidthleft = get_gaus_width_float_left_func(channel, guesses_floatgauswidthleft, e, t)
                func_floatgauswidthright = get_gaus_width_float_right_func(channel, guesses_floatgauswidthright, e, t)

                result_nominal = hist.Fit(func_nominal, 'SRBQ0')
                result_pol1 = hist.Fit(func_pol1, 'SRBQ0')
                result_pol3 = hist.Fit(func_pol3, 'SRBQ0')
                result_nogaus = hist.Fit(func_nogaus, 'SRBQ0')
                result_wideleft = hist.Fit(func_wideleft, 'SRBQ0')
                result_wideright = hist.Fit(func_wideright, 'SRBQ0')
                result_wideboth = hist.Fit(func_wideboth, 'SRBQ0')
                result_narrowleft = hist.Fit(func_narrowleft, 'SRBQ0')
                result_narrowright = hist.Fit(func_narrowright, 'SRBQ0')
                result_narrowboth = hist.Fit(func_narrowboth, 'SRBQ0')
                result_floatvoigtwidthleft = hist.Fit(func_floatvoigtwidthleft, 'SRBQ0')
                result_floatvoigtwidthright = hist.Fit(func_floatvoigtwidthright, 'SRBQ0')
                result_floatgausmeanleft = hist.Fit(func_floatgausmeanleft, 'SRBQ0')
                result_floatgausmeanright = hist.Fit(func_floatgausmeanright, 'SRBQ0')
                result_floatgauswidthleft = hist.Fit(func_floatgauswidthleft, 'SRBQ0')
                result_floatgauswidthright = hist.Fit(func_floatgauswidthright, 'SRBQ0')

                voit_nominal, gaus_nominal, bkg_nominal = get_nominal_components(func_nominal)
                voit_pol1, gaus_pol1, bkg_pol1 = get_pol1_components(func_pol1)
                voit_pol3, gaus_pol3, bkg_pol3 = get_pol3_components(func_pol3)
                voit_nogaus, bkg_nogaus = get_nogaus_components(func_nogaus)
                voit_wideleft, gaus_wideleft, bkg_wideleft = get_wideleft_components(func_wideleft)
                voit_wideright, gaus_wideright, bkg_wideright = get_wideright_components(func_wideright)
                voit_wideboth, gaus_wideboth, bkg_wideboth = get_wideboth_components(func_wideboth)
                voit_narrowleft, gaus_narrowleft, bkg_narrowleft = get_narrowleft_components(func_narrowleft)
                voit_narrowright, gaus_narrowright, bkg_narrowright = get_narrowright_components(func_narrowright)
                voit_narrowboth, gaus_narrowboth, bkg_narrowboth = get_narrowboth_components(func_narrowboth)
                voit_floatvoigtwidthleft, gaus_floatvoigtwidthleft, bkg_floatvoigtwidthleft = get_voigt_width_float_components(func_floatvoigtwidthleft)
                voit_floatvoigtwidthright, gaus_floatvoigtwidthright, bkg_floatvoigtwidthright = get_voigt_width_float_components(func_floatvoigtwidthright)
                voit_floatgausmeanleft, gaus_floatgausmeanleft, bkg_floatgausmeanleft = get_gaus_mean_float_components(func_floatgausmeanleft)
                voit_floatgausmeanright, gaus_floatgausmeanright, bkg_floatgausmeanright = get_gaus_mean_float_components(func_floatgausmeanright)
                voit_floatgauswidthleft, gaus_floatgauswidthleft, bkg_floatgauswidthleft = get_gaus_width_float_components(func_floatgauswidthleft)
                voit_floatgauswidthright, gaus_floatgauswidthright, bkg_floatgauswidthright = get_gaus_width_float_components(func_floatgauswidthright)

                funcs_nominal.append((func_nominal, voit_nominal, gaus_nominal, bkg_nominal))
                funcs_pol1.append((func_pol1, voit_pol1, gaus_pol1, bkg_pol1))
                funcs_pol3.append((func_pol3, voit_pol3, gaus_pol3, bkg_pol3))
                funcs_nogaus.append((func_nogaus, voit_nogaus, bkg_nogaus))
                funcs_wideleft.append((func_wideleft, voit_wideleft, gaus_wideleft, bkg_wideleft))
                funcs_wideright.append((func_wideright, voit_wideright, gaus_wideright, bkg_wideright))
                funcs_wideboth.append((func_wideboth, voit_wideboth, gaus_wideboth, bkg_wideboth))
                funcs_narrowleft.append((func_narrowleft, voit_narrowleft, gaus_narrowleft, bkg_narrowleft))
                funcs_narrowright.append((func_narrowright, voit_narrowright, gaus_narrowright, bkg_narrowright))
                funcs_narrowboth.append((func_narrowboth, voit_narrowboth, gaus_narrowboth, bkg_narrowboth))
                funcs_floatvoigtwidthleft.append((func_floatvoigtwidthleft, voit_floatvoigtwidthleft, gaus_floatvoigtwidthleft, bkg_floatvoigtwidthleft))
                funcs_floatvoigtwidthright.append((func_floatvoigtwidthright, voit_floatvoigtwidthright, gaus_floatvoigtwidthright, bkg_floatvoigtwidthright))
                funcs_floatgausmeanleft.append((func_floatgausmeanleft, voit_floatgausmeanleft, gaus_floatgausmeanleft, bkg_floatgausmeanleft))
                funcs_floatgausmeanright.append((func_floatgausmeanright, voit_floatgausmeanright, gaus_floatgausmeanright, bkg_floatgausmeanright))
                funcs_floatgauswidthleft.append((func_floatgauswidthleft, voit_floatgauswidthleft, gaus_floatgauswidthleft, bkg_floatgauswidthleft))
                funcs_floatgauswidthright.append((func_floatgauswidthright, voit_floatgauswidthright, gaus_floatgauswidthright, bkg_floatgauswidthright))


                guesses_nominal = update_guesses(func_nominal)
                guesses_pol1 = update_guesses(func_pol1)
                guesses_pol3 = update_guesses(func_pol3)
                guesses_nogaus = update_guesses(func_nogaus)
                guesses_wideleft = update_guesses(func_wideleft)
                guesses_wideright = update_guesses(func_wideright)
                guesses_wideboth = update_guesses(func_wideboth)
                guesses_narrowleft = update_guesses(func_narrowleft)
                guesses_narrowright = update_guesses(func_narrowright)
                guesses_narrowboth = update_guesses(func_narrowboth)
                guesses_floatvoigtwidthleft = update_guesses(func_floatvoigtwidthleft)
                guesses_floatvoigtwidthright = update_guesses(func_floatvoigtwidthright)
                guesses_floatgausmeanleft = update_guesses(func_floatgausmeanleft)
                guesses_floatgausmeanright = update_guesses(func_floatgausmeanright)
                guesses_floatgauswidthleft = update_guesses(func_floatgauswidthleft)
                guesses_floatgauswidthright = update_guesses(func_floatgauswidthright)

                row_nominal = get_dataframe_row(channel, e, t, func_nominal, hists[-1])
                row_pol1 = get_dataframe_row(channel, e, t, func_pol1, hists[-1])
                row_pol3 = get_dataframe_row(channel, e, t, func_pol3, hists[-1])
                row_nogaus = get_dataframe_row(channel, e, t, func_nogaus, hists[-1])
                row_wideleft = get_dataframe_row(channel, e, t, func_wideleft, hists[-1])
                row_wideright = get_dataframe_row(channel, e, t, func_wideright, hists[-1])
                row_wideboth = get_dataframe_row(channel, e, t, func_wideboth, hists[-1])
                row_narrowleft = get_dataframe_row(channel, e, t, func_narrowleft, hists[-1])
                row_narrowright = get_dataframe_row(channel, e, t, func_narrowright, hists[-1])
                row_narrowboth = get_dataframe_row(channel, e, t, func_narrowboth, hists[-1])
                row_floatvoigtwidthleft = get_dataframe_row(channel, e, t, func_floatvoigtwidthleft, hists[-1])
                row_floatvoigtwidthright = get_dataframe_row(channel, e, t, func_floatvoigtwidthright, hists[-1])
                row_floatgausmeanleft = get_dataframe_row(channel, e, t, func_floatgausmeanleft, hists[-1])
                row_floatgausmeanright = get_dataframe_row(channel, e, t, func_floatgausmeanright, hists[-1])
                row_floatgauswidthleft = get_dataframe_row(channel, e, t, func_floatgauswidthleft, hists[-1])
                row_floatgauswidthright = get_dataframe_row(channel, e, t, func_floatgauswidthright, hists[-1])

                row = [channel, e, t]
                full_row = row + row_nominal + row_pol1 + row_pol3 + row_nogaus + row_wideleft + row_wideright + row_wideboth + row_narrowleft + row_narrowright + row_narrowboth + row_floatvoigtwidthleft + row_floatvoigtwidthright + row_floatgausmeanleft + row_floatgausmeanright + row_floatgauswidthleft  + row_floatgauswidthright
                # print(len(full_row))
                # print(len(rows))

                # for r in rows.keys():
                #     print(r)

                for i, header in enumerate(column_headers):
                    rows[header].append(full_row[i])

                # for key, val in rows.items():
                #     print(key, val)

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

                c_floatvoigtwidthleft.cd(t)
                hists[-1].Draw()
                funcs_floatvoigtwidthleft[-1][0].Draw('SAME')
                funcs_floatvoigtwidthleft[-1][1].Draw('SAME')
                funcs_floatvoigtwidthleft[-1][2].Draw('SAME')
                funcs_floatvoigtwidthleft[-1][3].Draw('SAME')

                c_floatgausmeanleft.cd(t)
                hists[-1].Draw()
                funcs_floatgausmeanleft[-1][0].Draw('SAME')
                funcs_floatgausmeanleft[-1][1].Draw('SAME')
                funcs_floatgausmeanleft[-1][2].Draw('SAME')
                funcs_floatgausmeanleft[-1][3].Draw('SAME')
                
                c_floatgauswidthleft.cd(t)
                hists[-1].Draw()
                funcs_floatgauswidthleft[-1][0].Draw('SAME')
                funcs_floatgauswidthleft[-1][1].Draw('SAME')
                funcs_floatgauswidthleft[-1][2].Draw('SAME')
                funcs_floatgauswidthleft[-1][3].Draw('SAME')

                c_floatvoigtwidthright.cd(t)
                hists[-1].Draw()
                funcs_floatvoigtwidthright[-1][0].Draw('SAME')
                funcs_floatvoigtwidthright[-1][1].Draw('SAME')
                funcs_floatvoigtwidthright[-1][2].Draw('SAME')
                funcs_floatvoigtwidthright[-1][3].Draw('SAME')

                c_floatgausmeanright.cd(t)
                hists[-1].Draw()
                funcs_floatgausmeanright[-1][0].Draw('SAME')
                funcs_floatgausmeanright[-1][1].Draw('SAME')
                funcs_floatgausmeanright[-1][2].Draw('SAME')
                funcs_floatgausmeanright[-1][3].Draw('SAME')
                
                c_floatgauswidthright.cd(t)
                hists[-1].Draw()
                funcs_floatgauswidthright[-1][0].Draw('SAME')
                funcs_floatgauswidthright[-1][1].Draw('SAME')
                funcs_floatgauswidthright[-1][2].Draw('SAME')
                funcs_floatgauswidthright[-1][3].Draw('SAME')

                c_nominal.Update()
                c_pol1.Update()
                c_pol3.Update()
                c_nogaus.Update()
                c_wideleft.Update()
                c_wideright.Update()
                c_wideboth.Update()
                c_narrowleft.Update()
                c_narrowright.Update()
                c_narrowboth.Update()
                c_floatvoigtwidthleft.Update()
                c_floatvoigtwidthright.Update()
                c_floatgausmeanleft.Update()
                c_floatgausmeanright.Update()
                c_floatgauswidthleft.Update()
                c_floatgauswidthright.Update()

            c_nominal.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_nominal_e{e}.pdf')
            c_pol1.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol1_e{e}.pdf')
            c_pol3.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_pol3_e{e}.pdf')
            c_nogaus.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_nogaus_e{e}.pdf')
            c_wideleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideleft_e{e}.pdf')
            c_wideright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideright_e{e}.pdf')
            c_wideboth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_wideboth_e{e}.pdf')
            c_narrowleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowleft_e{e}.pdf')
            c_narrowright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowright_e{e}.pdf')
            c_narrowboth.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_narrowboth_e{e}.pdf')
            c_floatvoigtwidthleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatvoigtwidthleft_e{e}.pdf')
            c_floatvoigtwidthright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatvoigtwidthright_e{e}.pdf')
            c_floatgausmeanleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgausmeanleft_e{e}.pdf')
            c_floatgausmeanright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgausmeanright_e{e}.pdf')
            c_floatgauswidthleft.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgauswidthleft_e{e}.pdf')
            c_floatgauswidthright.SaveAs(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/{channel}_floatgauswidthright_e{e}.pdf')
    
    df = pd.DataFrame(rows)
    df.to_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv')
    return


if __name__ == '__main__':

    """problems


    """
    main()