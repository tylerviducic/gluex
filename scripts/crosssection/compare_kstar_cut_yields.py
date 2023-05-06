# compare yields for different kstar cuts

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_nocut = pd.read_csv('/Users/tylerviducic/research/gluex/fit_csv/cs_dataframe_8_pipkmks_no_kstar_cut.csv')
df_kstar_plus_cut = pd.read_csv('/Users/tylerviducic/research/gluex/fit_csv/cs_dataframe_9_pipkmks_kstar_plus_cut.csv')
df_kstar_zero_cut = pd.read_csv('/Users/tylerviducic/research/gluex/fit_csv/cs_dataframe_9_pipkmks_kstar_zero_cut.csv')
df_kstar_both_cut = pd.read_csv('/Users/tylerviducic/research/gluex/fit_csv/cs_dataframe_9_pipkmks.csv')

fig = plt.figure()
ax1 = fig.add_subplot(111) 
# ax1.errorbar(df_pipkmks_7['t'], df_pipkmks_7['cs'], yerr=df_pipkmks_7['cs_err'], xerr=df_pimkpks_7['bin_width'], marker='o', color='green', ls='none', label='7 GeV')
# ax1.errorbar(df_nocut['t'], df_nocut['yield'], yerr=df_nocut['yield_percent_error']/100*df_nocut['yield'], xerr=df_nocut['bin_width']/2, marker='o', color='blue', ls='none', label='no cut')
ax1.errorbar(df_kstar_plus_cut['t'], df_kstar_plus_cut['yield'], yerr=df_kstar_plus_cut['yield_percent_error']/100*df_kstar_plus_cut['yield'], xerr=df_kstar_plus_cut['bin_width']/2, marker='o', color='red', ls='none', label='kstar+ cut')
ax1.errorbar(df_kstar_zero_cut['t'], df_kstar_zero_cut['yield'], yerr=df_kstar_zero_cut['yield_percent_error']/100*df_kstar_zero_cut['yield'], xerr=df_kstar_zero_cut['bin_width']/2, marker='o', color='black', ls='none', label='kstar0 cut')
ax1.errorbar(df_kstar_both_cut['t'], df_kstar_both_cut['yield'], yerr=df_kstar_both_cut['yield_percent_error']/100*df_kstar_both_cut['yield'], xerr=df_kstar_both_cut['bin_width']/2, marker='o', color='green', ls='none', label='kstar+ and kstar0 cut')
# ax1.set_yscale('log')
ax1.set_ylabel("yield")
ax1.set_xlabel("-t (GeV)^2")
# ax1.set_title("differential cross-section [pb]/GeV vs -t (GeV^2) \n for pi+ k- and pi- k+ channels")
ax1.legend()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(df_kstar_plus_cut['t'], df_kstar_plus_cut['yield']/df_kstar_both_cut['yield'], color='red')
ax2.scatter(df_kstar_plus_cut['t'], df_kstar_zero_cut['yield']/df_kstar_both_cut['yield'], color='blue')
ax1.set_ylabel("yield ratio")
ax1.set_xlabel("-t (GeV)^2")
ax2.set_ylim(0.1, 0.6)
plt.show()
