# script for making histograms from flat best chi2/ndf trees

import ROOT
import time
import os
from common_analysis_tools import *


filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_unconstrained.root'
treename = 'pipkmks__ks_pippim__B4_M16'


ks_pathlength_cut = 'pathlength_sig > 5'
ks_cut1 = 'cos_colin > 0.99'
ks_cut2 = ' vertex_distance > 3'
# ks_mass_cut = 'ks_m > 0.475 && ks_m < 0.525'
ks_mass_cut = f'abs(ks_m - {KSHORT_FIT_MEAN}) < {2 * KSHORT_FIT_WIDTH}'
ppim_mass_cut = 'ppip_m > 1.4'
kmp_mass_cut = 'kmp_m > 1.95'
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'
beam_range = 'e_beam >= 6.50000000000 && e_beam <= 10.5'
t_range = 'mand_t <= 1.9'
p_p_cut = 'p_p > 0.4'
mx2_ppipkmks_cut = 'abs(mx2_ppipkmks) < 0.01'

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

df = df.Filter(mx2_ppipkmks_cut).Filter(ks_pathlength_cut).Filter(ks_mass_cut).Filter(ppim_mass_cut).Filter(kmp_mass_cut).Filter(p_p_cut)

## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')

## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
# df.Snapshot(f'pipkmks_filtered_{run_dict[run_period]}', f'/w/halld-scshelf2101/home/viducic/data/pipkmks/data/bestX2/pipkmks_filtered_{run_dict[run_period]}.root')


## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
# df = df.Filter(beam_range).Filter(t_range)
 
hist_pipkmks_nocut = df.Histo1D(('pipkmks_nocut', 'pipkmks_nocut', 100, 1.0, 2.0), 'pipkmks_m')
hist_pipkmks_nocut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_pipkmks_kpcut = df.Filter(KSTAR_PLUS_CUT).Histo1D(('pipkmks_kpcut', 'pipkmks_kpcut', 100, 1.0, 2.0), 'pipkmks_m')
hist_pipkmks_kpcut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_pipkmks_kzcut = df.Filter(KSTAR_ZERO_CUT).Histo1D(('pipkmks_kzcut', 'pipkmks_kzcut', 100, 1.0, 2.0), 'pipkmks_m')
hist_pipkmks_kzcut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
hist_pipkmks_allcut = df.Filter(KSTAR_ALL_CUT).Histo1D(('pipkmks_allcut', 'pipkmks_allcut', 100, 1.0, 2.0), 'pipkmks_m')
hist_pipkmks_allcut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['orange']))

c = ROOT.TCanvas('c', 'c', 900, 900)
hist_pipkmks_nocut.Draw()
hist_pipkmks_kpcut.Draw("same")
hist_pipkmks_kzcut.Draw("same")
hist_pipkmks_allcut.Draw("same")
c.Update()

c2 = ROOT.TCanvas('c2', 'c2', 900, 900)
c2.cd()
hist_ks = df.Histo1D(('ks_measured', 'ks_measured', 100, 0.3, 0.7), 'ks_m_measured')
hist_ks.Draw()
c2.Update()

input('Press enter to continue...')