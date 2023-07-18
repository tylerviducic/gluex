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
    raise ValueError('Invalid run period')

filename = f'/w/halld-scshelf2101/home/viducic/data/pimkpks/data/bestX2/pimkpks_flat_bestX2_{RUN_DICT[run_period]}.root'
treename = 'pimkpks__B4_M16'

if run_period == '2019_unconstrained':
    treename = 'pimkpks__T1_S2_M16'
elif run_period == '2019_constrained':
    treename = 'pimkpks__T1_S2'

histo_array = []

ROOT.gInterpreter.Declare(T_BIN_FILTER)
ROOT.gInterpreter.Declare(BEAM_BIN_FILTER)

## LOAD IN DATA ##

df = ROOT.RDataFrame(treename, filename)

## DEFINE ALL NECESSARY COLUMNS ##

# print(df.GetColumnNames())

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

df = df.Define('ks_px', "pim2_px + pip_px")
df = df.Define('ks_py', "pim2_py + pip_py")
df = df.Define('ks_pz', "pim2_pz + pip_pz")
df = df.Define('ks_E', "pim2_E + pip_E")
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

df = df.Define('ks_px_measured', "pim2_px_measured + pip_px_measured")
df = df.Define('ks_py_measured', "pim2_py_measured + pip_py_measured")
df = df.Define('ks_pz_measured', "pim2_pz_measured + pip_pz_measured")
df = df.Define('ks_E_measured', "pim2_E_measured + pip_E_measured")
df = df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

df = df.Define('mxpx_ppimkpks', '-p_px_measured - pim1_px_measured - kp_px_measured - ks_px_measured')
df = df.Define('mxpy_ppimkpks', '-p_py_measured - pim1_py_measured - kp_py_measured - ks_py_measured')
df = df.Define('mxpz_ppimkpks', 'e_beam - p_pz_measured - pim1_pz_measured - kp_pz_measured - ks_pz_measured')
df = df.Define('mxe_ppimkpks', 'e_beam + 0.938272088 - p_E_measured - pim1_E_measured - kp_E_measured - ks_E_measured')
df = df.Define('mx2_ppimkpks', 'mxe_ppimkpks*mxe_ppimkpks - mxpx_ppimkpks*mxpx_ppimkpks - mxpy_ppimkpks*mxpy_ppimkpks - mxpz_ppimkpks*mxpz_ppimkpks')

df = df.Define('ppim_px', 'pim1_px + p_px')
df = df.Define('ppim_py', 'pim1_py + p_py')
df = df.Define('ppim_pz', 'pim1_pz + p_pz')
df = df.Define('ppim_E', 'pim1_E + p_E')
df = df.Define('ppim_m', 'sqrt(ppim_E*ppim_E - ppim_px*ppim_px - ppim_py*ppim_py - ppim_pz*ppim_pz)')


df = df.Define('missing_px', '-p_px - pim1_px - ks_px - kp_px')
df = df.Define('missing_py', '-p_py - pim1_py - ks_py - kp_py')
df = df.Define('missing_pz', 'e_beam - p_pz - pim1_pz - ks_pz - kp_pz')
df = df.Define('missing_E', 'e_beam + 0.938 - p_E - pim1_E - ks_E - kp_E')

df = df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

df = df.Define('kpp_px', 'p_px + kp_px')
df = df.Define('kpp_py', 'p_py + kp_py')
df = df.Define('kpp_pz', 'p_pz + kp_pz')
df = df.Define('kpp_E', 'p_E + kp_E')

df = df.Define('kpp_m', 'sqrt(kpp_E*kpp_E - kpp_px*kpp_px - kpp_py*kpp_py - kpp_pz*kpp_pz)')

df = df.Define('ksp_px', 'p_px + ks_px')
df = df.Define('ksp_py', 'p_py + ks_py')
df = df.Define('ksp_pz', 'p_pz + ks_pz')
df = df.Define('ksp_E', 'p_E + ks_E')

df = df.Define('ksp_m', 'sqrt(ksp_E*ksp_E - ksp_px*ksp_px - ksp_py*ksp_py - ksp_pz*ksp_pz)')

