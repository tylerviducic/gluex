# script for making histograms from flat best chi2/ndf trees

import ROOT
import time
import os
from common_analysis_tools import *
import sys 


os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

start_time = time.time()


run_period = sys.argv[1]

if run_period not in ALLOWED_RUN_PERIODS:
    if run_period not in ['2019_unconstrained', '2019_constrained']:
        raise ValueError('Invalid run period')


filename = f'/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_{RUN_DICT[run_period]}.root'
treename = 'pipkmks__B4_M16'

if run_period == '2019_unconstrained':
    treename = 'pipkmks__T1_S2_M16'
elif run_period == '2019_constrained':
    treename = 'pipkmks__T1_S2'

histo_array = []

## DEFINE CUTS ##
#TODO cuts to use NUMBA

ROOT.gInterpreter.Declare(T_BIN_FILTER)
ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)

## LOAD IN DATA ##

df = ROOT.RDataFrame(treename, filename)

## DEFINE ALL NECESSARY COLUMNS ##

# print(df.GetColumnNames())

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

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

df = df.Define('mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
df = df.Define('mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
df = df.Define('mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
df = df.Define('mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
df = df.Define('mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')

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

df = df.Define('e_bin', 'get_beam_bin_index(e_beam)')
df = df.Define('t_bin', 'get_t_bin_index(mand_t)')


## FILTER DATAFRAME AFTER DATA IS DEFINED ##

df = df.Filter(MX2_PPIPKMKS_CUT).Filter(KS_PATHLENGTH_CUT).Filter(KS_MASS_CUT).Filter(PPIP_MASS_CUT).Filter(KMP_MASS_CUT).Filter(P_P_CUT)
print('cuts done in {} seconds'.format(time.time() - start_time))



## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')

## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
df.Snapshot(f'pipkmks_filtered_{RUN_DICT[run_period]}', f'/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_filtered_{RUN_DICT[run_period]}.root')


## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
df = df.Filter(BEAM_RANGE).Filter(T_RANGE)

print('cut file written in {} seconds'.format(time.time() - start_time))
 

## LOOP OVER K* CUTS AND EXECUTE HISTO FILLING FUNCTION ##

n_e_bins = len(ALLOWED_E_BINS)
n_t_bins = len(ALLOWED_T_BINS)

def fill_histos(cut_df, histo_array, cut, beam_index=0, t_index=0):
    cut_name = KSTAR_CUT_NAME_DICT_PIPKMKS[cut]
    hist_name = f'pipkmks_cut_{cut_name}_'
    beam_name = 'beam_full_'
    t_name = 't_full'
    if beam_index > 0:
        beam_low = BEAM_CUT_DICT[beam_index][0]
        beam_high = BEAM_CUT_DICT[beam_index][1]
        beam_name = f'beam_{beam_low}_{beam_high}_'
    if t_index > 0:
        t_low = T_CUT_DICT[t_index][0]
        t_high = T_CUT_DICT[t_index][1]
        t_name = f't_{t_low}_{t_high}'
    hist_name += beam_name + t_name
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 150, 1.0, 2.5), 'pipkmks_m'))

for cut in F1_CUT_LIST_PIPKMKS:
    cut_df = df.Filter(cut)
    fill_histos(cut_df, histo_array, cut)
        

    for energy_index in range(1, n_e_bins+1):
        e_cut_df = cut_df.Filter(f'e_bin == {energy_index}')
        fill_histos(e_cut_df, histo_array, cut, beam_index=energy_index)

        for t_index in range(1, n_t_bins+1):
            e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
            fill_histos(e_t_cut_df, histo_array, cut, beam_index=energy_index, t_index=t_index)
         
    for t_index in range(1, n_t_bins+1):
       t_cut_df = cut_df.Filter(f't_bin == {t_index}')
       fill_histos(t_cut_df, histo_array, cut, t_index=t_index)

print("histos done in {} seconds".format(time.time() - start_time))

## WRITE HISTOGRAMS TO FILE ##

target_file = ROOT.TFile(f"/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_result_{RUN_DICT[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))


ks_m.Write()

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close()

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/pipkmks_graph_{RUN_DICT[run_period]}.dot")
    
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

    # for i in range(len(beam_df_array)):

    #     beam = i + 5

    #     if(cut == "no_cut"):
    #         cut_df = beam_df_array[i]
    #     else:
    #         cut_df = beam_df_array[i].Filter(cut)
            
    #     for t in t_low:
    #         histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
    #         histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
    #         histo_array_low.append(cut_df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))
    #     for t in t_med:
    #         histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
    #         histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
    #         histo_array_med.append(cut_df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))
    #     for t in t_high:
    #         histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_narrow'.format(beam, t, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
    #         histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_medium'.format(beam, t, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
    #         histo_array_high.append(cut_df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 'pipkmks_beam_{}_t_{}_{}_wide'.format(beam, t, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))

# for histo in histo_array_low:
#     histo.Write()
# print("low t histos written in {} seconds".format(time.time() - start_time))
# for histo in histo_array_med:
#     histo.Write()
# print("med t histos written in {} seconds".format(time.time() - start_time))
# for histo in histo_array_high:
#     histo.Write()
# print("high t histos written in {} seconds".format(time.time() - start_time))

# f1_nocut = df.Histo1D(('f1_nocut', 'f1_nocut', 50, 1.0, 1.7), 'pipkmks_m')
# f1_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut', 'f1_kstar_plus_cut', 50, 1.0, 1.7), 'pipkmks_m')
# f1_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut', 'f1_kstar_zero_cut', 50, 1.0, 1.7), 'pipkmks_m')
# f1_kstar_all_cut = df.Filter(kstar_all_cut).Histo1D(('f1_kstar_all_cut', 'f1_kstar_all_cut', 50, 1.0, 1.7), 'pipkmks_m')

# f1_mass_range_all = df.Filter(kstar_all_cut).Histo1D(('massrange_all', 'massrange_all', 200, 1.0, 4.0), 'pipkmks_m')
# f1_mass_range_none = df.Histo1D(('massrange_none', 'massrange_none', 200, 1.0, 4.0), 'pipkmks_m')
# f1_mass_range_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('massrange_kstar_zero_cut', 'massrange_kstar_zero_cut', 200, 1.0, 4.0), 'pipkmks_m')
# f1_mass_range_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('massrange_kstar_plus_cut', 'massrange_kstar_plus_cut', 200, 1.0, 4.0), 'pipkmks_m')

# f1_nocut_narrow = df.Histo1D(('f1_nocut_narrow', 'f1_nocut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
# f1_nocut_medium = df.Histo1D(('f1_nocut_medium', 'f1_nocut_medium', 100, 1.0, 2.5), 'pipkmks_m')
# f1_nocut_wide = df.Histo1D(('f1_nocut_wide', 'f1_nocut_wide', 200, 1.0, 3.8), 'pipkmks_m')

# f1_kstar_plus_cut_narrow = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_narrow', 'f1_kstar_plus_cut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
# f1_kstar_plus_cut_medium = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_medium', 'f1_kstar_plus_cut_medium', 100, 1.0, 2.5), 'pipkmks_m')
# f1_kstar_plus_cut_wide = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut_wide', 'f1_kstar_plus_cut_wide', 200, 1.0, 3.8), 'pipkmks_m')

# f1_kstar_zero_cut_narrow = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_narrow', 'f1_kstar_zero_cut_narrow', 50, 1.0, 1.7), 'pipkmks_m')
# f1_kstar_zero_cut_medium = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_medium', 'f1_kstar_zero_cut_medium', 100, 1.0, 2.5), 'pipkmks_m')
# f1_kstar_zero_cut_wide = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut_wide', 'f1_kstar_zero_cut_wide', 200, 1.0, 3.8), 'pipkmks_m')

# f1_mass_range_all.SetLineColor(1)
# f1_mass_range_none.SetLineColor(2)
# f1_mass_range_kstar_zero_cut.SetLineColor(6)
# f1_mass_range_kstar_plus_cut.SetLineColor(4)

# f1_nocut.SetLineColor(1)
# f1_kstar_plus_cut.SetLineColor(2)
# f1_kstar_zero_cut.SetLineColor(6)
# f1_kstar_all_cut.SetLineColor(4)

# f1_nocut.Write()
# f1_kstar_plus_cut.Write()
# f1_kstar_zero_cut.Write()
# f1_kstar_all_cut.Write()
# f1_nocut_narrow.Write()
# f1_nocut_medium.Write()
# f1_nocut_wide.Write()
# f1_kstar_plus_cut_narrow.Write()
# f1_kstar_plus_cut_medium.Write()
# f1_kstar_plus_cut_wide.Write()
# f1_kstar_zero_cut_narrow.Write()
# f1_kstar_zero_cut_medium.Write()
# f1_kstar_zero_cut_wide.Write()

    # if(cut == 'no_cut'):
    #     pt_diff_array.append(df.Histo1D(('pt_diff_{}'.format(kstar_cut_dict[cut]), 'pt_diff_{}'.format(kstar_cut_dict[cut]), 100, -0.5, 0.5), 'pipkmks_p_pt_diff'))
    #     tslope_array.append(df.Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))

    # else:
    #     pt_diff_array.append(df.Filter(cut).Histo1D(('pt_diff_{}'.format(kstar_cut_dict[cut]), 'pt_diff_{}'.format(kstar_cut_dict[cut]), 100, -0.5, 0.5), 'pipkmks_p_pt_diff'))
    #     tslope_array.append(df.Filter(cut).Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))

        # beam_low = beam_dict[beam_index][0]
        # beam_high = beam_dict[beam_index][1]
        # histo_array.append(df.Filter(f'e_bin == {beam_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
        # histo_array.append(df.Filter(f'e_bin == {beam_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
        # histo_array.append(df.Filter(f'e_bin == {beam_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))

                # for t_index in range(1, 9):
        #     t_low = t_dict[t_index][0]
        #     t_high = t_dict[t_index][1]
        #     cut_df = cut_df.Filter(f't_bin == {t_index}')
        #     histo_array.append(cut_df.Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 50, 1.0, 1.7), 'pipkmks_m'))
        #     histo_array.append(cut_df.Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 100, 1.0, 2.5), 'pipkmks_m'))
        #     histo_array.append(cut_df.Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 200, 1.0, 3.8), 'pipkmks_m'))

# pt_diff_array = []
# tslope_array = []

#for slope in tslope_array:
    # slope.Write()

    # def fill_and_store_histograms(hlist, filtered_df, n_e_bins, n_t_bins, cut):
#         cut_name = kstar_cut_dict[cut]
        
#         hlist.append(filtered_df.Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))

#         for energy_index in range(1, n_e_bins+1):
#             beam_low = beam_dict[energy_index][0]
#             beam_high = beam_dict[energy_index][1]
#             hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('tslope_{}_beam_{}-{}'.format(kstar_cut_dict[cut], beam_low, beam_high), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
#             hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
#             hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
#             hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))


#             for t_index in range(1, n_t_bins+1):
#                 t_low = t_dict[t_index][0]
#                 t_high = t_dict[t_index][1]
#                 histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 50, 1.0, 1.7), 'pipkmks_m'))
#                 histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 100, 1.0, 2.5), 'pipkmks_m'))
#                 histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 200, 1.0, 3.8), 'pipkmks_m'))

#         return hlist

# df = df.Filter(ks_mass_cut)
# print('cut 2 done in {} seconds'.format(time.time() - start_time))
# df = df.Filter(ppim_mass_cut)
# print("cut 3 done in {} seconds".format(time.time() - start_time))
# df = df.Filter(kmp_mass_cut)
# print("cut 4 done in {} seconds".format(time.time() - start_time))

    # histo_array = fill_and_store_histograms(histo_array, df.Filter(cut), 4, 8, cut=cut)

    # histo_array.append(df.Filter(cut).Histo1D(('pipkmks_fullbeam_cut_{}_full_t_narrow'.format(cut_name), 'pipkmks_fullbeam_cut_{}_full_t_narrow'.format(cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
#     histo_array.append(df.Filter(cut).Histo1D(('pipkmks_fullbeam_cut_{}_full_t_narrow_measured'.format(cut_name), 'pipkmks_fullbeam_cut_{}_full_t_narrow_measured'.format(cut_name), 200, 1.0, 3.8), 'pipkmks_m'))
#     histo_array.append(df.Filter(cut).Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
#  histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Histo1D(('tslope_{}_beam_{}-{}'.format(kstar_cut_dict[cut], beam_low, beam_high), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
#         histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
#         histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))
#  histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 50, 1.0, 1.7), 'pipkmks_m'))
#             histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 200, 1.0, 3.8), 'pipkmks_m'))
#  histo_array.append(df.Filter(cut).Filter(f't_bin == {t_index}').Histo1D(('pipkmks_fullbeam_cut_{}_t_{}-{}_narrow'.format(cut_name, t_low, t_high), 'pipkmks_fullbeam_cut_{}_t_{}-{}_narrow'.format(cut_name, t_low, t_high), 50, 1.0, 1.7), 'pipkmks_m'))
#         histo_array.append(df.Filter(cut).Filter(f't_bin == {t_index}').Histo1D(('pipkmks_fullbeam_cut_{}_t_{}-{}_wide'.format(cut_name, t_low, t_high), 'pipkmks_fullbeam_cut_{}_t_{}-{}_wide'.format(cut_name, t_low, t_high), 200, 1.0, 3.8), 'pipkmks_m'))

        # t_low = t_dict[t_index][0]
    # cut_name = kstar_cut_dict[cut]
    # histo_array.append(df.Filter(cut).Histo1D(('pipkmks_fullbeam_cut_{}_full_t_medium'.format(cut_name), 'pipkmks_fullbeam_cut_{}_full_t_medium'.format(cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
        # beam_low = beam_dict[energy_index][0]
        # beam_high = beam_dict[energy_index][1]
        # histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
            # t_low = t_dict[t_index][0]
            # t_high = t_dict[t_index][1]
            # histo_array.append(df.Filter(cut).Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 100, 1.0, 2.5), 'pipkmks_m'))
        # t_high = t_dict[t_index][1]
        # histo_array.append(df.Filter(cut).Filter(f't_bin == {t_index}').Histo1D(('pipkmks_fullbeam_cut_{}_t_{}-{}_medium'.format(cut_name, t_low, t_high), 'pipkmks_fullbeam_cut_{}_t_{}-{}_medium'.format(cut_name, t_low, t_high), 100, 1.0, 2.5), 'pipkmks_m'))