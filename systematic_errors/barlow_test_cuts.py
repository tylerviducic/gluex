import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# TODO: make title and legend more descriptive
def barlow_test(nominal, variation, sigma_nominal, sigma_variation):
    """
    Barlow test for systematic errors
    """
    delta = nominal - variation
    sigma = np.sqrt(abs(sigma_nominal*sigma_nominal - sigma_variation*sigma_variation))
    return delta/sigma


colors_dict = {
    'pipkmks_loose': 'lightblue',
    'pimkpks_loose': 'salmon',
    'pipkmks_tight': 'darkblue',
    'pimkpks_tight': 'darkred',
}


def main():
    df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
    df['barlow_loose'] = np.where(True, barlow_test(df['cross_section_loose'], df['cross_section_nominal'], df['cross_section_error_loose'], df['cross_section_error_nominal']), np.nan)
    df['barlow_tight'] = np.where(True, barlow_test(df['cross_section_tight'], df['cross_section_nominal'], df['cross_section_error_tight'], df['cross_section_error_nominal']), np.nan)

    df['sigma_barlow'] = np.where(abs(df['cross_section_loose']-df['cross_section_nominal'])/df['cross_section_nominal'] > abs(df['cross_section_tight']-df['cross_section_nominal'])/df['cross_section_nominal'], barlow_test(df['cross_section_loose'], df['cross_section_nominal'], df['cross_section_error_loose'], df['cross_section_error_nominal']), barlow_test(df['cross_section_tight'], df['cross_section_nominal'], df['cross_section_error_tight'], df['cross_section_error_nominal']))
    barlow_results = df[['cut', 'e', 't', 'channel', 'barlow_loose', 'barlow_tight', 'sigma_barlow']]
    barlow_results.to_csv('/work/halld/home/viducic/systematic_errors/barlow_results.csv')
    sig_cuts = df.loc[(abs(df['barlow_loose']) > 4.0) | (abs(df['barlow_tight']) > 4.0)]
    sig_cuts.to_csv('/work/halld/home/viducic/systematic_errors/signifigant_cut_systematics.csv')

    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize =(12,10))

    
    grouped = df.groupby('cut')
    for name, group in grouped:
        # print(name)
        pipkmks_group = group.loc[group['channel'] == 'pipkmks']
        pipkmks_group_8 = pipkmks_group.loc[pipkmks_group['e'] == 8]
        pipkmks_group_9 = pipkmks_group.loc[pipkmks_group['e'] == 9]
        pipkmks_group_10 = pipkmks_group.loc[pipkmks_group['e'] == 10]
        pipkmks_group_11 = pipkmks_group.loc[pipkmks_group['e'] == 11]

        pimkpks_group = group.loc[group['channel'] == 'pimkpks']
        pimkpks_group_8 = pimkpks_group.loc[pimkpks_group['e'] == 8]
        pimkpks_group_9 = pimkpks_group.loc[pimkpks_group['e'] == 9]
        pimkpks_group_10 = pimkpks_group.loc[pimkpks_group['e'] == 10]
        pimkpks_group_11 = pimkpks_group.loc[pimkpks_group['e'] == 11]
        
        ax1.scatter(pipkmks_group_8['t'], pipkmks_group_8['barlow_loose'], label='$\pi^+K^-K_s$ loose', color=colors_dict['pipkmks_loose'])
        ax1.scatter(pimkpks_group_8['t'], pimkpks_group_8['barlow_loose'], label='$\pi^-K^+K_s$ loose', color=colors_dict['pimkpks_loose'])
        ax1.scatter(pipkmks_group_8['t'], pipkmks_group_8['barlow_tight'], label='$\pi^+K^-K_s$tight', color=colors_dict['pipkmks_tight'])
        ax1.scatter(pimkpks_group_8['t'], pimkpks_group_8['barlow_tight'], label='$\pi^-K^+K_s$ tight', color=colors_dict['pimkpks_tight'])
        ax1.axhline(4.0, linestyle='--')
        ax1.axhline(-4.0, linestyle='--')
        ax1.set_title(f'Barlow test for cut {name} at E=8')
        ax1.set_xlabel('t bin')
        ax1.set_xlim(0, 8)
        ax1.set_ylim(-17, 17)
        ax1.set_ylabel('$\sigma_{barlow}$')
        ax1.legend()
        
        ax2.scatter(pipkmks_group_9['t'], pipkmks_group_9['barlow_loose'], color=colors_dict['pipkmks_loose'])
        ax2.scatter(pimkpks_group_9['t'], pimkpks_group_9['barlow_loose'], color=colors_dict['pimkpks_loose'])
        ax2.scatter(pipkmks_group_9['t'], pipkmks_group_9['barlow_tight'], color=colors_dict['pipkmks_tight'])
        ax2.scatter(pimkpks_group_9['t'], pimkpks_group_9['barlow_tight'], color=colors_dict['pimkpks_tight'])
        ax2.axhline(4.0, linestyle='--')
        ax2.axhline(-4.0, linestyle='--')
        ax2.set_title(f'Barlow test for cut {name} at E=9')
        ax2.set_xlabel('t bin')
        ax2.set_xlim(0, 8)
        ax2.set_ylim(-17, 17)
        ax2.set_ylabel('$\sigma_{barlow}$')

        ax3.scatter(pipkmks_group_10['t'], pipkmks_group_10['barlow_loose'], color=colors_dict['pipkmks_loose'])
        ax3.scatter(pimkpks_group_10['t'], pimkpks_group_10['barlow_loose'], color=colors_dict['pimkpks_loose'])
        ax3.scatter(pipkmks_group_10['t'], pipkmks_group_10['barlow_tight'], color=colors_dict['pipkmks_tight'])
        ax3.scatter(pimkpks_group_10['t'], pimkpks_group_10['barlow_tight'], color=colors_dict['pimkpks_tight'])
        ax3.axhline(4.0, linestyle='--')
        ax3.axhline(-4.0, linestyle='--')
        ax3.set_title(f'Barlow test for cut {name} at E=10')
        ax3.set_xlabel('t bin')
        ax3.set_xlim(0, 8)
        ax3.set_ylim(-17, 17)
        ax3.set_ylabel('$\sigma_{barlow}$')

        ax4.scatter(pipkmks_group_11['t'], pipkmks_group_11['barlow_loose'], color=colors_dict['pipkmks_loose'])
        ax4.scatter(pimkpks_group_11['t'], pimkpks_group_11['barlow_loose'], color=colors_dict['pimkpks_loose'])
        ax4.scatter(pipkmks_group_11['t'], pipkmks_group_11['barlow_tight'], color=colors_dict['pipkmks_tight'])
        ax4.scatter(pimkpks_group_11['t'], pimkpks_group_11['barlow_tight'], color=colors_dict['pimkpks_tight'])
        ax4.axhline(4.0, linestyle='--')
        ax4.axhline(-4.0, linestyle='--')
        ax4.set_title(f'Barlow test for cut {name} at E=11')
        ax4.set_xlabel('t bin')
        ax4.set_xlim(0, 8)
        ax4.set_ylim(-17, 17)
        ax4.set_ylabel('$\sigma_{barlow}$')


        fig.savefig(f'/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_cut_{name}.png')
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        # for index, row in df.iterrows():
        #     print(f"cut: {row['cut']}, E: {row['e']}, t: {row['t']} :: loose: {row['f1_yield_loose']} +/- {row['f1_yield_error_loose']}, nominal: {row['f1_yield_nominal']} +/- {row['f1_yield_error_nominal']}, tight: {row['f1_yield_tight']} +/- {row['f1_yield_error_tight']}")

    




if __name__ == '__main__':
    main()
