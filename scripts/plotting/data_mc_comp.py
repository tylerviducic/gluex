# compare data and MC with cuts applied post analysis script running

#### REMEMBER TO APPLY F1 SIGNAL REGION CUT ####


import ROOT
import math

def get_taller_hist(hist1, hist2):
    if hist1.GetMaximum() > hist2.GetMaximum():
        return (hist1, hist2)
    else:
        return (hist2, hist1)

run_period = 'spring'
run_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017'
}

ROOT.gROOT.SetBatch(True) # run ROOT in batch mode to create canvas without drawing to screen

data_filename = f'/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_filtered_{run_dict[run_period]}.root'
mc_filename = f'/w/halld-scshelf2101/home/viducic/data/pipkmks/mc/signal/mc_pipkmks_filtered_{run_dict[run_period]}.root'
print(data_filename)

data_tree_name = 'pipkmks_filtered_2018_spring'
mc_tree_name = 'mc_pipkmks_filtered_2018_spring'

data_df = ROOT.RDataFrame(data_tree_name, data_filename)
mc_df = ROOT.RDataFrame(mc_tree_name, mc_filename)

kinematic_variables = ['e_beam', 
                       'pip1_px', 'pip1_py', 'pip1_pz', 'pip1_E', 
                       'pip2_px', 'pip2_py', 'pip2_pz', 'pip2_E', 
                       'pim_px', 'pim_py', 'pim_pz', 'pim_E', 
                       'km_px', 'km_py', 'km_pz', 'km_E', 
                       'p_px', 'p_py', 'p_pz', 'p_E', 'p_p',
                       'vertex_distance', 'mand_t', 'w', 's']

angular_variables = ['pip1_theta', 'pip2_theta', 'pim_theta', 'km_theta', 'p_theta', 
                     'pip1_phi', 'pip2_phi', 'pim_phi', 'km_phi', 'p_phi']

hist_range_dict = {
                       'e_beam': [4.0, 12.0], 
                       'pip1_px': [-0.6, 0.6], 'pip1_py': [-0.6, 0.6], 'pip1_pz': [0.0, 7.0], 'pip1_E': [0.0, 7.0], 
                       'pip2_px': [-0.6, 0.6], 'pip2_py': [-0.6, 0.6], 'pip2_pz': [0.0, 7.0], 'pip2_E': [0.0, 7.0], 
                       'pim_px': [-0.6, 0.6], 'pim_py': [-0.6, 0.6], 'pim_pz': [0.0, 7.0], 'pim_E': [0.0, 7.0], 
                       'km_px': [-0.6, 0.6], 'km_py': [-0.6, 0.6], 'km_pz': [0.0, 7.0], 'km_E': [0.0, 7.0], 
                       'p_px': [-1.5, 1.5], 'p_py': [-1.5, 1.5], 'p_pz': [0.0, 3.0], 'p_E': [0.0, 3.0], 'p_p': [0.0, 3.0],
                       'vertex_distance': [0.0, 150.0], 'mand_t': [0.0, 2.0], 'w': [3.0, 5.0], 's': [5.0, 25.0],
                       'pip1_theta': [0.0, 60.0], 'pip2_theta': [0.0, 60.0], 'pim_theta': [0.0, 80.0], 'km_theta': [0.0, 40.0], 'p_theta': [0.0, 70.0], 
                       'pip1_phi': [0.0, 180.0], 'pip2_phi': [0.0, 180.0], 'pim_phi': [0.0, 180.0], 'km_phi': [0.0, 180.0], 'p_phi': [0.0, 180.0]
                    }


