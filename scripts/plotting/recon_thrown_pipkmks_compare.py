# plot the quantity M(recon)-M(thrown) for the signal MC

import ROOT
from common_analysis_tools import *

ROOT.gStyle.SetOptStat(0)


# file_and_tree = get_flat_file_and_tree('pipkmks', 'spring', 'signal')
# df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
filename = '/work/halld/home/viducic/data/pipkmks/mc/signal/mc_pipkmks_flat_bestX2_2018_fall_debug.root'
treename = 'pipkmks__ks_pippim__B4_M16'

df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())

# df = df.Define('p_px_thrown', 'p_p4_true.Px()')
# df = df.Define('p_py_thrown', 'p_p4_true.Py()')
# df = df.Define('p_pz_thrown', 'p_p4_true.Pz()')
# df = df.Define('p_E_thrown', 'p_p4_true.E()')

# df = df.Define('pip1_px_thrown', 'pip1_p4_true.Px()')
# df = df.Define('pip1_py_thrown', 'pip1_p4_true.Py()')
# df = df.Define('pip1_pz_thrown', 'pip1_p4_true.Pz()')
# df = df.Define('pip1_E_thrown', 'pip1_p4_true.E()')

# df = df.Define('pip2_px_thrown', 'pip2_p4_true.Px()')
# df = df.Define('pip2_py_thrown', 'pip2_p4_true.Py()')
# df = df.Define('pip2_pz_thrown', 'pip2_p4_true.Pz()')
# df = df.Define('pip2_E_thrown', 'pip2_p4_true.E()')

# df = df.Define('pim_px_thrown', 'pim_p4_true.Px()')
# df = df.Define('pim_py_thrown', 'pim_p4_true.Py()')
# df = df.Define('pim_pz_thrown', 'pim_p4_true.Pz()')
# df = df.Define('pim_E_thrown', 'pim_p4_true.E()')

# df = df.Define('km_px_thrown', 'km_p4_true.Px()')
# df = df.Define('km_py_thrown', 'km_p4_true.Py()')
# df = df.Define('km_pz_thrown', 'km_p4_true.Pz()')
# df = df.Define('km_E_thrown', 'km_p4_true.E()')
# df = df.Define('km_m_thrown_4v', 'km_p4_true.M()')

df = df.Define('p_pt', 'sqrt(p_px_measured*p_px_measured + p_py_measured*p_py_measured)')
df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
# df = df.Define('ks_E_fixed', 'fix_ks_energy(ks_px, ks_py, ks_pz)')
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")
# df = df.Define('ks_m_fixed', 'sqrt(ks_E_fixed*ks_E_fixed - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)')

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
# df = df.Define('pipkmks_E_fixed', 'pip1_E + km_E + ks_E_fixed')
df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')
# df = df.Define('pipkmks_m_fixed', 'sqrt(pipkmks_E_fixed*pipkmks_E_fixed - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

df = df.Define('pipkmks_px_measured', "pip1_px_measured + km_px_measured + ks_px_measured")
df = df.Define('pipkmks_py_measured', "pip1_py_measured + km_py_measured + ks_py_measured")
df = df.Define('pipkmks_pz_measured', "pip1_pz_measured + km_pz_measured + ks_pz_measured")
df = df.Define('pipkmks_pt', 'sqrt(pipkmks_px_measured*pipkmks_px_measured + pipkmks_py_measured*pipkmks_py_measured)')

df = df.Define('pipkmks_p_pt_diff', 'pipkmks_pt - p_pt')

df = df.Define('kmks_px', 'km_px + ks_px')
df = df.Define('kmks_py', 'km_py + ks_py')
df = df.Define('kmks_pz', 'km_pz + ks_pz')
df = df.Define('kmks_E', 'km_E + ks_E')
df = df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')
df = df.Define('km_m_thrown_double', 'sqrt(km_E_thrown*km_E_thrown - km_px_thrown*km_px_thrown - km_py_thrown*km_py_thrown - km_pz_thrown*km_pz_thrown)')

df = df.Define('pipkmks_px_thrown', 'pip1_px_thrown + pip2_px_thrown + km_px_thrown + pim_px_thrown')
df = df.Define('pipkmks_py_thrown', 'pip1_py_thrown + pip2_py_thrown + km_py_thrown + pim_py_thrown')
df = df.Define('pipkmks_pz_thrown', 'pip1_pz_thrown + pip2_pz_thrown + km_pz_thrown + pim_pz_thrown')
df = df.Define('pipkmks_E_thrown', 'pip1_E_thrown + pip2_E_thrown + km_E_thrown + pim_E_thrown')
df = df.Define('pipkmks_m_thrown', 'sqrt(pipkmks_E_thrown*pipkmks_E_thrown - pipkmks_px_thrown*pipkmks_px_thrown - pipkmks_py_thrown*pipkmks_py_thrown - pipkmks_pz_thrown*pipkmks_pz_thrown)')

