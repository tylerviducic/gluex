# script for testing the thrown energy vs recon energy for different beam ranges

import ROOT
from common_analysis_tools import *


channel = 'pipkmks'
run_period = '2017'
recon_file_and_tree = get_flat_phasespace_file_and_tree(channel, run_period)
thrown_filename = '/volatile/halld/home/viducic/selector_output/f1_pipkmks/thrown/pipkmks_thrown_2017.root'
thrown_treename = 'pipkmks_thrown'

recon_df = ROOT.RDataFrame(recon_file_and_tree[1], recon_file_and_tree[0])
thrown_df = ROOT.RDataFrame(thrown_treename, thrown_filename)

thrown_df = thrown_df.Define("P_p", "sqrt(Proton_px*Proton_px + Proton_py*Proton_py + Proton_pz*Proton_pz)")

hist_beam_thrown = thrown_df.Histo1D(('hist_beam_thrown', 'hist_beam_thrown', 200, 5, 11.5), 'Beam_E').GetValue()
hist_beam_recon = recon_df.Histo1D(('hist_beam_recon', 'hist_beam_recon', 200, 5, 11.5), 'e_beam')

acceptance = hist_beam_recon.Clone('acceptance')
acceptance.Divide(hist_beam_thrown)

hist_beam_thrown.Scale(1/hist_beam_thrown.Integral())
hist_beam_recon.Scale(1/hist_beam_recon.Integral())

hist_beam_recon.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_beam_thrown.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))

hist_pp_thrown_vs_beam = thrown_df.Histo2D(('hist_pp_thrown_vs_beam', 'hist_pp_thrown_vs_beam', 100, 5, 11.5, 50, 0, 1.0), 'Beam_E', 'P_p')



c = ROOT.TCanvas('c', 'c', 1200, 900)
hist_beam_thrown.Draw("hist")
hist_beam_recon.Draw('same hist')
c.Update()

c1 = ROOT.TCanvas('c1', 'c1', 1200, 900)
c1.Divide(2, 1)
c1.cd(1)
acceptance.Draw('hist')
c1.cd(2)
hist_pp_thrown_vs_beam.Draw('colz')
c1.SetLogz()
c1.Update()



input('Press enter to exit')
