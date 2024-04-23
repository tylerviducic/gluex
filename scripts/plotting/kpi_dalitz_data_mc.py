import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts
import my_library.gluex_style as gstyle

data_df = tools.get_dataframe('pipkmks', 'fall', 'data')
mc_df = tools.get_dataframe('pipkmks', 'fall', 'signal')

data_df = data_df.Filter(kcuts.BEAM_RANGE).Filter(kcuts.T_RANGE).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS)
mc_df = mc_df.Filter(kcuts.BEAM_RANGE).Filter(kcuts.T_RANGE).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS)

data_df = data_df.Define('kspip_m2', 'kspip_m*kspip_m').Define('kmpip_m2', 'kmpip_m*kmpip_m')
mc_df = mc_df.Define('kspip_m2', 'kspip_m*kspip_m').Define('kmpip_m2', 'kmpip_m*kmpip_m')

data_dalitz = data_df.Histo2D(('data_dalitz', 'Dalitz plot', 50, 0.35, 0.75, 50, 0.35, 0.75), 'kspip_m2', 'kmpip_m2')
mc_dalitz = mc_df.Histo2D(('mc_dalitz', 'Dalitz plot', 100, 0.35, 0.75, 100, 0.35, 0.75), 'kspip_m2', 'kmpip_m2')
kstar_cut_data_dalitz = data_df.Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS).Histo2D(('cut_data_dalitz', 'Dalitz plot', 50, 0.35, 0.75, 50, 0.35, 0.75), 'kspip_m2', 'kmpip_m2')
a0_cut_data_dalitz = data_df.Filter('kmks_m < 1.05').Histo2D(('cut_data_dalitz', 'Dalitz plot', 50, 0.35, 0.75, 50, 0.35, 0.75), 'kspip_m2', 'kmpip_m2')


data_dalitz.GetXaxis().SetTitle('M^{2}(K_{S}#pi^{+}) (GeV^{2})')
data_dalitz.GetXaxis().SetTitleSize(0.05)
data_dalitz.GetYaxis().SetTitle('M^{2}(K^{-}#pi^{+}) (GeV^{2})')
data_dalitz.GetYaxis().SetTitleOffset(1.4)
data_dalitz.GetYaxis().SetTitleSize(0.05)

kstar_cut_data_dalitz.GetXaxis().SetTitle('M^{2}(K_{S}#pi^{+}) (GeV^{2})')
kstar_cut_data_dalitz.GetXaxis().SetTitleSize(0.05)
kstar_cut_data_dalitz.GetYaxis().SetTitle('M^{2}(K^{-}#pi^{+}) (GeV^{2})')
kstar_cut_data_dalitz.GetYaxis().SetTitleOffset(1.4)
kstar_cut_data_dalitz.GetYaxis().SetTitleSize(0.05)

a0_cut_data_dalitz.GetXaxis().SetTitle('M^{2}(K_{S}#pi^{+}) (GeV^{2})')
a0_cut_data_dalitz.GetXaxis().SetTitleSize(0.05)
a0_cut_data_dalitz.GetYaxis().SetTitle('M^{2}(K^{-}#pi^{+}) (GeV^{2})')
a0_cut_data_dalitz.GetYaxis().SetTitleOffset(1.4)
a0_cut_data_dalitz.GetYaxis().SetTitleSize(0.05)

mc_dalitz.GetXaxis().SetTitle('M^{2}(K_{S}#pi^{+}) (GeV^{2})')
mc_dalitz.GetXaxis().SetTitleSize(0.05)
mc_dalitz.GetYaxis().SetTitle('M^{2}(K^{-}#pi^{+}) (GeV^{2})')
mc_dalitz.GetYaxis().SetTitleOffset(1.4)
mc_dalitz.GetYaxis().SetTitleSize(0.05)

c = ROOT.TCanvas('c', 'c', 800, 800)
c.Divide(2, 2)
pad1 = c.cd(1)
pad1.SetLeftMargin(0.15)
data_dalitz.Draw('colz')
pad2 = c.cd(2)
pad2.SetLeftMargin(0.15)
mc_dalitz.Draw('colz')
pad3 = c.cd(3)
pad3.SetLeftMargin(0.15)
kstar_cut_data_dalitz.Draw('colz')
pad4 = c.cd(4)
pad4.SetLeftMargin(0.15)
a0_cut_data_dalitz.Draw('colz')
c.Update()
c.Draw()

input('Press enter to continue...')
