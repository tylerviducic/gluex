# script to get the integrated acceptance for the binned e and t

import ROOT
import pandas as pd
import numpy as np
from common_analysis_tools import *

channel = 'pimkpks'
# channel = 'pipkmks'

df = pd.DataFrame()

acceptance_list = []
e_list = []
t_list = []

for e in range(7, 11):
    for t in range(1, 8):
        acceptance_spring = get_binned_integrated_phasespace_acceptance(channel, 'spring', e, t, range_lower=1.2, range_upper=1.5)
        acceptance_fall = get_binned_integrated_phasespace_acceptance(channel, 'fall', e, t, range_lower=1.2, range_upper=1.5)
        acceptance_2017 = get_binned_integrated_phasespace_acceptance(channel, '2017', e, t, range_lower=1.2, range_upper=1.5)
        
        lumi_spring = get_luminosity('spring', e-0.5, e+0.5)
        lumi_fall = get_luminosity('fall', e-0.5, e+0.5)
        lumi_2017 = get_luminosity('2017', e-0.5, e+0.5)
        lumi_total = lumi_spring + lumi_fall + lumi_2017

        avg_acceptance = (acceptance_spring*lumi_spring + acceptance_fall*lumi_fall + acceptance_2017*lumi_2017)/lumi_total

        acceptance_list.append(avg_acceptance)
        e_list.append(e)
        t_bin_middle = (t_cut_dict[t][0] + t_cut_dict[t][1]) / 2
        t_list.append(t_bin_middle)

df['acceptance'] = acceptance_list
df['beam_energy'] = e_list
df['t_bin_middle'] = t_list

# write df to a csv 
df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_integrated_acceptance.csv', index=False)

