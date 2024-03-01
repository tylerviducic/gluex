"""script to check how much impact each cut has on the efficiency"""
# TODO: check the change of the efficiency for each cut

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

colors_dict = {
    8: ('lightblue', 'lightcoral'),
    9: ('blue', 'red'),
    10: ('slateblue', 'firebrick'),
    11: ('darkblue', 'darkred')
}

df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
# print(df.columns)
df['acceptance_change_loose'] = np.where(True, (df['f1_acceptance_nominal'] - df['f1_acceptance_loose'])/df['f1_acceptance_nominal'], np.nan)
df['acceptance_change_tight'] = np.where(True, (df['f1_acceptance_nominal'] - df['f1_acceptance_tight'])/df['f1_acceptance_nominal'], np.nan)

acceptance_change = df[['cut', 'e', 't', 'channel', 'f1_acceptance_nominal', 'f1_acceptance_loose', 'f1_acceptance_tight', 'acceptance_change_loose', 'acceptance_change_tight']]

print(acceptance_change.head().to_string())


grouped = df.groupby(['e', 'cut'])
# print(grouped.ngroups)

fig_loose, axs_loose = plt.subplots(4, 3, sharex=True, sharey=True, figsize=(10,10))
fig_tight, axs_tight = plt.subplots(4, 3, sharex=True, sharey=True, figsize=(10,10))
cuts = [cut[1] for cut in grouped.groups.keys()]
# print(cuts)

for name, group in grouped:
    # print(name)
    n_cut = cuts.index(name[1])
    row_index = n_cut // 3
    col_index = n_cut % 3
    group_pipkmks = group[group['channel'] == 'pipkmks']
    group_pimkpks = group[group['channel'] == 'pimkpks']
    axs_loose[row_index, col_index].scatter(group_pipkmks['t'], group_pipkmks['acceptance_change_loose'], label='$\pi^+K^-K_s$', color=colors_dict[name[0]][0])
    axs_loose[row_index, col_index].scatter(group_pimkpks['t'], group_pimkpks['acceptance_change_loose'], label='$\pi^+K^-K_s$', color=colors_dict[name[0]][1])
    axs_tight[row_index, col_index].scatter(group_pipkmks['t'], group_pipkmks['acceptance_change_tight'], label='$\pi^-K^+K_s$', color=colors_dict[name[0]][0])
    axs_tight[row_index, col_index].scatter(group_pimkpks['t'], group_pimkpks['acceptance_change_tight'], label='$\pi^-K^+K_s$', color=colors_dict[name[0]][1])

    axs_loose[row_index, col_index].set_title(f'Cut {name[1]} at E={name[0]}')
    axs_tight[row_index, col_index].set_title(f'Cut {name[1]} at E={name[0]}')

fig_loose.savefig('/work/halld/home/viducic/systematic_errors/efficiency_plots/loose_cut_efficiency_change.png')
fig_tight.savefig('/work/halld/home/viducic/systematic_errors/efficiency_plots/tight_cut_efficiency_change.png')

    


