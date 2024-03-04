"""script to check if the variations are larger than the error on the fits"""
# TODO: compare the percent change of the variation vs the percent error ont he fit 

import pandas as pd
import numpy as np

max_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/max_changes.csv')
cut_var_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
# print(max_df.columns)

cut_var_df['percent_change_loose'] = np.where(True, cut_var_df['cross_section_loose'] - cut_var_df['cross_section_nominal']/cut_var_df['cross_section_nominal'], 0)
cut_var_df['percent_change_tight'] = np.where(True, cut_var_df['cross_section_tight'] - cut_var_df['cross_section_nominal']/cut_var_df['cross_section_nominal'], 0)

signifigant_cuts = pd.DataFrame(columns = ['e', 't', 'channel', 'cut', 'cs_nom', 'cs_varied', 'error_nom', 'error_varied', 'percent_change', 'loose_tight'])

# print(cut_var_df.columns)
# print(cut_var_df.head())

# TODO: select only the variations > the systematic on the fit

grouped = cut_var_df.groupby(['e', 't', 'channel'])
for name, group in grouped:
    max_fit_deviation = max_df.loc[(max_df['e'] == name[0]) & (max_df['t'] == name[1]) & (max_df['channel'] == name[2])]['max_percent_change'].values[0]
    # print(max_fit_deviation)
    # add cut
    # sig_cuts = np.where()
    et_sig_cuts_loose = group.loc[group['percent_change_loose'] > max_fit_deviation][['e', 't', 'channel', 'cut', 'cross_section_nominal', 'cross_section_loose', 'cross_section_error_nominal', 'cross_section_error_loose', 'percent_change_loose']]
    et_sig_cuts_tight = group.loc[group['percent_change_tight'] > max_fit_deviation][['e', 't', 'channel', 'cut', 'cross_section_nominal', 'cross_section_tight', 'cross_section_error_nominal', 'cross_section_error_tight', 'percent_change_tight']]
    print(et_sig_cuts_loose)
    et_sig_cuts_loose['loose_tight'] = 'loose'
    et_sig_cuts_tight['loose_tight'] = 'tight'
    signigigant_cuts = signifigant_cuts.append(et_sig_cuts_tight, ignore_index = True)
    
    # print(group)

print(signifigant_cuts.head())