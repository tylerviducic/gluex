# script for making histograms from flat best chi2/ndf trees

import ROOT
import time
import os
import pdb
import random

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

start_time = time.time()


run_period_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017',
}
run_period = 'spring'
data_type = 'phasespace'
charge_channel = 'pipkmks'

file_path = '/work/halld/home/viducic/selector_output/f1_flat/'

data_type_dict = {'data': f'{charge_channel}_filtered_{run_period_dict[run_period]}',
                  'signal_mc': f'mc_{charge_channel}_filtered_{run_period_dict[run_period]}',
                  'phasespace': f'mc_{charge_channel}__phasespace_filtered_{run_period_dict[run_period]}'
                  }


filename = file_path + data_type_dict[data_type] + '.root'
treename = data_type_dict[data_type]


t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']

t_dict = {
    1: (0.0, 0.1), 2: (0.1, 0.2), 3: (0.2, 0.3), 4: (0.3, 0.4), 
    5: (0.4, 0.65), 6: (0.65, 0.9), 7: (0.9, 1.4), 8: (1.4, 1.9)
}

beam_dict = {
    1: (6.5, 7.5), 2: (7.5, 8.5), 3: (8.5, 9.5), 4: (9.5, 10.5)
}


## DEFINE CUTS ##
#TODO cuts to not be just-in-time compiled

ks_pathlength_cut = 'pathlength_sig > 5'
ks_cut1 = 'cos_colin > 0.99'
ks_cut2 = ' vertex_distance > 3'
ks_mass_cut = 'ks_m > 0.45 && ks_m < 0.55'
ppim_mass_cut = 'ppip_m > 1.4'
kmp_mass_cut = 'kmp_m > 1.95'
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'
beam_range = 'e_beam > 6.50000000000 && e_beam <= 10.5'
t_range = 'mand_t <= 1.9'

kstar_no_cut = 'kspip_m > 0.0'
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

kstar_cut_dict = {
    'kspip_m > 0.0': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

f1_cut_list = [kstar_no_cut, kstar_plus_cut, kstar_zero_cut, kstar_all_cut]

t_bin_filter = """
int get_t_bin_index(double t) {
    if (t <= 0.4) {
        return static_cast<int>(t/0.1)+1;
    }
    else if (t > 0.4 && t <= 0.9) {
        return static_cast<int>((t-0.4)/0.25)+5;
    }
    else if (t > 0.9 && t <= 1.9) {
        return static_cast<int>((t-0.9)/0.5)+7;
    }
    else {
        return -1;
    }
}
"""

ROOT.gInterpreter.Declare(t_bin_filter)

df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())

## FILTER DATAFRAME AFTER DATA IS DEFINED ##

# df = df.Filter(beam_range, "beam_range").Filter(t_range, "t_range")
df = df.Filter(beam_range).Filter(t_range)


## LOOP OVER K* CUTS, ENERGY BINS, AND T BINS ## 

n_e_bins = 4
n_t_bins = 8
for cut in f1_cut_list:
        cut_name = kstar_cut_dict[cut]
        
        for energy_index in range(1, n_e_bins+1):
            beam_low = beam_dict[energy_index][0]
            beam_high = beam_dict[energy_index][1]

            for t_index in range(1, n_t_bins+1):
                t_low = t_dict[t_index][0]
                t_high = t_dict[t_index][1]
                df.Filter(cut).Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}', f'E(Beam) = [{beam_low} - {beam_high}], t = [{t_low, t_high}], K* cut = {cut_name}').Report().Print()

    