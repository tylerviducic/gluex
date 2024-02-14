"""script to vary the fitting procedure to estimate the systematic errors"""

import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants

def get_data(channel, e, t):
    if channel == 'pipkmks':
        hist_title = 'K^{-}K_{s}#pi^{+}'
    elif channel == 'pimkpks':
        hist_title = 'K^{+}K_{s}#pi^{-}'

    cor_hist = tools.get_binned_gluex1_kstar_corrected_data(channel, e, t)
    hist = tools.remove_zero_datapoints(cor_hist)
    hist.GetXaxis().SetRangeUser(1.15, 1.52)
    hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)

    hist.GetXaxis().SetTitle(hist_title + ' (GeV)')
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetTitle('Counts/10 MeV')

    hist.SetTitle('E_{#gamma} = ' + str(e) + ' GeV || ' + f'{constants.T_CUT_DICT[t][0]} < -t < {constants.T_CUT_DICT[t][1]}' + ' GeV^{2}')
    hist.SetTitleSize(0.055)
    hist.SetDirectory(0)
    return hist

# FIXME: guesses need to be a parameter passed to the methods that return the functions so that they can be updated
def get_properties(channel):
    if channel == 'pipkmks':
        properties = {
            'v_mean': constants.F1_PIPKMKS_VOIGHT_MEAN,
            'v_width': constants.F1_PIPKMKS_VOIGHT_WIDTH,
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
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_nominal_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_nominal_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# POL1
def get_pol1_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
    }
    return initial_guesses


def pol1_fit(channel, e, t):
    properties = get_properties(channel)
    guesses = get_pol1_guesses(properties)
    func = ROOT.TF1(f'func_pol1_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol1(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParameter(8, guesses[8]) # bkg par2
    return func


# POL3
def get_pol3_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
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


def pol3_fit(channel, e, t):
    properties = get_properties(channel)
    guesses = get_pol3_guesses(properties)
    func = ROOT.TF1(f'func_pol3_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol3(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    func.SetParameter(10, guesses[10]) # bkg par4
    return func


# NO GAUS
def get_no_gaus_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        3: properties['v_width'], # voight width
        4: -100, # bkg par1
        5: 100, # bkg par2
        6: 1 # bkg par3
    }
    return initial_guesses


def get_no_gaus_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_no_gaus_guesses(properties)
    func = ROOT.TF1(f'func_nominal_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + pol2(4)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # bkg par1
    func.SetParLimits(4, -100000, 0.0)
    func.FixParameter(5, guesses[5])# bkg par2
    func.FixParameter(6, guesses[6]) # bkg par3
    return func


# EXPONENTIAL POL2
def get_exp_pol2_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: 1, # bkg par1
        8: 1, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_exp_pol2_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_exp_pol2_guesses(properties)
    func = ROOT.TF1(f'func_exp_pol2_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + ROOT.TMath.Exp(par[6] + par[7]*x + par[8]*x*x)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# CHEBYSHEV
def get_chebyshev_guesses(properties):
    initial_guesses = {
        0: 5, # voight amplitude
        1: properties['v_mean'], # voight mean
        3: properties['v_width'], # voight width
        4: 15, # gaus amplitude
        5: properties['gaus_mean'], # gaus mean
        6: properties['gaus_width'], # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    return initial_guesses


def get_chebyshev_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_chebyshev_guesses(properties)
    func = ROOT.TF1(f'func_chebyshev_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + cheb2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# FLOAT VOIGT MEAN
def get_voigt_mean_float_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_float_voigt_mean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.SetParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# FLOAT VOIGT WIDTH
def get_voigt_width_float_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_float_voigt_width_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
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


# FLOAT GAUS MEAN
def get_voigt_mean_float_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_float_gaus_mean_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.SetParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# FLOAT GAUS WIDTH
def get_voigt_width_float_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_float_gaus_width_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.SetParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# WIDE LEFT
def get_wider_left_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_wider_left_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# WIDE RIGHT
def get_wider_right_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_wider_right_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.52)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# WIDE BOTH
def get_wider_both_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_wider_both_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.14, 1.52)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# NARROW LEFT
def get_narrow_left_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_narrow_left_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, properties['range_high'])
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# NARROW RIGHT
def get_narrow_right_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_narrow_right_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', properties['range_low'], 1.5)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func


# NARROW BOTH
def get_narrow_both_func(channel, e, t):
    properties = get_properties(channel)
    guesses = get_nominal_guesses(properties)
    func = ROOT.TF1(f'func_narrow_both_{channel}_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', 1.16, 1.5)
    func.SetParameter(0, guesses[0]) # voight amplitude
    func.SetParLimits(0, 0.1, 100000)
    func.FixParameter(1, guesses[1]) # voight mean
    func.FixParameter(2, guesses[3]) # voight width
    func.SetParameter(4, guesses[4]) # gaus amplitude
    func.SetParLimits(4, 0.1, 10000)
    func.FixParameter(5, guesses[5])# gaus mean
    func.FixParameter(6, guesses[6]) # gaus width
    func.SetParameter(7, guesses[7]) # bkg par1
    func.SetParLimits(7, -100000, 0.0)
    func.SetParameter(8, guesses[8]) # bkg par2
    func.SetParameter(9, guesses[9]) # bkg par3
    return func
    

def fit_hist(hist, func, guesses):
    return


def main():
    return


if __name__ == '__main__':
    main()