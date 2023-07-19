# thrown mc analysis with root dataframe
import ROOT
import time
import os
import my_library.common_analysis_tools as ct

os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

start_time = time.time()

run_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017',
}

run_period = 'spring'

filename = f"/volatile/halld/home/viducic/selector_output/f1_pimkpks/thrown/pimkpks_thrown_{run_dict[run_period]}.root"
treename = "pimkpks_thrown"

histo_array = []

beam_range = 'Beam_E >= 6.50000000000 && Beam_E <= 10.5'
t_range = 'men_t <= 1.9'

kstar_no_cut = 'kspim_m > 0.0'
kstar_plus_cut = 'kspim_m < 0.8 || kspim_m > 1.0'
kstar_zero_cut = 'kppim_m < 0.8 || kppim_m > 1.0'
kstar_all_cut = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'

t_dict = {
    1: (0.0, 0.1), 2: (0.1, 0.2), 3: (0.2, 0.3), 4: (0.3, 0.4), 
    5: (0.4, 0.65), 6: (0.65, 0.9), 7: (0.9, 1.4), 8: (1.4, 1.9)
}

beam_dict = {
    1: (6.5, 7.5), 2: (7.5, 8.5), 3: (8.5, 9.5), 4: (9.5, 10.5)
}

kstar_cut_dict = {
    'kspim_m > 0.0': 'kstar_no_cut',
    'kspim_m < 0.8 || kspim_m > 1.0': 'kstar_minus_cut',
    'kppim_m < 0.8 || kppim_m > 1.0': 'kstar_zero_cut',
    '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)': 'kstar_all_cut'
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


# columns = ["nParticles", "nThrown", "Beam_px", "Beam_py", "Beam_pz", "Beam_E", 
#            "Target_px", "Target_py", "Target_pz", "Target_E", 
#            "PiMinus1_px", "PiMinus1_py", "PiMinus1_pz", "PiMinus1_E", 
#            "PiPlus2_px", "PiPlus2_py", "PiPlus2_pz", "PiPlus2_E", 
#            "PiMinus_px", "PiMinus_py", "PiMinus_pz", "PiMinus_E", 
#            "KPlus_px", "KPlus_py", "KPlus_pz", "KPlus_E", 
#            "Proton_px", "Proton_py", "Proton_pz", "Proton_E", 
#            "Ks_px", "Ks_py", "Ks_pz", "Ks_E", 
#            "theta_p", "mom_p", "phi_p", 
#            "theta_km", "mom_km", "phi_km", 
#            "theta_pip1", "mom_pip1", "phi_pip1",
#            "theta_pip2", "mom_pip2", "phi_pip2", 
#            "theta_pim", "mom_pim", "phi_pim", 
#            "theta_f1", "mom_f1", "phi_f1", "mass_f1", 
#            "mpippim", "mppip1", "mKsKm", 
#            "men_s", "men_t", "cosTheta_f1_cm", "phi_f1_cm", "cosTheta_Ks_cm", "phi_Ks_cm"]

df = df.Define('pimkpks_px', 'PiMinus1_px + KPlus_px + Ks_px')
df = df.Define('pimkpks_py', 'PiMinus1_py + KPlus_py + Ks_py')
df = df.Define('pimkpks_pz', 'PiMinus1_pz + KPlus_pz + Ks_pz')
df = df.Define('pimkpks_E', 'PiMinus1_E + KPlus_E + Ks_E')
df = df.Define('pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')
df = df.Define('e_bin', 'get_beam_bin_index(Beam_E)')
df = df.Define('t_bin', 'get_t_bin_index(men_t)')


# df = df.Filter(beam_range).Filter(t_range)
# for i in range(int(df.Min('e_bin').GetValue()), int(df.Max('e_bin').GetValue())+1):
#     print(f"number of events in E Bin({i}) = {df.Filter(f'e_bin == {i}').Count().GetValue()}")

#     for j in range(int(df.Min('t_bin').GetValue()), int(df.Max('t_bin').GetValue())+1):
#         print(f"number of events in E Bin({i}) and t Bin({j}) = {df.Filter(f'e_bin == {i}').Filter(f't_bin == {j}').Count().GetValue()}")

        

histo_array.append(df.Histo1D(('pimkpks', 'pimkpks', 150, 1.0, 2.5), 'pimkpks_m'))
print(df.Filter('men_t > 0.1 && men_t < 0.5').Filter('Beam_E > 8.0 && Beam_E < 10.0').Count().GetValue())


n_e_bins = 4
n_t_bins = 8

def fill_histos(cut_df, histo_array, beam_index=0, t_index=0):
    hist_name = f'pimkpks_'
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
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 150, 1.0, 2.5), 'pimkpks_m'))


