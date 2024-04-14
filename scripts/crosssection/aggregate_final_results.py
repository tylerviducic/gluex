import numpy as np
import pandas as pd

path_to_fit_result_files = '/work/halld/home/viducic/data/fit_params/{}/tf1_gaus_cross_section_values.csv'
path_to_errors_file = '/work/halld/home/viducic/systematic_errors/cs_total_error.csv'

results_pipkmks = pd.read_csv(path_to_fit_result_files.format('pipkmks'))
results_pimkpks = pd.read_csv(path_to_fit_result_files.format('pimkpks'))

errors = pd.read_csv(path_to_errors_file)
errors = errors.rename(columns={'e': 'beam_energy', 't': 't_bin_middle'})

pipkmks_errors = errors[errors['channel'] == 'pipkmks']
pimkpks_errors = errors[errors['channel'] == 'pimkpks']

merged_pipkmks = results_pipkmks.merge(pipkmks_errors, on=['beam_energy', 't_bin_middle'], how='inner')
merged_pimkpks = results_pimkpks.merge(pimkpks_errors, on=['beam_energy', 't_bin_middle'], how='inner')
merged_pipkmks['fit_error'] = np.abs(merged_pipkmks['fit_error'])
merged_pimkpks['fit_error'] = np.abs(merged_pimkpks['fit_error'])
# print(merged_pipkmks.columns)
# print(merged_pipkmks)

final_pipkmks = merged_pipkmks[['beam_energy', 't_bin_middle', 't_bin_width', 'cross_section', 'stat_error', 'fit_error', 'cut_error', 'sys_error', 'total_percent_error']]
final_pimkpks = merged_pimkpks[['beam_energy', 't_bin_middle', 't_bin_width', 'cross_section', 'stat_error', 'fit_error', 'cut_error', 'sys_error', 'total_percent_error']]
final_pipkmks.to_csv('/work/halld/home/viducic/data/fit_params/pipkmks/cs_final.csv')
final_pimkpks.to_csv('/work/halld/home/viducic/data/fit_params/pimkpks/cs_final.csv')
