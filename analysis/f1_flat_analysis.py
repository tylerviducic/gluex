# flat tree analysis with python

import ROOT
import pandas
import numpy as np
import uproot
#import matplotlib

filename_spring = "/Users/tylerviducic/research/gluex/selector_output/flat_pipkmks_2018_spring.root"
filename_fall = "/Users/tylerviducic/research/gluex/selector_output/flat_pipkmks_2018_fall.root"

root_file_spring = uproot.open(filename_spring)
tree_spring = root_file_spring["pipkmks__B4_M16"]
root_file_fall = uproot.open(filename_fall)
tree_fall = root_file_fall["pipkmks__B4_M16"]

#c1 = ROOT.TCanvas("c1")
histo_spring = ROOT.TH1F("histo1", "h1", 100, 0, 3)
histo_fall = ROOT.TH1F("histo2", "h2", 100, 0, 3)

ROOT.gStyle.SetOptStat(0)

df_spring = tree_spring.arrays(['e_beam', 'accidental_weight', 'minus_t', 'tmin', 'pipkmks_e', 'pipkmks_px', 'pipkmks_py', 'pipkmks_pz', 'pipkmks_phi', 'pipkmks_theta', 'p_e', 'p_px', 'p_py', 'p_pz', 'kstar_m', 'w'], library="pd")
df_fall = tree_fall.arrays(['e_beam', 'accidental_weight', 'minus_t', 'tmin', 'pipkmks_e', 'pipkmks_px', 'pipkmks_py', 'pipkmks_pz', 'pipkmks_phi', 'pipkmks_theta', 'p_e', 'p_px', 'p_py', 'p_pz', 'kstar_m', 'w'], library="pd")
# df["f1_mass2"] = df["pimkpks_e"] * df["pimkpks_e"] - df["pimkpks_px"] * df["pimkpks_px"] - df["pimkpks_py"] * df["pimkpks_py"] - df["pimkpks_pz"] * df["pimkpks_pz"]
# df["f1_mass"] = np.sqrt(df["f1_mass2"])
# df['minusT_tmin'] = df['minus_t'] + df['tmin']
# df['minusT_tmin'] = df['minusT_tmin'].astype()
# f1_1285 = df[ (df["f1_mass"] >  1.2) & (df["f1_mass"] < ) ]
# print(f1_1285)
#df.hist(column='minusT_tmin', bins=100, range=[0, 3])
print("filling")
histo_spring.FillN(len(df_spring['minus_t']), df_spring['minus_t'].to_numpy(), np.ones(len(df_spring['minus_t'])))
histo_spring.SetLineColor(2)
histo_fall.FillN(len(df_fall['minus_t']), df_fall['minus_t'].to_numpy(), np.ones(len(df_fall['minus_t'])))

print("drawing")

# print(histo.GetEntries())
c2 = ROOT.TCanvas("c2", "testing")
c2.cd()
histo_fall.Draw()
histo_spring.Draw("same")
c2.Update()

print("done")