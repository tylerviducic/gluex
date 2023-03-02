# python analysis of thrown MC trees

import ROOT
import pandas
import numpy as np
import uproot
#import matplotlib

filename = "/Users/tylerviducic/research/gluex/selector_output/pimkpks_thrown_spring.root"
# filename = "/volatile/halld/home/viducic/selector_output/f1_pipkmks/thrown/pipkmks_thrown.root"

root_file = uproot.open(filename)
tree = root_file["pimkpks_thrown"]

target_file = ROOT.TFile('pimkpks_t_binned_thrown_0_2_fullbeam_spring.root', 'RECREATE')

histo_list = []

# histo = ROOT.TH1F("histo", "tminus", 225, 0, 2.25)
# h_f1_200 = ROOT.TH1F("f1_t_0.2", "f1_t_0.2", 125, 1, 2.25)
# h_f1_400 = ROOT.TH1F("f1_t_0.4", "f1_t_0.4", 125, 1, 2.25)
# h_f1_600 = ROOT.TH1F("f1_t_0.6", "f1_t_0.6", 125, 1, 2.25)
# h_f1_800 = ROOT.TH1F("f1_t_0.8", "f1_t_0.8", 125, 1, 2.25)
# h_f1_1000 = ROOT.TH1F("f1_t_1.0", "f1_t_1.0", 125, 1, 2.25)
# h_f1_1200 = ROOT.TH1F("f1_t_1.2", "f1_t_1.2", 125, 1, 2.25)
# h_f1_1400 = ROOT.TH1F("f1_t_1.4", "f1_t_1.4", 125, 1, 2.25)
# h_f1_1600 = ROOT.TH1F("f1_t_1.6", "f1_t_1.6", 125, 1, 2.25)
# h_f1_1800 = ROOT.TH1F("f1_t_1.8", "f1_t_1.8", 125, 1, 2.25)
# h_f1_2000 = ROOT.TH1F("f1_t_2.0", "f1_t_2.0", 125, 1, 2.25)

# histo = ROOT.TH1F("histo", "npart", 10, 0, 10)
# histo = ROOT.TH1F("histo", "pid", 20, 0, 20)

h_f1_100 = ROOT.TH1F("f1_t_0.1", "f1_t_0.1", 125, 1, 2.25)
h_f1_150 = ROOT.TH1F("f1_t_0.15", "f1_t_0.15", 125, 1, 2.25)
h_f1_200 = ROOT.TH1F("f1_t_0.2", "f1_t_0.2", 125, 1, 2.25)
h_f1_250 = ROOT.TH1F("f1_t_0.25", "f1_t_0.25", 125, 1, 2.25)
h_f1_300 = ROOT.TH1F("f1_t_0.3", "f1_t_0.3", 125, 1, 2.25)
h_f1_350 = ROOT.TH1F("f1_t_0.35", "f1_t_0.35", 125, 1, 2.25)
h_f1_400 = ROOT.TH1F("f1_t_0.4", "f1_t_0.4", 125, 1, 2.25)
h_f1_500 = ROOT.TH1F("f1_t_0.5", "f1_t_0.5", 125, 1, 2.25)
h_f1_600 = ROOT.TH1F("f1_t_0.6", "f1_t_0.6", 125, 1, 2.25)
h_f1_700 = ROOT.TH1F("f1_t_0.7", "f1_t_0.7", 125, 1, 2.25)
h_f1_800 = ROOT.TH1F("f1_t_0.8", "f1_t_0.8", 125, 1, 2.25)
h_f1_900 = ROOT.TH1F("f1_t_0.9", "f1_t_0.9", 125, 1, 2.25)
h_f1_1100 = ROOT.TH1F("f1_t_1.1", "f1_t_1.1", 125, 1, 2.25)
h_f1_1300 = ROOT.TH1F("f1_t_1.3", "f1_t_1.3", 125, 1, 2.25)