data_df = data_df.Define("pip1_theta", "atan2( sqrt(pip1_px*pip1_px + pip1_py*pip1_py), pip1_pz)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("pip2_theta", "atan2( sqrt(pip2_px*pip2_px + pip2_py*pip2_py), pip2_pz)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("pim_theta", "atan2( sqrt(pim_px*pim_px + pim_py*pim_py), pim_pz)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("km_theta", "atan2( sqrt(km_px*km_px + km_py*km_py), km_pz)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("p_theta", "atan2( sqrt(p_px*p_px + p_py*p_py), p_pz)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("pip1_phi", "atan2(pip1_py, pip1_px)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("pip2_phi", "atan2(pip2_py, pip2_px)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("pim_phi", "atan2(pim_py, pim_px)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("km_phi", "atan2(km_py, km_px)*(180.0/3.141592653589793238463)")
data_df = data_df.Define("p_phi", "atan2(p_py, p_px)*(180.0/3.141592653589793238463)")
# data_df = data_df.Define("p_p", "sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)")

mc_df = mc_df.Define("pip1_theta", "atan2( sqrt(pip1_px*pip1_px + pip1_py*pip1_py), pip1_pz)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("pip2_theta", "atan2( sqrt(pip2_px*pip2_px + pip2_py*pip2_py), pip2_pz)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("pim_theta", "atan2( sqrt(pim_px*pim_px + pim_py*pim_py), pim_pz)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("km_theta", "atan2( sqrt(km_px*km_px + km_py*km_py), km_pz)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("p_theta", "atan2( sqrt(p_px*p_px + p_py*p_py), p_pz)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("pip1_phi", "atan2(pip1_py, pip1_px)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("pip2_phi", "atan2(pip2_py, pip2_px)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("pim_phi", "atan2(pim_py, pim_px)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("km_phi", "atan2(km_py, km_px)*(180.0/3.141592653589793238463)")
mc_df = mc_df.Define("p_phi", "atan2(p_py, p_px)*(180.0/3.141592653589793238463)")
# mc_df = mc_df.Define("p_p", "sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)")

pp_cut = "p_p > 0.4"
f1_region = 'pipkmks_m > 1.24 && pipkmks_m < 1.32'

data_df = data_df.Filter(pp_cut).Filter(f1_region)
mc_df = mc_df.Filter(pp_cut).Filter(f1_region)

# print(data_df.Count().GetValue())


all_variables = kinematic_variables + angular_variables

target_file_name = f'/work/halld/home/viducic/plots/data_mc_compare/data_mc_compare_f1_flat_{run_dict[run_period]}.root'
target_file = ROOT.TFile(target_file_name, 'RECREATE')

canvas_array = []

pdf_filename = '/w/halld-scshelf2101/home/viducic/plots/data_mc_compare/mc_data_pipkmks_comparison.pdf'

c1 = ROOT.TCanvas("c1", "c1", 1200, 900)
c1.Print(pdf_filename + "[")
c1.Clear()

for variable in all_variables:
    # print(variable)
    if (variable in angular_variables):
        n_bins = 50
    else:
        n_bins = 150

    c1.cd()

    if variable.split("_")[0] == ('pip2' or 'pim'):
        hist_name = "ks_" + variable
    else:
        hist_name = variable

    data_hist = data_df.Histo1D((hist_name, hist_name, n_bins, hist_range_dict[variable][0], hist_range_dict[variable][1]), variable)
    # data_hist = data_df.Histo1D(variable)
    # print(data_hist.Integral())
    mc_hist = mc_df.Histo1D((hist_name, hist_name, n_bins, hist_range_dict[variable][0], hist_range_dict[variable][1]), variable)
    data_hist.Scale(1.0/data_hist.Integral())
    mc_hist.Scale(1.0/mc_hist.Integral())

    # if variable in kinematic_variables:
    #     # print(variable)
    #     c1.SetLogy()
    # else:
    #     c1.SetLogy(0)

    hists_by_size = get_taller_hist(data_hist, mc_hist) 

    data_hist.SetLineColor(ROOT.kBlue)
    mc_hist.SetLineColor(ROOT.kRed)


    hists_by_size[0].Draw("HIST")
    hists_by_size[1].Draw("HIST SAME")
    c1.Update()
    c1.Write()
    c1.Print(pdf_filename)
    c1.Clear()

c1.Print(pdf_filename+']')
target_file.Close()









