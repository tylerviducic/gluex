import ROOT
import pandas
import numpy as np
import uproot
#import matplotlib

filename = "/Users/tylerviducic/research/gluex/acceptance_study/acceptance_study_pipkmks_thrown_flat.root"

root_file = uproot.open(filename)
tree = root_file["pipkmks_thrown"]

target_file = ROOT.TFile("pipkmks_thrown_histos.root", "RECREATE")

df = tree.arrays([  
                    'men_t',
                    'mass_f1',
                    'nThrown',
                    'nParticles',
                    'Beam_E', 
                    'PiPlus1_px', 
                    'PiPlus1_py',
                    'PiPlus1_pz',
                    'PiPlus1_E',
                    'PiPlus2_px', 
                    'PiPlus2_py',
                    'PiPlus2_pz',
                    'PiPlus2_E',
                    'PiMinus_px', 
                    'PiMinus_py',
                    'PiMinus_pz',
                    'PiMinus_E',
                    'KMinus_px', 
                    'KMinus_py',
                    'KMinus_pz',
                    'KMinus_E',
                    'Proton_px', 
                    'Proton_py',
                    'Proton_pz',
                    'Proton_E',
                    'Ks_px', 
                    'Ks_py',
                    'Ks_pz',
                    'Ks_E',
                    ], library="pd")

df["ks_m2"] = df['Ks_E']**2 - df['Ks_px']**2 - df['Ks_py']**2 - df['Ks_pz']**2
df["ks_m"] = np.sqrt(df["ks_m2"])

hist_ks = ROOT.TH1F("hist_ks", "hist_ks", 100, 0.0, 1.0)

ks_mass = df["ks_m"]
print(ks_mass)

hist_ks.FillN(len(ks_mass), ks_mass.to_numpy(), np.ones(len(ks_mass)))

target_file.Write()

print("done")
