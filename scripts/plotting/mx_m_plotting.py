# script for checking the mx values for moskov 

import ROOT
from common_analysis_tools import *
import os

os.nice(18)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)

file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'data', filtered=False)
df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])


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

df = df.Define('p_m_measured', "sqrt(p_E_measured*p_E_measured - p_px_measured*p_px_measured - p_py_measured*p_py_measured - p_pz_measured*p_pz_measured)")

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
df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

df = df.Define('pipkmks_px_measured', "pip1_px_measured + km_px_measured + ks_px_measured")
df = df.Define('pipkmks_py_measured', "pip1_py_measured + km_py_measured + ks_py_measured")
df = df.Define('pipkmks_pz_measured', "pip1_pz_measured + km_pz_measured + ks_pz_measured")
df = df.Define('pipkmks_E_measured', "pip1_E_measured + km_E_measured + ks_E_measured")
df = df.Define('pipkmks_m_measured', "sqrt(pipkmks_E_measured*pipkmks_E_measured - pipkmks_px_measured*pipkmks_px_measured - pipkmks_py_measured*pipkmks_py_measured - pipkmks_pz_measured*pipkmks_pz_measured)")
df = df.Define('pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')

df = df.Define('mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
df = df.Define('mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
df = df.Define('mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
df = df.Define('mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
df = df.Define('mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

df = df.Define('ppip_px', 'pip1_px + p_px')
df = df.Define('ppip_py', 'pip1_py + p_py')
df = df.Define('ppip_pz', 'pip1_pz + p_pz')
df = df.Define('ppip_E', 'pip1_E + p_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')

df = df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')

df = df.Define('kmks_px', 'km_px + ks_px')
df = df.Define('kmks_py', 'km_py + ks_py')
df = df.Define('kmks_pz', 'km_pz + ks_pz')
df = df.Define('kmks_E', 'km_E + ks_E')
df = df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')

# df = df.Define('e_bin', 'get_beam_bin_index(e_beam)')
# df = df.Define('t_bin', 'get_t_bin_index(mand_t)')

df = df.Define('mx_f1_px', "-pip1_px_measured - ks_px_measured - km_px_measured")
df = df.Define('mx_f1_py', "-pip1_py_measured - ks_py_measured - km_py_measured")
df = df.Define('mx_f1_pz', "e_beam - pip1_pz_measured - ks_pz_measured - km_pz_measured")
df = df.Define('mx_f1_E', "e_beam + 0.938272088 - pip1_E_measured - ks_E_measured - km_E_measured")
df = df.Define('mx_f1_m', "sqrt(mx_f1_E*mx_f1_E - mx_f1_px*mx_f1_px - mx_f1_py*mx_f1_py - mx_f1_pz*mx_f1_pz)")

df = df.Define('mx_p_px', "-p_px_measured")
df = df.Define('mx_p_py', "-p_py_measured")
df = df.Define('mx_p_pz', "e_beam - p_pz_measured")
df = df.Define('mx_p_E', "e_beam + 0.938272088 - p_E_measured")
df = df.Define('mx_p_m', "sqrt(mx_p_E*mx_p_E - mx_p_px*mx_p_px - mx_p_py*mx_p_py - mx_p_pz*mx_p_pz)")

df = df.Define('mx_delta_px', '-km_px - ks_px')
df = df.Define('mx_delta_py', '-km_py - ks_py')
df = df.Define('mx_delta_pz', 'e_beam - km_pz - ks_pz')
df = df.Define('mx_delta_E', 'e_beam + 0.938272088 - km_E - ks_E')
df = df.Define('mx_delta_m', 'sqrt(mx_delta_E*mx_delta_E - mx_delta_px*mx_delta_px - mx_delta_py*mx_delta_py - mx_delta_pz*mx_delta_pz)')

df = df.Define('mx_ppipkm_px', "-p_px_measured -pip1_px_measured - km_px_measured")
df = df.Define('mx_ppipkm_py', "-p_py_measured -pip1_py_measured - km_py_measured")
df = df.Define('mx_ppipkm_pz', "e_beam - p_pz_measured -pip1_pz_measured - km_pz_measured")
df = df.Define('mx_ppipkm_E', "e_beam + 0.938272088 - p_E_measured -pip1_E_measured - km_E_measured")
df = df.Define('mx_ppipkm_m', "sqrt(mx_ppipkm_E*mx_ppipkm_E - mx_ppipkm_px*mx_ppipkm_px - mx_ppipkm_py*mx_ppipkm_py - mx_ppipkm_pz*mx_ppipkm_pz)")

df_missing = df.Filter(KS_PATHLENGTH_CUT).Filter(KS_MASS_CUT).Filter(KSTAR_ALL_CUT)
df = df.Filter(KS_PATHLENGTH_CUT).Filter(MX2_PPIPKMKS_CUT).Filter(PPIM_MASS_CUT).Filter(KMP_MASS_CUT).Filter(P_P_CUT).Filter(KS_MASS_CUT).Filter(KSTAR_ALL_CUT)
print(f'baseline number of events: {df.Count().GetValue()}')
df_missing = df_missing.Filter('mx_f1_m < 1.1 && mx_f1_m > 0.8')
print(f'number of events with missing proton cut: {df_missing.Count().GetValue()}')
# df_missing = df_missing.Filter('mx_delta_m > 1.3')
print(f'number of events with missing proton and delta cut: {df_missing.Count().GetValue()}')

hist_missing_mass_proton = df.Histo1D(('hist_missing_proton', 'Missing Proton', 100, 1.0, 2.0), 'mx_p_m')
hist_measured_kkpi_mass = df.Histo1D(('hist_measured_kkpi_mass', 'Measured K K Pi Mass', 100, 1.0, 2.0), 'pipkmks_m_measured')
hist_measured_kkpi_mass.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_missing_mass_f1 = df.Histo1D(('hist_missing_f1', 'Missing F1', 100, 0.5, 1.5), 'mx_f1_m')
hist_measured_proton_mass = df.Histo1D(('hist_measured_proton_mass', 'Measured Proton Mass', 100, 0.5, 1.5), 'p_m_measured')
hist_measured_proton_mass.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_missing_ppipkm = df.Histo1D(('hist_missing_ppipkm', 'Missing ppipkm', 100, 0.3, 0.7), 'mx_ppipkm_m')
hist_measured_ks_mass = df.Histo1D(('hist_measured_ks_mass', 'Measured Ks Mass', 100, 0.3, 0.7), 'ks_m_measured')
hist_measured_ks_mass.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_f1 = df.Histo1D(('hist_f1', 'F1', 100, 1.0, 2.0), 'pipkmks_m')
hist_f1_missing = df_missing.Histo1D(('hist_f1_missing', 'F1_missing', 100, 1.0, 2.0), 'pipkmks_m')
hist_f1_missing.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))

c = ROOT.TCanvas('c', 'c', 800, 600)
c.Divide(3, 1)
c.cd(1)
hist_f1.Draw()
hist_f1_missing.Draw('same')
c.cd(2)
hist_missing_mass_f1.Draw()
c.cd(3)
df_missing.Histo1D(('hist_delta', 'Delta', 100, 1.0, 2.0), 'mx_delta_m').Draw()
c.Update()

# canvas = ROOT.TCanvas('canvas', 'canvas', 800, 600)
# canvas.Divide(3,1)
# canvas.cd(1)
# hist_measured_kkpi_mass.Draw()
# hist_missing_mass_proton.Draw('same')
# canvas.cd(2)
# hist_measured_proton_mass.Draw()
# hist_missing_mass_f1.Draw('same')
# canvas.cd(3)
# hist_measured_ks_mass.Draw()
# hist_missing_ppipkm.Draw('same')
# canvas.Update()

input('Press any key to continue...')