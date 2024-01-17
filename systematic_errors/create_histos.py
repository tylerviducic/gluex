import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts

ROOT.EnableImplicitMT()

# baseline_pipkmks, baseline_pimkpks = 35865, 41281
baseline_pipkmks, baseline_pimkpks = 32850, 37448

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


df_pipkmks_loose = ROOT.RDataFrame('pipkmks_loose', '/work/halld/home/viducic/data/pipkmks/systematics/pipkmks_loose.root')
df_pimkpks_loose = ROOT.RDataFrame('pimkpks_loose', '/work/halld/home/viducic/data/pimkpks/systematics/pimkpks_loose.root')


# TODO: loop over loose cuts. apply all nominal cuts except the one being varied. make histogram.
# TODO: then apply tight cut and make histogram. 
# TODO: first attempt to add strings together. 

# for nominal_cut in nominal_cuts_dict_pipkmks:
#     # varied_df_loose_pipkmks = df_pipkmks_loose.Filter('true')
#     # varied_df_tight_pipkmks = df_pipkmks_loose.Filter('true')
#     # varied_df_loose_pimkpks = df_pimkpks_loose.Filter('true')
#     # varied_df_tight_pimkpks = df_pimkpks_loose.Filter('true')
#     loose_cut_string = ''
#     for cut in varied_cuts_dict_pipkmks:
#         if cut == nominal_cut:

hists = []

for cut in varied_cuts_dict_pipkmks:
    loose_cut_string_pipkmks = f'({varied_cuts_dict_pipkmks[cut][0]})'
    tight_cut_string_pipkmks = f'({varied_cuts_dict_pipkmks[cut][1]})'
    for nominal_cut in nominal_cuts_dict_pipkmks:
        if nominal_cut != cut:
            loose_cut_string_pipkmks += f' && ({nominal_cuts_dict_pipkmks[nominal_cut]})'
            tight_cut_string_pipkmks += f' && ({nominal_cuts_dict_pipkmks[nominal_cut]})'
            nominal_cut_string_pipkmks = f'({nominal_cuts_dict_pipkmks[nominal_cut]})'
    print(f'loose cut string: {loose_cut_string_pipkmks}')
    print(f'tight cut string: {tight_cut_string_pipkmks}')
    print(f'nominal cut string: {nominal_cut_string_pipkmks}')

    hist_loose_pipkmks = df_pipkmks_loose.Filter(loose_cut_string_pipkmks).Histo1D(f'{cut}_loose', f'{cut}_loose')
    hist_tight_pipkmks = df_pipkmks_loose.Filter(tight_cut_string_pipkmks).Histo1D(f'{cut}_tight', f'{cut}_tight')
    hist_nominal_pipkmks = df_pipkmks_loose.Filter(nominal_cut_string_pipkmks).Histo1D(f'{cut}_nominal', f'{cut}_nominal')

    hists.append(hist_nominal_pipkmks, hist_loose_pipkmks, hist_tight_pipkmks)

c = ROOT.TCanvas('c', 'c', 1200, 900)
c.Divide(5, 2)
for i, hist in enumerate(hists):
    c.cd(i+1)
    hist[0].SetLineColor(ROOT.kBlack)
    hist[1].SetLineColor(ROOT.kRed)
    hist[2].SetLineColor(ROOT.kBlue)
    hist[0].Draw()
    hist[1].Draw('same')
    hist[2].Draw('same')

input('Press enter to exit.')

