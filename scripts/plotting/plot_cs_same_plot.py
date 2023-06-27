# script for plotting the results of the cross section calculation

import pandas
import numpy
import matplotlib.pyplot as plt
from common_analysis_tools import *
import pandas as pd

channel = 'pipkmks'
filename = f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv'
theory_filename = '/work/halld/home/viducic/theory_predictions/t-slope-{}GeVnew.dat'

df = pandas.read_csv(filename)
# print(df.to_string())

variables = ['mean', 'width', 'yield', 'cross_section', 'chi2ndf']


grouped = df.groupby('beam_energy')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

#create two figures, one with 4 sub plots and the other without subplots
fig2, ax5 = plt.subplots()



color_dict = {
    7: 'red',
    8: 'blue',
    9: 'green',
    10: 'purple'
}

for name, group in grouped:
    # if name == 7:
    #     continue
    # print(f'name = {name}')
    x = group['t_bin_middle'].values
    cs = group['cross_section'].values
    cs_err = group['cross_section_error'].values
    ax1.errorbar(x, cs, yerr=cs_err, fmt='o', color=color_dict[name], label=f'{name} GeV')
    theory_df = pd.read_csv(theory_filename.format(name), delim_whitespace=True)
    theory_df.columns = ['t', 'diff_cs']
    theory_df = theory_df.loc[(theory_df['t'] > 0.1) & (theory_df['t'] < 1.9)]
    theory_df['diff_cs'] = theory_df['diff_cs']
    ax1.plot(theory_df['t'], theory_df['diff_cs'], color=color_dict[name])
    ax1.legend()
    ax1.set_xlabel('t (GeV^2)')
    ax1.set_ylabel('d^2\sigma/dtdM (nb/GeV^4)')
    ax1.set_title('Cross section')
    #draw this on ax5 as well
    ax5.errorbar(x, cs, yerr=cs_err, fmt='o', color=color_dict[name], label=f'{name} GeV')
    # ax5.plot(theory_df['t'], theory_df['diff_cs'], color=color_dict[name])
    ax5.legend()
    ax5.set_xlabel('t (GeV^2)')
    ax5.set_ylabel('d^2\sigma/dtdM (nb/GeV^4)')
    ax5.set_title('Cross section')


    mean = group['mean'].values
    mean_err = group['mean_error'].values
    ax2.errorbar(x, mean, yerr=mean_err, fmt='o', color=color_dict[name], label=f'{name} GeV')
    ax2.set_xlabel('t (GeV^2)')
    ax2.set_ylabel('Mean (GeV)')
    ax2.set_title('Mean')
    # ax2.legend()

    # width = group['width'].values
    # width_err = group['width_error'].values
    # ax3.errorbar(x, width, yerr=width_err, fmt='o', color=color_dict[name], label=f'{name} GeV')

    ac_yield = group['yield'].values
    ac_yield_err = group['yield_error'].values
    ax3.errorbar(x, ac_yield, yerr=ac_yield_err, fmt='o', color=color_dict[name], label=f'{name} GeV')
    ax3.set_xlabel('t (GeV^2)')
    ax2.set_ylabel('Yield')
    ax3.set_title('Yield')

    chi2ndf = group['chi2ndf'].values
    ax4.plot(x, chi2ndf, 'o', color=color_dict[name], label=f'{name} GeV')
    ax4.set_xlabel('t (GeV^2)')
    ax4.set_ylabel('\chi^2/ndf')
    ax4.set_title('\chi^2/ndf')

        # Show or save the plot
        # plt.show()  # or 
fig.savefig(f'/work/halld/home/viducic/plots/cross_section/{channel}_same_plots.png')
#save ax5 as it's own image 
# plt.figure(2)
ax5.figure.savefig(f'/work/halld/home/viducic/plots/cross_section/{channel}_cs_same_plot.png')
