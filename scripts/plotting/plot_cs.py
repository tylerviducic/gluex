# script for plotting the results of the cross section calculation

import pandas
import numpy
import matplotlib.pyplot as plt

channel = 'pipkmks'
filename = f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv'

df = pandas.read_csv(filename)
print(df.to_string())

variables = ['mean', 'width', 'yield', 'cross_section', 'chi2ndf']

for variable in range(variables):
    # Select the data for the current plot
    x = df['t_bin_middle'].values
    y = df[variable].values
    x_err = df['t_bin_width'].values
    y_err = df[variable+'_error'].values

    # Create a new figure and axis for the scatterplot
    fig, ax = plt.subplots()

    # Plot the data with error bars
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o')

    # Set the axis labels
    ax.set_xlabel('X-axis label')
    ax.set_ylabel('Y-axis label')

    # Show or save the plot
    plt.show()  # or plt.savefig('scatterplot_{}.png'.format(i))