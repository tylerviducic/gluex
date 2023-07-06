# script to compare cross-section results of pimkpks and pipkmks

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from common_analysis_tools import *

channels = ['pipkmks', 'pimkpks']
theory_filename = '/work/halld/home/viducic/theory_predictions/t-slope-{}GeVnew.dat'

color_dict = {
    7: 'purple',
    8: 'blue',
    9: 'green',
    10: 'red'
}

fig, ax = plt.subplots()


for channel in channels:
    filename = f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv'
    df = pd.read_csv(filename)
    grouped = df.groupby('beam_energy')


    for name, group in grouped:
        if name == 7:
            continue

        if channel == 'pipkmks':
            cs_fc = color_dict[name]
        else:
            cs_fc = 'none'

        x = group['t_bin_middle'].values
        cs = group['cross_section'].values
        cs_err = group['cross_section_error'].values
        ax.errorbar(x, cs, yerr=cs_err, fmt='o', label=f'{latex_axis_label_dict[channel]} {name} GeV', mfc = cs_fc, mec = color_dict[name], color=color_dict[name])
        ax.legend()

ax.set_xlabel(latex_axis_label_dict['t'], fontsize=13)
ax.set_ylabel(latex_axis_label_dict['cross_section'], fontsize=13)
ax.tick_params(axis='y', labelsize=7)
cs_title = '$\\frac{d\sigma}{dt}$'
ax.set_title(f'{cs_title} for {latex_axis_label_dict[channels[0]]} and {latex_axis_label_dict[channels[1]]}', fontsize=18)

ax.yaxis.set_label_coords(-.08, .9)
ax.xaxis.set_label_coords(.92, -0.07)

fig.savefig(f'/work/halld/home/viducic/plots/cross_section/kkpi_cs_same_plots.png')
