"""
this file contains the cuts used for event selection cuts
it is broken down into compiled funcitons and string cuts
"""

import ROOT
from my_library.constants import KSHORT_FIT_MEAN, KSHORT_FIT_WIDTH


@ROOT.Numba.Declare(['float'], 'bool')
def kinfit_cl_cut(kinfit_cl):
    return kinfit_cl > 1e-5
KINFIT_CL_CUT = 'Numba::kinfit_cl_cut(kinfit_cl)'
KINFIT_CL_CUT_STRING = 'kinfit_cl > 1e-5'


@ROOT.Numba.Declare(['float'], 'bool')
def ks_pathlength_cut(pathlength_sig):
    return pathlength_sig > 5
KS_PATHLENGTH_CUT = 'Numba::ks_pathlength_cut(pathlength_sig)'
KS_PATHLENGTH_CUT_STRING = 'pathlength_sig > 5'


KS_COLIN_CUT_STRING = 'cos_colin > 0.99'
KS_VERTEX_CUT_STRING = ' vertex_distance > 3'
OLD_KS_MASS_CUT_STRING = 'ks_m > 0.475 && ks_m < 0.525'


@ROOT.Numba.Declare(['float'], 'bool')
def kshort_mass_cut(ks_m):
    return abs(ks_m - KSHORT_FIT_MEAN) < 2 * KSHORT_FIT_WIDTH
KS_MASS_CUT = 'Numba::kshort_mass_cut(ks_m)'
KS_MASS_CUT_STRING = f'abs(ks_m - {KSHORT_FIT_MEAN}) < 2 * {KSHORT_FIT_WIDTH}'


@ROOT.Numba.Declare(['float'], 'bool')
def ppip_mass_cut(ppip_m):
    return ppip_m > 1.4
PPIP_MASS_CUT = 'Numba::ppip_mass_cut(ppip_m)'
PPIP_MASS_CUT_STRING = 'ppip_m > 1.4'


@ROOT.Numba.Declare(['float'], 'bool')
def kmp_mass_cut(kmp_m):
    return kmp_m > 1.95
KMP_MASS_CUT = 'Numba::kmp_mass_cut(kmp_m)'
KMP_MASS_CUT_STRING = 'kmp_m > 2.0'


@ROOT.Numba.Declare(['float'], 'bool')
def kpp_mass_cut(kpp_m):
    return kpp_m > 1.95
KPP_MASS_CUT = 'Numba::kpp_mass_cut(kpp_m)'
KPP_MASS_CUT_STRING = 'kpp_m > 2.0'


@ROOT.Numba.Declare(['float'], 'bool')
def f1_signal_region_pipkmks(pipkmks_m):
    return pipkmks_m > 1.24 and pipkmks_m < 1.35
F1_SIGNAL_REGION_PIPKMKS = 'Numba::f1_signal_region_pipkmks(pipkmks_m)'
F1_SIGNAL_REGION_PIPKMKS_STRING = 'pipkmks_m > 1.24 && pipkmks_m < 1.35'


@ROOT.Numba.Declare(['float'], 'bool')
def f1_signal_region_pimkpks(pimkpks_m):
    return pimkpks_m > 1.24 and pimkpks_m < 1.35
F1_SIGNAL_REGION_PIMKPKS = 'Numba::f1_signal_region_pimkpks(pimkpks_m)'
F1_SIGNAL_REGION_PIMKPKS_STRING = 'pimkpks_m > 1.24 && pimkpks_m < 1.35'


@ROOT.Numba.Declare(['float'], 'bool')
def beam_range(e_beam):
    return e_beam >= 6.5 and e_beam <= 11.5
BEAM_RANGE = 'Numba::beam_range(e_beam)'
BEAM_RANGE_STRING = 'e_beam >= 6.5 && e_beam <= 11.5'


@ROOT.Numba.Declare(['float'], 'bool')
def t_range(mand_t):
    return mand_t >= 0.1 and mand_t <= 1.9
T_RANGE = 'Numba::t_range(mand_t)'
T_RANGE_STRING = 'mand_t >= 0.1 && mand_t <= 1.9'


@ROOT.Numba.Declare(['float'], 'bool')
def p_p_cut(p_p):
    return p_p > 0.4
P_P_CUT = 'Numba::p_p_cut(p_p)'
P_P_CUT_STRING = 'p_p > 0.4'


