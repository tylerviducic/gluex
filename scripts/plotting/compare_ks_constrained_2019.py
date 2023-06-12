# script to compare the results of the Ks constraint with 2019 data

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'


file_and_tree_unconstrained = get_flat_file_and_tree(channel, '2019_unconstrained', 'data')
df_unconstrained = ROOT.RDataFrame(file_and_tree_unconstrained[1], file_and_tree_unconstrained[0])

file_and_tree_constrained = get_flat_file_and_tree(channel, '2019_constrained', 'data')
df_constrained = ROOT.RDataFrame(file_and_tree_constrained[1], file_and_tree_constrained[0])

df_unconstrained = df_unconstrained.Filter(BEAM_RANGE).Filter(T_RANGE).Filter(KSTAR_ALL_CUT)
df_constrained = df_constrained.Filter(BEAM_RANGE).Filter(T_RANGE).Filter(KSTAR_ALL_CUT)

hist_constrained = df_constrained.Histo1D(('kkpi_ks_constrained', 'kkpi_ks_constrained', 30, 1.2, 1.5), 'pipkmks_m')
hist_unconstrained = df_unconstrained.Histo1D(('kkpi_ks_unconstrained', 'kkpi_ks_unconstrained', 30, 1.2, 1.5), 'pipkmks_m')

hist_constrained.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_unconstrained.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))

c = ROOT.TCanvas('c', 'c', 800, 600)
hist_constrained.Draw()
hist_unconstrained.Draw('same')
c.Update()

constrained_integral = hist_constrained.Integral(hist_constrained.FindBin(1.2), hist_constrained.FindBin(1.3))
unconstrained_integral = hist_unconstrained.Integral(hist_unconstrained.FindBin(1.2), hist_unconstrained.FindBin(1.3))
print('constrained integral: {}'.format(constrained_integral))
print('unconstrained integral: {}'.format(unconstrained_integral))

input('Press any key to continue...')
