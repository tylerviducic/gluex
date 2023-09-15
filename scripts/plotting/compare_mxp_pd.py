# script to compare the MXP and PD data

import ROOT
from my_library.kinematic_cuts import KSTAR_ALL_CUT_PIPKMKS
from my_library.constants import COLORBLIND_HEX_DICT as colorblind_hex_dict

ROOT.gStyle.SetOptStat(0)

mxp_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_filtered.root'
mxp_ksc_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_ksc_filtered.root'
pd_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_filtered.root'
pd_ksc_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_ksc_filtered.root'

mxp_unfiltered_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_unconstrained.root'
mxp_ksc_unfiltered_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_mxp_constrained.root'
pd_unfiltered_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_unconstrained.root'
pd_ksc_unfiltered_filename = '/work/halld/home/viducic/data/pipkmks/data/mxp_study/pipkmks_pd_constrained.root'

mxp_unfiltered_treename = 'pipkmksmissprot__ks_pippim__B4_M16'
mxp_ksc_unfiltered_treename = 'pipkmksmissprot__ks_pippim__B4'
pd_unfiltered_treename = 'pipkmks__ks_pippim__B4_M16'
pd_ksc_unfiltered_treename = 'pipkmks__ks_pippim__B4'

mxp_treename = 'pipkmks_mxp_filtered'
mxp_ksc_treename = 'pipkmks_mxp_ksc_filtered'
pd_treename = 'pipkmks_pd_filtered'
pd_ksc_treename = 'pipkmks_pd_ksc_filtered'

df_mxp = ROOT.RDataFrame(mxp_treename, mxp_filename)
df_mxp_ksc = ROOT.RDataFrame(mxp_ksc_treename, mxp_ksc_filename)
df_pd = ROOT.RDataFrame(pd_treename, pd_filename)
df_pd_ksc = ROOT.RDataFrame(pd_ksc_treename, pd_ksc_filename)

df_mxp_unfiltered = ROOT.RDataFrame(mxp_unfiltered_treename, mxp_unfiltered_filename)
df_mxp_ksc_unfiltered = ROOT.RDataFrame(mxp_ksc_unfiltered_treename, mxp_ksc_unfiltered_filename)
df_pd_unfiltered = ROOT.RDataFrame(pd_unfiltered_treename, pd_unfiltered_filename)
df_pd_ksc_unfiltered = ROOT.RDataFrame(pd_ksc_unfiltered_treename, pd_ksc_unfiltered_filename)

df_mxp = df_mxp.Filter(KSTAR_ALL_CUT_PIPKMKS)
df_mxp_ksc = df_mxp_ksc.Filter(KSTAR_ALL_CUT_PIPKMKS)
df_pd = df_pd.Filter(KSTAR_ALL_CUT_PIPKMKS)
df_pd_ksc = df_pd_ksc.Filter(KSTAR_ALL_CUT_PIPKMKS)

hist_mxp_pipkmks = df_mxp.Histo1D(('pipkmks_mxp', 'pipkmks_mxp', 50, 1.0, 1.8), 'pipkmks_m').GetValue()
hist_mxp_ksc_pipkmks = df_mxp_ksc.Histo1D(('pipkmks_mxp_ksc', 'pipkmks_mxp_ksc', 50, 1.0, 1.8), 'pipkmks_m').GetValue()
hist_pd_pipkmks = df_pd.Histo1D(('pipkmks_pd', 'pipkmks_pd', 50, 1.0, 1.8), 'pipkmks_m').GetValue()
hist_pd_ksc_pipkmks = df_pd_ksc.Histo1D(('pipkmks_pd_ksc', 'pipkmks_pd_ksc', 50, 1.0, 1.8), 'pipkmks_m').GetValue()

hist_mxp_ks = df_mxp.Histo1D(('ks_mxp', 'ks_mxp', 100, 0.3, 0.7), 'ks_m_measured').GetValue()
hist_mxp_ksc_ks = df_mxp_ksc.Histo1D(('ks_mxp_ksc', 'ks_mxp_ksc', 100, 0.3, 0.7), 'ks_m_measured').GetValue()
hist_pd_ks = df_pd.Histo1D(('ks_pd', 'ks_pd', 100, 0.3, 0.7), 'ks_m_measured').GetValue()
hist_pd_ksc_ks = df_pd_ksc.Histo1D(('ks_pd_ksc', 'ks_pd_ksc', 100, 0.3, 0.7), 'ks_m_measured').GetValue()

chi2_to_cl = """
double chi2_to_cl(double chi2, int ndf) {
    return TMath::Prob(chi2, ndf);
    }
"""

ROOT.gInterpreter.Declare(chi2_to_cl)

