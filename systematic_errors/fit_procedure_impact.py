import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

colors_dict = {
        8: ('lightblue', 'lightcoral'),
        9: ('blue', 'red'),
        10: ('slateblue', 'firebrick'),
        11: ('darkblue', 'darkred'),
        12: ('darkslateblue', 'darkred')
    }


df = pd.read_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv', index_col=0)


variations = ['nominal', 'pol1', 'pol3', 'nogaus', 'exppol2', 'chebyshev', 'wideleft',
            'wideright', 'wideboth', 'narrowleft', 'narrowright', 'narrowboth',
            'floatvoigtmean', 'floatvoigtwidth', 'floatgausmean', 'floatgauswidth']

for var in variations:
    df[f'{var}_percent_change'] = np.where(True, (df[f'{var}_cross_section'] - df['nominal_cross_section'])/df['nominal_cross_section'], np.nan)

fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(20, 20))

grouped = df.groupby(['e'])
for name, group in grouped:
    # print(name)
    # print(group.head())

    for i, var in enumerate(variations):
        row_index = i // 4
        col_index = i % 4
        ax[row_index, col_index].clear()
        group_pipkmks = group[group['channel'] == 'pipkmks']
        group_pimkpks = group[group['channel'] == 'pimkpks']
        ax[row_index, col_index].scatter(group_pipkmks['t'], group_pipkmks[f'{var}_percent_change'], label='$\pi^+K^-K_s$', color=colors_dict[name][0])
        ax[row_index, col_index].scatter(group_pimkpks['t'], group_pimkpks[f'{var}_percent_change'], label='$\pi^-K^+K_s$', color=colors_dict[name][1])
        ax[row_index, col_index].set_title(f'{var} at E={name}')
        ax[row_index, col_index].set_xlabel('t bin')
        ax[row_index, col_index].set_ylabel('percent change')
        # ax[row_index, col_index].axhline(0.1, linestyle='--')
        ax[row_index, col_index].axhline(0.1, linestyle='--')
        ax[row_index, col_index].axhline(0.05, linestyle='--')
        ax[row_index, col_index].legend()
        # ax[row_index, col_index].set_ylim([0.0, 0.015])
    fig.savefig(f'/work/halld/home/viducic/systematic_errors/fit_variation_plots/percent_change_{name}.png')

max_df = pd.DataFrame(columns = ['e', 't', 'channel', 'max_var', 'max_percent_change'])
max_grouped = df.groupby(['e', 't'])
for name, group in max_grouped:
    cols = [f'{var}_percent_change' for var in variations]
    pipkmks_group = group[group['channel'] == 'pipkmks']
    pimkpks_group = group[group['channel'] == 'pimkpks']
    pipkmks_group = pipkmks_group[cols]
    pimkpks_group = pimkpks_group[cols]

    pipkmks_max = 0
    pimkpks_max = 0
    pipkmks_max_var = ''
    pimkpks_max_var = ''

    for col in cols:
        if np.abs(pipkmks_group[col].max()) > np.abs(pipkmks_max):
            pipkmks_max = pipkmks_group[col].max()
            pipkmks_max_var = col
        if np.abs(pimkpks_group[col].max()) > np.abs(pimkpks_max):
            pimkpks_max = pimkpks_group[col].max()
            pimkpks_max_var = col
        var_name_pipkmks = pipkmks_max_var.split('_')[0]
        var_name_pimkpks = pimkpks_max_var.split('_')[0]
    max_df = max_df.append({'e': name[0], 't': name[1], 'channel': 'pipkmks', 'max_var': var_name_pipkmks, 'max_percent_change': pipkmks_max}, ignore_index=True)
    max_df = max_df.append({'e': name[0], 't': name[1], 'channel': 'pimkpks', 'max_var': var_name_pimkpks, 'max_percent_change': pimkpks_max}, ignore_index=True)


# print(max_df.to_string())
max_df.to_csv('/work/halld/home/viducic/systematic_errors/max_changes.csv', index=False)

fig_max, ax_max = plt.subplots(figsize=(10, 10))
grouped = max_df.groupby(['e', 'channel'])
for name, group in grouped:
    if name[1]=='pipkmks':
        color = colors_dict[name[0]][0]
        label = f'$\pi^+K^-K_s$ for E = {name[0]}'
    else:
        color = colors_dict[name[0]][1]
        label = f'$\pi^-K^+K_s$ for E = {name[0]}'
    ax_max.scatter(group['t'], group['max_percent_change'], label=label, color=color)
    ax_max.set_title('Max percent change for each E and t bin')
    ax_max.set_xlabel('t bin')
    ax_max.set_ylabel('max percent change')
    ax_max.legend()
fig_max.savefig('/work/halld/home/viducic/systematic_errors/fit_variation_plots/max_percent_change.png')

    # max_var = 0
    # for var in variations:
        