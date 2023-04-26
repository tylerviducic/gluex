# script for making histograms from flat best chi2/ndf trees

import ROOT
import time

ROOT.gStyle.SetOptStat(0)
ROOT.EnableImplicitMT()

start_time = time.time()

run_period_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017',
}

run_period = 'fall'
filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_bestX2_{run_period_dict[run_period]}.root'
treename = 'pipkmks__B4_M16'

beam_df_array = []
histo_array_low = []
histo_array_med = []
histo_array_high = []

## DEFINE CUTS ##
#TODO cuts to not be just-in-time compiled

ks_pathlength_cut = 'pathlength_sig > 5'
ks_cut1 = 'cos_colin > 0.99'
ks_cut2 = ' vertex_distance > 3'
ks_mass_cut = 'ks_m > 0.45 && ks_m < 0.55'
ppim_mass_cut = 'ppip_m > 1.4'
kmp_mass_cut = 'kmp_m > 1.95'
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'

kstar_no_cut = "no_cut"
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

kstar_cut_dict = {
    'no_cut': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

f1_cut_list = [kstar_no_cut, kstar_plus_cut, kstar_zero_cut, kstar_all_cut]


df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())


## DEFINE ALL NECESSARY COLUMNS ##

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

df = df.Define('ks_px_measured', "pip2_px_measured + pim_px_measured")
df = df.Define('ks_py_measured', "pip2_py_measured + pim_py_measured")
df = df.Define('ks_pz_measured', "pip2_pz_measured + pim_pz_measured")
df = df.Define('ks_E_measured', "pip2_E_measured + pim_E_measured")
df = df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

df = df.Define('ppip_px', 'pip1_px + p_px')
df = df.Define('ppip_py', 'pip1_py + p_py')
df = df.Define('ppip_pz', 'pip1_pz + p_pz')
df = df.Define('ppip_E', 'pip1_E + p_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')

df = df.Define('ppip_px', 'pip1_px + p_px')
df = df.Define('ppip_py', 'pip1_py + p_py')
df = df.Define('ppip_pz', 'pip1_pz + p_pz')
df = df.Define('ppip_E', 'pip1_E + p_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')

df = df.Define('missing_px', '-p_px - pip1_px - ks_px - km_px')
df = df.Define('missing_py', '-p_py - pip1_py - ks_py - km_py')
df = df.Define('missing_pz', 'e_beam - p_pz - pip1_pz - ks_pz - km_pz')
df = df.Define('missing_E', 'e_beam + 0.938 - p_E - pip1_E - ks_E - km_E')

df = df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

df = df.Define('kmp_px', 'p_px + km_px')
df = df.Define('kmp_py', 'p_py + km_py')
df = df.Define('kmp_pz', 'p_pz + km_pz')
df = df.Define('kmp_E', 'p_E + km_E')

df = df.Define('kmp_m', 'sqrt(kmp_E*kmp_E - kmp_px*kmp_px - kmp_py*kmp_py - kmp_pz*kmp_pz)')

df = df.Define('kspip_px', 'pip1_px + ks_px')
df = df.Define('kspip_py', 'pip1_py + ks_py')
df = df.Define('kspip_pz', 'pip1_pz + ks_pz')
df = df.Define('kspip_E', 'pip1_E + ks_E')

df = df.Define('kspip_m', 'sqrt(kspip_E*kspip_E - kspip_px*kspip_px - kspip_py*kspip_py - kspip_pz*kspip_pz)')

df = df.Define('kmpip_px', 'pip1_px + km_px')
df = df.Define('kmpip_py', 'pip1_py + km_py')
df = df.Define('kmpip_pz', 'pip1_pz + km_pz')
df = df.Define('kmpip_E', 'pip1_E + km_E')

df = df.Define('kmpip_m', 'sqrt(kmpip_E*kmpip_E - kmpip_px*kmpip_px - kmpip_py*kmpip_py - kmpip_pz*kmpip_pz)')

