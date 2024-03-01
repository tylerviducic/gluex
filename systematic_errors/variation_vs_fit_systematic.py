"""script to check if the variations are larger than the error on the fits"""
# TODO: compare the percent change of the variation vs the percent error ont he fit 

import pandas as pd
import numpy as np

max_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/max_changes.csv')
cut_var_df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')

signifigant_cuts = pd.DataFrame(columns = ['e', 't', 'channel', 'cut', 'loose_tight' 'percent_change', 'percent_error'])

print(cut_var_df.head().to_string())

# TODO: select only the variations > the systematic on the fit