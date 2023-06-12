# script to analyze flat tree for pipkmks with missing proton

import ROOT
import os
import math

os.nice(18)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)

filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_unconstrained.root'
treename = 'pipkmksmissprot__ks_pippim__B4_M16'

df = ROOT.RDataFrame(treename, filename)

df = df.Define('ks_px', 'pip2_px + pim_px')
df = df.Define('ks_py', 'pip2_py + pim_py')
df = df.Define('ks_pz', 'pip2_pz + pim_pz')
df = df.Define('ks_E', 'pip2_E + pim_E')
df = df.Define('ks_m', 'sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)')

df = df.Define('ks_px_measured', 'pip2_px_measured + pim_px_measured')
df = df.Define('ks_py_measured', 'pip2_py_measured + pim_py_measured')
df = df.Define('ks_pz_measured', 'pip2_pz_measured + pim_pz_measured')
df = df.Define('ks_E_measured', 'pip2_E_measured + pim_E_measured')
df = df.Define('ks_m_measured', 'sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)')

df = df.Define('mx_pipkmks_px', '-pip1_px_measured - ks_px_measured - km_px_measured')
df = df.Define('mx_pipkmks_py', '-pip1_py_measured - ks_py_measured - km_py_measured')
df = df.Define('mx_pipkmks_pz', 'e_beam - pip1_pz_measured - ks_pz_measured - km_pz_measured')
df = df.Define('mx_pipkmks_E', 'e_beam + 0.938 - pip1_E_measured - ks_E_measured - km_E_measured')
df = df.Define('mx_pipkmks_m', 'sqrt(mx_pipkmks_E*mx_pipkmks_E - mx_pipkmks_px*mx_pipkmks_px - mx_pipkmks_py*mx_pipkmks_py - mx_pipkmks_pz*mx_pipkmks_pz)')

hist_mx_kkpi = df.Histo1D(('mx_kkpi', 'mx_kkpi', 500, 0.0, 2.0), 'mx_pipkmks_m')
mean = hist_mx_kkpi.GetMean()
width = hist_mx_kkpi.GetRMS()
print(f'Mean = {mean} +- {hist_mx_kkpi.GetMeanError()}')
print(f'RMS = {width} +- {hist_mx_kkpi.GetRMSError()}')
print(f'proposed cut = {abs(hist_mx_kkpi.GetMean() +- hist_mx_kkpi.GetRMS())}')


hist_mx_kkpi_cut = df.Filter('abs(mx_pipkmks_m - 0.9586708347706232 ) < 0.22293539653812539').Histo1D(('mx_kkpi_cut', 'mx_kkpi_cut', 500, 0.0, 2.0), 'mx_pipkmks_m')
hist_mx_kkpi_cut.SetLineColor(ROOT.kRed)

# c = ROOT.TCanvas('c', 'c', 900, 900)
# hist_mx_kkpi.Draw()
# hist_mx_kkpi_cut.Draw('same')
# c.Update()

# input('Press any key to continue...')

#TODO cut on missing kkpi then plot the Ks before and after
