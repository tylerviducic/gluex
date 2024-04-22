import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts

ROOT.EnableImplicitMT(12)

data_df = tools.get_dataframe('pipkmks', 'spring', 'data').Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter('e_beam > 8.0 && e_beam < 10.0').Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS)
recon_df = tools.get_dataframe('pipkmks', 'spring', 'signal').Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter('e_beam > 8.0 && e_beam < 10.0').Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS)

data_t = data_df.Histo1D(('data_t', 'data_t', 40, 0.1, 0.6), 'mand_t')
data_t.Scale(1.0 / data_t.Integral())
recon_t = recon_df.Histo1D(('recon_t', 'recon_t', 40, 0.1, 0.6), 'mand_t')
recon_t.Scale(1.0 / recon_t.Integral())
recon_t.SetLineColor(ROOT.kRed)

c = ROOT.TCanvas('c', 'c', 800, 600)
data_t.Draw()
recon_t.Draw('same')

c.Update()
c.Draw()

input('Press enter to continue...')