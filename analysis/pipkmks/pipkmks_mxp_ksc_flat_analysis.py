# script to analyze flat tree for pipkmks with missing proton

import ROOT
import os
import math
from common_analysis_tools import *

os.nice(18)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)

#TODO cut on xi2 or CL (by calling root fucnction for it) to be much tighter

filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_constrained.root'
treename = 'pipkmksmissprot__ks_pippim__B4'

df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())
# "kin_chisq", "kin_ndf

chi2_to_cl = """
double chi2_to_cl(double chi2, int ndf) {
    return TMath::Prob(chi2, ndf);
    }
"""

ROOT.gInterpreter.Declare(chi2_to_cl)


df = df.Define('kinfit_cl', 'chi2_to_cl(kin_chisq, kin_ndf)')

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

df = df.Define('mx_kmks_px', '-km_px - ks_px')
df = df.Define('mx_kmks_py', '-km_py - ks_py')
df = df.Define('mx_kmks_pz', 'e_beam - km_pz - ks_pz')
df = df.Define('mx_kmks_E', 'e_beam + 0.938 - km_E - ks_E')
df = df.Define('mx_kmks_m', 'sqrt(mx_kmks_E*mx_kmks_E - mx_kmks_px*mx_kmks_px - mx_kmks_py*mx_kmks_py - mx_kmks_pz*mx_kmks_pz)')

df = df.Define('pipkmks_px', 'pip1_px_measured + ks_px_measured + km_px_measured')
df = df.Define('pipkmks_py', 'pip1_py_measured + ks_py_measured + km_py_measured')
df = df.Define('pipkmks_pz', 'pip1_pz_measured + ks_pz_measured + km_pz_measured')
df = df.Define('pipkmks_E', 'pip1_E_measured + ks_E_measured + km_E_measured')
df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

df = df.Define('kspip_px', 'ks_px + pip1_px')
df = df.Define('kspip_py', 'ks_py + pip1_py')
df = df.Define('kspip_pz', 'ks_pz + pip1_pz')
df = df.Define('kspip_E', 'ks_E + pip1_E')
df = df.Define('kspip_m', 'sqrt(kspip_E*kspip_E - kspip_px*kspip_px - kspip_py*kspip_py - kspip_pz*kspip_pz)')

df = df.Define('kmpip_px', 'km_px + pip1_px')
df = df.Define('kmpip_py', 'km_py + pip1_py')
df = df.Define('kmpip_pz', 'km_pz + pip1_pz')
df = df.Define('kmpip_E', 'km_E + pip1_E')
df = df.Define('kmpip_m', 'sqrt(kmpip_E*kmpip_E - kmpip_px*kmpip_px - kmpip_py*kmpip_py - kmpip_pz*kmpip_pz)')

df = df.Define('mx_kspip_px', '-pip1_px - ks_px')
df = df.Define('mx_kspip_py', '-pip1_py - ks_py')
df = df.Define('mx_kspip_pz', 'e_beam - pip1_pz - ks_pz')
df = df.Define('mx_kspip_E', 'e_beam + 0.938 - pip1_E - ks_E')
df = df.Define('mx_kspip_m', 'sqrt(mx_kspip_E*mx_kspip_E - mx_kspip_px*mx_kspip_px - mx_kspip_py*mx_kspip_py - mx_kspip_pz*mx_kspip_pz)')

missing_kkpi_cut = 'abs(mx_pipkmks_m - 0.9586708347706232 ) < 0.22293539653812539'
pathlength_sig_cut = 'pathlength_sig > 5'
delta_pp_cut = 'mx_kmks_m > 1.5'
lambda_cut = 'mx_kspip_m > 2.0'
cl_cut = 'kinfit_cl > 0.5'

# confidence level of kinfit

# hist_cl = df.Histo1D(('cl', 'cl', 100, 0.0, 1.0), 'kinfit_cl')
# hist_cl.Draw()

# input('Press <Enter> to continue')

##############################################################################################################

#missing kkpi testing for proton cut 

hist_mx_kkpi = df.Histo1D(('mx_kkpi', 'mx_kkpi', 500, 0.0, 2.0), 'mx_pipkmks_m')
mean = hist_mx_kkpi.GetMean()
width = hist_mx_kkpi.GetRMS()
# print(f'Mean = {mean} +- {hist_mx_kkpi.GetMeanError()}')
# print(f'RMS = {width} +- {hist_mx_kkpi.GetRMSError()}')
# print(f'proposed cut = {abs(hist_mx_kkpi.GetMean() +- hist_mx_kkpi.GetRMS())}')


##############################################################################################################

# df = df.Filter(missing_kkpi_cut).Filter(pathlength_sig_cut).Filter(delta_pp_cut).Filter(lambda_cut).Filter(cl_cut)
df = df.Filter(cl_cut).Filter(pathlength_sig_cut).Filter(delta_pp_cut).Filter(lambda_cut)

# pathlength signifgance testing for ks background suppression

# hist_ks_pathsig = df.Histo2D(('ks_pathsig', 'ks_pathsig', 100, 0.3, 0.7, 100, 2.0, 10.0), 'ks_m', 'pathlength_sig')
# hist_ks_pathsig.Draw('colz')

# input('Press <Enter> to continue')
# hist_ks_pls_1 = df.Filter('pathlength_sig > 1').Histo1D(('ks_fs_1', 'ks_fs_1', 100, 0.3, 0.7), 'ks_m')
# hist_ks_pls_1.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['orange']))
# hist_ks_pls_3 = df.Filter('pathlength_sig > 3').Histo1D(('ks_fs_3', 'ks_fs_3', 100, 0.3, 0.7), 'ks_m')
# hist_ks_pls_3.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
# hist_ks_pls_5 = df.Filter('pathlength_sig > 5').Histo1D(('ks_fs_5', 'ks_fs_5', 100, 0.3, 0.7), 'ks_m')
# hist_ks_pls_5.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
# hist_ks_pls_7 = df.Filter('pathlength_sig > 7').Histo1D(('ks_fs_7', 'ks_fs_7', 100, 0.3, 0.7), 'ks_m')
# hist_ks_pls_7.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
# hist_ks_pls_9 = df.Filter('pathlength_sig > 9').Histo1D(('ks_fs_9', 'ks_fs_9', 100, 0.3, 0.7), 'ks_m')
# hist_ks_pls_9.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['cyan']))

# c = ROOT.TCanvas('c', 'c', 900, 900)
# hist_ks_pls_3.Draw()
# hist_ks_pls_5.Draw("same")
# hist_ks_pls_7.Draw("same")
# # hist_ks_pls_9.Draw("same")
# c.Update()

# input("Press <Enter> to continue")

##############################################################################################################

# missing kskm testing for delta++ cut 

# hist_mx_kmks = df.Histo1D(('mx_kmks', 'mx_kmks', 500, 0.7, 2.0), 'mx_kmks_m')
# hist_mx_kmks.Draw()

# input('Press <Enter> to continue')

##############################################################################################################

# testing for lamba resonances 
# hist_mx_kspip = df.Histo1D(('mx_kspip', 'mx_kspip', 500, 1.4, 2.5), 'mx_kspip_m')
# hist_mx_kspip.Draw()
# input('Press <Enter> to continue')
##############################################################################################################

# f1 plotting and testing

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
