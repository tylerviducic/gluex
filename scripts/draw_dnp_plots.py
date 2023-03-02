#draw plots for DNP

import ROOT

ROOT.gStyle.SetOptStat(0)

# filename = '/Users/tylerviducic/research/gluex/selector_output/dnp_plots_4.root'
filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_spring.root'

root_file = ROOT.TFile(filename, "READ")

# ks_before = ROOT.TFile("ks_before.root", 'READ')
# ks_after = ROOT.TFile("ks_after.root", 'READ')

c1 = ROOT.TCanvas("c1")

# hist = root_file.Get("Ks_vs_FlightSig")
# hist = root_file.Get("IM_KmP")
# hist = root_file.Get("IM_KmP")
# hist = root_file.Get("IM_PipPim")
# hist = root_file.Get("IM_KsKmPip_1285")
hist = root_file.Get("IM_KsKmPip")
# hist = root_file.Get("IM_KsKmPip_1420")
# hist = root_file.Get("IM_KsPip")
# hist = root_file.Get("IM_KmPip")
# hist.SetAxisRange(0.3, 0.68)

# hist1 = ks_before.Get("IM_PipPim")
# hist1.SetMinimum(0)
# hist1.SetLineColor(2)
# hist2 = ks_after.Get("IM_PipPim")
# hist2.SetMinimum(0)

hist.Draw()

# hist1.Draw("hist")
# hist2.Draw("same, hist")
c1.Update()


# target_file = ROOT.TFile("ks_before.root", 'RECREATE')
# target_file = ROOT.TFile("ks_after.root", 'RECREATE')

# hist.Write()
