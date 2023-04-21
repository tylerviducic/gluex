# comapre kinematics of mc and data

import ROOT


data_filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_bestX2_2018_spring.root'
mc_filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_flat_bestX2_spring.root'

data_treename = 'pipkmks__B4_M16'
mc_treename = 'pipkmks__ks_pippim__B4_M16'

data_df = ROOT.RDataFrame(data_treename, data_filename)
mc_df = ROOT.RDataFrame(mc_treename, mc_filename)

# print(data_df.GetColumnNames())

# f1 region cut
data_df = data_df.Define("f1_px", "pip1_px + pip2_px + pim_px + km_px")
data_df = data_df.Define("f1_py", "pip1_py + pip2_py + pim_py + km_py")
data_df = data_df.Define("f1_pz", "pip1_pz + pip2_pz + pim_pz + km_pz")
data_df = data_df.Define("f1_E", "pip1_E + pip2_E + pim_E + km_E")
data_df = data_df.Define("f1_m", "sqrt(f1_E*f1_E - f1_px*f1_px - f1_py*f1_py - f1_pz*f1_pz)")

data_df = data_df.Define("pip1_theta", "atan2( sqrt(pip1_px*pip1_px + pip1_py*pip1_py), pip1_pz)")
data_df = data_df.Define("pip2_theta", "atan2( sqrt(pip2_px*pip2_px + pip2_py*pip2_py), pip2_pz)")
data_df = data_df.Define("pim_theta", "atan2( sqrt(pim_px*pim_px + pim_py*pim_py), pim_pz)")
data_df = data_df.Define("km_theta", "atan2( sqrt(km_px*km_px + km_py*km_py), km_pz)")
data_df = data_df.Define("p_theta", "atan2( sqrt(p_px*p_px + p_py*p_py), p_pz)")
data_df = data_df.Define("pip1_phi", "atan2(pip1_py, pip1_px)")
data_df = data_df.Define("pip2_phi", "atan2(pip2_py, pip2_px)")
data_df = data_df.Define("pim_phi", "atan2(pim_py, pim_px)")
data_df = data_df.Define("km_phi", "atan2(km_py, km_px)")
data_df = data_df.Define("p_phi", "atan2(p_py, p_px)")
data_df = data_df.Define("p_p", "sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)")


mc_df = mc_df.Define("pip1_theta", "atan2( sqrt(pip1_px*pip1_px + pip1_py*pip1_py), pip1_pz)")
mc_df = mc_df.Define("pip2_theta", "atan2( sqrt(pip2_px*pip2_px + pip2_py*pip2_py), pip2_pz)")
mc_df = mc_df.Define("pim_theta", "atan2( sqrt(pim_px*pim_px + pim_py*pim_py), pim_pz)")
mc_df = mc_df.Define("km_theta", "atan2( sqrt(km_px*km_px + km_py*km_py), km_pz)")
mc_df = mc_df.Define("p_theta", "atan2( sqrt(p_px*p_px + p_py*p_py), p_pz)")
mc_df = mc_df.Define("pip1_phi", "atan2(pip1_py, pip1_px)")
mc_df = mc_df.Define("pip2_phi", "atan2(pip2_py, pip2_px)")
mc_df = mc_df.Define("pim_phi", "atan2(pim_py, pim_px)")
mc_df = mc_df.Define("km_phi", "atan2(km_py, km_px)")
mc_df = mc_df.Define("p_phi", "atan2(p_py, p_px)")

f1_region_cut = "f1_m > 1.2 && f1_m < 1.325"
data_df.Filter(f1_region_cut)

momentum_variable_list = ["e_beam", 
                 "pip1_px", "pip1_py", "pip1_pz", "pip1_E", 
                 "pip2_px", "pip2_py", "pip2_pz", "pip2_E", 
                 "pim_px", "pim_py", "pim_pz", "pim_E", 
                 "km_px", "km_py", "km_pz", "km_E",
                 "p_px", "p_py", "p_pz", "p_E", 
                 # "pathlength_sig", "cos_colin", "vertex_distance", 
                 "mand_t", "w", "s" ]

angular_variable_list = [
    "pip1_theta", "pip2_theta", "pim_theta", "km_theta", "p_theta",
    "pip1_phi", "pip2_phi", "pim_phi", "km_phi", "p_phi"
]

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
c1.Divide(5, 5)

c2 = ROOT.TCanvas("c2", "c2", 800, 600)
c2.Divide(2, 5)

momentum_data_hist_array = []
momentum_mc_hist_array = []
angular_data_hist_array = []
angular_mc_hist_array = []

for variable in momentum_variable_list:
    data_hist = data_df.Histo1D(variable)
    mc_hist = mc_df.Histo1D(variable)
    data_hist.Scale(1.0/data_hist.Integral())
    mc_hist.Scale(1.0/mc_hist.Integral())

    mc_hist.SetLineColor(ROOT.kRed)
    data_hist.SetLineColor(ROOT.kBlue)
    momentum_data_hist_array.append(data_hist)
    momentum_mc_hist_array.append(mc_hist)

for variable in angular_variable_list:
    data_hist = data_df.Histo1D(variable)
    mc_hist = mc_df.Histo1D(variable)
    data_hist.Scale(1.0/data_hist.Integral())
    mc_hist.Scale(1.0/mc_hist.Integral())

    mc_hist.SetLineColor(ROOT.kRed)
    data_hist.SetLineColor(ROOT.kBlue)
    angular_data_hist_array.append(data_hist)
    angular_mc_hist_array.append(mc_hist)

# c1 = ROOT.TCanvas("c1", "c1", 800, 600)
# proton_p_hist = data_df.Histo1D(("p_p", "p_p", 500, 0, 2.0), "p_p")
# proton_p_hist.Draw("HIST")
# c1.Update()

for i in range(len(momentum_data_hist_array)):
    c1.cd(i+1)
    momentum_data_hist_array[i].Draw("HIST")
    momentum_mc_hist_array[i].Draw("same, HIST")

for j in range(len(angular_data_hist_array)):
    c2.cd(j+1)
    angular_data_hist_array[j].Draw("HIST")
    angular_mc_hist_array[j].Draw("same, HIST")

c1.Update()
c2.Update()