@ROOT.Numba.Declare(['float'], 'bool')
def mx2_ppipkmks_cut(mx2_ppipkmks):
    return abs(mx2_ppipkmks) < 0.01
MX2_PPIPKMKS_CUT = 'Numba::mx2_ppipkmks_cut(mx2_ppipkmks)'
MX2_PPIPKMKS_CUT_STRING = 'abs(mx2_ppipkmks) < 0.01'


@ROOT.Numba.Declare(['float'], 'bool')
def mx2_ppimkpks_cut(mx2_ppimkpks):
    return abs(mx2_ppimkpks) < 0.01
MX2_PPIMKPKS_CUT = 'Numba::mx2_ppimkpks_cut(mx2_ppimkpks)'
MX2_PPIMKPKS_CUT_STRING = 'abs(mx2_ppimkpks) < 0.01'


# PPIM_MASS_CUT = 'ppim_m > 1.8'
@ROOT.Numba.Declare(['float'], 'bool')
def ppim_mass_cut(ppim_m):
    return ppim_m > 1.4
PPIM_MASS_CUT = 'Numba::ppim_mass_cut(ppim_m)'
PPIM_MASS_CUT_STRING = 'ppim_m > 1.4'


@ROOT.Numba.Declare(['float'], 'bool')
def ksp_mass_cut(ksp_m):
    return ksp_m > 1.95
KSP_MASS_CUT = 'Numba::ksp_mass_cut(ksp_m)'
KSP_MASS_CUT_STRING = 'ksp_m > 2.0'

## KSTAR CUTS ##

@ROOT.Numba.Declare(['float'], 'bool')
def kstar_no_cut_pipkmks(kspip_m):
    return kspip_m > 0.0
KSTAR_NO_CUT_PIPKMKS = 'Numba::kstar_no_cut_pipkmks(kspip_m)'
KSTAR_NO_CUT_PIPKMKS_STRING = 'kspip_m > 0.0'


@ROOT.Numba.Declare(['float'], 'bool')
def kstar_plus_cut(kspip_m):
    return kspip_m < 0.8 or kspip_m > 1.0
KSTAR_PLUS_CUT = 'Numba::kstar_plus_cut(kspip_m)'
KSTAR_PLUS_CUT_STRING = 'kspip_m < 0.8 || kspip_m > 1.0'

@ROOT.Numba.Declare(['float'], 'bool')
def kstar_minus_cut(kspim_m):
    return kspim_m < 0.8 or kspim_m > 1.0
KSTAR_MINUS_CUT = 'Numba::kstar_minus_cut(kspim_m)'
KSTAR_MINUS_CUT_STRING = 'kspim_m < 0.8 || kspim_m > 1.0'


@ROOT.Numba.Declare(['float'], 'bool')
def kstar_zero_cut_pipkmks(kmpip_m):
    return kmpip_m < 0.8 or kmpip_m > 1.0
KSTAR_ZERO_CUT_PIPKMKS = 'Numba::kstar_zero_cut_pipkmks(kmpip_m)'
KSTAR_ZERO_CUT_PIPKMKS_STRING = 'kmpip_m < 0.8 || kmpip_m > 1.0'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def kstar_all_cut_pipkmks(kspip, kmpip):
    return (kspip < 0.8 or kspip > 1.0) and (kmpip < 0.8 or kmpip > 1.0)
KSTAR_ALL_CUT_PIPKMKS = 'Numba::kstar_all_cut_pipkmks(kspip_m, kmpip_m)'
KSTAR_ALL_CUT_PIPKMKS_STRING = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def keep_neutral_reject_charged_pipkmks(kspip, kmpip):
    return (kspip < 0.8 or kspip > 1.0) and (kmpip > 0.8 and kmpip < 1.0)
KEEP_NEUTRAL_REJECT_CHARGED_PIPKMKS = 'Numba::keep_neutral_reject_charged_pipkmks(kspip_m, kmpip_m)'
KEEP_NEUTRAL_REJECT_CHARGED_PIPKMKS_STRING = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m > 0.8 && kmpip_m < 1.0)'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def keep_charged_reject_neutral_pipkmks(kspip, kmpip):
    return (kspip > 0.8 and kspip < 1.0) and (kmpip < 0.8 or kmpip > 1.0)
