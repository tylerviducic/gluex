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
    df = pd.read_csv('/work/halld/home/viducic/systematic_errors/fit_variation_data.csv', index_col=0)
    # print(df.head(30).to_string())

    grouped = df.groupby(['e', 't', 'channel'])

    for name, group in grouped:
        print(name)
        print(group.head().to_string())
        print('++++++++++++++++++++++++++++++++')
      
    
    # grouped = df.groupby('fit_variation')
    # for name, group in grouped:
    #     print(name)
    #     print(group.head(14).to_string())
    #     print('++++++++++++++++++++++++++++++++')




if __name__ == '__main__':
    main()
