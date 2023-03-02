# script to draw the cs from the pi+ k- and pi- k+ channels

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_pipkmks_7 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_7_pipkmks.csv')
df_pipkmks_8 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_8_pipkmks.csv')
df_pipkmks_9 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_9_pipkmks.csv')
df_pipkmks_10 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_10_pipkmks.csv')
df_pimkpks_7 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_7_pimkpks.csv')
df_pimkpks_8 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_8_pimkpks.csv')
df_pimkpks_9 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_9_pimkpks.csv')
df_pimkpks_10 = pd.read_csv('/Users/tylerviducic/research/gluex/cs_dataframe_10_pimkpks.csv')

df_pimkpks_7['cs_err'] = df_pimkpks_7['cs'] * df_pimkpks_7['yield_percent_error']/100
df_pimkpks_8['cs_err'] = df_pimkpks_8['cs'] * df_pimkpks_8['yield_percent_error']/100
df_pimkpks_9['cs_err'] = df_pimkpks_9['cs'] * df_pimkpks_9['yield_percent_error']/100
df_pimkpks_10['cs_err'] = df_pimkpks_10['cs'] * df_pimkpks_10['yield_percent_error']/100
df_pipkmks_7['cs_err'] = df_pipkmks_7['cs'] * df_pipkmks_7['yield_percent_error']/100
df_pipkmks_8['cs_err'] = df_pipkmks_8['cs'] * df_pipkmks_8['yield_percent_error']/100
df_pipkmks_9['cs_err'] = df_pipkmks_9['cs'] * df_pipkmks_9['yield_percent_error']/100
df_pipkmks_10['cs_err'] = df_pipkmks_10['cs'] * df_pipkmks_10['yield_percent_error']/100

# plot the cs for the pi+ k- and pi- k+ channels
fig = plt.figure()
ax1 = fig.add_subplot(111) 
# ax1.errorbar(df_pipkmks_7['t'], df_pipkmks_7['cs'], yerr=df_pipkmks_7['cs_err'], xerr=df_pimkpks_7['bin_width'], marker='o', color='green', ls='none', label='7 GeV')
ax1.errorbar(df_pipkmks_8['t'], df_pipkmks_8['cs'], yerr=df_pipkmks_8['cs_err'], xerr=df_pimkpks_8['bin_width']/2, marker='x', color='red', ls='none', label='8 GeV Pi- K+')
ax1.errorbar(df_pipkmks_9['t'], df_pipkmks_9['cs'], yerr=df_pipkmks_9['cs_err'], xerr=df_pimkpks_9['bin_width']/2, marker='o', color='red', ls='none', label='9 GeV Pi- K+')
# ax1.errorbar(df_pipkmks_10['t'], df_pipkmks_10['cs'], yerr=df_pipkmks_10['cs_err'], xerr=df_pimkpks_10['bin_width'], marker='o', color='black', ls='none', label='10 GeV')
# ax1.errorbar(df_pimkpks_7['t'], df_pimkpks_7['cs'], yerr=df_pimkpks_7['cs_err'], xerr=df_pimkpks_7['bin_width'], marker='x', color='green', ls='none', label='7 GeV')
ax1.errorbar(df_pimkpks_8['t'], df_pimkpks_8['cs'], yerr=df_pimkpks_8['cs_err'], xerr=df_pimkpks_8['bin_width']/2, marker='x', color='blue', ls='none', label='8 GeV Pi+ K-')
ax1.errorbar(df_pimkpks_9['t'], df_pimkpks_9['cs'], yerr=df_pimkpks_9['cs_err'], xerr=df_pimkpks_9['bin_width']/2, marker='o', color='blue', ls='none', label='9 GeV Pi+ K-')
# ax1.errorbar(df_pimkpks_10['t'], df_pimkpks_10['cs'], yerr=df_pimkpks_10['cs_err'], xerr=df_pimkpks_10['bin_width'], marker='x', color='black', ls='none', label='10 GeV')
ax1.set_yscale('log')
ax1.set_ylabel("differential cross section [pb/GeV]")
ax1.set_xlabel("-t (GeV)^2")
ax1.set_title("differential cross-section [pb]/GeV vs -t (GeV^2) \n for pi+ k- and pi- k+ channels")
ax1.legend()



plt.show()