df = df.Define('pipkmks_px', 'pip1_px + km_px + ks_px')
df = df.Define('pipkmks_py', 'pip1_py + km_py + ks_py')
df = df.Define('pipkmks_pz', 'pip1_pz + km_pz + ks_pz')
df = df.Define('pipkmks_E', 'pip1_E + km_E + ks_E')

df = df.Define('pipkmks_px_measured', "pip1_px_measured + km_px_measured + ks_px_measured")
df = df.Define('pipkmks_py_measured', "pip1_py_measured + km_py_measured + ks_py_measured")
df = df.Define('pipkmks_pz_measured', "pip1_pz_measured + km_pz_measured + ks_pz_measured")
df = df.Define('pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')

df = df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')

df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

df = df.Define('kmks_px', 'km_px + ks_px')
df = df.Define('kmks_py', 'km_py + ks_py')
df = df.Define('kmks_pz', 'km_pz + ks_pz')
df = df.Define('kmks_E', 'km_E + ks_E')
df = df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')

## FILTER DATAFRAME AFTER DATA IS DEFINED ##

df = df.Filter(ks_pathlength_cut)
print('cut 1 done in {} seconds'.format(time.time() - start_time))
df = df.Filter(ks_mass_cut)
print('cut 2 done in {} seconds'.format(time.time() - start_time))
df = df.Filter(ppim_mass_cut)
print("cut 3 done in {} seconds".format(time.time() - start_time))
df = df.Filter(kmp_mass_cut)
print("cut 4 done in {} seconds".format(time.time() - start_time))

## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')
f1_nocut = df.Histo1D(('f1_nocut', 'f1_nocut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut', 'f1_kstar_plus_cut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut', 'f1_kstar_zero_cut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_all_cut = df.Filter(kstar_all_cut).Histo1D(('f1_kstar_all_cut', 'f1_kstar_all_cut', 50, 1.0, 1.7), 'pipkmks_m')

f1_mass_range_all = df.Filter(kstar_all_cut).Histo1D(('massrange_all', 'massrange_all', 200, 1.0, 4.0), 'pipkmks_m')
f1_mass_range_none = df.Histo1D(('massrange_none', 'massrange_none', 200, 1.0, 4.0), 'pipkmks_m')
f1_mass_range_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('massrange_kstar_zero_cut', 'massrange_kstar_zero_cut', 200, 1.0, 4.0), 'pipkmks_m')
f1_mass_range_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('massrange_kstar_plus_cut', 'massrange_kstar_plus_cut', 200, 1.0, 4.0), 'pipkmks_m')

