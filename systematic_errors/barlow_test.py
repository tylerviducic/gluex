import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# TODO: what os the best way to visualize the results?
# TODO: what is the threshold for the systematic error?
# TODO: how do we handle loose/tight cuts?


def barlow_test(nominal, variation, sigma_nominal, sigma_variation):
    """
    Barlow test for systematic errors
    """
    delta = nominal - variation
    sigma = np.sqrt(sigma_nominal*sigma_nominal + sigma_variation*sigma_variation)
    return delta/sigma


def main():
    df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
    df['barlow_loose'] = np.where(True, barlow_test(df['cross_section_loose'], df['cross_section_nominal'], df['cross_section_error_loose'], df['cross_section_error_nominal']), np.nan)
    df['barlow_tight'] = np.where(True, barlow_test(df['cross_section_tight'], df['cross_section_nominal'], df['cross_section_error_tight'], df['cross_section_error_nominal']), np.nan)


    #make seaborn relplot
    sns.relplot(data=df, x='t', y='barlow_loose', hue='e', style='cut', kind='scatter', row='channel')
    plt.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_loose.png')
    sns.relplot(data=df, x='t', y='barlow_tight', hue='e', style='cut', kind='scatter', row='channel')
    plt.savefig('/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_tight.png')
    # input('Press enter to continue')
    
    fig, ax = plt.subplots()
    
    grouped = df.groupby(['channel', 'cut', 'e'])
    for name, group in grouped:
        # print(name)
        ax.scatter(group['t'], group['barlow_loose'], label='loose', color='blue')
        ax.scatter(group['t'], group['barlow_tight'], label='tight', color='red')
        ax.set_title(f'Barlow test for channel: {name[0]}, cut: {name[1]}, e: {name[2]}')
        ax.set_xlabel('t bin')
        ax.set_ylabel('$\sigma_barlow$')
        ax.legend()
        fig.savefig(f'/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_{name[0]}_{name[1]}_{name[2]}.png')
        ax.clear()

        # for index, row in df.iterrows():
        #     print(f"cut: {row['cut']}, E: {row['e']}, t: {row['t']} :: loose: {row['f1_yield_loose']} +/- {row['f1_yield_error_loose']}, nominal: {row['f1_yield_nominal']} +/- {row['f1_yield_error_nominal']}, tight: {row['f1_yield_tight']} +/- {row['f1_yield_error_tight']}")





if __name__ == '__main__':
    main()