for energy_index in range(1, n_e_bins+1):
    e_cut_df = df.Filter(f'e_bin == {energy_index}')
    fill_histos(e_cut_df, histo_array, beam_index=energy_index)


    for t_index in range(1, n_t_bins+1):
        e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
        fill_histos(e_t_cut_df, histo_array, beam_index=energy_index, t_index=t_index)


for t_index in range(1, n_t_bins+1):
        t_cut_df = df.Filter(f't_bin == {t_index}')
        fill_histos(t_cut_df, histo_array, t_index=t_index)

print("histos done in {} seconds".format(time.time() - start_time))

target_file = ROOT.TFile(f"/work/halld/home/viducic/data/pimkpks/mc/thrown/mc_pimkpks_thrown_flat_result_{run_dict[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close() 

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/mc_pimkpks_thrown_graph_{run_dict[run_period]}.dot")


##############################
## OLD AND DEPRECIATED CODE ##
##############################

# beam = 10 


# target_file = ROOT.TFile(f'pimkpks_t_binned_thrown_0_2_{beam}_fall.root', 'RECREATE')

# df = df.Define("f1_px", "PiMinus1_px + KPlus_px + Ks_px")
# df = df.Define("f1_py", "PiMinus1_py + KPlus_py + Ks_py")
# df = df.Define("f1_pz", "PiMinus1_pz + KPlus_pz + Ks_pz")
# df = df.Define("f1_E", "PiMinus1_E + KPlus_E + Ks_E")

# df = df.Define("f1_m2", "f1_E*f1_E - f1_px*f1_px - f1_py*f1_py - f1_pz*f1_pz")
# df = df.Define("f1_m", "sqrt(f1_m2)")


# beam_low = beam - 0.5
# beam_high = beam + 0.5

# cut_energy = f'Beam_E > {beam_low} && Beam_E < {beam_high}'

# df = df.Filter(cut_energy)

# hist_100 = df.Filter("men_t > 0.0 && men_t <= 0.1").Histo1D(("f1_t_0.1", "f1_t_0.1", 70, 1, 1.7), "f1_m")
# hist_200 = df.Filter("men_t > 0.1 && men_t <= 0.2").Histo1D(("f1_t_0.2", "f1_t_0.2", 70, 1, 1.7), "f1_m")
# hist_300 = df.Filter("men_t > 0.2 && men_t <= 0.3").Histo1D(("f1_t_0.3", "f1_t_0.3", 70, 1, 1.7), "f1_m")
# hist_400 = df.Filter("men_t > 0.3 && men_t <= 0.4").Histo1D(("f1_t_0.4", "f1_t_0.4", 70, 1, 1.7), "f1_m")

# hist_650 = df.Filter("men_t > 0.4 && men_t <= 0.65").Histo1D(("f1_t_0.65", "f1_t_0.65", 70, 1, 1.7), "f1_m")
# hist_900 = df.Filter("men_t > 0.65 && men_t <= 0.9").Histo1D(("f1_t_0.9", "f1_t_0.9", 70, 1, 1.7), "f1_m")

# hist_1400 = df.Filter("men_t > 0.6 && men_t <= 1.4").Histo1D(("f1_t_1.4", "f1_t_1.4", 70, 1, 1.7), "f1_m")
# hist_1900 = df.Filter("men_t > 1.4 && men_t <= 1.9").Histo1D(("f1_t_1.9", "f1_t_1.9", 70, 1, 1.7), "f1_m")

# # hist_150 = df.Filter("men_t > 0.1 && men_t <= 0.15").Histo1D(("f1_t_0.15", "f1_t_0.15", 125, 1, 2.25), "f1_m")
# # hist_200 = df.Filter("men_t > 0.15 && men_t <= 0.2").Histo1D(("f1_t_0.2", "f1_t_0.2", 125, 1, 2.25), "f1_m")
# # hist_250 = df.Filter("men_t > 0.2 && men_t <= 0.25").Histo1D(("f1_t_0.25", "f1_t_0.25", 125, 1, 2.25), "f1_m")
# # hist_300 = df.Filter("men_t > 0.25 && men_t <= 0.3").Histo1D(("f1_t_0.3", "f1_t_0.3", 125, 1, 2.25), "f1_m")
# # hist_350 = df.Filter("men_t > 0.3 && men_t <= 0.35").Histo1D(("f1_t_0.35", "f1_t_0.35", 125, 1, 2.25), "f1_m")
# # hist_400 = df.Filter("men_t > 0.35 && men_t <= 0.4").Histo1D(("f1_t_0.4", "f1_t_0.4", 125, 1, 2.25), "f1_m")
# # hist_500 = df.Filter("men_t > 0.4 && men_t <= 0.5").Histo1D(("f1_t_0.5", "f1_t_0.5", 125, 1, 2.25), "f1_m")
# # hist_600 = df.Filter("men_t > 0.5 && men_t <= 0.6").Histo1D(("f1_t_0.6", "f1_t_0.6", 125, 1, 2.25), "f1_m")
# # hist_700 = df.Filter("men_t > 0.6 && men_t <= 0.7").Histo1D(("f1_t_0.7", "f1_t_0.7", 125, 1, 2.25), "f1_m")
# # hist_800 = df.Filter("men_t > 0.7 && men_t <= 0.8").Histo1D(("f1_t_0.8", "f1_t_0.8", 125, 1, 2.25), "f1_m")
# # hist_900 = df.Filter("men_t > 0.8 && men_t <= 0.9").Histo1D(("f1_t_0.9", "f1_t_0.9", 125, 1, 2.25), "f1_m")
# # hist_1100 = df.Filter("men_t > 0.9 && men_t <= 1.1").Histo1D(("f1_t_1.1", "f1_t_1.1", 125, 1, 2.25), "f1_m")
# # hist_1300 = df.Filter("men_t > 1.1 && men_t <= 1.3").Histo1D(("f1_t_1.3", "f1_t_1.3", 125, 1, 2.25), "f1_m")
# # hist_1500 = df.Filter("men_t > 1.3 && men_t <= 1.5").Histo1D(("f1_t_1.5", "f1_t_1.5", 125, 1, 2.25), "f1_m")
# # hist_1700 = df.Filter("men_t > 1.5 && men_t <= 1.7").Histo1D(("f1_t_1.7", "f1_t_1.7", 125, 1, 2.25), "f1_m")
# # hist_1900 = df.Filter("men_t > 1.7 && men_t <= 1.9").Histo1D(("f1_t_1.9", "f1_t_1.9", 125, 1, 2.25), "f1_m")


# # c1 = ROOT.TCanvas("c1")
# hist_100.Write() 
# # hist_150.Write()  
# hist_200.Write() 
# # hist_250.Write() 
# hist_300.Write() 
# # hist_350.Write() 
# hist_400.Write() 
# # hist_500.Write()
# hist_650.Write()
# # hist_700.Write()
# # hist_800.Write()
# hist_900.Write()
# # hist_1100.Write()
# # hist_1300.Write()
# hist_1400.Write()
# # hist_1700.Write()
# hist_1900.Write()
# # target_file.Write()
# target_file.Close()
# print("Done")