f1_nocut_narrow = df.Histo1D(('f1_nocut_narrow', 'f1_nocut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
f1_nocut_medium = df.Histo1D(('f1_nocut_medium', 'f1_nocut_medium', 100, 1.0, 2.5), 'pipkmks_m')
f1_nocut_wide = df.Histo1D(('f1_nocut_wide', 'f1_nocut_wide', 200, 1.0, 3.8), 'pipkmks_m')

f1_kstar_plus_cut_narrow = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_narrow', 'f1_kstar_plus_cut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_plus_cut_medium = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_medium', 'f1_kstar_plus_cut_medium', 100, 1.0, 2.5), 'pipkmks_m')
f1_kstar_plus_cut_wide = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_wide', 'f1_kstar_plus_cut_wide', 200, 1.0, 3.8), 'pipkmks_m')

f1_kstar_zero_cut_narrow = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_narrow', 'f1_kstar_zero_cut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_zero_cut_medium = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_medium', 'f1_kstar_zero_cut_medium', 100, 1.0, 2.5), 'pipkmks_m')
f1_kstar_zero_cut_wide = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_wide', 'f1_kstar_zero_cut_wide', 200, 1.0, 3.8), 'pipkmks_m')


f1_mass_range_all.SetLineColor(1)
f1_mass_range_none.SetLineColor(2)
f1_mass_range_kstar_zero_cut.SetLineColor(6)
f1_mass_range_kstar_plus_cut.SetLineColor(4)

f1_nocut.SetLineColor(1)
f1_kstar_plus_cut.SetLineColor(2)
f1_kstar_zero_cut.SetLineColor(6)
f1_kstar_all_cut.SetLineColor(4)

# UNCOMMENT FOR SIGNAL REGION FILTER 
# data_mc_comparison_df = df.Filter(f1_region)
# data_mc_comparison_df.Snapshot(f'pipkmks_signal_filtered_{run_period_dict[run_period]}', f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_signal_filtered_{run_period_dict[run_period]}.root')
# print('cut file written in {} seconds'.format(time.time() - start_time))

# UNCOMMENT FOR FULL MASS SPECTRUM FILTERED DATA 
df.Snapshot(f'pipkmks_filtered_{run_period_dict[run_period]}', f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_filtered_{run_period_dict[run_period]}.root')
print('cut file written in {} seconds'.format(time.time() - start_time))

## LOOP OVER ENERGY AND T BINS ## 
#TODO - refactor beam cuts to be columns in the df

for beam_value in range(5, 11):
    beam_low = beam_value - 0.5
    beam_high = beam_value + 0.5
    beam_df_array.append(df.Filter('e_beam > {} && e_beam <= {}'.format(beam_low, beam_high)))


print("beam cuts done in {} seconds".format(time.time() - start_time))

t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']

pt_diff_array = []
tslope_array = []

for cut in f1_cut_list:
    # print(cut)
    # print(kstar_cut_dict[cut])
    if(cut == 'no_cut'):
        pt_diff_array.append(df.Histo1D(('pt_diff_{}'.format(kstar_cut_dict[cut]), 'pt_diff_{}'.format(kstar_cut_dict[cut]), 100, -0.5, 0.5), 'pipkmks_p_pt_diff'))
        tslope_array.append(df.Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
    else:
        pt_diff_array.append(df.Filter(cut).Histo1D(('pt_diff_{}'.format(kstar_cut_dict[cut]), 'pt_diff_{}'.format(kstar_cut_dict[cut]), 100, -0.5, 0.5), 'pipkmks_p_pt_diff'))
        tslope_array.append(df.Filter(cut).Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
    
    histo_name = kstar_cut_dict[cut]

    for i in range(len(beam_df_array)):

        #TODO refactor this to filter on beam value instead of adding an entire array of dataframes
        beam = i + 5

        if(cut == "no_cut"):
            cut_df = beam_df_array[i]
        else:
            cut_df = beam_df_array[i].Filter(cut)
            
        for t in t_low:
            histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 50, 1.0, 1.7), 'pipkmks_m'))
            histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 100, 1.0, 2.5), 'pipkmks_m'))
            histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 200, 1.0, 3.8), 'pipkmks_m'))
        for t in t_med:
            histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 50, 1.0, 1.7), 'pipkmks_m'))
            histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 100, 1.0, 2.5), 'pipkmks_m'))
            histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 200, 1.0, 3.8), 'pipkmks_m'))
        for t in t_high:
            histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, histo_name), 50, 1.0, 1.7), 'pipkmks_m'))
            histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, histo_name), 100, 1.0, 2.5), 'pipkmks_m'))
            histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, histo_name), 200, 1.0, 3.8), 'pipkmks_m'))

print("histos done in {} seconds".format(time.time() - start_time))

## WRITE HISTOGRAMS TO FILE ##

