import ROOT
import my_library.constants
import my_library.common_analysis_tools as tools
import my_library.kinematic_cuts as cuts
import os

ROOT.EnableImplicitMT()
os.nice(18)

# data_type = 'data'
data_type = 'signal'

cut_dict = {}

df_pipkmks = tools.get_dataframe('pipkmks', 'spring', data_type, filtered=False).Filter(cuts.F1_SIGNAL_REGION_PIPKMKS)
df_pimkpks = tools.get_dataframe('pimkpks', 'spring', data_type, filtered=False).Filter(cuts.F1_SIGNAL_REGION_PIMKPKS)

cut_dict['f1_region'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KINFIT_CL_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.KINFIT_CL_CUT)

cut_dict['kinfit_cl'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.MX2_PPIPKMKS_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.MX2_PPIMKPKS_CUT)

cut_dict['mx2_all'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.P_P_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.P_P_CUT)

cut_dict['pp'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KS_PATHLENGTH_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.KS_PATHLENGTH_CUT)

cut_dict['pathlength'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KS_MASS_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.KS_MASS_CUT)

cut_dict['ks_m'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.PPIP_MASS_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.PPIM_MASS_CUT)

cut_dict['ppi'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KMP_MASS_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.KPP_MASS_CUT)

cut_dict['kp'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KSP_MASS_CUT)
df_pimkpks = df_pimkpks.Filter(cuts.KSP_MASS_CUT)

cut_dict['ksp'] = (df_pipkmks.Count(), df_pimkpks.Count())

df_pipkmks = df_pipkmks.Filter(cuts.KSTAR_ALL_CUT_PIPKMKS)
df_pimkpks = df_pimkpks.Filter(cuts.KSTAR_ALL_CUT_PIMKPKS)

cut_dict['kstar'] = (df_pipkmks.Count(), df_pimkpks.Count())

n_pipkmks = cut_dict['f1_region'][0].GetValue()
n_pimkpks = cut_dict['f1_region'][1].GetValue()

for cut in cut_dict:
    print(f'{cut}: eff_pipkmks = {cut_dict[cut][0].GetValue()/n_pipkmks}, eff_pimkpks =  {cut_dict[cut][1].GetValue()/n_pimkpks}')
    n_pipkmks = cut_dict[cut][0].GetValue()
    n_pimkpks = cut_dict[cut][1].GetValue()