df = df.Define('kspim_px', 'pim1_px + ks_px')
df = df.Define('kspim_py', 'pim1_py + ks_py')
df = df.Define('kspim_pz', 'pim1_pz + ks_pz')
df = df.Define('kspim_E', 'pim1_E + ks_E')

df = df.Define('kspim_m', 'sqrt(kspim_E*kspim_E - kspim_px*kspim_px - kspim_py*kspim_py - kspim_pz*kspim_pz)')

df = df.Define('kppim_px', 'pim1_px + kp_px')
df = df.Define('kppim_py', 'pim1_py + kp_py')
df = df.Define('kppim_pz', 'pim1_pz + kp_pz')
df = df.Define('kppim_E', 'pim1_E + kp_E')

df = df.Define('kppim_m', 'sqrt(kppim_E*kppim_E - kppim_px*kppim_px - kppim_py*kppim_py - kppim_pz*kppim_pz)')

df = df.Define('pimkpks_px', 'pim1_px + kp_px + ks_px')
df = df.Define('pimkpks_py', 'pim1_py + kp_py + ks_py')
df = df.Define('pimkpks_pz', 'pim1_pz + kp_pz + ks_pz')
df = df.Define('pimkpks_E', 'pim1_E + kp_E + ks_E')

df = df.Define('pimkpks_px_measured', "pim1_px_measured + kp_px_measured + ks_px_measured")
df = df.Define('pimkpks_py_measured', "pim1_py_measured + kp_py_measured + ks_py_measured")
df = df.Define('pimkpks_pz_measured', "pim1_pz_measured + kp_pz_measured + ks_pz_measured")
df = df.Define('pimkpks_pt', 'sqrt(pimkpks_px_measured*pimkpks_px_measured + pimkpks_py_measured*pimkpks_py_measured)')

df = df.Define('pimkpks_p_pt_diff', 'pimkpks_pt - p_pt')

df = df.Define('pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')

df = df.Define('kpks_px', 'kp_px + ks_px')
df = df.Define('kpks_py', 'kp_py + ks_py')
df = df.Define('kpks_pz', 'kp_pz + ks_pz')
df = df.Define('kpks_E', 'kp_E + ks_E')
df = df.Define('kpks_m', 'sqrt(kpks_E*kpks_E - kpks_px*kpks_px - kpks_py*kpks_py - kpks_pz*kpks_pz)')

df = df.Define('e_bin', 'get_beam_bin_index(e_beam)')
df = df.Define('t_bin', 'get_t_bin_index(mand_t)')

df = df.Define('ppip_px', 'p_px + pip_px')
df = df.Define('ppip_py', 'p_py + pip_py')
df = df.Define('ppip_pz', 'p_pz + pip_pz')
df = df.Define('ppip_E', 'p_E + pip_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')


## FILTER DATAFRAME AFTER DATA IS DEFINED ##

df = df.Filter(MX2_PPIMKPKS_CUT).Filter(KS_PATHLENGTH_CUT).Filter(KS_MASS_CUT).Filter(PPIM_MASS_CUT).Filter(KSP_MASS_CUT).Filter(P_P_CUT)
print('cuts done in {} seconds'.format(time.time() - start_time))


## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')

## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
df.Snapshot(f'pimkpks_filtered_{RUN_DICT[run_period]}', f'/w/halld-scshelf2101/home/viducic/data/pimkpks/data/bestX2/pimkpks_filtered_{RUN_DICT[run_period]}.root')


# ## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
df = df.Filter(BEAM_RANGE).Filter(T_RANGE)

print('cut file written in {} seconds'.format(time.time() - start_time))

## LOOP OVER K* CUTS AND EXECUTE HISTO FILLING FUNCTION ##

n_e_bins = len(ALLOWED_E_BINS)
n_t_bins = len(ALLOWED_T_BINS)

