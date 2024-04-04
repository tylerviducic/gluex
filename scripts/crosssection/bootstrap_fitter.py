import ROOT
import my_library.common_analysis_tools as tools
import my_library.kinematic_cuts as kcuts
import my_library.constants as constants
import pandas as pd
import numpy as np

# channel = 'pipkmks'
channel = 'pimkpks'

#TODO: move this to contants
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

#TODO: move this to contants or tools
df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv') 

# amplitude_df = pd.DataFrame(columns=['t_bin', 'e_bin', 'trial', 'amplitude'])

fit_low, fit_high = 1.15, 1.51

rows = {
    'e_bin': [],
    't_bin': [],
    'trial': [],
    'amplitude': []
}

rng = np.random.default_rng()

for e in range(8, 12):
# for e in range(8, 9):
    luminosity = tools.get_luminosity_gluex_1(e-0.5, e+0.5)*1000

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
    # for t in range(2, 3):
        cor_hist = tools.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist = tools.remove_zero_datapoints(cor_hist)
        hist.GetXaxis().SetRangeUser(fit_low, fit_high)
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]

        f_nominal = ROOT.TF1(f'fnominal_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', fit_low, fit_high)
        f_nominal.SetParameter(0, initial_guesses[0]) # voight amplitude
        f_nominal.SetParLimits(0, 0.1, 100000)
        f_nominal.FixParameter(1, initial_guesses[1]) # voight mean
        f_nominal.FixParameter(2, e_t_sigma)
        f_nominal.FixParameter(3, initial_guesses[3]) # voight width
        f_nominal.SetParameter(4, initial_guesses[4]) # gaus amplitude
        f_nominal.SetParLimits(4, 0.1, 10000)
        f_nominal.FixParameter(5, initial_guesses[5])# gaus mean
        f_nominal.FixParameter(6, initial_guesses[6]) # gaus width
        f_nominal.SetParameter(7, initial_guesses[7]) # bkg par1
        f_nominal.SetParameter(8, initial_guesses[8]) # bkg par2
        f_nominal.SetParameter(9, initial_guesses[9]) # bkg par3

        r_nom = hist.Fit(f_nominal, 'SRBEQ')
        amp_nom = f_nominal.GetParameter(0)
        snom = f_nominal.GetParError(0)

        hists = []

        # for i in range(1, 101):
        for i in range(1, 101):
            trial_hist = hist.Clone(f"trial_{i}")
            trial_hist.SetTitle(f"trial_{i}")
            trial_hist.GetXaxis().SetRangeUser(fit_low, fit_high)
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
            
            f_trial = f_nominal.Clone(f'ftrial_{i}')

            r = trial_hist.Fit(f_trial, 'SRBEQ')
            amp = f_trial.GetParameter(0)

            rows['t_bin'].append(t)
            rows['e_bin'].append(e)
            rows['trial'].append(i)
            rows['amplitude'].append(amp)

        initial_guesses[0] = f_nominal.GetParameter(0)
        initial_guesses[4] = f_nominal.GetParameter(4)
        initial_guesses[7] = f_nominal.GetParameter(7)
        initial_guesses[8] = f_nominal.GetParameter(8)
        initial_guesses[9] = f_nominal.GetParameter(9)

bs_df = pd.DataFrame(rows)
bs_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/bootstrap_amplitudes.csv', index=False)






