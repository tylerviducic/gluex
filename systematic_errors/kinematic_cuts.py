import ROOT
# import sys
# sys.path.append('/work/halld/home/viducic/')
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts

# TODO: define pipeline
# TODO: make sure variation in cut does not change statistics by > 10% 

baseline_pipkmks, baseline_pimkpks = 35865, 41281

# convention is (loose, tight)
varied_cuts_dict_pipkmks = {
            'kinfit_cl': ('kinfit_cl > 1e-6', 'kinfit_cl > 1e-4'),
            'pathlength': ('pathlength_sig > 4', 'pathlength_sig > 6'),
            'ks_m': (f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 2.5 * {constants.KSHORT_FIT_WIDTH}', f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 1.5 * {constants.KSHORT_FIT_WIDTH}'),
            'ppi': ('ppip_m > 1.3', 'ppip_m > 1.5'),
            'kp': ('kmp_m > 1.9', 'kmp_m > 2.1'),
            'ksp': ('ksp_m > 1.9', 'ksp_m > 2.1'),
            'pp': ('p_p > 0.3', 'p_p > 0.5'),
            'neutral_kstar': '(kmpip_m > 0.75 && kmpip_m < 1.05)',
            'charged_kstar': '(kspip_m > 0.75 && kspip_m < 1.05)'
             }

nominal_cuts_dict_pipkmks = {
            'kinfit_cl': cuts.KINFIT_CL_CUT,
            'pathlength': cuts.KS_PATHLENGTH_CUT,
            'ks_m': cuts.KS_MASS_CUT,
            'ppi': cuts.PPIP_MASS_CUT,
            'kp': cuts.KMP_MASS_CUT,
            'ksp': cuts.KSP_MASS_CUT,
            'pp': cuts.P_P_CUT,
            'neutral_kstar': cuts.KSTAR_ZERO_CUT_PIPKMKS,
            'charged_kstar': cuts.KSTAR_PLUS_CUT
            }

df_pipkmks = tools.get_dataframe('pipkmks', 'gluex1', 'data', filtered=False)

for varied_cut in varied_cuts_dict_pipkmks:
    varied_df = df_pipkmks.Filter("true")
    for nominal_cut in nominal_cuts_dict_pipkmks:
        if varied_cut == nominal_cut:
            continue
        else:
            varied_df = varied_df.Filter(nominal_cuts_dict_pipkmks[nominal_cut])
    df_low = varied_df.Filter(varied_cuts_dict_pipkmks[varied_cut][0])
    df_high = varied_df.Filter(varied_cuts_dict_pipkmks[varied_cut][1])

    # for e in 