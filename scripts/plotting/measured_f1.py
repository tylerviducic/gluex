# script to check the f1 distribution using only measured quantities 

import ROOT
from common_analysis_tools import *

file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'data', filtered=False)

ks_mass_cut = f'abs(ks_m - {KSHORT_FIT_MEAN}) < 3*{KSHORT_FIT_WIDTH}'
ks_pathlength_cut = 'pathlength_sig > 5'
ppim_mass_cut = 'ppip_m > 1.4'
kmp_mass_cut = 'kmp_m > 1.95'
beam_range = 'e_beam >= 6.50000000000 && e_beam <= 10.5'
t_range = 'mand_t > 0.1 && mand_t <= 1.9'
p_p_cut = 'p_p_measured > 0.4'
mx2_ppipkmks_cut = 'abs(mx2_ppipkmks) < 0.01'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

# t_bin_cut


kstar_cut_dict = {
    'kspip_m > 0.0': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.75 || kspip_m > 1.0) && (kmpip_m < 0.75 || kmpip_m > 1.0)': 'kstar_all_cut'
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

ks_energy_fix = """
double fix_ks_energy(double ks_px, double ks_py, double ks_pz) {
    double pdg_ksm = 0.497611;
    double ks_p2 = ks_px*ks_px + ks_py*ks_py + ks_pz*ks_pz;
    double ks_E = sqrt(ks_p2 + pdg_ksm*pdg_ksm);
    return ks_E;
}
"""

ROOT.gInterpreter.Declare(t_bin_filter)
ROOT.gInterpreter.Declare(beam_bin_filter)
ROOT.gInterpreter.Declare(ks_energy_fix)

## LOAD IN DATA ##

df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

## DEFINE ALL NECESSARY COLUMNS ##

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')
df = df.Define('p_p_measured', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured + p_pz_measured*p_pz_measured)')

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
df = df.Define('ks_E_fixed', 'fix_ks_energy(ks_px, ks_py, ks_pz)')
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")
df = df.Define('ks_m_fixed', 'sqrt(ks_E_fixed*ks_E_fixed - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)')

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
df = df.Define('pipkmks_E_fixed', 'pip1_E + km_E + ks_E_fixed')
df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')
df = df.Define('pipkmks_m_fixed', 'sqrt(pipkmks_E_fixed*pipkmks_E_fixed - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

df = df.Define('pipkmks_px_measured', "pip1_px_measured + km_px_measured + ks_px_measured")
df = df.Define('pipkmks_py_measured', "pip1_py_measured + km_py_measured + ks_py_measured")
df = df.Define('pipkmks_pz_measured', "pip1_pz_measured + km_pz_measured + ks_pz_measured")
df = df.Define('pipkmks_E_measured', "pip1_E_measured + km_E_measured + ks_E_measured")
df = df.Define('pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')
df = df.Define('pipkmks_m_measured', "sqrt(pipkmks_E_measured*pipkmks_E_measured - pipkmks_px_measured*pipkmks_px_measured - pipkmks_py_measured*pipkmks_py_measured - pipkmks_pz_measured*pipkmks_pz_measured)")

df = df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')

df = df.Define('kmks_px', 'km_px + ks_px')
df = df.Define('kmks_py', 'km_py + ks_py')
df = df.Define('kmks_pz', 'km_pz + ks_pz')
df = df.Define('kmks_E', 'km_E + ks_E')
df = df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')\

df = df.Define('e_bin', 'get_beam_bin_index(e_beam)')
df = df.Define('t_bin', 'get_t_bin_index(mand_t)')

hist_mx_all = df.Histo1D(('mx2_ppipkmks', 'mx2_ppipkmks', 500, -0.05, 0.05), 'mx2_ppipkmks')

## FILTER DATAFRAME AFTER DATA IS DEFINED ##
df = df.Filter(mx2_ppipkmks_cut).Filter(ks_pathlength_cut).Filter(ppim_mass_cut).Filter(kmp_mass_cut).Filter(p_p_cut).Filter(kstar_all_cut).Filter(ks_mass_cut).Filter(beam_range).Filter(t_range)

hist_pipkmks_measured = df.Histo1D(('pipkmks_measured', 'pipkmks_measured', 110, 1.1, 2.2), 'pipkmks_m_measured')
hist_pipkmks = df.Histo1D(('pipkmks', 'pipkmks', 110, 1.1, 2.2), 'pipkmks_m')
hist_pipkmks_fixed = df.Histo1D(('pipkmks_fixed', 'pipkmks_fixed', 110, 1.1, 2.2), 'pipkmks_m_fixed')
hist_pipkmks_fixed.SetLineColor(ROOT.kBlack)
hist_pipkmks.SetLineColor(ROOT.kRed)

hist_pipkmks_fixed2 = df.Filter('t_bin == 2').Histo1D(('pipkmks_fixed2', 'pipkmks_fixed2', 110, 1.1, 2.2), 'pipkmks_m_fixed')
hist_pipkmks_fixed3 = df.Filter('t_bin == 3').Histo1D(('pipkmks_fixed3', 'pipkmks_fixed3', 110, 1.1, 2.2), 'pipkmks_m_fixed')
hist_pipkmks_fixed4 = df.Filter('t_bin == 4').Histo1D(('pipkmks_fixed4', 'pipkmks_fixed4', 110, 1.1, 2.2), 'pipkmks_m_fixed')
hist_pipkmks_fixed5 = df.Filter('t_bin == 4').Histo1D(('pipkmks_fixed5', 'pipkmks_fixed5', 110, 1.1, 2.2), 'pipkmks_m_fixed')

c1 = ROOT.TCanvas("c1", "c1", 800, 600)

c1.Divide(2,2)
c1.cd(1)
hist_pipkmks_fixed2.Draw()
# hist_mx_all.Draw()
c1.cd(2)
# hist_pipkmks_fixed.Draw()
# hist_pipkmks_measured.Draw('same')
# hist_pipkmks.Draw('same')
hist_pipkmks_fixed3.Draw()
c1.cd(3)
hist_pipkmks_fixed4.Draw()
c1.cd(4)
hist_pipkmks_fixed5.Draw()

c1.Update()

input("Press Enter to continue...")