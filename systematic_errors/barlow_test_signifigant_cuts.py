import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from barlow_test_cuts import barlow_test

colors_dict = {
    8: ('lightblue', 'lightcoral'),
    9: ('blue', 'red'),
    10: ('slateblue', 'firebrick'),
    11: ('darkblue', 'darkred')
}

df = pd.read_csv('/work/halld/home/viducic/systematic_errors/signifigant_cuts.csv')

df['sigma_barlow'] = np.where(True, barlow_test(df['cs_nom'], df['cs_varied'], df['error_nom'], df['error_varied']), 0)

cut = ['charged_kstar', 'kinfit_cl', 'kp', 'ks_m', 'ksp', 'mx2_all', 'neutral_kstar', 'pathlength', 'pp', 'ppi']
plot_titles = ['Charged $K^*$', 'Kinematic Fit Confidence Level', '$K^+$', '$K_s$ Mass', '$K_s$ Momentum', '$M_x^2$ All', 'Neutral $K^*$', 'Path Length', '$p$', '$p\pi$']

grouped = df.groupby('cut')
# print the number of groups
# print(grouped.groups.keys())

fig, axs = plt.subplots(3, 4, sharex=True, sharey=True, figsize=(20, 20))
fig.suptitle('Barlow Test for Cuts with Variations Larger than Fit Systematic', fontsize=16)
for name, group in grouped:
    group_pipkmks = group[group['channel'] == 'pipkmks']
    group_pimkpks = group[group['channel'] == 'pimkpks']
    index = cut.index(name)
    row_index = index // 4
    col_index = index % 4
    ax = axs[row_index, col_index]
    ax.scatter(group_pipkmks['t'], group_pipkmks['sigma_barlow'], c=colors_dict[group['e'].values[0]][0], label='$\pi^+K^-K_s$')
    ax.scatter(group_pimkpks['t'], group_pimkpks['sigma_barlow'], c=colors_dict[group['e'].values[0]][1], label='$\pi^-K^+K_s$')
    ax.set_title(plot_titles[index])
    ax.set_xlabel('-t (GeV$^2)$')
    ax.set_ylabel('$\sigma_{Barlow}$')
    ax.axhline(4.0, linestyle='--')
    ax.axhline(-4.0, linestyle='--')
    ax.legend()
    ax.set_xlim(0, 8)
    ax.set_ylim(-15, 15)
fig.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_signifigant_cuts.png')
# plt.show()



