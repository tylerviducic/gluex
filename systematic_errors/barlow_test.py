import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def barlow_test(nominal, variation, sigma_nominal, sigma_variation):
    """
    Barlow test for systematic errors
    """
    delta = nominal - variation
    sigma = np.sqrt(abs(sigma_nominal*sigma_nominal - sigma_variation*sigma_variation))
    return delta/sigma

# TODO: for each cut and E-bin, plot barlow as a function of t. 4 panels/figure, 1 for each t-bin.
# TODO: loose and tight should be dark/light shades of the color for the channel. or could use different markers, i guess
def main():
    df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
    df['barlow_loose'] = np.where(True, barlow_test(df['cross_section_loose'], df['cross_section_nominal'], df['cross_section_error_loose'], df['cross_section_error_nominal']), np.nan)
    df['barlow_tight'] = np.where(True, barlow_test(df['cross_section_tight'], df['cross_section_nominal'], df['cross_section_error_tight'], df['cross_section_error_nominal']), np.nan)

    sig_cuts = df.loc[(abs(df['barlow_loose']) > 4.0) | (abs(df['barlow_tight']) > 4.0)]
    sig_cuts.to_csv('/work/halld/home/viducic/systematic_errors/signifigant_cut_systematics.csv')

    #make seaborn relplot
    sns.relplot(data=df, x='t', y='barlow_loose', hue='e', style='cut', kind='scatter', row='channel')
    plt.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_loose.png')
    sns.relplot(data=df, x='t', y='barlow_tight', hue='e', style='cut', kind='scatter', row='channel')
    plt.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_tight.png')
    # # input('Press enter to continue')
    
    fig, ax = plt.subplots()
    
    grouped = df.groupby(['channel', 'cut', 'e'])
    for name, group in grouped:
        # print(name)
        ax.scatter(group['t'], group['barlow_loose'], label='loose', color='blue')
        ax.scatter(group['t'], group['barlow_tight'], label='tight', color='red')
        ax.set_title(f'Barlow test for channel: {name[0]}, cut: {name[1]}, e: {name[2]}')
        ax.set_xlabel('t bin')
        ax.set_xlim(0, 9)
        ax.set_ylim(-5, 5)
        ax.set_ylabel('$\sigma_barlow$')
        ax.legend()
        fig.savefig(f'/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_{name[0]}_{name[1]}_{name[2]}.png')
        ax.clear()

        # for index, row in df.iterrows():
        #     print(f"cut: {row['cut']}, E: {row['e']}, t: {row['t']} :: loose: {row['f1_yield_loose']} +/- {row['f1_yield_error_loose']}, nominal: {row['f1_yield_nominal']} +/- {row['f1_yield_error_nominal']}, tight: {row['f1_yield_tight']} +/- {row['f1_yield_error_tight']}")





if __name__ == '__main__':
    main()