def fill_histos(cut_df, histo_array, cut, beam_index=0, t_index=0):
    cut_name = KSTAR_CUT_NAME_DICT_PIMKPKS[cut]
    hist_name = f'pimkpks_kstar_{cut_name}_cut_'
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
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 150, 1.0, 2.5), 'pimkpks_m'))

    

for cut in F1_CUT_LIST_PIMKPKS:
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

target_file = ROOT.TFile(f"/w/halld-scshelf2101/home/viducic/data/pimkpks/data/bestX2/pimkpks_flat_result_{RUN_DICT[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))


ks_m.Write()

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close()

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/pimkpks_graph_{RUN_DICT[run_period]}.dot")
    
######################
## DEPRECIATED CODE ##
######################


# hist_ks_before = df.Histo1D(('ks_m_before', 'ks_m_before', 100, 0.3, 0.7), 'ks_m')
# hist_ks_after = df.Filter(KS_PATHLENGTH_CUT).Histo1D(('ks_m_after', 'ks_m_after', 100, 0.3, 0.7), 'ks_m')
# hist_ks_before.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
# hist_ks_after.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))

# c = ROOT.TCanvas('c', 'c', 900, 900)
# hist_ks_before.Draw()
# hist_ks_after.Draw('same')
# c.Update()


# hist_mx_all = df.Histo1D(('mx_all', 'mx_all', 100, -0.05, 0.05), 'mx2_ppimkpks')
# hist_mx_all.Draw()


# c = ROOT.TCanvas('c', 'c', 500, 500)
# c.Divide(2,1)
# c.cd(1)
# hist_ppip = df.Histo1D(('ppip_m', 'ppip_m', 100, 1.0, 2.5), 'ppip_m')
# hist_ppip.Draw()
# c.cd(2)
# hist_ppim = df.Histo1D(('ppim_m', 'ppim_m', 100, 1.0, 2.5), 'ppim_m')
# hist_ppim.Draw()
# c.Update()


# hist_kpp = df.Histo1D(('kpp_m', 'kpp_m', 150, 1.3, 3.0), 'kpp_m')
# hist_kpp.Draw()

# hist_pks = df.Histo1D(('pks_m', 'pks_m', 200, 1.3, 3.0), 'ksp_m')
# hist_pks.Draw()

# hist_kspim = df.Histo1D(('kspim_m', 'kspim_m', 150, 0.5, 2.0), 'kspim_m')
# hist_kppim = df.Histo1D(('kppim_m', 'kppim_m', 150, 0.5, 2.0), 'kppim_m')

# c = ROOT.TCanvas()
# c.Divide(2,1)
# c.cd(1)
# hist_kspim.Draw()
# c.cd(2)
# hist_kppim.Draw()
# c.Update()

# hist_kkpi_nocuts = df.Histo1D(('kkpi_nocuts', 'kkpi_nocuts', 100, 1.1, 1.7), 'pimkpks_m')
# hist_kkpi_nocuts.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
# hist_kkpi_kstar_minus_cut = df.Filter(KSTAR_MINUS_CUT).Histo1D(('kkpi_kstar_minus_cut', 'kkpi_kstar_minus_cut', 100, 1.1, 1.7), 'pimkpks_m')
# hist_kkpi_kstar_minus_cut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
# hist_kkpi_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('kkpi_kstar_zero_cut', 'kkpi_kstar_zero_cut', 100, 1.1, 1.7), 'pimkpks_m')
# hist_kkpi_kstar_zero_cut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
# hist_kkpi_kstar_all_cut = df.Filter(kstar_all_cut).Histo1D(('kkpi_kstar_all_cut', 'kkpi_kstar_all_cut', 100, 1.1, 1.7), 'pimkpks_m')
# hist_kkpi_kstar_all_cut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['purple']))

# c1 = ROOT.TCanvas('c1', 'c1', 800, 600)
# hist_kkpi_nocuts.Draw()
# hist_kkpi_kstar_minus_cut.Draw('same')
# hist_kkpi_kstar_zero_cut.Draw('same')
# hist_kkpi_kstar_all_cut.Draw('same')
# c1.Update()

# input('Press any key to continue...')
