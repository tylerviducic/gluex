# script for plotting the results of the cross section calculation

import pandas
import numpy
import matplotlib.pyplot as plt
from common_analysis_tools import *

channel = 'pipkmks'
filename = f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv'

df = pandas.read_csv(filename)
print(df.to_string())

variables = ['mean', 'width', 'yield', 'cross_section', 'chi2ndf']

beam_enery = 10
df = df.loc[df['beam_energy']==beam_enery]

for variable in variables:
    # Select the data for the current plot

    x = df['t_bin_middle'].values
    y = df[variable].values
    x_err = df['t_bin_width'].values


    if(variable == 'chi2ndf'):
        y_err = numpy.zeros(len(x))
    else:
        y_err = df[variable+'_error'].values

    # Create a new figure and axis for the scatterplot
    fig, ax = plt.subplots()

    # Plot the data with error bars
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o')

    # Set the axis labels
    ax.set_xlabel(latex_axis_label_dict['t'])
    ax.set_ylabel(latex_axis_label_dict[variable])

    # Show or save the plot
    # plt.show()  # or 
    plt.savefig(f'/work/halld/home/viducic/plots/cross_section/{channel}_plot_of_{variable}_beam-{beam_enery}.png')