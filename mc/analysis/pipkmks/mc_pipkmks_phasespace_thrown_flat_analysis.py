# thrown mc analysis with root dataframe
import ROOT
import time
import os
from common_analysis_tools import *

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

start_time = time.time()


run_period = 'fall'

filename = f"/volatile/halld/home/viducic/selector_output/f1_pipkmks/thrown/pipkmks_phasespace_thrown_{run_dict[run_period]}.root"
treename = "pipkmks_thrown"
print(filename)
histo_array = []

beam_range = 'Beam_E >= 6.50000000000 && Beam_E <= 10.5'
t_range = 'men_t <= 1.9'

kstar_no_cut = 'kspip_m > 0.0'
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

t_dict = {
    1: (0.0, 0.1), 2: (0.1, 0.2), 3: (0.2, 0.3), 4: (0.3, 0.4), 
    5: (0.4, 0.65), 6: (0.65, 0.9), 7: (0.9, 1.4), 8: (1.4, 1.9)
}

beam_dict = {
    1: (6.5, 7.5), 2: (7.5, 8.5), 3: (8.5, 9.5), 4: (9.5, 10.5)
}

kstar_cut_dict = {
    'kspip_m > 0.0': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

beam_bin_filter = """
int get_beam_bin_index(double e_beam) {
        return static_cast<int>(e_beam-6.5) + 1;
}
"""

t_bin_filter = """
int get_t_bin_index(double t) {
    if (t <= 0.4) {
        return static_cast<int>(t/0.1)+1;
    }
    else if (t > 0.4 && t <= 0.9) {
        return static_cast<int>((t-0.4)/0.25)+5;
    }
    else if (t > 0.9 && t <= 1.9) {
        return static_cast<int>((t-0.9)/0.5)+7;
    }
    else {
        return -1;
    }
}
"""

ROOT.gInterpreter.Declare(t_bin_filter)
ROOT.gInterpreter.Declare(beam_bin_filter)

df = ROOT.RDataFrame(treename, filename)

columns = ["nThrown",
           "PiPlus1_px",# "PiPlus1_py", "PiPlus1_pz", "PiPlus1_E", 
           "PiPlus2_px",# "PiPlus2_py", "PiPlus2_pz", "PiPlus2_E", 
           "PiMinus_px",# "PiMinus_py", "PiMinus_pz", "PiMinus_E", 
           "KMinus_px", #"KMinus_py", "KMinus_pz", "KMinus_E", 
           "Proton_px",# "Proton_py", "Proton_pz", "Proton_E", 
           "Ks_px"#, "Ks_py", "Ks_pz", "Ks_E"
]


# columns = ["nParticles", "nThrown", "Beam_px", "Beam_py", "Beam_pz", "Beam_E", 
#            "Target_px", "Target_py", "Target_pz", "Target_E", 
#            "PiPlus1_px", "PiPlus1_py", "PiPlus1_pz", "PiPlus1_E", 
#            "PiPlus2_px", "PiPlus2_py", "PiPlus2_pz", "PiPlus2_E", 
#            "PiMinus_px", "PiMinus_py", "PiMinus_pz", "PiMinus_E", 
#            "KMinus_px", "KMinus_py", "KMinus_pz", "KMinus_E", 
#            "Proton_px", "Proton_py", "Proton_pz", "Proton_E", 
#            "Ks_px", "Ks_py", "Ks_pz", "Ks_E"]
#            "theta_p", "mom_p", "phi_p", 
#            "theta_km", "mom_km", "phi_km", 
#            "theta_pip1", "mom_pip1", "phi_pip1",
#            "theta_pip2", "mom_pip2", "phi_pip2", 
#            "theta_pim", "mom_pim", "phi_pim", 
#            "theta_f1", "mom_f1", "phi_f1", "mass_f1", 
#            "mpippim", "mppip1", "mKsKm", 
#            "men_s", "men_t", "cosTheta_f1_cm", "phi_f1_cm", "cosTheta_Ks_cm", "phi_Ks_cm"]

df = df.Define('pipkmks_px', 'PiPlus1_px + KMinus_px + Ks_px')
df = df.Define('pipkmks_py', 'PiPlus1_py + KMinus_py + Ks_py')
df = df.Define('pipkmks_pz', 'PiPlus1_pz + KMinus_pz + Ks_pz')
df = df.Define('pipkmks_E', 'PiPlus1_E + KMinus_E + Ks_E')
df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')
df = df.Define('e_bin', 'get_beam_bin_index(Beam_E)')
df = df.Define('t_bin', 'get_t_bin_index(men_t)')

# print(df.Display(['men_t', 't_bin', 'Beam_E', 'e_bin', 'pipkmks_m', 'Proton_E']).Print())
# print(df.Filter('t_bin != 6').Count().GetValue())
# input("Press Enter to continue...")

# df = df.Define('km_m', 'sqrt(KMinus_E*KMinus_E - KMinus_px*KMinus_px - KMinus_py*KMinus_py - KMinus_pz*KMinus_pz)')
# define masses for kshort, piplus1, piminus, and piplu2
# df = df.Define('ks_m', 'sqrt(Ks_E*Ks_E - Ks_px*Ks_px - Ks_py*Ks_py - Ks_pz*Ks_pz)')
# df = df.Define('pip1_m', 'sqrt(PiPlus1_E*PiPlus1_E - PiPlus1_px*PiPlus1_px - PiPlus1_py*PiPlus1_py - PiPlus1_pz*PiPlus1_pz)')
# df = df.Define('pim_m', 'sqrt(PiMinus_E*PiMinus_E - PiMinus_px*PiMinus_px - PiMinus_py*PiMinus_py - PiMinus_pz*PiMinus_pz)')
# df = df.Define('pip2_m', 'sqrt(PiPlus2_E*PiPlus2_E - PiPlus2_px*PiPlus2_px - PiPlus2_py*PiPlus2_py - PiPlus2_pz*PiPlus2_pz)')

# hist_m_test = df.Histo1D(('pim_m', 'pim_m', 100, -0.1, 1.0), 'pim_m')
# hist_m_test.Draw()
# input("Press Enter to continue...")

# df = df.Filter(beam_range).Filter(t_range)
# for i in range(int(df.Min('e_bin').GetValue()), int(df.Max('e_bin').GetValue())+1):
#     print(f"number of events in E Bin({i}) = {df.Filter(f'e_bin == {i}').Count().GetValue()}")

#     for j in range(int(df.Min('t_bin').GetValue()), int(df.Max('t_bin').GetValue())+1):
#         print(f"number of events in E Bin({i}) and t Bin({j}) = {df.Filter(f'e_bin == {i}').Filter(f't_bin == {j}').Count().GetValue()}")

# histo_array.append(df.Histo1D(('pipkmks', 'pipkmks', 100, 1.0, 2.5), 'pipkmks_m'))
histo_array.append(df.Filter('Beam_E >= 6.5 && Beam_E <=10.5').Filter('men_t >= 0.1 & men_t <= 1.9').Histo1D(('pipkmks', 'pipkmks', 30, 1.2, 1.5), 'pipkmks_m'))
histo_array.append(df.Filter('Beam_E >= 6.5 && Beam_E <=10.5').Filter('men_t >= 0.1 & men_t <= 1.9').Histo1D(('pipkmks_f1_res_30', 'pipkmks', 30, 1.2, 1.5), 'pipkmks_m'))
histo_array.append(df.Filter('Beam_E >= 6.5 && Beam_E <=10.5').Filter('men_t >= 0.1 & men_t <= 1.9').Histo1D(('pipkmks_f1_res_90', 'pipkmks_f1_res', 90, 1.2, 1.5), 'pipkmks_m'))
histo_array.append(df.Filter('Beam_E >= 6.5 && Beam_E <=10.5').Filter('men_t >= 0.1 & men_t <= 1.9').Histo1D(('pipkmks_f1_res_200', 'pipkmks_f1_res', 200, 1.2, 1.5), 'pipkmks_m'))
histo_array.append(df.Filter('Beam_E >= 6.5 && Beam_E <=10.5').Filter('men_t >= 0.1 & men_t <= 1.9').Histo1D(('pipkmks_f1_res_500', 'pipkmks_f1_res', 500, 1.2, 1.5), 'pipkmks_m'))
histo_array.append(df.Filter('men_t > 0.1 && men_t < 0.5').Filter('Beam_E > 8.0 && Beam_E < 10.0').Histo1D(('pipkmks_sf', 'pipkmks_sf', 30, 1.2, 1.5), 'pipkmks_m'))


n_e_bins = 4
n_t_bins = 8

def fill_histos(cut_df, histo_array, beam_index=0, t_index=0):
    hist_name = f'pipkmks_'
    beam_name = 'beam_full_'
    t_name = 't_full'
    if beam_index > 0:
        beam_low = beam_dict[beam_index][0]
        beam_high = beam_dict[beam_index][1]
        beam_name = f'beam_{beam_low}_{beam_high}_'
    if t_index > 0:
        t_low = t_dict[t_index][0]
        t_high = t_dict[t_index][1]
        t_name = f't_{t_low}_{t_high}'
    hist_name += beam_name + t_name
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 100, 1.0, 2.5), 'pipkmks_m'))