df = tree.arrays([  
                    'men_t',
                    'mass_f1',
                    'nThrown',
                    'nParticles',
                    'Beam_E', 
                    'PiMinus1_px', 
                    'PiMinus1_py',
                    'PiMinus1_pz',
                    'PiMinus1_E',
                    'PiMinus2_px', 
                    'PiMinus2_py',
                    'PiMinus2_pz',
                    'PiMinus2_E',
                    'PiPlus_px', 
                    'PiPlus_py',
                    'PiPlus_pz',
                    'PiPlus_E',
                    'KPlus_px', 
                    'KPlus_py',
                    'KPlus_pz',
                    'KPlus_E',
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
df['f1_px'] = df['PiMinus1_px'] + df['KPlus_px'] + df['Ks_px'] 
df['f1_py'] = df['PiMinus1_py'] + df['KPlus_py'] + df['Ks_py'] 
df['f1_pz'] = df['PiMinus1_pz'] + df['KPlus_pz'] + df['Ks_pz'] 
df['f1_E'] = df['PiMinus1_E'] + df['KPlus_E'] + df['Ks_E']
df['f1_mass2'] = df['f1_E'] * df['f1_E']  - df['f1_px'] * df['f1_px'] - df['f1_py'] * df['f1_py'] - df['f1_pz'] * df['f1_pz']
df['f1_mass'] = np.sqrt(df['f1_mass2'])

beam_low = 6.5
beam_high = 10.5

df_100 = df[(df['men_t'] > 0.05) & (df['men_t'] <= 0.1)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_150 = df[(df['men_t'] > 0.1) & (df['men_t'] <= 0.15)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_200 = df[(df['men_t'] > 0.15) & (df['men_t'] <= 0.20)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_250 = df[(df['men_t'] > 0.2) & (df['men_t'] <= 0.25)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_300 = df[(df['men_t'] > 0.25) & (df['men_t'] <= 0.3)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_350 = df[(df['men_t'] > 0.3) & (df['men_t'] <= 0.35)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_400 = df[(df['men_t'] > 0.35) & (df['men_t'] <= 0.4)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_500 = df[(df['men_t'] > 0.4) & (df['men_t'] <= 0.5)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_600 = df[(df['men_t'] > 0.5) & (df['men_t'] <= 0.6)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_700 = df[(df['men_t'] > 0.6) & (df['men_t'] <= 0.7)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_800 = df[(df['men_t'] > 0.7) & (df['men_t'] <= 0.8)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_900 = df[(df['men_t'] > 0.8) & (df['men_t'] <= 0.9)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_1100 = df[(df['men_t'] > 0.9) & (df['men_t'] <= 1.1)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
df_1300 = df[(df['men_t'] > 1.1) & (df['men_t'] <= 1.3)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']


# df_200 = df[(df['men_t'] > 0) & (df['men_t'] < 0.2)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_400 = df[(df['men_t'] >= 0.2) & (df['men_t'] < 0.4)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_600 = df[(df['men_t'] >= 0.4) & (df['men_t'] < 0.6)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_800 = df[(df['men_t'] >= 0.6) & (df['men_t'] < 0.8)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_1000 = df[(df['men_t'] >= 0.8) & (df['men_t'] < 1.0)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_1200 = df[(df['men_t'] >= 1.0) & (df['men_t'] < 1.2)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_1400 = df[(df['men_t'] >= 1.2) & (df['men_t'] < 1.4)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_1600 = df[(df['men_t'] >= 1.4) & (df['men_t'] < 1.6)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_1800 = df[(df['men_t'] >= 1.6) & (df['men_t'] < 1.8)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']
# df_2000 = df[(df['men_t'] >= 1.8) & (df['men_t'] < 2.0)& (df['Beam_E'] > beam_low) & (df['Beam_E'] <= beam_high)]['f1_mass']

df_200.columns=['f1_mass']
print(df_200)
print("filling")
# histo.FillN(len(df['f1_mass']), df['f1_mass'].to_numpy(), np.ones(len(df['f1_mass'])))
# histo.FillN(len(df['mass_f1']), df['mass_f1'].to_numpy(), np.ones(len(df['mass_f1'])))
# histo.FillN(len(df['men_t']), df['men_t'].to_numpy(), np.ones(len(df['men_t'])))
h_f1_100.FillN(len(df_100), df_100.to_numpy(), np.ones(len(df_100)))
h_f1_150.FillN(len(df_150), df_150.to_numpy(), np.ones(len(df_150)))
h_f1_200.FillN(len(df_200), df_200.to_numpy(), np.ones(len(df_200)))
h_f1_250.FillN(len(df_250), df_250.to_numpy(), np.ones(len(df_250)))
h_f1_300.FillN(len(df_300), df_300.to_numpy(), np.ones(len(df_300)))
h_f1_350.FillN(len(df_350), df_350.to_numpy(), np.ones(len(df_350)))
h_f1_400.FillN(len(df_400), df_400.to_numpy(), np.ones(len(df_400)))
h_f1_500.FillN(len(df_500), df_500.to_numpy(), np.ones(len(df_500)))
h_f1_600.FillN(len(df_600), df_600.to_numpy(), np.ones(len(df_600)))
h_f1_700.FillN(len(df_700), df_700.to_numpy(), np.ones(len(df_700)))
h_f1_800.FillN(len(df_800), df_800.to_numpy(), np.ones(len(df_800)))
h_f1_900.FillN(len(df_900), df_900.to_numpy(), np.ones(len(df_900)))
h_f1_1100.FillN(len(df_1100), df_1100.to_numpy(), np.ones(len(df_1100)))
h_f1_1300.FillN(len(df_1300), df_1300.to_numpy(), np.ones(len(df_1300)))


# h_f1_200.FillN(len(df_200), df_200.to_numpy(), np.ones(len(df_200)))
# h_f1_400.FillN(len(df_400), df_400.to_numpy(), np.ones(len(df_400)))
# h_f1_600.FillN(len(df_600), df_600.to_numpy(), np.ones(len(df_600)))
# h_f1_800.FillN(len(df_800), df_800.to_numpy(), np.ones(len(df_800)))
# h_f1_1000.FillN(len(df_1000), df_1000.to_numpy(), np.ones(len(df_1000)))
# h_f1_1200.FillN(len(df_1200), df_1200.to_numpy(), np.ones(len(df_1200)))
# h_f1_1400.FillN(len(df_1400), df_1400.to_numpy(), np.ones(len(df_1400)))
# h_f1_1600.FillN(len(df_1600), df_1600.to_numpy(), np.ones(len(df_1600)))
# h_f1_1800.FillN(len(df_1800), df_1800.to_numpy(), np.ones(len(df_1800)))
# h_f1_2000.FillN(len(df_2000), df_2000.to_numpy(), np.ones(len(df_2000)))
# print("drawing")

# c2 = ROOT.TCanvas("c2", "testing")
# c2.Divide(3, 2)
# c2.cd(1)
# h_f1_200.Draw()
# c2.cd(2)
# h_f1_400.Draw()
# c2.cd(3)
# h_f1_1600.Draw()
# c2.cd(4)
# h_f1_1800.Draw()
# c2.cd(5)
# h_f1_2000.Draw()
# c2.Update()

h_f1_200.Write()
target_file.Write()

print("done")