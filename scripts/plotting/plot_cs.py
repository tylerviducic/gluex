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

for name, group in grouped:
    # print(f'name = {name}')
    for variable in variables:
        # Select the data for the current plot

        x = group['t_bin_middle'].values
        y = group[variable].values
        x_err = group['t_bin_width'].values


        if(variable == 'chi2ndf'):
            y_err = numpy.zeros(len(x))
        else:
            y_err = group[variable+'_error'].values

        # Create a new figure and axis for the scatterplot
        fig, ax = plt.subplots()

        # Plot the data with error bars
        ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o')
        if(variable == 'cross_section'):
            theory_df = pd.read_csv(theory_filename.format(name), delim_whitespace=True)
            theory_df.columns = ['t', 'diff_cs']
            theory_df = theory_df.loc[(theory_df['t'] > 0.1) & (theory_df['t'] < 1.9)]
            theory_df['diff_cs'] = theory_df['diff_cs']
            ax.plot(theory_df['t'], theory_df['diff_cs'], 'r-')

        # Set the axis labels
        ax.set_xlabel(latex_axis_label_dict['t'])
        ax.set_ylabel(latex_axis_label_dict[variable])

        # Show or save the plot
        # plt.show()  # or 
        plt.savefig(f'/work/halld/home/viducic/plots/cross_section/{channel}_plot_of_{variable}_beam-{name}.png')