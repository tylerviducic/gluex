import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts
import my_library.gluex_style

ROOT.EnableImplicitMT(12)

df_recon = tools.get_dataframe('pipkmks', 'fall', 'signal').Filter('e_beam > 8.0 && e_beam < 10.0').Filter('mand_t >= 0.1 && mand_t <= 0.5')#.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS)
df_thrown = tools.get_dataframe('pipkmks', 'fall', 'signal', filtered=False, thrown=True).Filter('e_beam > 8.0 && e_beam < 10.0').Filter('mand_t >= 0.1 && mand_t <= 0.5')#.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS)
# print(df_thrown.GetColumnNames())
df_thrown = df_thrown.Define('kmks_px', 'KMinus_px + Ks_px')
df_thrown = df_thrown.Define('kmks_py', 'KMinus_py + Ks_py')
df_thrown = df_thrown.Define('kmks_pz', 'KMinus_pz + Ks_pz')
df_thrown = df_thrown.Define('kmks_E', 'KMinus_E + Ks_E')
df_thrown = df_thrown.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')

kk_recon = df_recon.Histo1D(('kk_recon', ';M(K^{-}K_{s}) [GeV]', 250, 0.99, 1.7), 'kmks_m')
kk_thrown = df_thrown.Histo1D(('kk_thrown', ';M(K^{-}K_{s}) [GeV]', 250, 0.99, 1.7), 'kmks_m')
kkpi_recon = df_recon.Histo1D(('kkpi_recon', ';M(K^{-}K_{s}#pi^{+}) [GeV]', 250, 1.1, 1.7), 'pipkmks_m')

overall_acc = df_recon.Count().GetValue() / df_thrown.Count().GetValue()

kk_recon.Sumw2()
kk_thrown.Sumw2()

acceptance = kk_recon.GetValue().Clone('acceptance')
acceptance.Divide(kk_thrown.GetValue())
acceptance.GetYaxis().SetTitle('Acceptance')

acc_line = ROOT.TLine(0.99, overall_acc, 1.7, overall_acc)
acc_line.SetLineColor(ROOT.kRed)
acc_line.SetLineWidth(2)

c = ROOT.TCanvas('c', 'c', 800, 600)
acceptance.Draw("E1")
acc_line.Draw()
c.Draw()
c.Update()

input('Press Enter to continue...')

# c.Clear()
# kk_recon.Draw()
# c.Draw()
# c.Update()

# input('Press Enter to continue...')


