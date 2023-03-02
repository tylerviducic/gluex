# scale MC to match data so that lidya can test on eta pi pi

import ROOT

data_filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_flat_result_2018_fall.root'
mc_filename = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_flat_result_2018_fall.root'

hist_file_data = ROOT.TFile.Open(data_filename, "READ")
hist_file_mc = ROOT.TFile.Open(mc_filename, "READ")


topology = 'pipkmks'

hist_name = 'f1_kstar_zero_cut'

data_hist = hist_file_data.Get(hist_name)
mc_hist = hist_file_mc.Get(hist_name)
mc_hist.SetLineColor(ROOT.kRed)

scale_factor = 0.0075

mc_hist.Scale(scale_factor)

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
mc_hist.Draw("HIST")
data_hist.Draw("same")
c1.Update()

