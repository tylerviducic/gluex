import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from barlow_test_cuts import barlow_test
import matplotlib.lines as mlines

# TODO: make figure look nicer

colors_dict = {
    8: ('lightblue', 'lightcoral'),
    9: ('blue', 'red'),
    10: ('slateblue', 'firebrick'),
    11: ('darkblue', 'darkred')
}

def make_legend():
    blue_lines = [mlines.Line2D([], [], color=colors_dict[e][0], label=f'{e} GeV - $\pi^+K^-K_s$') for e in colors_dict.keys()]
    red_lines = [mlines.Line2D([], [], color=colors_dict[e][1], label=f'{e} GeV - $\pi^-K^+K_s$') for e in colors_dict.keys()]
    lines = blue_lines + red_lines
    return lines


df = pd.read_csv('/work/halld/home/viducic/systematic_errors/signifigant_cuts.csv')

df['sigma_barlow'] = np.where(True, barlow_test(df['cs_nom'], df['cs_varied'], df['error_nom'], df['error_varied']), 0)

cut = ['charged_kstar', 'kinfit_cl', 'kp', 'ks_m', 'ksp', 'mx2_all', 'neutral_kstar', 'pathlength', 'pp', 'ppi']
plot_titles = ['Charged $K^*$', 'Kinematic Fit Confidence Level', '$M(Kp)$', '$M(\pi^+\pi^-)$', '$M(K_sp)$', '$M_x^2(pKK\pi)$', 'Neutral $K^*$', 'Path Length', '$\\vec{p}$', '$M(p\pi)$']

grouped = df.groupby(['e', 'cut'])
# print the number of groups
# print(grouped.groups.keys())

fig, axs = plt.subplots(3, 4, sharex=True, sharey=True, figsize=(20, 20))
fig.suptitle('Barlow Test for Cuts with Variations Larger than Fit Systematic', fontsize=16)
for name, group in grouped:
    group_pipkmks = group[group['channel'] == 'pipkmks']
    group_pimkpks = group[group['channel'] == 'pimkpks']
    if name[1] not in cut:
        continue
    if name[1] in ['charged_kstar', 'neutral_kstar']:
        print(group)
    index = cut.index(name[1])
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
    ax.set_xlim(0, 8)
    ax.set_ylim(-20, 20)
    # draw the legend from the charged K* plot on the empty 11th pad
    # if index == 10:
    #     ax.legend()
    #     lines = make_legend()
    #     fig.legend(handles=lines, loc='upper right')

lines = make_legend()
axs[2, 2].legend(handles=lines, prop={'size': 18})
fig.tight_layout()

fig.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_signifigant_cuts.png')
# plt.show()

fig2, axs2 = plt.subplots(3, 4, sharex=True, sharey=True, figsize=(20, 20))
fig2.suptitle('Barlow Test for Cuts with Variations Larger than Fit Systematic', fontsize=16)
for name, group in grouped:
    group_pipkmks = group[group['channel'] == 'pipkmks']
    group_pimkpks = group[group['channel'] == 'pimkpks']
    if name[1] not in cut:
        continue
    # if name[1] in ['charged_kstar', 'neutral_kstar']:
    #     print(group)
    index = cut.index(name[1])
    row_index = index // 4
    col_index = index % 4
    ax2 = axs2[row_index, col_index]
    ax2.scatter(group_pipkmks['t'], group_pipkmks['percent_change'], c=colors_dict[group['e'].values[0]][0], label='$\pi^+K^-K_s$')
    ax2.scatter(group_pimkpks['t'], group_pimkpks['percent_change'], c=colors_dict[group['e'].values[0]][1], label='$\pi^-K^+K_s$')
    ax2.set_title(plot_titles[index])
    ax2.set_xlabel('-t (GeV$^2)$')
    ax2.set_ylabel('Percent Change')
    # ax2.axhline(4.0, linestyle='--')
    # ax2.axhline(-4.0, linestyle='--')
    ax2.set_xlim(0, 8)
    # ax2.set_ylim(-20, 20)
    # draw the legend from the charged K* plot on the empty 11th pad
    # if index == 10:
    #     ax.legend()
    #     lines = make_legend()
    #     fig.legend(handles=lines, loc='upper right')

lines = make_legend()
axs2[2, 2].legend(handles=lines, prop={'size': 18})
fig2.tight_layout()

fig2.savefig('/work/halld/home/viducic/systematic_errors/fit_variation_plots/percent_change_signifigant_cuts.png')


