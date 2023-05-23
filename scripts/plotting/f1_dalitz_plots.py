# script to draw Dalitz plots for f1 in data

import ROOT
from common_analysis_tools import *

ROOT.gStyle.SetOptStat(0)


file_and_tree = get_flat_file_and_tree("pipkmks", "spring", "data")
df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

f1_signal_region = "pipkmks_m > 1.24 && pipkmks_m < 1.32"

# df = df.Filter(f1_signal_region).Filter('(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)')

"""
i want a code block that will create dalitz plots from the f1 decay products.
there should be 3 plots, for for each 2 body decay combination
ks + km, ks + pip, km + pip
"""

# define the columns to be used in the dalitz plots
df = df.Define("dalitz_ks_km_px", "ks_px + km_px")
df = df.Define("dalitz_ks_km_py", "ks_py + km_py")
df = df.Define("dalitz_ks_km_pz", "ks_pz + km_pz")
df = df.Define("dalitz_ks_km_E", "ks_E + km_E")
df = df.Define("dalitz_ks_km_m2", "dalitz_ks_km_E * dalitz_ks_km_E - dalitz_ks_km_px * dalitz_ks_km_px - dalitz_ks_km_py * dalitz_ks_km_py - dalitz_ks_km_pz * dalitz_ks_km_pz")

df = df.Define("dalitz_ks_pip1_px", "ks_px + pip1_px")
df = df.Define("dalitz_ks_pip1_py", "ks_py + pip1_py")
df = df.Define("dalitz_ks_pip1_pz", "ks_pz + pip1_pz")
df = df.Define("dalitz_ks_pip1_E", "ks_E + pip1_E")
df = df.Define("dalitz_ks_pip1_m2", "dalitz_ks_pip1_E * dalitz_ks_pip1_E - dalitz_ks_pip1_px * dalitz_ks_pip1_px - dalitz_ks_pip1_py * dalitz_ks_pip1_py - dalitz_ks_pip1_pz * dalitz_ks_pip1_pz")

df = df.Define("dalitz_km_pip1_px", "km_px + pip1_px")
df = df.Define("dalitz_km_pip1_py", "km_py + pip1_py")
df = df.Define("dalitz_km_pip1_pz", "km_pz + pip1_pz")
df = df.Define("dalitz_km_pip1_E", "km_E + pip1_E")
df = df.Define("dalitz_km_pip1_m2", "dalitz_km_pip1_E * dalitz_km_pip1_E - dalitz_km_pip1_px * dalitz_km_pip1_px - dalitz_km_pip1_py * dalitz_km_pip1_py - dalitz_km_pip1_pz * dalitz_km_pip1_pz")

df = df.Filter('pipkmks_m > 1.1 && pipkmks_m < 1.35')

# define the dalitz plot histograms
hist_kspip_kskm = df.Histo2D(("dalitz_ks_km", "Dalitz Plot for KsPi+ vs KsK-", 50, 0.9, 1.5, 50, 0.4, 0.1), "dalitz_ks_km_m2", "dalitz_ks_pip1_m2")
# hist_kspip_kskm.GetXaxis().SetTitle("KsK- Invariant Mass Squared (GeV^{2}/c^{4})")
# hist_kspip_kskm.GetYaxis().SetTitle("KsPi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kmpip_kskm = df.Histo2D(("dalitz_ks_pip1", "Dalitz Plot for K-Pi+ vs KsK-", 50, 0.9, 1.5, 50, 0.4, 0.1), "dalitz_ks_km_m2", "dalitz_km_pip1_m2")
# hist_kmpip_kskm.GetXaxis().SetTitle("KsK- Invariant Mass Squared (GeV^{2}/c^{4})")
# hist_kmpip_kskm.GetYaxis().SetTitle("K-Pi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kmpip_kspip = df.Histo2D(("dalitz_km_pip1", "Dalitz Plot for K-Pi+ vs KsPi+", 50, 0.4, 0.7, 50, 0.4, 0.7), "dalitz_ks_pip1_m2", "dalitz_km_pip1_m2")
hist_kmpip_kspip.GetXaxis().SetTitle("K-Pi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kmpip_kspip.GetYaxis().SetTitle("KsPi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kstar_f1_region = df.Filter('pipkmks_m > 1.1 && pipkmks_m < 1.35').Histo2D(("dalitz_kstar_f1_region", "Dalitz Plot for KsPi+ vs K-Pi+", 50, 0.4, 1.0, 50, 0.4, 1.0), "dalitz_ks_pip1_m2", "dalitz_km_pip1_m2")
hist_kstar_f1_region.GetXaxis().SetTitle("K-Pi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kstar_f1_region.GetYaxis().SetTitle("KsPi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kstar_non_f1_region = df.Filter('pipkmks_m > 1.35 && pipkmks_m < 1.5').Histo2D(("dalitz_kstar_non_f1_region", "Dalitz Plot for KsPi+ vs K-Pi+", 50, 0.4, 1.0, 50, 0.4, 1.0), "dalitz_ks_pip1_m2", "dalitz_km_pip1_m2")
hist_kstar_non_f1_region.GetXaxis().SetTitle("K-Pi+ Invariant Mass Squared (GeV^{2}/c^{4})")
hist_kstar_non_f1_region.GetYaxis().SetTitle("KsPi+ Invariant Mass Squared (GeV^{2}/c^{4})")

# c1 = ROOT.TCanvas("c1", "Dalitz Plot f1")
# c2 = ROOT.TCanvas("c2", "Dalitz Plots non f1")
# c1.cd()
# hist_kstar_f1_region.Draw("colz")
# c2.cd()
# hist_kstar_non_f1_region.Draw("colz")
# c1.Update()
# c2.Update()

c1 = ROOT.TCanvas("c1", "Dalitz Plot a0")
c1.Divide(2, 1)
c1.cd(1)
hist_kspip_kskm.Draw("colz")
c1.cd(2)
hist_kmpip_kskm.Draw("colz")
c1.Update()

# draw the dalitz plots
# c = ROOT.TCanvas("c", "Dalitz Plots")
# c.Divide(3, 1)
# c.cd(1)
# hist_ks_km.Draw("colz")
# c.cd(2)
# hist_ks_pip.Draw("colz")
# c.cd(3)
# hist_km_pip.Draw("colz")
# c.Update()

input("Press Enter to continue...")