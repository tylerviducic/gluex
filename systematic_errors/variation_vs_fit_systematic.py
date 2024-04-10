"""script to check if the variations are larger than the error on the fits"""
# TODO: compare the percent change of the variation vs the percent error ont he fit 

import pandas as pd
import numpy as np

max_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/max_changes.csv')
cut_var_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
# print(max_df.columns)

cut_var_df['percent_change_loose'] = np.where(True, (cut_var_df['cross_section_loose'] - cut_var_df['cross_section_nominal'])/cut_var_df['cross_section_nominal'], 0)
cut_var_df['mag_percent_change_loose'] = np.where(True, np.abs((cut_var_df['cross_section_loose'] - cut_var_df['cross_section_nominal'])/cut_var_df['cross_section_nominal']), 0)
cut_var_df['percent_change_tight'] = np.where(True, (cut_var_df['cross_section_tight'] - cut_var_df['cross_section_nominal'])/cut_var_df['cross_section_nominal'], 0)
cut_var_df['mag_percent_change_tight'] = np.where(True, np.abs((cut_var_df['cross_section_tight'] - cut_var_df['cross_section_nominal'])/cut_var_df['cross_section_nominal']), 0)
cut_var_df['mag_percent_change'] = np.where(cut_var_df['mag_percent_change_tight'] > cut_var_df['mag_percent_change_loose'], cut_var_df['mag_percent_change_tight'], cut_var_df['mag_percent_change_loose'])

print(cut_var_df)

signifigant_cuts = pd.DataFrame(columns = ['e', 't', 'channel', 'cut', 'cs_nom', 'cs_varied', 'error_nom', 'error_varied', 'percent_change', 'loose_tight'])
cut_sys_df= cut_var_df[['e', 't', 'channel', 'cut', 'mag_percent_change']]
cut_sys_df.to_csv('/work/halld/home/viducic/systematic_errors/largest_mag_cuts.csv', index = False)

# print(cut_var_df.columns)
# print(cut_var_df.head())


grouped = cut_var_df.groupby(['e', 't', 'channel'])
for name, group in grouped:
    max_fit_deviation = np.abs(max_df.loc[(max_df['e'] == name[0]) & (max_df['t'] == name[1]) & (max_df['channel'] == name[2])]['max_percent_change'].values[0])
    # print(max_fit_deviation)
    # add cut
    # sig_cuts = np.where()
    et_sig_cuts_loose = group.loc[group['mag_percent_change_loose'] > max_fit_deviation][['e', 't', 'channel', 'cut', 'cross_section_nominal', 'cross_section_loose', 'cross_section_error_nominal', 'cross_section_error_loose', 'percent_change_loose']]
    et_sig_cuts_tight = group.loc[group['mag_percent_change_tight'] > max_fit_deviation][['e', 't', 'channel', 'cut', 'cross_section_nominal', 'cross_section_tight', 'cross_section_error_nominal', 'cross_section_error_tight', 'percent_change_tight']]
    # change column names to match the signifigant_cuts df
    et_sig_cuts_loose.columns = ['e', 't', 'channel', 'cut', 'cs_nom', 'cs_varied', 'error_nom', 'error_varied', 'percent_change']
    et_sig_cuts_tight.columns = ['e', 't', 'channel', 'cut', 'cs_nom', 'cs_varied', 'error_nom', 'error_varied', 'percent_change']
    et_sig_cuts_loose['loose_tight'] = 'loose'
    et_sig_cuts_tight['loose_tight'] = 'tight'
    # append these to the di
    signifigant_cuts = signifigant_cuts.append(et_sig_cuts_tight, ignore_index = True)
    signifigant_cuts = signifigant_cuts.append(et_sig_cuts_loose, ignore_index = True)
    
    # print(group)

signifigant_cuts.to_csv('/work/halld/home/viducic/systematic_errors/signifigant_cuts.csv', index = False)