target_file = ROOT.TFile(f"/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_result_{run_period_dict[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))

for histo in histo_array_low:
    histo.Write()
print("low t histos written in {} seconds".format(time.time() - start_time))
for histo in histo_array_med:
    histo.Write()
print("med t histos written in {} seconds".format(time.time() - start_time))
for histo in histo_array_high:
    histo.Write()
print("high t histos written in {} seconds".format(time.time() - start_time))

f1_nocut.Write()
f1_kstar_plus_cut.Write()
f1_kstar_zero_cut.Write()
f1_kstar_all_cut.Write()
f1_nocut_narrow.Write()
f1_nocut_medium.Write()
f1_nocut_wide.Write()
f1_kstar_plus_cut_narrow.Write()
f1_kstar_plus_cut_medium.Write()
f1_kstar_plus_cut_wide.Write()
f1_kstar_zero_cut_narrow.Write()
f1_kstar_zero_cut_medium.Write()
f1_kstar_zero_cut_wide.Write()
ks_m.Write()

for slope in tslope_array:
    slope.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close()
    
######################
## DEPRECIATED CODE ##
######################

# ks_no_pl = df.Filter(ks_cut2).Histo1D(('ks_no_pl', 'ks_no_pl', 100, 0.3, 0.7), 'ks_m')
# ks_all = df.Filter(ks_cut1).Filter(ks_cut2).Histo1D(('ks_all', 'ks_all', 100, 0.3, 0.7), 'ks_m')
# ks_none = df.Histo1D(('ks_none', 'ks_none', 100, 0.2, 0.8), 'ks_m')

#.Histo1D(('ks_pl', 'ks_pl', 100, 0.3, 0.7), 'ks_m')
# ks_pl = df.Filter(ks_pathlength_cut).Histo1D(('ks_pl', 'ks_pl', 400, 0.35, 0.7), 'ks_m')
# ks_no_pl = df.Filter(ks_cut1).Filter(ks_cut2).Histo1D(('ks_no_pl', 'ks_no_pl', 400, 0.35, 0.7), 'ks_m')
# ks_all = df.Filter(ks_cut1).Filter(ks_cut2).Filter(ks_pathlength_cut).Histo1D(('ks_all', 'ks_all', 400, 0.35, 0.7), 'ks_m')
# ks_none = df.Histo1D(('ks_none', 'ks_none', 400, 0.35, 0.7), 'ks_m')

# ks_pl.SetLineColor(4)
# ks_no_pl.SetLineColor(2)
# ks_all.SetLineColor(7)
# ks_none.SetLineColor(1)

# mx_all_hist = df.Histo1D(('mx_all', 'mx_all', 100, -0.5, 0.5), 'missing_m')
# mx_all_hist.Draw()

# df = df.Filter(kstar_all_cut)
# df = df.Filter(kstar_plus_cut)


# c1 = ROOT.TCanvas()
# f1_mass_range_none.Draw()
# f1_mass_range_kstar_zero_cut.Draw('same')
# f1_mass_range_kstar_plus_cut.Draw('same')
# f1_mass_range_all.Draw('same')
# # f1_nocut.Draw()
# # f1_kstar_plus_cut.Draw('same')
# # f1_kstar_zero_cut.Draw('same')
# # f1_kstar_all_cut.Draw('same')
# c1.Update()

# azero = df.Filter(f1_region).Histo1D(('azero', 'azero', 60, 0.6, 1.2), 'kmks_m')
# azero.Draw()



    # df_beam_5 = df.Filter('e_beam > 4.5 && e_beam <= 5.5')
    # df_beam_6 = df.Filter('e_beam > 5.5 && e_beam <= 6.5')
    # df_beam_7 = df.Filter('e_beam > 6.5 && e_beam <= 7.5')
    # df_beam_8 = df.Filter('e_beam > 7.5 && e_beam <= 8.5')
    # df_beam_9 = df.Filter('e_beam > 8.5 && e_beam <= 9.5')
    # df_beam_10 = df.Filter('e_beam > 9.5 && e_beam <= 10.5')

    # cut_df = df.Filter(cut)
    
            # histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}'.format(beam, t), 'pipkmks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pipkmks_m'))
            # histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}'.format(beam, t), 'pipkmks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pipkmks_m'))
            # histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}'.format(beam, t), 'pipkmks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pipkmks_m'))

# print(len(histo_array_low))
# c1 = ROOT.TCanvas("c1", "c1", 800, 600)
# c1.Divide(2, 2)

# for pt_hist in pt_diff_array:
#     c1.cd(pt_diff_array.index(pt_hist) + 1)
#     pt_hist.Draw()

# print("closing file")
# target_file.Close()

# c1.Update()