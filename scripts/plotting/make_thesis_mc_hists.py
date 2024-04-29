import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts

channel = 'pipkmks'
run_period = 'fall'

df_recon_no_cuts = tools.get_dataframe(channel, run_period, 'signal', filtered=False).Filter(kcuts.BEAM_RANGE).Filter(kcuts.KINFIT_CL_CUT)
df_recon_filtered = tools.get_dataframe(channel, run_period, 'signal')

hist_pipkmks = df_recon_filtered.Histo1D((channel, f'{channel}_m', 200, 1.1, 1.6), f'{channel}_m')
hist_t = df_recon_filtered.Histo1D(('mand_t', 'mand_t', 200, 0.1, 2), 'mand_t')
hist_ks = df_recon_no_cuts.Histo1D(('ks_m', 'ks_m', 200, 0.4, 0.6), 'ks_m')

out_file = ROOT.TFile(f'/work/halld/home/viducic/scripts/plotting/thesis_{channel}_{run_period}_mc_hists.root', 'recreate')
hist_pipkmks.Write()
hist_t.Write()
hist_ks.Write()

out_file.Close()



