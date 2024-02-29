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


def main():

    colors_dict = {
        8: ('lightblue', 'lightcoral'),
        9: ('blue', 'red'),
        10: ('slateblue', 'firebrick'),
        11: ('darkblue', 'darkred')
    }

    df = pd.read_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv', index_col=0)
    # print(df.columns)

    # grouped = df.groupby(['e', 't', 'channel'])

    # for name, group in grouped:
    #     print(name)
    #     print(group.head().to_string())
    #     print('++++++++++++++++++++++++++++++++')
      
    
    # grouped = df.groupby('fit_variation')
    # for name, group in grouped:
    #     print(name)
    #     print(group.head(14).to_string())
    #     print('++++++++++++++++++++++++++++++++')
    variations = ['nominal', 'pol1', 'pol3', 'nogaus', 'exppol2', 'chebyshev', 'wideleft',
                  'wideright', 'wideboth', 'narrowleft', 'narrowright', 'narrowboth',
                  'floatvoigtmean', 'floatvoigtwidth', 'floatgausmean', 'floatgauswidth']
    
    for var in variations:
        df[f'barlow_{var}'] = np.where(True, barlow_test(df['nominal_cross_section'], df[f'{var}_cross_section'], df['nominal_cross_section_error'], df[f'{var}_cross_section_error']), np.nan)
    
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
            ax[row_index, col_index].scatter(group_pipkmks['t'], group_pipkmks[f'barlow_{var}'], label='$\pi^+K^-K_s$', color=colors_dict[name][0])
            ax[row_index, col_index].scatter(group_pimkpks['t'], group_pimkpks[f'barlow_{var}'], label='$\pi^-K^+K_s$', color=colors_dict[name][1])
            ax[row_index, col_index].axhline(4.0, linestyle='--')
            ax[row_index, col_index].axhline(-4.0, linestyle='--')
            ax[row_index, col_index].set_title(f'Barlow test for {var} at E={name}')
            ax[row_index, col_index].set_xlabel('t bin')
            ax[row_index, col_index].set_xlim(0, 8)
            ax[row_index, col_index].set_ylim(-17, 17)
            ax[row_index, col_index].set_ylabel('$\sigma_{barlow}$')
            ax[row_index, col_index].legend()
        fig.tight_layout()
        fig.savefig(f'/work/halld/home/viducic/systematic_errors/barlow_plots/barlow_test_fit_procedure_{name}.png')










if __name__ == '__main__':
    main()