for energy_index in range(1, n_e_bins+1):
    e_cut_df = df.Filter(f'e_bin == {energy_index}')
    fill_histos(e_cut_df, histo_array, beam_index=energy_index)


    for t_index in range(1, n_t_bins+1):
        # print(df.Filter('t_bin == {}'.format(t_index)).Filter('e_bin == {}'.format(energy_index)).Count().GetValue())
        e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
        hist = e_t_cut_df.Histo1D(('pipkmks', 'pipkmks', 100, 1.0, 2.5), 'pipkmks_m')
        fill_histos(e_t_cut_df, histo_array, beam_index=energy_index, t_index=t_index)


for t_index in range(1, n_t_bins+1):
        t_cut_df = df.Filter(f't_bin == {t_index}')
        fill_histos(t_cut_df, histo_array, t_index=t_index)

print("histos done in {} seconds".format(time.time() - start_time))

print(f"/work/halld/home/viducic/data/pipkmks/mc/thrown/mc_pipkmks_phasespace_thrown_flat_result_{run_dict[run_period]}.root")
target_file = ROOT.TFile(f"/work/halld/home/viducic/data/pipkmks/mc/thrown/mc_pipkmks_phasespace_thrown_flat_result_{run_dict[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))

for histo in histo_array:
    histo.Write()

print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close() 

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/mc_pipkmks_phasespace_thrown_graph_{run_dict[run_period]}.dot")