df = df.Define('ks_px_thrown', 'pim_px_thrown + pip2_px_thrown')
df = df.Define('ks_py_thrown', 'pim_py_thrown + pip2_py_thrown')
df = df.Define('ks_pz_thrown', 'pim_pz_thrown + pip2_pz_thrown')
df = df.Define('ks_E_thrown', 'pim_E_thrown + pip2_E_thrown')
df = df.Define('ks_m_thrown', 'sqrt(ks_E_thrown*ks_E_thrown - ks_px_thrown*ks_px_thrown - ks_py_thrown*ks_py_thrown - ks_pz_thrown*ks_pz_thrown)')

df = df.Define('pip1_m_thrown', 'sqrt(pip1_E_thrown*pip1_E_thrown - pip1_px_thrown*pip1_px_thrown - pip1_py_thrown*pip1_py_thrown - pip1_pz_thrown*pip1_pz_thrown)')
df = df.Define('pip2_m_thrown', 'sqrt(pip2_E_thrown*pip2_E_thrown - pip2_px_thrown*pip2_px_thrown - pip2_py_thrown*pip2_py_thrown - pip2_pz_thrown*pip2_pz_thrown)')

df = df.Define('pipkmks_resolution', 'pipkmks_m - pipkmks_m_thrown')
df = df.Define('ks_resolution', 'ks_m - ks_m_thrown')

hist_r_t = df.Histo1D(('pipkmks_resolution', 'pipkmks_resolution', 100, -0.1, 0.1), 'pipkmks_resolution')
hist_recon = df.Histo1D(('pipkmks_recon', 'pipkmks_recon', 100, 1.1, 1.5), 'pipkmks_m')
hist_recon.SetLineColor(ROOT.kRed)
hist_recon.Scale(1/hist_recon.Integral())
hist_thrown = df.Histo1D(('pipkmks_thrown', 'pipkmks_thrown', 100, 1.1, 1.5), 'pipkmks_m_thrown')
hist_thrown.Scale(1/hist_thrown.Integral())
hist_ks_thrown = df.Histo1D(('ks_thrown', 'ks_thrown', 100, 0.3, 0.7), 'ks_m_thrown')
hist_ks_thrown.Scale(1/hist_ks_thrown.Integral())
hist_ks_recon = df.Histo1D(('ks_recon', 'ks_recon', 100, 0.3, 0.7), 'ks_m')
hist_ks_recon.SetLineColor(ROOT.kRed)
hist_ks_recon.Scale(1/hist_ks_recon.Integral())

hist_ks_r_t = df.Histo1D(('ks_resolution', 'ks_resolution', 100, -0.1, 0.1), 'ks_resolution')
hist_pip1_m = df.Histo1D(('pip1_m_thrown', 'pip1_m_thrown', 100, -0.1, 0.2), 'pip1_m_thrown')
hist_pip2_m = df.Histo1D(('pip2_m_thrown', 'pip2_m_thrown', 100, 0.1, 0.2), 'pip2_m_thrown')
hist_pip1_m.SetLineColor(ROOT.kRed)

# hist_km_4v = df.Histo1D(('km_4v', 'km_4v', 100, 0.0, 1.0), 'km_m_thrown_4v')
hist_km_double = df.Histo1D(('km_double', 'km_double', 100, 0.0, 1.0), 'km_m_thrown_double')
hist_km_double.SetLineColor(ROOT.kRed)

c = ROOT.TCanvas('c', 'c', 800, 600)
c.Divide(2,1)
c.cd(1)
hist_r_t.Draw()
# c.cd(2)
# hist_thrown.Draw('HIST')
# hist_recon.Draw("same HIST")
c.cd(2)
hist_ks_r_t.Draw()
# c.cd(4)
# hist_ks_thrown.Draw('HIST')
# hist_ks_recon.Draw('same HIST')
# hist_km_double.Draw()
# hist_km_4v.Draw('same')
# hist_ks_thrown.Draw()
# hist_pip1_m.Draw()
# hist_pip2_m.Draw('same')

# print(hist_pip1_m.GetMean())
# print(df.Mean('pip1_m_thrown').GetValue())
# print(df.Mean('pip2_m_thrown').GetValue())
c.Update()

input('Press any key to continue...')