df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_cl', 'chi2_to_cl(kin_chisq, kin_ndf)')
df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_cl', 'chi2_to_cl(kin_chisq, kin_ndf)')

df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_px_measured', 'pip2_px_measured + pim_px_measured')
df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_py_measured', 'pip2_py_measured + pim_py_measured')
df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_pz_measured', 'pip2_pz_measured + pim_pz_measured')
df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_E_measured', 'pip2_E_measured + pim_E_measured')
df_mxp_ksc_unfiltered = df_mxp_ksc_unfiltered.Define('ks_m_measured', 'sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)')

df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_px_measured', 'pip2_px_measured + pim_px_measured')
df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_py_measured', 'pip2_py_measured + pim_py_measured')
df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_pz_measured', 'pip2_pz_measured + pim_pz_measured')
df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_E_measured', 'pip2_E_measured + pim_E_measured')
df_mxp_unfiltered = df_mxp_unfiltered.Define('ks_m_measured', 'sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)')

hist_mxp_ks_unfiltered = df_mxp_unfiltered.Filter('ks_cl > 0.5').Histo1D(('ks_mxp_unfiltered', 'ks_mxp_unfiltered', 100, 0.3, 0.7), 'ks_m_measured').GetValue()
hist_mxp_ksc_ks_unfiltered = df_mxp_ksc_unfiltered.Filter('ks_cl > 0.5').Histo1D(('ks_mxp_ksc_unfiltered', 'ks_mxp_ksc_unfiltered', 100, 0.3, 0.7), 'ks_m_measured').GetValue()
hist_mxp_ks_unfiltered.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_mxp_ksc_ks_unfiltered.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))

hist_mxp_ks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_mxp_ks.SetLineWidth(2)
hist_mxp_ksc_ks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_mxp_ksc_ks.SetLineWidth(2)
hist_pd_ks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['cyan']))
hist_pd_ks.SetLineWidth(2)
hist_pd_ksc_ks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))

hist_mxp_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
hist_mxp_pipkmks.SetLineWidth(2)
hist_mxp_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
hist_mxp_ksc_pipkmks.SetLineWidth(2)
# hist_pd_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
# hist_pd_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['orange']))
hist_pd_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['cyan']))
hist_pd_pipkmks.SetLineWidth(2)
hist_pd_ksc_pipkmks.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
hist_pd_ksc_pipkmks.SetLineWidth(2)

legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
legend.AddEntry(hist_mxp_pipkmks, 'Missing Proton', 'lep')
legend.AddEntry(hist_mxp_ksc_pipkmks, 'Missing Proton Ks Constrained', 'lep')
legend.AddEntry(hist_pd_pipkmks, 'Proton Detected', 'lep')
legend.AddEntry(hist_pd_ksc_pipkmks, 'Proton Detected Ks Constrained', 'lep')


c = ROOT.TCanvas('c', 'c', 900, 900)
c.cd()
hist_mxp_pipkmks.SetTitle('Missing Proton vs Proton Detected')
hist_mxp_pipkmks.GetXaxis().SetTitle('M_{#pi^{+}K^{-}K^{0}_{S}} [GeV]')
hist_mxp_pipkmks.GetYaxis().SetTitle('Counts')
hist_mxp_pipkmks.Draw()
hist_mxp_ksc_pipkmks.Draw("same")
hist_pd_pipkmks.Draw("same")
hist_pd_ksc_pipkmks.Draw('same')
legend.Draw()
c.Update()

c2 = ROOT.TCanvas('c2', 'c2', 900, 900)
c2.cd()
hist_mxp_ksc_ks.SetTitle('Missing Proton vs Proton Detected')
hist_mxp_ksc_ks.GetXaxis().SetTitle('M_{#pi^{+}#pi^{-}} [GeV]')
hist_mxp_ksc_ks.GetYaxis().SetTitle('Counts')
hist_mxp_ksc_ks.Draw()
hist_mxp_ks.Draw("same")
hist_pd_ks.Draw("same")
hist_pd_ksc_ks.Draw('same')
legend.Draw()
c2.Update()

c3 = ROOT.TCanvas('c3', 'c3', 900, 900)
c3.cd()
hist_mxp_ksc_ks_unfiltered.SetTitle('Ks Unfiltered')
hist_mxp_ksc_ks_unfiltered.GetXaxis().SetTitle('M_{#pi^{+}#pi^{-}} [GeV]')
hist_mxp_ksc_ks_unfiltered.GetYaxis().SetTitle('Counts')
hist_mxp_ksc_ks_unfiltered.Draw()
hist_mxp_ks_unfiltered.Draw("same")
legend.Draw()
c3.Update()


input('Press any key to continue...')
