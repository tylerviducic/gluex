import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts


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

    for i in range(14, 22):
        cut_value = i/10
        cut_string_pipkmks = f'Numba::ppip_cut(ppip_m, {cut_value})'
        cut_string_pimkpks = f'Numba::ppim_cut(ppim_m, {cut_value})'
        hist_pipkmks = df_pipkmks.Filter(cut_string_pipkmks).Histo1D((f"pipkmks_cut_ppip_{cut_value}", "M(K^{-}K_{s}#pi^{+}) for M(p#pi^{+}) < " + str(cut_value), 100, 1.0, 2.0), "pipkmks_m")
        hist_pimkpks = df_pimkpks.Filter(cut_string_pimkpks).Histo1D((f"pimkpks_cut_ppim_{cut_value}", "M(K^{+}K_{s}#pi^{-}) for M(p#pi^{-}) < " + str(cut_value), 100, 1.0, 2.0), "pimkpks_m")

        # TODO: save histograms to a pdf