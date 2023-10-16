import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts


ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def ppim_cut(ppim_m, cut_val):
    return ppim_m > cut_val


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def ppip_cut(ppip_m, cut_val):
    return ppip_m > cut_val
#'Numba::ppip_mass_cut(ppip_m)'


if __name__ == "__main__":
    df_pipkmks = tools.get_dataframe("pipkmks", "spring", "data", filtered=False)
    df_pimkpks = tools.get_dataframe("pimkpks", "spring", "data", filtered=False)

    df_pipkmks = df_pipkmks.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIPKMKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.P_P_CUT).Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS)
    df_pimkpks = df_pimkpks.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIMKPKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.P_P_CUT).Filter(kcuts.KSTAR_ALL_CUT_PIMKPKS)

    c = ROOT.TCanvas("c", "c", 800, 600)
    c.Print("vary_ppi_cut.pdf[", "pdf")

    for i in range(14, 22):
        cut_value = i/10
        cut_string_pipkmks = f'Numba::ppip_cut(ppip_m, {cut_value})'
        cut_string_pimkpks = f'Numba::ppim_cut(ppim_m, {cut_value})'
        hist_pipkmks = df_pipkmks.Filter(cut_string_pipkmks).Histo1D((f"pipkmks_cut_ppip_{cut_value}", "M(K^{-}K_{s}#pi^{+}) for M(p#pi^{+}) < " + str(cut_value), 50, 1.0, 1.5), "pipkmks_m")
        hist_pimkpks = df_pimkpks.Filter(cut_string_pimkpks).Histo1D((f"pimkpks_cut_ppim_{cut_value}", "M(K^{+}K_{s}#pi^{-}) for M(p#pi^{-}) < " + str(cut_value), 50, 1.0, 1.5), "pimkpks_m")

        peak_ratio = hist_pimkpks.GetMaximum()/hist_pipkmks.GetMaximum()
        text = ROOT.TPaveText(0.6, 0.2, 0.9, 0.4, "NDC")
        text.AddText(f'ratio of peak heights: {peak_ratio:.2f}')

        hist_pipkmks.SetLineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['blue']))
        hist_pimkpks.SetLineColor(ROOT.TColor.GetColor(constants.COLORBLIND_HEX_DICT['red']))

        legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
        legend.AddEntry(hist_pipkmks.GetPtr(), "K^{-}K_{s}#pi^{+}", "l")
        legend.AddEntry(hist_pimkpks.GetPtr(), "K^{+}K_{s}#pi^{-}", "l")

        hist_pimkpks.Draw()
        hist_pipkmks.Draw("same")
        legend.Draw()
        text.Draw()
        c.Draw()
        c.Print("vary_ppi_cut.pdf", "pdf")

    c.Print("vary_ppi_cut.pdf]", "pdf")
