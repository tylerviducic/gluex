import ROOT
import my_library.common_analysis_tools as tools
import my_library.constants as constants
import my_library.gluex_style as gluex_style
import my_library.kinematic_cuts as cuts
import os


"""this code is awful im sorry im in a rush i need to graduate"""

ROOT.EnableImplicitMT()

nbins, xlow, xhigh = 40, 1.1, 1.5

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

filepath_pipkmks = '/work/halld/home/viducic/data/pipkmks/systematics'
filepath_pimkpks = '/work/halld/home/viducic/data/pimkpks/systematics'

print('starting loop')

df_pipkmks_spring = ROOT.RDataFrame('pipkmks_loose', f'{filepath_pipkmks}/pipkmks_loose_spring.root')
df_pimkpks_spring = ROOT.RDataFrame('pimkpks_loose', f'{filepath_pimkpks}/pimkpks_loose_spring.root')
df_pipkmks_fall = ROOT.RDataFrame('pipkmks_loose', f'{filepath_pipkmks}/pipkmks_loose_fall.root')
df_pimkpks_fall = ROOT.RDataFrame('pimkpks_loose', f'{filepath_pimkpks}/pimkpks_loose_fall.root')
df_pipkmks_2017 = ROOT.RDataFrame('pipkmks_loose', f'{filepath_pipkmks}/pipkmks_loose_2017.root')
df_pimkpks_2017 = ROOT.RDataFrame('pimkpks_loose', f'{filepath_pimkpks}/pimkpks_loose_2017.root')
df_pipkmks_data = ROOT.RDataFrame('pipkmks_loose', f'{filepath_pipkmks}/pipkmks_loose.root')
df_pimkpks_data = ROOT.RDataFrame('pimkpks_loose', f'{filepath_pimkpks}/pimkpks_loose.root')

data_hists_pipkmks = []
data_hists_pimkpks = []
mc_hists_pipkmks_spring = []
mc_hists_pimkpks_spring = []
mc_hists_pipkmks_fall = []
mc_hists_pimkpks_fall = []
mc_hists_pipkmks_2017 = []
mc_hists_pimkpks_2017 = []


