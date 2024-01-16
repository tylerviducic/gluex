import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts

ROOT.EnableImplicitMT()

# convention is (loose, tight)
varied_cuts_dict_pipkmks = {
            'kinfit_cl': ('kinfit_cl > 1e-6', 'kinfit_cl > 1e-4'),
            'pathlength': ('pathlength_sig > 4', 'pathlength_sig > 6'),
            'ks_m': (f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 2.5 * {constants.KSHORT_FIT_WIDTH}', f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 1.5 * {constants.KSHORT_FIT_WIDTH}'),
            'ppi': ('ppip_m > 1.3', 'ppip_m > 1.5'),
            'kp': ('kmp_m > 1.9', 'kmp_m > 2.1'),
            'ksp': ('ksp_m > 1.9', 'ksp_m > 2.1'),
            'pp': ('p_p > 0.35', 'p_p > 0.45'),
            'neutral_kstar': ('abs(kmpip_m - 0.89555) > (1.5 * 0.0473)', 'abs(kmpip_m - 0.89555) > (2.5 * 0.0473)'),
            'charged_kstar': ('abs(kspip_m - 0.89167) > (1.75 * 0.0514)', 'abs(kspip_m - 0.89167) > (2.25 * 0.0514)'),
            'mx2_all': ('abs(mx2_ppipkmks) < 0.02', 'abs(mx2_ppipkmks) < 0.007')
             }

# convention is (loose, tight)
varied_cuts_dict_pipkmks = {
            'kinfit_cl': ('kinfit_cl > 1e-6', 'kinfit_cl > 1e-4'),
            'pathlength': ('pathlength_sig > 4', 'pathlength_sig > 6'),
            'ks_m': (f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 2.5 * {constants.KSHORT_FIT_WIDTH}', f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 1.5 * {constants.KSHORT_FIT_WIDTH}'),
            'ppi': ('ppip_m > 1.3', 'ppip_m > 1.5'),
            'kp': ('kmp_m > 1.9', 'kmp_m > 2.1'),
            'ksp': ('ksp_m > 1.9', 'ksp_m > 2.1'),
            'pp': ('p_p > 0.35', 'p_p > 0.45'),
            'neutral_kstar': ('abs(kmpip_m - 0.89555) > (1.5 * 0.0473)', 'abs(kmpip_m - 0.89555) > (2.5 * 0.0473)'),
            'charged_kstar': ('abs(kspip_m - 0.89167) > (1.75 * 0.0514)', 'abs(kspip_m - 0.89167) > (2.25 * 0.0514)'),
            'mx2_all': ('abs(mx2_ppipkmks) < 0.02', 'abs(mx2_ppipkmks) < 0.007')
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
            'charged_kstar': cuts.KSTAR_PLUS_CUT,
            'mx2_all': cuts.MX2_PPIPKMKS_CUT
            }

varied_cuts_dict_pimkpks = {
            'kinfit_cl': ('kinfit_cl > 1e-6', 'kinfit_cl > 1e-4'),
            'pathlength': ('pathlength_sig > 4', 'pathlength_sig > 6'),
            'ks_m': (f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 2.5 * {constants.KSHORT_FIT_WIDTH}', f'abs(ks_m - {constants.KSHORT_FIT_MEAN}) < 1.5 * {constants.KSHORT_FIT_WIDTH}'),
            'ppi': ('ppim_m > 1.3', 'ppim_m > 1.5'),
            'kp': ('kpp_m > 1.9', 'kpp_m > 2.1'),
            'ksp': ('ksp_m > 1.9', 'ksp_m > 2.1'),
            'pp': ('p_p > 0.35', 'p_p > 0.45'),
            'neutral_kstar': ('abs(kppim_m - 0.89555) > (1.5 * 0.0473)', 'abs(kppim_m - 0.89555) > (2.5 * 0.0473)'),
            'charged_kstar': ('abs(kspim_m - 0.89167) > (1.75 * 0.0514)', 'abs(kspim_m - 0.89167) > (2.25 * 0.0514)'),
            'mx2_all': ('abs(mx2_ppimkpks) < 0.02', 'abs(mx2_ppimkpks) < 0.007')
             }

nominal_cuts_dict_pimkpks = {
            'kinfit_cl': cuts.KINFIT_CL_CUT,
            'pathlength': cuts.KS_PATHLENGTH_CUT,
            'ks_m': cuts.KS_MASS_CUT,
            'ppi': cuts.PPIM_MASS_CUT,
            'kp': cuts.KPP_MASS_CUT,
            'ksp': cuts.KSP_MASS_CUT,
            'pp': cuts.P_P_CUT,
            'neutral_kstar': cuts.KSTAR_ZERO_CUT_PIMKPKS,
            'charged_kstar': cuts.KSTAR_MINUS_CUT,
            'mx2_all': cuts.MX2_PPIMKPKS_CUT
            }

df_pipkmks = tools.get_dataframe('pipkmks', 'gluex1', 'data', filtered=False)
df_pimkpks = tools.get_dataframe('pimkpks', 'gluex1', 'data', filtered=False)

for cut in varied_cuts_dict_pipkmks:
    df_pipkmks = df_pipkmks.Filter(varied_cuts_dict_pipkmks[cut][0])
    df_pimkpks = df_pimkpks.Filter(varied_cuts_dict_pimkpks[cut][0])

output_path_pipkmks = '/work/halld/home/viducic/data/pipkmks/systematics'
output_path_pimkpks = '/work/halld/home/viducic/data/pimkpks/systematics'

df_pipkmks.Snapshot('pipkmks_loose', f'{output_path_pipkmks}/pipkmks_loose.root')
df_pimkpks.Snapshot('pimkpks_loose', f'{output_path_pimkpks}/pimkpks_loose.root')
