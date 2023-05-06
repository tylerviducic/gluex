import ROOT

ROOT.gROOT.SetBatch(True) # run ROOT in batch mode to create canvas without drawing to screen

run_period = 'spring'

run_period_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017',
}

file_name = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks__phasespace_filtered_{run_period_dict[run_period]}.root'
tree_name = f'mc_pipkmks__phasespace_filtered_{run_period_dict[run_period]}'

kstar_no_cut = 'kspip_m > 0.0'
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

kstar_cut_dict = {
    'kspip_m > 0.0': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

f1_cut_list = [kstar_no_cut, kstar_plus_cut, kstar_zero_cut, kstar_all_cut]

df = ROOT.RDataFrame(tree_name, file_name)
# print(df.GetColumnNames())

kinematic_variables = ['e_beam', 
                       'pip1_px', 'pip1_py', 'pip1_pz', 'pip1_E', 
                       'pip2_px', 'pip2_py', 'pip2_pz', 'pip2_E', 
                       'pim_px', 'pim_py', 'pim_pz', 'pim_E', 
                       'km_px', 'km_py', 'km_pz', 'km_E', 
                       'p_px', 'p_py', 'p_pz', 'p_E', 
                       'vertex_distance', 'mand_t', 'w', 's', "pathlength_sig"]

angular_variables = ['pip1_theta', 'pip2_theta', 'pim_theta', 'km_theta', 'p_theta', 
                     'pip1_phi', 'pip2_phi', 'pim_phi', 'km_phi', 'p_phi']

mass_variables = ['ks_m', 'kmp_m', 'kspip_m', 'ppip_m', 'kmpip_m', 'pipkmks_m']

hist_range_dict = {
                       'e_beam': [4.0, 12.0], 
                       'pip1_px': [-0.6, 0.6], 'pip1_py': [-0.6, 0.6], 'pip1_pz': [0.0, 7.0], 'pip1_E': [0.0, 7.0], 
                       'pip2_px': [-0.6, 0.6], 'pip2_py': [-0.6, 0.6], 'pip2_pz': [0.0, 7.0], 'pip2_E': [0.0, 7.0], 
                       'pim_px': [-0.6, 0.6], 'pim_py': [-0.6, 0.6], 'pim_pz': [0.0, 7.0], 'pim_E': [0.0, 7.0], 
                       'km_px': [-0.6, 0.6], 'km_py': [-0.6, 0.6], 'km_pz': [0.0, 7.0], 'km_E': [0.0, 7.0], 
                       'p_px': [-1.5, 1.5], 'p_py': [-1.5, 1.5], 'p_pz': [0.0, 3.0], 'p_E': [0.0, 3.0], 
                       'vertex_distance': [0.0, 150.0], 'mand_t': [0.0, 4.0], 'w': [3.0, 5.0], 's': [5.0, 25.0], 'pathlength_sig': [0.0, 10.0],
                       'pip1_theta': [0.0, 60.0], 'pip2_theta': [0.0, 60.0], 'pim_theta': [0.0, 80.0], 'km_theta': [0.0, 40.0], 'p_theta': [0.0, 70.0], 
                       'pip1_phi': [0.0, 180.0], 'pip2_phi': [0.0, 180.0], 'pim_phi': [0.0, 180.0], 'km_phi': [0.0, 180.0], 'p_phi': [0.0, 180.0],
                       'ks_m': [0.2, 0.8], 'kmp_m': [1.0, 2.5], 'kspip_m': [0.5, 1.0], 'ppip_m': [0.5, 2.0], 'kmpip_m': [0.5, 1.0], 'pipkmks_m': [1.0, 2.5]
                    }


df = df.Define("pip1_theta", "atan2( sqrt(pip1_px*pip1_px + pip1_py*pip1_py), pip1_pz)*(180.0/3.141592653589793238463)")
df = df.Define("pip2_theta", "atan2( sqrt(pip2_px*pip2_px + pip2_py*pip2_py), pip2_pz)*(180.0/3.141592653589793238463)")
df = df.Define("pim_theta", "atan2( sqrt(pim_px*pim_px + pim_py*pim_py), pim_pz)*(180.0/3.141592653589793238463)")
df = df.Define("km_theta", "atan2( sqrt(km_px*km_px + km_py*km_py), km_pz)*(180.0/3.141592653589793238463)")
df = df.Define("p_theta", "atan2( sqrt(p_px*p_px + p_py*p_py), p_pz)*(180.0/3.141592653589793238463)")
df = df.Define("pip1_phi", "atan2(pip1_py, pip1_px)*(180.0/3.141592653589793238463)")
df = df.Define("pip2_phi", "atan2(pip2_py, pip2_px)*(180.0/3.141592653589793238463)")
df = df.Define("pim_phi", "atan2(pim_py, pim_px)*(180.0/3.141592653589793238463)")
df = df.Define("km_phi", "atan2(km_py, km_px)*(180.0/3.141592653589793238463)")
df = df.Define("p_phi", "atan2(p_py, p_px)*(180.0/3.141592653589793238463)")
df = df.Define("p_p", "sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)")

pp_cut = "p_p > 0.4"
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'

## FILTER HERE IF NEEDED ##

all_variables = kinematic_variables + angular_variables + mass_variables

target_file_name = f'/work/halld/home/viducic/plots/data_mc_compare/phasespace_mc_kinematic_{run_period_dict[run_period]}.root'
target_file = ROOT.TFile(target_file_name, 'RECREATE')

canvas_array = []

pdf_filename = f'/w/halld-scshelf2101/home/viducic/plots/data_mc_compare/phasespace_mc_kinematics_{run_period_dict[run_period]}.pdf'

c1 = ROOT.TCanvas("c1", "c1", 1200, 900)
c1.Print(pdf_filename + "[")
c1.Clear();

for variable in all_variables:
    # print(variable)
    if (variable in angular_variables):
        n_bins = 50
    else:
        n_bins = 100

    c1.cd()

    if variable.split("_")[0] == ('pip2' or 'pim'):
        hist_name = "ks_" + variable
    else:
        hist_name = variable

    if variable == 'pipkmks_m':
        for cut in f1_cut_list:
            hist = df.Filter(cut).Histo1D((hist_name+'_'+kstar_cut_dict[cut], hist_name+'_'+kstar_cut_dict[cut], n_bins, hist_range_dict[variable][0], hist_range_dict[variable][1]), variable)
            hist.Draw("HIST")
            c1.Update()
            c1.Write()
            c1.Print(pdf_filename)
            c1.Clear()
        continue
    
    else:
        hist = df.Histo1D((hist_name, hist_name, n_bins, hist_range_dict[variable][0], hist_range_dict[variable][1]), variable)


    # if variable in kinematic_variables:
    #     print(variable)
    #     c1.SetLogy()
    # else:
    #     c1.SetLogy(0)

    hist.Draw("HIST")

    c1.Update()
    c1.Write()
    c1.Print(pdf_filename)
    c1.Clear()


c1.Print(pdf_filename+']')
target_file.Close()