for cut in varied_cuts_dict_pipkmks:

    loose_cut_string_pipkmks = f'({varied_cuts_dict_pipkmks[cut][0]})'
    tight_cut_string_pipkmks = f'({varied_cuts_dict_pipkmks[cut][1]})'
    nominal_cut_string_pipkmks = f'({nominal_cuts_dict_pipkmks[cut]})'

    loose_cut_string_pimkpks = f'({varied_cuts_dict_pimkpks[cut][0]})'
    tight_cut_string_pimkpks = f'({varied_cuts_dict_pimkpks[cut][1]})'
    nominal_cut_string_pimkpks = f'({nominal_cuts_dict_pimkpks[cut]})'

    for nominal_cut in nominal_cuts_dict_pipkmks:
        nominal_cut_string_pipkmks += f' && ({nominal_cuts_dict_pipkmks[nominal_cut]})'
        nominal_cut_string_pimkpks += f' && ({nominal_cuts_dict_pimkpks[nominal_cut]})'
        if nominal_cut != cut:
            loose_cut_string_pipkmks += f' && ({nominal_cuts_dict_pipkmks[nominal_cut]})'
            tight_cut_string_pipkmks += f' && ({nominal_cuts_dict_pipkmks[nominal_cut]})'
            loose_cut_string_pimkpks += f' && ({nominal_cuts_dict_pimkpks[nominal_cut]})'
            tight_cut_string_pimkpks += f' && ({nominal_cuts_dict_pimkpks[nominal_cut]})'

    data_hist_integrated_pipkmks_nominal = df_pipkmks_data.Filter(nominal_cut_string_pipkmks).Histo1D((f'pipkmks_data_integrated_{cut}_nominal', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_nominal_spring = df_pipkmks_spring.Filter(nominal_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_nominal_spring', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_nominal_fall = df_pipkmks_fall.Filter(nominal_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_nominal_fall', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_nominal_2017 = df_pipkmks_2017.Filter(nominal_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_nominal_2017', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
    data_hist_integrated_pimkpks_nominal = df_pimkpks_data.Filter(nominal_cut_string_pimkpks).Histo1D((f'pimkpks_data_integrated_{cut}_nominal', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_nominal_spring = df_pimkpks_spring.Filter(nominal_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_nominal_spring', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_nominal_fall = df_pimkpks_fall.Filter(nominal_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_nominal_fall', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_nominal_2017 = df_pimkpks_2017.Filter(nominal_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_nominal_2017', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')

    data_hist_integrated_pipkmks_loose = df_pipkmks_data.Filter(loose_cut_string_pipkmks).Histo1D((f'pipkmks_data_integrated_{cut}_loose', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_loose_spring = df_pipkmks_spring.Filter(loose_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_loose_spring', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_loose_fall = df_pipkmks_fall.Filter(loose_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_loose_fall', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_loose_2017 = df_pipkmks_2017.Filter(loose_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_loose_2017', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
    data_hist_integrated_pimkpks_loose = df_pimkpks_data.Filter(loose_cut_string_pimkpks).Histo1D((f'pimkpks_data_integrated_{cut}_loose', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_loose_spring = df_pimkpks_spring.Filter(loose_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_loose_spring', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_loose_fall = df_pimkpks_fall.Filter(loose_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_loose_fall', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_loose_2017 = df_pimkpks_2017.Filter(loose_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_loose_2017', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
    
    data_hist_integrated_pipkmks_tight = df_pipkmks_data.Filter(tight_cut_string_pipkmks).Histo1D((f'pipkmks_data_integrated_{cut}_tight', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_tight_spring = df_pipkmks_spring.Filter(tight_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_tight_spring', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_tight_fall = df_pipkmks_fall.Filter(tight_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_tight_fall', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
    signal_hist_integrated_pipkmks_tight_2017 = df_pipkmks_2017.Filter(tight_cut_string_pipkmks).Histo1D((f'pipkmks_signal_integrated_{cut}_tight_2017', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
    data_hist_integrated_pimkpks_tight = df_pimkpks_data.Filter(tight_cut_string_pimkpks).Histo1D((f'pimkpks_data_integrated_{cut}_tight', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_tight_spring = df_pimkpks_spring.Filter(tight_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_tight_spring', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_tight_fall = df_pimkpks_fall.Filter(tight_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_tight_fall', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
    signal_hist_integrated_pimkpks_tight_2017 = df_pimkpks_2017.Filter(tight_cut_string_pimkpks).Histo1D((f'pimkpks_signal_integrated_{cut}_tight_2017', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
    
    data_hists_pipkmks.extend([data_hist_integrated_pipkmks_nominal, data_hist_integrated_pipkmks_loose, data_hist_integrated_pipkmks_tight])
    mc_hists_pipkmks_spring.extend([signal_hist_integrated_pipkmks_nominal_spring, signal_hist_integrated_pipkmks_loose_spring, signal_hist_integrated_pipkmks_tight_spring])
    mc_hists_pipkmks_fall.extend([signal_hist_integrated_pipkmks_nominal_fall, signal_hist_integrated_pipkmks_loose_fall, signal_hist_integrated_pipkmks_tight_fall])
    mc_hists_pipkmks_2017.extend([signal_hist_integrated_pipkmks_nominal_2017, signal_hist_integrated_pipkmks_loose_2017, signal_hist_integrated_pipkmks_tight_2017])
    data_hists_pimkpks.extend([data_hist_integrated_pimkpks_nominal, data_hist_integrated_pimkpks_loose, data_hist_integrated_pimkpks_tight])
    mc_hists_pimkpks_spring.extend([signal_hist_integrated_pimkpks_nominal_spring, signal_hist_integrated_pimkpks_loose_spring, signal_hist_integrated_pimkpks_tight_spring])
    mc_hists_pimkpks_fall.extend([signal_hist_integrated_pimkpks_nominal_fall, signal_hist_integrated_pimkpks_loose_fall, signal_hist_integrated_pimkpks_tight_fall])
    mc_hists_pimkpks_2017.extend([signal_hist_integrated_pimkpks_nominal_2017, signal_hist_integrated_pimkpks_loose_2017, signal_hist_integrated_pimkpks_tight_2017])


    for e in range(8, 12):

        e_filter_string = f'(e_beam > {e - 0.5}) && (e_beam < {e + 0.5})'
        for t in range(1, 8):
            print(f'e: {e}, t: {t}')
            t_filter_string = cuts.SELECT_T_BIN.format(t)
        
            data_hist_pipkmks_nominal = df_pipkmks_data.Filter(nominal_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_data_{cut}_nominal_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_nominal_spring = df_pipkmks_spring.Filter(nominal_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_nominal_spring_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_nominal_fall = df_pipkmks_fall.Filter(nominal_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_nominal_fall_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_nominal_2017 = df_pipkmks_2017.Filter(nominal_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_nominal_2017_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pipkmks_m')
            data_hist_pimkpks_nominal = df_pimkpks_data.Filter(nominal_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_data_{cut}_nominal_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_nominal_spring = df_pimkpks_spring.Filter(nominal_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_nominal_spring_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_nominal_fall = df_pimkpks_fall.Filter(nominal_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_nominal_fall_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_nominal_2017 = df_pimkpks_2017.Filter(nominal_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_nominal_2017_e{e}_t{t}', f'{cut}_nominal', nbins, xlow, xhigh), 'pimkpks_m')

            data_hist_pipkmks_loose = df_pipkmks_data.Filter(loose_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_data_{cut}_loose_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_loose_spring = df_pipkmks_spring.Filter(loose_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_loose_spring_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_loose_fall = df_pipkmks_fall.Filter(loose_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_loose_fall_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_loose_2017 = df_pipkmks_2017.Filter(loose_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_loose_2017_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pipkmks_m')
            data_hist_pimkpks_loose = df_pimkpks_data.Filter(loose_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_data_{cut}_loose_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_loose_spring = df_pimkpks_spring.Filter(loose_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_loose_spring_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_loose_fall = df_pimkpks_fall.Filter(loose_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_loose_fall_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_loose_2017 = df_pimkpks_2017.Filter(loose_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_loose_2017_e{e}_t{t}', f'{cut}_loose', nbins, xlow, xhigh), 'pimkpks_m')

            data_hist_pipkmks_tight = df_pipkmks_data.Filter(tight_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_data_{cut}_tight_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_tight_spring = df_pipkmks_spring.Filter(tight_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_tight_spring_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_tight_fall = df_pipkmks_fall.Filter(tight_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_tight_fall_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
            signal_hist_pipkmks_tight_2017 = df_pipkmks_2017.Filter(tight_cut_string_pipkmks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pipkmks_signal_{cut}_tight_2017_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pipkmks_m')
            data_hist_pimkpks_tight = df_pimkpks_data.Filter(tight_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_data_{cut}_tight_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_tight_spring = df_pimkpks_spring.Filter(tight_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_tight_spring_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_tight_fall = df_pimkpks_fall.Filter(tight_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_tight_fall_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')
            signal_hist_pimkpks_tight_2017 = df_pimkpks_2017.Filter(tight_cut_string_pimkpks).Filter(e_filter_string).Filter(t_filter_string).Histo1D((f'pimkpks_signal_{cut}_tight_2017_e{e}_t{t}', f'{cut}_tight', nbins, xlow, xhigh), 'pimkpks_m')

            data_hists_pipkmks.extend([data_hist_pipkmks_nominal, data_hist_pipkmks_loose, data_hist_pipkmks_tight])
            mc_hists_pipkmks_spring.extend([signal_hist_pipkmks_nominal_spring, signal_hist_pipkmks_loose_spring, signal_hist_pipkmks_tight_spring])
            mc_hists_pipkmks_fall.extend([signal_hist_pipkmks_nominal_fall, signal_hist_pipkmks_loose_fall, signal_hist_pipkmks_tight_fall])
            mc_hists_pipkmks_2017.extend([signal_hist_pipkmks_nominal_2017, signal_hist_pipkmks_loose_2017, signal_hist_pipkmks_tight_2017])
            data_hists_pimkpks.extend([data_hist_pimkpks_nominal, data_hist_pimkpks_loose, data_hist_pimkpks_tight])
            mc_hists_pimkpks_spring.extend([signal_hist_pimkpks_nominal_spring, signal_hist_pimkpks_loose_spring, signal_hist_pimkpks_tight_spring])
            mc_hists_pimkpks_fall.extend([signal_hist_pimkpks_nominal_fall, signal_hist_pimkpks_loose_fall, signal_hist_pimkpks_tight_fall])
            mc_hists_pimkpks_2017.extend([signal_hist_pimkpks_nominal_2017, signal_hist_pimkpks_loose_2017, signal_hist_pimkpks_tight_2017])



df_pipkmks_data.Count().GetValue()
df_pipkmks_spring.Count().GetValue()
df_pipkmks_fall.Count().GetValue()
df_pipkmks_2017.Count().GetValue()
df_pimkpks_data.Count().GetValue()
df_pimkpks_spring.Count().GetValue()
df_pimkpks_fall.Count().GetValue()
df_pimkpks_2017.Count().GetValue()

# c = ROOT.TCanvas('c', 'c', 900, 900)
# c.Divide(5, 2)
# for i, hist in enumerate(integrated_data_hists_pipkmks):
#     hist[0].SetLineColor(ROOT.kBlack)
#     hist[1].SetLineColor(ROOT.kRed)
#     hist[2].SetLineColor(ROOT.kBlue)
#     hist[1].GetXaxis().SetTitle(hist[0].GetName())
#     c.cd(i + 1)
#     hist[1].Draw()
#     hist[0].Draw('same')
#     hist[2].Draw('same')
#     c.Update()
# c.Draw()

# input('press enter to continue')

path_to_output_pipkmks = '/work/halld/home/viducic/data/pipkmks/systematics/hists'
path_to_output_pimkpks = '/work/halld/home/viducic/data/pimkpks/systematics/hists'

print('writing out histograms to file')

output_file_data_pipkmks = ROOT.TFile(f'{path_to_output_pipkmks}/pipkmks_data.root', 'RECREATE')
for hist in data_hists_pipkmks:
    print(hist.GetName())
    hist.Write()
output_file_data_pipkmks.Close()

output_file_data_pimkpks = ROOT.TFile(f'{path_to_output_pimkpks}/pimkpks_data.root', 'RECREATE')
for hist in data_hists_pimkpks:
    hist.Write()
output_file_data_pimkpks.Close()

output_file_mc_pipkmks_spring = ROOT.TFile(f'{path_to_output_pipkmks}/pipkmks_mc_spring.root', 'RECREATE')
for hist in mc_hists_pipkmks_spring:
    hist.Write()
output_file_mc_pipkmks_spring.Close()

output_file_mc_pimkpks_spring = ROOT.TFile(f'{path_to_output_pimkpks}/pimkpks_mc_spring.root', 'RECREATE')
for hist in mc_hists_pimkpks_spring:
    hist.Write()
output_file_mc_pimkpks_spring.Close()

output_file_mc_pipkmks_fall = ROOT.TFile(f'{path_to_output_pipkmks}/pipkmks_mc_fall.root', 'RECREATE')
for hist in mc_hists_pipkmks_fall:
    hist.Write()
output_file_mc_pipkmks_fall.Close()

output_file_mc_pimkpks_fall = ROOT.TFile(f'{path_to_output_pimkpks}/pimkpks_mc_fall.root', 'RECREATE')
for hist in mc_hists_pimkpks_fall:
    hist.Write()
output_file_mc_pimkpks_fall.Close()

output_file_mc_pipkmks_2017 = ROOT.TFile(f'{path_to_output_pipkmks}/pipkmks_mc_2017.root', 'RECREATE')
for hist in mc_hists_pipkmks_2017:
    hist.Write()
output_file_mc_pipkmks_2017.Close()

output_file_mc_pimkpks_2017 = ROOT.TFile(f'{path_to_output_pimkpks}/pimkpks_mc_2017.root', 'RECREATE')
for hist in mc_hists_pimkpks_2017:
    hist.Write()
output_file_mc_pimkpks_2017.Close()

print('done')