# python analysis of thrown MC trees

import ROOT
import pandas
import numpy as np
import uproot
#import matplotlib

filename = "/Users/tylerviducic/research/gluex/selector_output/pimkpks_thrown_fall.root"
# filename = "/volatile/halld/home/viducic/selector_output/f1_pipkmks/thrown/pipkmks_thrown.root"

root_file = uproot.open(filename)
tree = root_file["pimkpks_thrown"]

target_file = ROOT.TFile('pimkpks_t_binned_thrown_0_1_fall.root', 'RECREATE')

histo_list = []

# histo = ROOT.TH1F("histo", "tminus", 225, 0, 2.25)
h_f1_200 = ROOT.TH1F("f1_t_0.2", "f1_t_0.2", 125, 1, 2.25)
h_f1_400 = ROOT.TH1F("f1_t_0.4", "f1_t_0.4", 125, 1, 2.25)
h_f1_600 = ROOT.TH1F("f1_t_0.6", "f1_t_0.6", 125, 1, 2.25)
h_f1_800 = ROOT.TH1F("f1_t_0.8", "f1_t_0.8", 125, 1, 2.25)
h_f1_1000 = ROOT.TH1F("f1_t_1.0", "f1_t_1.0", 125, 1, 2.25)
h_f1_1200 = ROOT.TH1F("f1_t_1.2", "f1_t_1.2", 125, 1, 2.25)
h_f1_1400 = ROOT.TH1F("f1_t_1.4", "f1_t_1.4", 125, 1, 2.25)
h_f1_1600 = ROOT.TH1F("f1_t_1.6", "f1_t_1.6", 125, 1, 2.25)
h_f1_1800 = ROOT.TH1F("f1_t_1.8", "f1_t_1.8", 125, 1, 2.25)
h_f1_2000 = ROOT.TH1F("f1_t_2.0", "f1_t_2.0", 125, 1, 2.25)
# histo = ROOT.TH1F("histo", "npart", 10, 0, 10)
# histo = ROOT.TH1F("histo", "pid", 20, 0, 20)

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
# df = df[df['nParticles'] == 5]
df['f1_px'] = df['PiPlus1_px'] + df['KMinus_px'] + df['Ks_px'] 
df['f1_py'] = df['PiPlus1_py'] + df['KMinus_py'] + df['Ks_py'] 
df['f1_pz'] = df['PiPlus1_pz'] + df['KMinus_pz'] + df['Ks_pz'] 
df['f1_E'] = df['PiPlus1_E'] + df['KMinus_E'] + df['Ks_E']
df['f1_mass2'] = df['f1_E'] * df['f1_E']  - df['f1_px'] * df['f1_px'] - df['f1_py'] * df['f1_py'] - df['f1_pz'] * df['f1_pz']
df['f1_mass'] = np.sqrt(df['f1_mass2'])

df_200 = df[(df['men_t'] > 0) & (df['men_t'] < 0.2)]['f1_mass']
df_400 = df[(df['men_t'] >= 0.2) & (df['men_t'] < 0.4)]['f1_mass']
df_600 = df[(df['men_t'] >= 0.4) & (df['men_t'] < 0.6)]['f1_mass']
df_800 = df[(df['men_t'] >= 0.6) & (df['men_t'] < 0.8)]['f1_mass']
df_1000 = df[(df['men_t'] >= 0.8) & (df['men_t'] < 1.0)]['f1_mass']
df_1200 = df[(df['men_t'] >= 1.0) & (df['men_t'] < 1.2)]['f1_mass']
df_1400 = df[(df['men_t'] >= 1.2) & (df['men_t'] < 1.4)]['f1_mass']
df_1600 = df[(df['men_t'] >= 1.4) & (df['men_t'] < 1.6)]['f1_mass']
df_1800 = df[(df['men_t'] >= 1.6) & (df['men_t'] < 1.8)]['f1_mass']
df_2000 = df[(df['men_t'] >= 1.8) & (df['men_t'] < 2.0)]['f1_mass']

df_200.columns=['f1_mass']
print(df_200)
print("filling")
# histo.FillN(len(df['f1_mass']), df['f1_mass'].to_numpy(), np.ones(len(df['f1_mass'])))
# histo.FillN(len(df['mass_f1']), df['mass_f1'].to_numpy(), np.ones(len(df['mass_f1'])))
# histo.FillN(len(df['men_t']), df['men_t'].to_numpy(), np.ones(len(df['men_t'])))
h_f1_200.FillN(len(df_200), df_200.to_numpy(), np.ones(len(df_200)))
h_f1_400.FillN(len(df_400), df_400.to_numpy(), np.ones(len(df_400)))
h_f1_600.FillN(len(df_600), df_600.to_numpy(), np.ones(len(df_600)))
h_f1_800.FillN(len(df_800), df_800.to_numpy(), np.ones(len(df_800)))
h_f1_1000.FillN(len(df_1000), df_1000.to_numpy(), np.ones(len(df_1000)))
h_f1_1200.FillN(len(df_1200), df_1200.to_numpy(), np.ones(len(df_1200)))
h_f1_1400.FillN(len(df_1400), df_1400.to_numpy(), np.ones(len(df_1400)))
h_f1_1600.FillN(len(df_1600), df_1600.to_numpy(), np.ones(len(df_1600)))
h_f1_1800.FillN(len(df_1800), df_1800.to_numpy(), np.ones(len(df_1800)))
h_f1_2000.FillN(len(df_2000), df_2000.to_numpy(), np.ones(len(df_2000)))
print("drawing")

c2 = ROOT.TCanvas("c2", "testing")
c2.Divide(3, 2)
c2.cd(1)
h_f1_200.Draw()
c2.cd(2)
h_f1_400.Draw()
c2.cd(3)
h_f1_1600.Draw()
c2.cd(4)
h_f1_1800.Draw()
c2.cd(5)
h_f1_2000.Draw()
c2.Update()

h_f1_200.Write()
target_file.Write()

print("done")