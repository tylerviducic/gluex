# compare data and MC with cuts applied post analysis script running
# f1 region cut has already been applied

import ROOT

run_period = 'spring'
run_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017'
}

ROOT.gROOT.SetBatch(True) # run ROOT in batch mode to create canvas without drawing to screen

data_filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_signal_filtered_{run_dict[run_period]}.root'
mc_filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_signal_filtered_{run_dict[run_period]}.root'

data_tree_name = 'pipkmks_signal_filtered_2018_spring'
mc_tree_name = 'mc_pipkmks_signal_filtered_2018_spring'

data_df = ROOT.RDataFrame(data_tree_name, data_filename)
mc_df = ROOT.RDataFrame(mc_tree_name, mc_filename)

kinematic_variables = ['e_beam', 
                       'pip1_px', 'pip1_py', 'pip1_pz', 'pip1_E', 
                       'pip2_px', 'pip2_py', 'pip2_pz', 'pip2_E', 
                       'pim_px', 'pim_py', 'pim_pz', 'pim_E', 
                       'km_px', 'km_py', 'km_pz', 'km_E', 
                       'p_px', 'p_py', 'p_pz', 'p_E', 'vertex_distance', 'mand_t', 'w', 's']



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

angular_variables = ['pip1_theta', 'pip2_theta', 'pim_theta', 'km_theta', 'p_theta', 
                     'pip1_phi', 'pip2_phi', 'pim_phi', 'km_phi', 'p_phi']

all_variables = kinematic_variables + angular_variables

target_file_name = f'/work/halld/home/viducic/plots/data_mc_compare/data_mc_compare_f1_flat_{run_dict[run_period]}.root'
target_file = ROOT.TFile(target_file_name, 'RECREATE')

canvas_array = []

for variable in all_variables:
    # print(variable)
    c = ROOT.TCanvas(variable, variable, 1200, 900)
    c.cd()
    data_hist = data_df.Histo1D(variable)
    mc_hist = mc_df.Histo1D(variable)
    data_hist.Scale(1.0/data_hist.Integral())
    mc_hist.Scale(1.0/mc_hist.Integral())
    data_hist.SetLineColor(ROOT.kBlue)
    mc_hist.SetLineColor(ROOT.kRed)
    data_hist.Draw("HIST")
    mc_hist.Draw("HIST SAME")
    c.Update()
    c.Write()
    # canvas_array.append(c)
    # del(c)









