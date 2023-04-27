# thrown mc analysis with root dataframe
import ROOT

filename = "/volatile/halld/home/viducic/selector_output/f1_pipkmks/thrown/pipkmks_thrown_fall.root"
treename = "pipkmks_thrown"

df = ROOT.RDataFrame(treename, filename)

print(df.GetColumnNames())

##############################
## OLD AND DEPRECIATED CODE ##
##############################

# beam = 10 

# target_file = ROOT.TFile(f'pipkmks_t_binned_thrown_0_2_{beam}_fall.root', 'RECREATE')

# df = df.Define("f1_px", "PiPlus1_px + KMinus_px + Ks_px")
# df = df.Define("f1_py", "PiPlus1_py + KMinus_py + Ks_py")
# df = df.Define("f1_pz", "PiPlus1_pz + KMinus_pz + Ks_pz")
# df = df.Define("f1_E", "PiPlus1_E + KMinus_E + Ks_E")

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