KEEP_CHARGED_REJECT_NEUTRAL_PIPKMKS = 'Numba::keep_charged_reject_neutral_pipkmks(kspip_m, kmpip_m)'
KEEP_CHARGED_REJECT_NEUTRAL_PIPKMKS_STRING = '(kspip_m > 0.8 && kspip_m < 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'


@ROOT.Numba.Declare(['float'], 'bool')
def kstar_no_cut_pimkpks(kspim_m):
    return kspim_m > 0.0
KSTAR_NO_CUT_PIMKPKS = 'Numba::kstar_no_cut_pimkpks(kspim_m)'
KSTAR_NO_CUT_PIMKPKS_STRING = 'kspim_m > 0.0'


@ROOT.Numba.Declare(['float'], 'bool')
def kstar_zero_cut_pimkpks(kppim_m):
    return kppim_m < 0.8 or kppim_m > 1.0
KSTAR_ZERO_CUT_PIMKPKS = 'Numba::kstar_zero_cut_pimkpks(kppim_m)'
KSTAR_ZERO_CUT_PIMKPKS_STRING = 'kppim_m < 0.8 || kppim_m > 1.0'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def kstar_all_cut_pimkpks(kspim, kppim):
    return (kspim < 0.8 or kspim > 1.0) and (kppim < 0.8 or kppim > 1.0)
KSTAR_ALL_CUT_PIMKPKS = 'Numba::kstar_all_cut_pimkpks(kspim_m, kppim_m)'
KSTAR_ALL_CUT_PIMKPKS_STRING = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def keep_neutral_reject_charged_pimkpks(kspim, kppim):
    return (kspim < 0.8 or kspim > 1.0) and (kppim > 0.8 and kppim < 1.0)
KEEP_NEUTRAL_REJECT_CHARGED_PIMKPKS = 'Numba::keep_neutral_reject_charged_pimkpks(kspim_m, kppim_m)'
KEEP_NEUTRAL_REJECT_CHARGED_PIMKPKS_STRING = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m > 0.8 && kppim_m < 1.0)'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def keep_charged_reject_neutral_pimkpks(kspim, kppim):
    return (kspim > 0.8 and kspim < 1.0) and (kppim < 0.8 or kppim > 1.0)
KEEP_CHARGED_REJECT_NEUTRAL_PIMKPKS = 'Numba::keep_charged_reject_neutral_pimkpks(kspim_m, kppim_m)'
KEEP_CHARGED_REJECT_NEUTRAL_PIMKPKS_STRING = '(kspim_m > 0.8 && kspim_m < 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'


@ROOT.Numba.Declare(['float'], 'int')
def beam_bin_filter(e_beam):
    return int(e_beam-6.5) + 1
BEAM_BIN_FILTER = 'Numba::beam_bin_filter(e_beam)'


@ROOT.Numba.Declare(['float', 'float'], 'bool')
def select_beam_bin(e_bin, energy_index):
    return e_bin == energy_index
SELECT_BEAM_BIN = 'Numba::select_beam_bin(e_bin, {})'


@ROOT.Numba.Declare(['float'], 'int')
def t_bin_filter(t):
    if t <= 0.4:
        return int(t/0.1)
    elif t > 0.4 and t <= 0.9:
        return int((t-0.4)/0.25)+4
    elif t > 0.9 and t <= 1.9:
        return int((t-0.9)/0.5)+6
    else:
        return -1
T_BIN_FILTER = 'Numba::t_bin_filter(mand_t)'


@ROOT.Numba.Declare(['int', 'int'], 'bool')
def select_t_bin(t_bin, t_index):
    return t_bin == t_index
SELECT_T_BIN = 'Numba::select_t_bin(t_bin, {})'



# DICTIONARY FOR CALLING THESE FUNCTIONS

KSTAR_CUT_DICT_PIPKMKS = {
    'no': KSTAR_NO_CUT_PIPKMKS,
    'plus': KSTAR_PLUS_CUT,
    'zero': KSTAR_ZERO_CUT_PIPKMKS,
    'all': KSTAR_ALL_CUT_PIPKMKS
}


KSTAR_CUT_DICT_PIMKPKS = {
    'no': KSTAR_NO_CUT_PIMKPKS,
    'minus': KSTAR_MINUS_CUT,
    'zero': KSTAR_ZERO_CUT_PIMKPKS,
    'all': KSTAR_ALL_CUT_PIMKPKS
}

