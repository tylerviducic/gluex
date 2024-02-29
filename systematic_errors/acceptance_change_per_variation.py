"""script to check how much impact each cut has on the efficiency"""
# TODO: check the change of the efficiency for each cut

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/work/halld/home/viducic/systematic_errors/cs_systematics_results.csv')
# print(df.columns)
df['acceptance_change_loose'] = np.where(True, (df['f1_acceptance_nominal'] - df['f1_acceptance_loose'])/df['f1_acceptance_nominal'], np.nan)
df['acceptance_change_tight'] = np.where(True, (df['f1_acceptance_nominal'] - df['f1_acceptance_tight'])/df['f1_acceptance_nominal'], np.nan)

acceptance_change = df[['cut', 'e', 't', 'channel', 'acceptance_change_loose', 'acceptance_change_tight']]


grouped = df.groupby('cut')
print(grouped.ngroups)

fig, axs = plt.subplots(4, 3)
cuts = list(grouped.groups.keys())

for i, cut in enumerate(cuts):
    # TODO: plot eff variation for each cut vs nominal


