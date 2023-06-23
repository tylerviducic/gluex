# script to compare the MXP and PD data

import ROOT
from common_analysis_tools import *

mxp_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_filtered.root'
mxp_ksc_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_ksc_filtered.root'
pd_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_filtered.root'
pd_ksc_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_ksc_filtered.root'

mxp_treename = 'pipkmks_mxp_filtered'
mxp_ksc_treename = 'pipkmks_mxp_ksc_filtered'
pd_treename = 'pipkmks_pd_filtered'
pd_ksc_treename = 'pipkmks_pd_ksc_filtered'

df_mxp = ROOT.RDataFrame(mxp_treename, mxp_filename)
df_mxp_ksc = ROOT.RDataFrame(mxp_ksc_treename, mxp_ksc_filename)
df_pd = ROOT.RDataFrame(pd_treename, pd_filename)
df_pd_ksc = ROOT.RDataFrame(pd_ksc_treename, pd_ksc_filename)

df_mxp = df_mxp.Filter(KSTAR_ALL_CUT)
df_mxp_ksc = df_mxp_ksc.Filter(KSTAR_ALL_CUT)
df_pd = df_pd.Filter(KSTAR_ALL_CUT)
df_pd_ksc = df_pd_ksc.Filter(KSTAR_ALL_CUT)

hist_mxp_pipkmks = df_mxp.Histo1D(('pipkmks_mxp', 'pipkmks_mxp', 30, 1.2, 1.5), 'pipkmks_m')
hist_mxp_ksc_pipkmks = df_mxp_ksc.Histo1D(('pipkmks_mxp_ksc', 'pipkmks_mxp_ksc', 30, 1.2, 1.5), 'pipkmks_m')
hist_pd_pipkmks = df_pd.Histo1D(('pipkmks_pd', 'pipkmks_pd', 30, 1.2, 1.5), 'pipkmks_m')
hist_pd_ksc_pipkmks = df_pd_ksc.Histo1D(('pipkmks_pd_ksc', 'pipkmks_pd_ksc', 30, 1.2, 1.5), 'pipkmks_m')

hist_mxp_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_mxp_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_pd_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_pd_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['orange']))
# hist_pd_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['cyan']))
# hist_pd_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))

c = ROOT.TCanvas('c', 'c', 900, 900)
# hist_mxp_pipkmks.Draw()
# hist_mxp_ksc_pipkmks.Draw()
hist_pd_pipkmks.Draw()
hist_pd_ksc_pipkmks.Draw('same')
c.Update()

input('Press any key to continue...')
