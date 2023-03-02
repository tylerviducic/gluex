# copy histograms from one file to another for sean

import ROOT

c1 = ROOT.TCanvas("c1")

source_filename = "/home/tylerviducic/research/gluex/selector_output/f1_analysis.root"
source_file = ROOT.TFile.Open(source_filename, "READ")
target_file = ROOT.TFile("forSean.root", 'RECREATE')

phi_hist_0 = source_file.Get("phi_0_1285_0.200") 
phi_hist_90 = source_file.Get("phi_90_1285_0.200") 

hist_asym = phi_hist_0.GetAsymmetry(phi_hist_90)


# phi_hist_0.Draw()
# phi_hist_90.Draw("same")
hist_asym.Draw()

source_file.GetList().Write()

target_file.Write()