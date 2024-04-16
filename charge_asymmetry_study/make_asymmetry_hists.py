
import ROOT
import my_library.common_analysis_tools as tools
import my_library.kinematic_cuts as kcuts
import my_library.constants as constants
import os

ROOT.EnableImplicitMT()
os.nice(18)
ROOT.gStyle.SetOptStat(0)

df_pipkmks = tools.get_dataframe('pipkmks', 'gluex1', 'data', filtered=False)
df_pimkpks = tools.get_dataframe('pimkpks', 'gluex1', 'data', filtered=False)

df_pipkmks = df_pipkmks.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIPKMKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.P_P_CUT)
df_pimkpks = df_pimkpks.Filter(kcuts.KINFIT_CL_CUT).Filter(kcuts.MX2_PPIMKPKS_CUT).Filter(kcuts.KS_PATHLENGTH_CUT).Filter(kcuts.KS_MASS_CUT).Filter(kcuts.P_P_CUT)

df_pipkmks_kstar_cut = df_pipkmks.Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS)
df_pimkpks_kstar_cut = df_pimkpks.Filter(kcuts.KSTAR_ALL_CUT_PIMKPKS)

df_pipkmks_all_cuts = df_pipkmks.Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT)
df_pimkpks_all_cuts = df_pimkpks.Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT)

df_pipkmks_all_cuts_kstar_cut = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ALL_CUT_PIPKMKS)
df_pimkpks_all_cuts_kstar_cut = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ALL_CUT_PIMKPKS)

hist_file = ROOT.TFile('asym_hists.root', 'recreate')


# ## $KK\pi$ Plots 

# #### Integrated E and t $KK\pi$ Plots with and without K* Rejection

n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max = 90, 1.1, 2.0
n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max = 40, 1.1, 1.5
n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max = 11, 1.24, 1.35

hist_pipkmks = df_pipkmks_all_cuts.Histo1D(('pipkmks_no_cut', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max), 'pipkmks_m')
hist_pipkmks_kstar_cut = df_pipkmks_all_cuts_kstar_cut.Histo1D(('pipkmks_kstar_cut', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks = df_pimkpks_all_cuts.Histo1D(('pimkpks_no_cut', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max), 'pimkpks_m')
hist_pimkpks_kstar_cut = df_pimkpks_all_cuts_kstar_cut.Histo1D(('pimkpks_kstar_cut', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')



# #### Integrated E, binned in t $KK\pi$ plots with and without K* Rejection

pipkmks_hists = []
pimkpks_hists = []
pipkmks_kstar_cut_hists = []
pimkpks_kstar_cut_hists = []
for t in constants.ALLOWED_T_BINS:
    pipkmks_hists.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_t_bin_{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max), 'pipkmks_m'))
    pipkmks_kstar_cut_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_kstar_cut_t_bin_{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    pimkpks_hists.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_t_bin_{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max), 'pimkpks_m'))
    pimkpks_kstar_cut_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_kstar_cut_t_bin_{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    
    

# ## Particle Kinematics Plots 
# **All Plots Will Have K\* Rejection Applied**

# ### Kaon Kinematics 

# #### Integrated Distributions

n_bins_kaon_p, kaon_p_min, kaon_p_max = 50, 0, 8
n_bins_kaon_theta, kaon_theta_min, kaon_theta_max = 20, 0, 20

hist_km_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('km_p', 'p_{K^{-}}', n_bins_kaon_p, kaon_p_min, kaon_p_max), 'km_p')
hist_kp_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('kp_p', 'p_{K^{+}}', n_bins_kaon_p, kaon_p_min, kaon_p_max), 'kp_p')
hist_km_theta = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('km_theta', '#theta_{K^{-}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max), 'km_theta')
hist_kp_theta = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('kp_theta', '#theta_{K^{+}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max), 'kp_theta')
hist_km_theta_vs_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo2D(('km_theta_vs_p', '#theta_{K^{-}} vs p_{K^{-}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kaon_p, kaon_p_min, kaon_p_max), 'km_theta', 'km_p')
hist_kp_theta_vs_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo2D(('kp_theta_vs_p', '#theta_{K^{+}} vs p_{K^{+}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kaon_p, kaon_p_min, kaon_p_max), 'kp_theta', 'kp_p')
hist_km_p_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('km_p_vs_pipkmks', 'p_{K^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kaon_p, kaon_p_min, kaon_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'km_p', 'pipkmks_m')
hist_kp_p_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('kp_p_vs_pimkpks', 'p_{K^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kaon_p, kaon_p_min, kaon_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'kp_p', 'pimkpks_m')
hist_km_theta_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('km_theta_vs_pipkmks', '#theta_{K^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'km_theta', 'pipkmks_m')
hist_kp_theta_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('kp_theta_vs_pimkpks', '#theta_{K^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'kp_theta', 'pimkpks_m')

# #### Binned Distributions

ks_pipkmks_p_hists = []
ks_pimkpks_p_hists = []
ks_pipkmks_theta_hists = []
ks_pimkpks_theta_hists = []
ks_pipkmks_theta_vs_p_hists = []
ks_pimkpks_theta_vs_p_hists = []
ks_pipkmks_p_vs_pipkmks_hists = []
ks_pimkpks_p_vs_pimkpks_hists = []
ks_pipkmks_theta_vs_pipkmks_hists = []
ks_pimkpks_theta_vs_pimkpks_hists = []

for t in constants.ALLOWED_T_BINS:
    ks_pipkmks_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'km_p_t{t}', 'p_{K^{-}}', n_bins_kaon_p, kaon_p_min, kaon_p_max), 'km_p'))
    ks_pimkpks_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kp_p_t{t}', 'p_{K^{+}}', n_bins_kaon_p, kaon_p_min, kaon_p_max), 'kp_p'))
    ks_pipkmks_theta_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'km_theta_t{t}', '#theta_{K^{-}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max), 'km_theta'))
    ks_pimkpks_theta_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kp_theta_t{t}', '#theta_{K^{+}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max), 'kp_theta'))
    ks_pipkmks_theta_vs_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'km_theta_vs_p_t{t}', '#theta_{K^{-}} vs p_{K^{-}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kaon_p, kaon_p_min, kaon_p_max), 'km_theta', 'km_p'))
    ks_pimkpks_theta_vs_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kp_theta_vs_p_t{t}', '#theta_{K^{+}} vs p_{K^{+}}', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kaon_p, kaon_p_min, kaon_p_max), 'kp_theta', 'kp_p'))
    ks_pipkmks_p_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'km_p_vs_pipkmks_t{t}', 'p_{K^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kaon_p, kaon_p_min, kaon_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'km_p', 'pipkmks_m'))
    ks_pimkpks_p_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kp_p_vs_pimkpks_t{t}', 'p_{K^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kaon_p, kaon_p_min, kaon_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'kp_p', 'pimkpks_m'))
    ks_pipkmks_theta_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'km_theta_vs_pipkmks_t{t}', '#theta_{K^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'km_theta', 'pipkmks_m'))
    ks_pimkpks_theta_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kp_theta_vs_pimkpks_t{t}', '#theta_{K^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kaon_theta, kaon_theta_min, kaon_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'kp_theta', 'pimkpks_m'))

# ### Pion Kinematics 

# #### Integrated Distributions

n_bins_pion_p, pion_p_min, pion_p_max = 50, 0, 8
n_bins_pion_theta, pion_theta_min, pion_theta_max = 20, 0, 20

hist_pip1_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pip1_p', 'p_{#pi^{+}}', n_bins_pion_p,pion_p_min,pion_p_max), 'pip1_p')
hist_pim1_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pim1_p', 'p_{#pi^{-}}', n_bins_pion_p,pion_p_min,pion_p_max), 'pim1_p')
hist_pip1_theta = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pip1_theta', '#Theta_{#pi^{+}}', n_bins_pion_theta,pion_theta_min,pion_theta_max), 'pip1_theta')
hist_pim1_theta = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pim1_theta', '#Theta_{#pi^{-}}', n_bins_pion_theta,pion_theta_min,pion_theta_max), 'pim1_theta')
hist_pip1_theta_vs_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo2D(('pip1_theta_vs_p', '#Theta_{#pi^{+}} vs p_{#pi^{+}}', n_bins_pion_theta,pion_theta_min,pion_theta_max, n_bins_pion_p,pion_p_min,pion_p_max), 'pip1_theta', 'pip1_p')
hist_pim1_theta_vs_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo2D(('pim1_theta_vs_p', '#Theta_{#pi^{-}} vs p_{#pi^{-}}', n_bins_pion_theta,pion_theta_min,pion_theta_max, n_bins_pion_p,pion_p_min,pion_p_max), 'pim1_theta', 'pim1_p')
hist_pip1_p_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pip1_p_vs_pipkmks', 'p_{#pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_pion_p,pion_p_min,pion_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip1_p', 'pipkmks_m')
hist_pim1_p_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pim1_p_vs_pimkpks', 'p_{#pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_pion_p,pion_p_min,pion_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim1_p', 'pimkpks_m')
hist_pip1_theta_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pip1_theta_vs_pipkmks', '#Theta_{#pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_pion_theta,pion_theta_min,pion_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip1_theta', 'pipkmks_m')
hist_pim1_theta_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pim1_theta_vs_pimkpks', '#Theta_{#pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_pion_theta,pion_theta_min,pion_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim1_theta', 'pimkpks_m')

# #### Binned Distributions

pip1_p_hists = []
pim1_p_hists = []
pip1_theta_hists = []
pim1_theta_hists = []
pip1_theta_vs_p_hists = []
pim1_theta_vs_p_hists = []
pip1_p_vs_pipkmks_hists = []
pim1_p_vs_pimkpks_hists = []
pip1_theta_vs_pipkmks_hists = []
pim1_theta_vs_pimkpks_hists = []

for t in constants.ALLOWED_T_BINS:
    pip1_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pip1_p_vs_pipkmks_p_t{t}', 'p_{#pi^{+}}', n_bins_pion_p, pion_p_min, pion_p_max), 'pip1_p'))
    pim1_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pim1_p_p_t{t}', 'p_{#pi^{-}}', n_bins_pion_p, pion_p_min, pion_p_max), 'pim1_p'))
    pip1_theta_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pip1_theta_t{t}', '#Theta_{#pi^{+}}', n_bins_pion_theta, pion_theta_min, pion_theta_max), 'pip1_theta'))
    pim1_theta_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pim1_p_theta_t{t}', '#Theta_{#pi^{-}}', n_bins_pion_theta, pion_theta_min, pion_theta_max), 'pim1_theta'))
    pip1_theta_vs_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pip1_theta_vs_p_t{t}', '#Theta_{#pi^{+}} vs p_{#pi^{+}}', n_bins_pion_theta, pion_theta_min, pion_theta_max, n_bins_pion_p, pion_p_min, pion_p_max), 'pip1_theta', 'pip1_p'))
    pim1_theta_vs_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim1_p_theta_vs_p_t{t}', '#Theta_{#pi^{-}} vs p_{#pi^{-}}', n_bins_pion_theta, pion_theta_min, pion_theta_max, n_bins_pion_p, pion_p_min, pion_p_max), 'pim1_theta', 'pim1_p'))
    pip1_p_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pip1_p_vs_pipkmks_p_vs_pipkmks_t{t}', 'p_{#pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_pion_p, pion_p_min, pion_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip1_p', 'pipkmks_m'))
    pim1_p_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim1_p_p_vs_pimkpks_t{t}', 'p_{#pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_pion_p, pion_p_min, pion_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim1_p', 'pimkpks_m'))
    pip1_theta_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pip1_theta_vs_pipkmks_t{t}', '#Theta_{#pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_pion_theta, pion_theta_min, pion_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip1_theta', 'pipkmks_m'))
    pim1_theta_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim1_p_theta_vs_pimkpks_t{t}', '#Theta_{#pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_pion_theta, pion_theta_min, pion_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim1_theta', 'pimkpks_m'))

# ### $K_{s}$ Kinematics 
# <a name="kspip"></a>

# #### Integrated Distributions

n_bins_ks_p, ks_p_min, ks_p_max = 50, 0, 8
n_bins_ks_theta, ks_theta_min, ks_theta_max = 20, 0, 20

hist_ks_pipkmks_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('ks_p_pipkmks', 'p_{K_{s}}', n_bins_ks_p, ks_p_min, ks_p_max), 'ks_p')
hist_ks_pimkpks_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('ks_p_pimkpks', 'p_{K_{s}}', n_bins_ks_p, ks_p_min, ks_p_max), 'ks_p')
hist_ks_pipkmks_theta = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('ks_theta_pipkmks', '#theta_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max), 'ks_theta')
hist_ks_pimkpks_theta = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('ks_theta_pimkpks', '#theta_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max), 'ks_theta')
hist_ks_pipkmks_theta_vs_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo2D(('ks_theta_vs_p_pipkmks', '#theta_{K_{s}} vs p_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_ks_p, ks_p_min, ks_p_max), 'ks_theta', 'ks_p')
hist_ks_pimkpks_theta_vs_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo2D(('ks_theta_vs_p_pimkpks', '#theta_{K_{s}} vs p_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_ks_p, ks_p_min, ks_p_max), 'ks_theta', 'ks_p')
hist_ks_pipkmks_p_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('ks_p_vs_pipkmks', 'p_{K_{s}} vs M(#pi^{+}K^{-}K_{S})', n_bins_ks_p, ks_p_min, ks_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_p', 'pipkmks_m')
hist_ks_pimkpks_p_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('ks_p_vs_pimkpks', 'p_{K_{s}} vs M(#pi^{-}K^{+}K_{S})', n_bins_ks_p, ks_p_min, ks_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_p', 'pimkpks_m')
hist_ks_pipkmks_theta_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('ks_theta_vs_pipkmks', '#theta_{K_{s}} vs M(#pi^{+}K^{-}K_{S})', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_theta', 'pipkmks_m')
hist_ks_pimkpks_theta_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('ks_theta_vs_pimkpks', '#theta_{K_{s}} vs M(#pi^{-}K^{+}K_{S})', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_theta', 'pimkpks_m')

# #### Binned Distributions

ks_pipkmks_p_hists = []
ks_pimkpks_p_hists = []
ks_pipkmks_theta_hists = []
ks_pimkpks_theta_hists = []
ks_pipkmks_theta_vs_p_hists = []
ks_pimkpks_theta_vs_p_hists = []
ks_pipkmks_p_vs_pipkmks_hists = []
ks_pimkpks_p_vs_pimkpks_hists = []
ks_pipkmks_theta_vs_pipkmks_hists = []
ks_pimkpks_theta_vs_pimkpks_hists = []

for t in constants.ALLOWED_T_BINS:
    ks_pipkmks_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'ks_pipkmks_p_t{t}', 'p_{K_{s}}', n_bins_ks_p, ks_p_min, ks_p_max), 'ks_p'))
    ks_pimkpks_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'ks_pimkpks_p_t{t}', 'p_{K_{s}}', n_bins_ks_p, ks_p_min, ks_p_max), 'ks_p'))
    ks_pipkmks_theta_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'ks_pipkmks_theta_t{t}', '#theta_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max), 'ks_theta'))
    ks_pimkpks_theta_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'ks_pimkpks_theta_t{t}', '#theta_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max), 'ks_theta'))
    ks_pipkmks_theta_vs_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pipkmks_theta_vs_p_t{t}', '#theta_{K_{s}} vs p_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_ks_p, ks_p_min, ks_p_max), 'ks_theta', 'ks_p'))
    ks_pimkpks_theta_vs_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pimkpks_theta_vs_p_t{t}', '#theta_{K_{s}} vs p_{K_{s}}', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_ks_p, ks_p_min, ks_p_max), 'ks_theta', 'ks_p'))
    ks_pipkmks_p_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pipkmks_p_vs_pipkmks_t{t}', 'p_{K_{s}} vs M(#pi^{+}K^{-}K_{S})', n_bins_ks_p, ks_p_min, ks_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_p', 'pipkmks_m'))
    ks_pimkpks_p_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pimkpks_p_vs_pimkpks_t{t}', 'p_{K_{s}} vs M(#pi^{-}K^{+}K_{S})', n_bins_ks_p, ks_p_min, ks_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_p', 'pimkpks_m'))
    ks_pipkmks_theta_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pipkmks_theta_vs_pipkmks_t{t}', '#theta_{K_{s}} vs M(#pi^{+}K^{-}K_{S})', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_theta', 'pipkmks_m'))
    ks_pimkpks_theta_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'ks_pimkpks_theta_vs_pimkpks_t{t}', '#theta_{K_{s}} vs M(#pi^{-}K^{+}K_{S})', n_bins_ks_theta, ks_theta_min, ks_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'ks_theta', 'pimkpks_m'))

# ### $K_s \rightarrow \pi^+$ Kinematics
# 

# #### Integrated Distributions

n_bins_kspip_p, kspip_p_min, kspip_p_max = 50, 0, 8
n_bins_kspip_theta, kspip_theta_min, kspip_theta_max = 20, 0, 20

hist_pip2_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pip2_p', 'p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_p,kspip_p_min,kspip_p_max), 'pip2_p')
hist_pip_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pip_p', 'p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_p,kspip_p_min,kspip_p_max), 'pip_p')
hist_pip2_theta = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pip2_theta', '#Theta_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max), 'pip2_theta')
hist_pip_theta = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pip_theta', '#Theta_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max), 'pip_theta')
hist_pip2_theta_vs_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo2D(('pip2_theta_vs_p', '#Theta_{K_{s} #rightarrow #pi^{+}} vs p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max, n_bins_kspip_p,kspip_p_min,kspip_p_max), 'pip2_theta', 'pip2_p')
hist_pip_theta_vs_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo2D(('pip_theta_vs_p', '#Theta_{K_{s} #rightarrow #pi^{+}} vs p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max, n_bins_kspip_p,kspip_p_min,kspip_p_max), 'pip_theta', 'pip_p')
hist_pip2_p_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pip2_p_vs_pipkmks', 'p_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspip_p,kspip_p_min,kspip_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip2_p', 'pipkmks_m')
hist_pip_p_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pip_p_vs_pimkpks', 'p_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspip_p,kspip_p_min,kspip_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip_p', 'pimkpks_m')
hist_pip2_theta_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pip2_theta_vs_pipkmks', '#Theta_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip2_theta', 'pipkmks_m')
hist_pip_theta_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pip_theta_vs_pimkpks', '#Theta_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspip_theta,kspip_theta_min,kspip_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip_theta', 'pimkpks_m')

# #### Binned Distributions

pip2_p_hists = []
pip_p_hists = []
pip2_theta_hists = []
pip_theta_hists = []
pip2_theta_vs_p_hists = []
pip_theta_vs_p_hists = []
pip2_p_vs_pipkmks_hists = []
pip_p_vs_pimkpks_hists = []
pip2_theta_vs_pipkmks_hists = []
pip_theta_vs_pimkpks_hists = []

for t in constants.ALLOWED_T_BINS:
    pip2_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pip2_p_vs_pipkmks_p_t{t}', 'p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_p, kspip_p_min, kspip_p_max), 'pip2_p'))
    pip_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pip_p_p_t{t}', 'p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_p, kspip_p_min, kspip_p_max), 'pip_p'))
    pip2_theta_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pip2_theta_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max), 'pip2_theta'))
    pip_theta_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pip_p_theta_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max), 'pip_theta'))
    pip2_theta_vs_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pip2_theta_vs_p_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}} vs p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max, n_bins_kspip_p, kspip_p_min, kspip_p_max), 'pip2_theta', 'pip2_p'))
    pip_theta_vs_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pip_p_theta_vs_p_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}} vs p_{K_{s} #rightarrow #pi^{+}}', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max, n_bins_kspip_p, kspip_p_min, kspip_p_max), 'pip_theta', 'pip_p'))
    pip2_p_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pip2_p_vs_pipkmks_p_vs_pipkmks_t{t}', 'p_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspip_p, kspip_p_min, kspip_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip2_p', 'pipkmks_m'))
    pip_p_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pip_p_p_vs_pimkpks_t{t}', 'p_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspip_p, kspip_p_min, kspip_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip_p', 'pimkpks_m'))
    pip2_theta_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pip2_theta_vs_pipkmks_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip2_theta', 'pipkmks_m'))
    pip_theta_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pip_p_theta_vs_pimkpks_t{t}', '#Theta_{K_{s} #rightarrow #pi^{+}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspip_theta, kspip_theta_min, kspip_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pip_theta', 'pimkpks_m'))


# ### $K_s \rightarrow \pi^-$ Kinematics 

# #### Integrated Distributions

n_bins_kspim_p, kspim_p_min, kspim_p_max = 50, 0, 8
n_bins_kspim_theta, kspim_theta_min, kspim_theta_max = 20, 0, 20

hist_pim_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pim_p', 'p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_p,kspim_p_min,kspim_p_max), 'pim_p')
hist_pim2_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pim2_p', 'p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_p,kspim_p_min,kspim_p_max), 'pim2_p')
hist_pim_theta = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo1D(('pim_theta', '#Theta_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max), 'pim_theta')
hist_pim2_theta = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo1D(('pim2_theta', '#Theta_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max), 'pim2_theta')
hist_pim_theta_vs_p = df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Histo2D(('pim_theta_vs_p', '#Theta_{K_{s} #rightarrow #pi^{-}} vs p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max, n_bins_kspim_p,kspim_p_min,kspim_p_max), 'pim_theta', 'pim_p')
hist_pim2_theta_vs_p = df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Histo2D(('pim2_theta_vs_p', '#Theta_{K_{s} #rightarrow #pi^{-}} vs p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max, n_bins_kspim_p,kspim_p_min,kspim_p_max), 'pim2_theta', 'pim2_p')
hist_pim_p_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pim_p_vs_pipkmks', 'p_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspim_p,kspim_p_min,kspim_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim_p', 'pipkmks_m')
hist_pim2_p_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pim2_p_vs_pimkpks', 'p_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspim_p,kspim_p_min,kspim_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim2_p', 'pimkpks_m')
hist_pim_theta_vs_pipkmks = df_pipkmks_all_cuts_kstar_cut.Histo2D(('pim_theta_vs_pipkmks', '#Theta_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim_theta', 'pipkmks_m')
hist_pim2_theta_vs_pimkpks = df_pimkpks_all_cuts_kstar_cut.Histo2D(('pim2_theta_vs_pimkpks', '#Theta_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspim_theta,kspim_theta_min,kspim_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim2_theta', 'pimkpks_m')

# #### Binned Distributions

pim_p_hists = []
pim2_p_hists = []
pim_theta_hists = []
pim2_theta_hists = []
pim_theta_vs_p_hists = []
pim2_theta_vs_p_hists = []
pim_p_vs_pipkmks_hists = []
pim2_p_vs_pimkpks_hists = []
pim_theta_vs_pipkmks_hists = []
pim2_theta_vs_pimkpks_hists = []

for t in constants.ALLOWED_T_BINS:
    pim_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pim_p_vs_pipkmks_p_t{t}', 'p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_p, kspim_p_min, kspim_p_max), 'pim_p'))
    pim2_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pim2_p_p_t{t}', 'p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_p, kspim_p_min, kspim_p_max), 'pim2_p'))
    pim_theta_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pim_theta_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max), 'pim_theta'))
    pim2_theta_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'hist_pim2_p_theta_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max), 'pim2_theta'))
    pim_theta_vs_p_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pim_theta_vs_p_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}} vs p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max, n_bins_kspim_p, kspim_p_min, kspim_p_max), 'pim_theta', 'pim_p'))
    pim2_theta_vs_p_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim2_p_theta_vs_p_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}} vs p_{K_{s} #rightarrow #pi^{-}}', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max, n_bins_kspim_p, kspim_p_min, kspim_p_max), 'pim2_theta', 'pim2_p'))
    pim_p_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim_p_vs_pipkmks_p_vs_pipkmks_t{t}', 'p_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspim_p, kspim_p_min, kspim_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim_p', 'pipkmks_m'))
    pim2_p_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim2_p_p_vs_pimkpks_t{t}', 'p_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspim_p, kspim_p_min, kspim_p_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim2_p', 'pimkpks_m'))
    pim_theta_vs_pipkmks_hists.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'pim_theta_vs_pipkmks_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{+}K^{-}K_{S})', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim_theta', 'pipkmks_m'))
    pim2_theta_vs_pimkpks_hists.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'hist_pim2_p_theta_vs_pimkpks_t{t}', '#Theta_{K_{s} #rightarrow #pi^{-}} vs M(#pi^{-}K^{+}K_{S})', n_bins_kspim_theta, kspim_theta_min, kspim_theta_max, n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pim2_theta', 'pimkpks_m'))

# ## Particle Mass Combos
# 1. whole mass range with shading for cut
# 2. $1.24 < M(KK\pi) < 1.35$ with shading for cut
# 3. $KK\pi$ vs $p\pi$ for $1.24 < M(KK\pi) < 1.35$
# 4. $KK\pi$ vs $p\pi$ for $1.1 < M(KK\pi) < 1.6$ 
# 5. $KK\pi$ with and without cut on quantity 

# ### $p\pi$

# #### Integrated Distributions

n_bins_ppi, ppi_min, ppi_max = 100, 1.0, 3.0
hist_ppip = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppip', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m')
hist_ppim = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppim', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m')
hist_ppip_shaded = df_pipkmks_kstar_cut.Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppip_shaded', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m')
hist_ppim_shaded = df_pimkpks_kstar_cut.Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppim_shaded', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m')
hist_ppip_f1 = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppip_shaded', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m')
hist_ppim_f1 = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppim_shaded', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m')
hist_ppip_f1_shaded = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppip_f1_shaded', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m')
hist_ppim_f1_shaded = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('ppim_f1_shaded', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m')
hist_ppip_vs_kkpi_f1 = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D(('ppip_vs_kkpi_f1', 'M(p#pi^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_ppi, ppi_min, ppi_max,), 'pipkmks_m', 'ppip_m')
hist_ppim_vs_kkpi_f1 = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D(('ppim_vs_kkpi_f1', 'M(p#pi^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_ppi, ppi_min, ppi_max,), 'pimkpks_m', 'ppim_m')
hist_ppip_vs_kkpi = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D(('ppip_vs_kkpi', 'M(p#pi^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_ppi, ppi_min, ppi_max,), 'pipkmks_m', 'ppip_m')
hist_ppim_vs_kkpi = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D(('ppim_vs_kkpi', 'M(p#pi^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_ppi, ppi_min, ppi_max), 'pimkpks_m', 'ppim_m')
hist_pipkmks_before_ppi = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('pipkmks_before_ppi', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_ppi = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D(('pimkpks_before_ppi', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_ppi = df_pipkmks_all_cuts_kstar_cut.Histo1D(('pipkmks_after_ppi', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_ppi = df_pimkpks_all_cuts_kstar_cut.Histo1D(('pimkpks_after_ppi', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')

# #### Binned Distributions

hists_ppip = []
hists_ppim = []
hists_ppip_shaded = []
hists_ppim_shaded = []
hists_ppip_f1 = []
hists_ppim_f1 = []
hists_ppip_f1_shaded = []
hists_ppim_f1_shaded = []
hists_ppip_vs_kkpi_f1 = []
hists_ppim_vs_kkpi_f1 = []
hists_ppip_vs_kkpi = []
hists_ppim_vs_kkpi = []
hists_pipkmks_before_ppi = []
hists_pimkpks_before_ppi = []
hists_pipkmks_after_ppi = []
hists_pimkpks_after_ppi = []

for t in constants.ALLOWED_T_BINS:

    hists_ppip.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppip_{t}', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m'))
    hists_ppim.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppim_{t}', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m'))
    hists_ppip_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppip_{t}_shaded', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m'))
    hists_ppim_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppim_{t}_shaded', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m'))
    hists_ppip_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppip_{t}_f1', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m'))
    hists_ppim_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppim_{t}_f1', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m'))
    hists_ppip_f1_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.PPIP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppip_{t}_f1_shaded', 'M(p#pi^{+})', n_bins_ppi, ppi_min, ppi_max), 'ppip_m'))
    hists_ppim_f1_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.PPIM_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'ppim_{t}_f1_shaded', 'M(p#pi^{-})', n_bins_ppi, ppi_min, ppi_max), 'ppim_m'))
    hists_ppip_vs_kkpi_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D((f'ppip_vs_kkpi_{t}_f1', 'M(p#pi^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_ppi, ppi_min, ppi_max,), 'pipkmks_m', 'ppip_m'))
    hists_ppim_vs_kkpi_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D((f'ppim_vs_kkpi_{t}_f1', 'M(p#pi^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_ppi, ppi_min, ppi_max,), 'pimkpks_m', 'ppim_m'))
    hists_ppip_vs_kkpi.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D((f'ppip_vs_kkpi_{t}', 'M(p#pi^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_ppi, ppi_min, ppi_max,), 'pipkmks_m', 'ppip_m'))
    hists_ppim_vs_kkpi.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo2D((f'ppim_vs_kkpi_{t}', 'M(p#pi^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_ppi, ppi_min, ppi_max), 'pimkpks_m', 'ppim_m'))
    hists_pipkmks_before_ppi.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'pipkmks_before_ppi_{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_ppi.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Histo1D((f'pimkpks_before_ppi_{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_ppi.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_after_ppi_{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_ppi.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_after_ppi_{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))

# ### $pK^\mp$

# #### Integrated Distributions

n_bins_pk, pk_min, pk_max = 200, 1.0, 4.0
hist_pkm = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pkm', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kmp_m')
hist_pkp = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pkp', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kpp_m')
hist_pkm_shaded = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pkm_shaded', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kmp_m')
hist_pkp_shaded = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pkp_shaded', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kpp_m')
hist_pkm_f1 = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pkm_f1', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kmp_m')
hist_pkp_f1 = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pkp_f1', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kpp_m')
hist_pkm_f1_shaded = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pkm_f1_shaded', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kmp_m')
hist_pkp_f1_shaded = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pkp_f1_shaded', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kpp_m')
hist_pkm_vs_kkpi_f1 = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('pkm_vs_kkpi_f1', 'M(pK^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pk, pk_min, pk_max,), 'pipkmks_m', 'kmp_m')
hist_pkp_vs_kkpi_f1 = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('pkp_vs_kkpi_f1', 'M(pK^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pk, pk_min, pk_max,), 'pimkpks_m', 'kpp_m')
hist_pkm_vs_kkpi = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('pkm_vs_kkpi', 'M(pK^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pk, pk_min, pk_max,), 'pipkmks_m', 'kmp_m')
hist_pkp_vs_kkpi = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('pkp_vs_kkpi', 'M(pK^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pk, pk_min, pk_max), 'pimkpks_m', 'kpp_m')
hist_pipkmks_before_pkm = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pipkmks_before_pkm', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_pkp = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pimkpks_before_pkp', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_pkm = df_pipkmks_all_cuts_kstar_cut.Histo1D(('pipkmks_after_pkm', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_pkp = df_pimkpks_all_cuts_kstar_cut.Histo1D(('pimkpks_after_pkp', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')

# #### Binned Distributions

hists_pkm = []
hists_pkp = []
hists_pkm_shaded = []
hists_pkp_shaded = []
hists_pkm_f1 = []
hists_pkp_f1 = []
hists_pkm_f1_shaded = []
hists_pkp_f1_shaded = []
hists_pkm_vs_kkpi_f1 = []
hists_pkp_vs_kkpi_f1 = []
hists_pkm_vs_kkpi = []
hists_pkp_vs_kkpi = []
hists_pipkmks_before_pkm = []
hists_pimkpks_before_pkp = []
hists_pipkmks_after_pkm = []
hists_pimkpks_after_pkp = []

for t in constants.ALLOWED_T_BINS:
    hists_pkm.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pkm_t{t}', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kmp_m'))
    hists_pkp.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pkp_t{t}', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kpp_m'))
    hists_pkm_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pkm_t{t}_shaded', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kmp_m'))
    hists_pkp_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pkp_t{t}_shaded', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kpp_m'))
    hists_pkm_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pkm_f1_t{t}', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kmp_m'))
    hists_pkp_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pkp_f1_t{t}', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kpp_m'))
    hists_pkm_f1_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pkm_f1_t{t}_shaded', 'M(pK^{+})', n_bins_pk, pk_min, pk_max), 'kmp_m'))
    hists_pkp_f1_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pkp_f1_t{t}_shaded', 'M(pK^{-})', n_bins_pk, pk_min, pk_max), 'kpp_m'))
    hists_pkm_vs_kkpi_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'pkm_vs_kkpi_f1_t{t}', 'M(pK^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pk, pk_min, pk_max,), 'pipkmks_m', 'kmp_m'))
    hists_pkp_vs_kkpi_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'pkp_vs_kkpi_f1_t{t}', 'M(pK^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pk, pk_min, pk_max,), 'pimkpks_m', 'kpp_m'))
    hists_pkm_vs_kkpi.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'pkm_vs_kkpi_t{t}', 'M(pK^{+}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pk, pk_min, pk_max,), 'pipkmks_m', 'kmp_m'))
    hists_pkp_vs_kkpi.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'pkp_vs_kkpi_t{t}', 'M(pK^{-}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pk, pk_min, pk_max), 'pimkpks_m', 'kpp_m'))
    hists_pipkmks_before_pkm.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pipkmks_before_pkm_t{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_pkp.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pimkpks_before_pkp_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_pkm.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_after_pkm_t{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_pkp.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_after_pkp_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))


# ### $pK_s$

# #### Integrated Distributions

n_bins_pks, pks_min, pks_max = 200, 1.0, 4.0
hist_pks_pipkmks = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pks_pipkmks', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pimkpks = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pks_pimkpks', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pipkmks_shaded = df_pipkmks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pks_pipkmks_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pimkpks_shaded = df_pimkpks_kstar_cut.Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pks_pimkpks_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pipkmks_f1 = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pks_pipkmks_f1', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pimkpks_f1 = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pks_pimkpks_f1', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pipkmks_f1_shaded = df_pipkmks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pks_pipkmks_f1_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pimkpks_f1_shaded = df_pimkpks_kstar_cut.Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pks_pimkpks_f1_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m')
hist_pks_pipkmks_vs_kkpi_f1 = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('pks_pipkmks_vs_kkpi_f1', 'M(pK_{s}}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pks, pks_min, pks_max,), 'pipkmks_m', 'ksp_m')
hist_pks_pimkpks_vs_kkpi_f1 = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('pks_pimkpks_vs_kkpi_f1', 'M(pK_{s}}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pks, pks_min, pks_max,), 'pimkpks_m', 'ksp_m')
hist_pks_pipkmks_vs_kkpi = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('pks_pipkmks_vs_kkpi', 'M(pK_{s}}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pks, pks_min, pks_max,), 'pipkmks_m', 'ksp_m')
hist_pks_pimkpks_vs_kkpi = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('pks_pimkpks_vs_kkpi', 'M(pK_{s}}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pks, pks_min, pks_max), 'pimkpks_m', 'ksp_m')
hist_pipkmks_before_pks = df_pipkmks_kstar_cut.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pipkmks_before_pks', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_pks = df_pimkpks_kstar_cut.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pimkpks_before_pks', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_pks = df_pipkmks_all_cuts_kstar_cut.Histo1D(('pipkmks_after_pks', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_pks = df_pimkpks_all_cuts_kstar_cut.Histo1D(('pimkpks_after_pks', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')



# #### Binned Distributions

hists_pks_pipkmks = []
hists_pks_pimkpks = []
hists_pks_pipkmks_shaded = []
hists_pks_pimkpks_shaded = []
hists_pks_pipkmks_f1 = []
hists_pks_pimkpks_f1 = []
hists_pks_pipkmks_f1_shaded = []
hists_pks_pimkpks_f1_shaded = []
hists_pks_pipkmks_vs_kkpi_f1 = []
hists_pks_pimkpks_vs_kkpi_f1 = []
hists_pks_pipkmks_vs_kkpi = []
hists_pks_pimkpks_vs_kkpi = []
hists_pipkmks_before_pks = []
hists_pimkpks_before_pks = []
hists_pipkmks_after_pks = []
hists_pimkpks_after_pks = []

for t in constants.ALLOWED_T_BINS:
    hists_pks_pipkmks.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pks_pipkmks_{t}', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pimkpks.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pks_pimkpks_{t}', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pipkmks_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pks_pipkmks_{t}_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pimkpks_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pks_pimkpks_{t}_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pipkmks_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pks_pipkmks_f1_{t}', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pimkpks_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pks_pimkpks_f1_{t}', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pipkmks_f1_shaded.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pks_pipkmks_f1_{t}_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pimkpks_f1_shaded.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pks_pimkpks_f1_{t}_shaded', 'M(pK_{s}})', n_bins_pks, pks_min, pks_max), 'ksp_m'))
    hists_pks_pipkmks_vs_kkpi_f1.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'pks_pipkmks_vs_kkpi_f1_{t}', 'M(pK_{s}}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pks, pks_min, pks_max,), 'pipkmks_m', 'ksp_m'))
    hists_pks_pimkpks_vs_kkpi_f1.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'pks_pimkpks_vs_kkpi_f1_{t}', 'M(pK_{s}}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_pks, pks_min, pks_max,), 'pimkpks_m', 'ksp_m'))
    hists_pks_pipkmks_vs_kkpi.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'pks_pipkmks_vs_kkpi_{t}', 'M(pK_{s}}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pks, pks_min, pks_max,), 'pipkmks_m', 'ksp_m'))
    hists_pks_pimkpks_vs_kkpi.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'pks_pimkpks_vs_kkpi_{t}', 'M(pK_{s}}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_pks, pks_min, pks_max), 'pimkpks_m', 'ksp_m'))
    hists_pipkmks_before_pks.append(df_pipkmks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pipkmks_before_pks{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_pks.append(df_pimkpks_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pimkpks_before_pks{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_pks.append(df_pipkmks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_after_pks_{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_pks.append(df_pimkpks_all_cuts_kstar_cut.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_after_pks_{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))

# ### $K^\mp K_s$

# #### Integrated Distributions

n_bins_kk, kk_min, kk_max = 180, 0.95, 2.0
n_bins_kk_f1, kk_f1_min, kk_f1_max = 50, 0.95, 1.2
hist_kskm = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('kmks', 'M(K_{s}K^{-})', n_bins_kk, kk_min, kk_max), 'kmks_m')
hist_kskp = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('kpks', 'M(K_{s}K^{+})', n_bins_kk, kk_min, kk_max), 'kpks_m')
hist_kskm_shaded = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('kmks_shaded', 'M(K_{s}K^{-})', n_bins_kk, kk_min, kk_max), 'kmks_m')
hist_kskp_shaded = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('kpks_shaded', 'M(K_{s}K^{+})', n_bins_kk, kk_min, kk_max), 'kpks_m')
hist_kskm_f1 = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('kmks_f1', 'M(K_{s}K^{-})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kmks_m')
hist_kskp_f1 = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('kpks_f1', 'M(K_{s}K^{+})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kpks_m')
hist_kskm_f1_shaded = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('kmks_f1_shaded', 'M(K_{s}K^{-})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kmks_m')
hist_kskp_f1_shaded = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('kpks_f1_shaded', 'M(K_{s}K^{+})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kpks_m')
hist_kskm_vs_kkpi_f1 = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('kmks_vs_kkpi_f1', 'M(K_{s}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kk_f1, kk_f1_min, kk_f1_max,), 'pipkmks_m', 'kmks_m')
hist_kskp_vs_kkpi_f1 = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('kpks_vs_kkpi_f1', 'M(K_{s}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kk_f1, kk_f1_min, kk_f1_max,), 'pimkpks_m', 'kpks_m')
hist_kskm_vs_kkpi = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D(('kmks_vs_kkpi', 'M(K_{s}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kk, kk_min, kk_max,), 'pipkmks_m', 'kmks_m')
hist_kskp_vs_kkpi = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D(('kpks_vs_kkpi', 'M(K_{s}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kk, kk_min, kk_max), 'pimkpks_m', 'kpks_m')
hist_pipkmks_before_kskm = df_pipkmks.Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D(('pipkmks_before_kmks', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_kskp = df_pimkpks.Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D(('pimkpks_before_kpks', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_kskm = df_pipkmks_all_cuts.Filter('kmks_m < 1.05').Histo1D(('pipkmks_after_kmks', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_kskp = df_pimkpks_all_cuts.Filter('kpks_m < 1.05').Histo1D(('pimkpks_after_kpks', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')

# #### Binned Distributions

hists_kskm = []
hists_kskp = []
hists_kskm_shaded = []
hists_kskp_shaded = []
hists_kskm_f1 = []
hists_kskp_f1 = []
hists_kskm_f1_shaded = []
hists_kskp_f1_shaded = []
hists_kskm_vs_kkpi_f1 = []
hists_kskp_vs_kkpi_f1 = []
hists_kskm_vs_kkpi = []
hists_kskp_vs_kkpi = []
hists_pipkmks_before_kskm = []
hists_pimkpks_before_kskp = []
hists_pipkmks_after_kskm = []
hists_pimkpks_after_kskp = []

for t in constants.ALLOWED_T_BINS:

    hists_kskm.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'kmks_t{t}', 'M(K_{s}K^{-})', n_bins_kk, kk_min, kk_max), 'kmks_m'))
    hists_kskp.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'kpks_t{t}', 'M(K_{s}K^{+})', n_bins_kk, kk_min, kk_max), 'kpks_m'))
    hists_kskm_shaded.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'kmks_t{t}_shaded', 'M(K_{s}K^{-})', n_bins_kk, kk_min, kk_max), 'kmks_m'))
    hists_kskp_shaded.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'kpks_t{t}_shaded', 'M(K_{s}K^{+})', n_bins_kk, kk_min, kk_max), 'kpks_m'))
    hists_kskm_f1.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'kmks_f1_t{t}', 'M(K_{s}K^{-})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kmks_m'))
    hists_kskp_f1.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'kpks_f1_t{t}', 'M(K_{s}K^{+})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kpks_m'))
    hists_kskm_f1_shaded.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIPKMKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'kmks_f1_t{t}_shaded', 'M(K_{s}K^{-})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kmks_m'))
    hists_kskp_f1_shaded.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.F1_SIGNAL_REGION_PIMKPKS).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'kpks_f1_t{t}_shaded', 'M(K_{s}K^{+})', n_bins_kk_f1, kk_f1_min, kk_f1_max), 'kpks_m'))
    hists_kskm_vs_kkpi_f1.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'kmks_vs_kkpi_f1_t{t}', 'M(K_{s}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kk_f1, kk_f1_min, kk_f1_max,), 'pipkmks_m', 'kmks_m'))
    hists_kskp_vs_kkpi_f1.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'kpks_vs_kkpi_f1_t{t}', 'M(K_{s}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kk_f1, kk_f1_min, kk_f1_max,), 'pimkpks_m', 'kpks_m'))
    hists_kskm_vs_kkpi.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo2D((f'kmks_vs_kkpi_t{t}', 'M(K_{s}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kk, kk_min, kk_max,), 'pipkmks_m', 'kmks_m'))
    hists_kskp_vs_kkpi.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo2D((f'kpks_vs_kkpi_t{t}', 'M(K_{s}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kk, kk_min, kk_max), 'pimkpks_m', 'kpks_m'))
    hists_pipkmks_before_kskm.append(df_pipkmks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KMP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIP_MASS_CUT).Histo1D((f'pipkmks_before_kmks_t{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_kskp.append(df_pimkpks.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KPP_MASS_CUT).Filter(kcuts.KSP_MASS_CUT).Filter(kcuts.PPIM_MASS_CUT).Histo1D((f'pimkpks_before_kpks_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_kskm.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Filter('kmks_m < 1.05').Histo1D((f'pipkmks_after_kmks_t{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_kskp.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Filter('kpks_m < 1.05').Histo1D((f'pimkpks_after_kpks_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))


# ### $K^\mp \pi^\pm$

# #### Integrated Distributions

n_bins_kpi, kpi_min, kpi_max = 100, 0.5, 1.5
hist_kmpip = df_pipkmks_all_cuts.Histo1D(('kmpip', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m')
hist_kppim = df_pimkpks_all_cuts.Histo1D(('kppip', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m')
hist_kmpip_shaded = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Histo1D(('kmpip_shaded', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m')
hist_kppim_shaded = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Histo1D(('kppip_shaded', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m')
hist_kmpip_f1 = df_pipkmks_all_cuts.Histo1D(('kmpip_f1', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m')
hist_kppim_f1 = df_pimkpks_all_cuts.Histo1D(('kppip_f1', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m')
hist_kmpip_f1_shaded = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Histo1D(('kmpip_f1_shaded', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m')
hist_kppim_f1_shaded = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Histo1D(('kppip_f1_shaded', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m')
hist_kmpip_vs_kkpi_f1 = df_pipkmks_all_cuts.Histo2D(('kmpip_vs_kkpi_f1', 'M(#pi^{+}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kmpip_m')
hist_kppim_vs_kkpi_f1 = df_pimkpks_all_cuts.Histo2D(('kppip_vs_kkpi_f1', 'M(#pi^{-}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pimkpks_m', 'kppim_m')
hist_kmpip_vs_kkpi = df_pipkmks_all_cuts.Histo2D(('kmpip_vs_kkpi', 'M(#pi^{+}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kmpip_m')
hist_kppim_vs_kkpi = df_pimkpks_all_cuts.Histo2D(('kppip_vs_kkpi', 'M(#pi^{-}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max), 'pimkpks_m', 'kppim_m')
hist_pipkmks_before_kmpip = df_pipkmks_all_cuts.Histo1D(('pipkmks_before_kmpip', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_kppim = df_pimkpks_all_cuts.Histo1D(('pimkpks_before_kppim', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_kmpip = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Histo1D(('pipkmks_after_kmpip', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_kppim = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Histo1D(('pimkpks_after_kppim', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')

# #### Binned Distributions

hists_kmpip = []
hists_kppim = []
hists_kmpip_shaded = []
hists_kppim_shaded = []
hists_kmpip_f1 = []
hists_kppim_f1 = []
hists_kmpip_f1_shaded = []
hists_kppim_f1_shaded = []
hists_kmpip_vs_kkpi_f1 = []
hists_kppim_vs_kkpi_f1 = []
hists_kmpip_vs_kkpi = []
hists_kppim_vs_kkpi = []
hists_pipkmks_before_kmpip = []
hists_pimkpks_before_kppim = []
hists_pipkmks_after_kmpip = []
hists_pimkpks_after_kppim = []

for t in constants.ALLOWED_T_BINS:
    hists_kmpip.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kmpip_t{t}', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m'))
    hists_kppim.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kppip_t{t}', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m'))
    hists_kmpip_shaded.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kmpip_t{t}_shaded', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m'))
    hists_kppim_shaded.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kppip_t{t}_shaded', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m'))
    hists_kmpip_f1.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Histo1D((f'kmpip_f1_t{t}', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m'))
    hists_kppim_f1.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Histo1D((f'kppip_f1_t{t}', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m'))
    hists_kmpip_f1_shaded.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kmpip_f1_t{t}_shaded', 'M(#pi^{+}K^{-})', n_bins_kpi, kpi_min, kpi_max), 'kmpip_m'))
    hists_kppim_f1_shaded.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kppip_f1_t{t}_shaded', 'M(#pi^{-}K^{+})', n_bins_kpi, kpi_min, kpi_max), 'kppim_m'))
    hists_kmpip_vs_kkpi_f1.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kmpip_vs_kkpi_f1_t{t}', 'M(#pi^{+}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kmpip_m'))
    hists_kppim_vs_kkpi_f1.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kppip_vs_kkpi_f1_t{t}', 'M(#pi^{-}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pimkpks_m', 'kppim_m'))
    hists_kmpip_vs_kkpi.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kmpip_vs_kkpi_t{t}', 'M(#pi^{+}K^{-}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kmpip_m'))
    hists_kppim_vs_kkpi.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kppip_vs_kkpi_t{t}', 'M(#pi^{-}K^{+}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max), 'pimkpks_m', 'kppim_m'))
    hists_pipkmks_before_kmpip.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_before_kmpip_t{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_kppim.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_before_kppim_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_kmpip.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIPKMKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_after_kmpip_t{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_kppim.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_ZERO_CUT_PIMKPKS).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_after_kppim_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))


# ### $K_s \pi^\pm$

# #### Integrated Distributions

hist_kspip = df_pipkmks_all_cuts.Histo1D(('kspip', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m')
hist_kspim = df_pimkpks_all_cuts.Histo1D(('kspip', 'M(#pi^{-}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspim_m')
hist_kspip_shaded = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Histo1D(('kspip_shaded', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m')
hist_kspim_shaded = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Histo1D(('kspip_shaded', 'M(#pi^{-}K^_+s)', n_bins_kpi, kpi_min, kpi_max), 'kspim_m')
hist_kspip_f1 = df_pipkmks_all_cuts.Histo1D(('kspip_f1', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m')
hist_kspim_f1 = df_pimkpks_all_cuts.Histo1D(('kspip_f1', 'M(#pi^{-}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspim_m')
hist_kspip_f1_shaded = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Histo1D(('kspip_f1_shaded', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m')
hist_kspim_f1_shaded = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Histo1D(('kspip_f1_shaded', 'M(#pi^{-}K^_+s)', n_bins_kpi, kpi_min, kpi_max), 'kspim_m')
hist_kspip_vs_kkpi_f1 = df_pipkmks_all_cuts.Histo2D(('kspip_vs_kkpi_f1', 'M(#pi^{+}K_{s}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kspip_m')
hist_kspim_vs_kkpi_f1 = df_pimkpks_all_cuts.Histo2D(('kspip_vs_kkpi_f1', 'M(#pi^{-}K_{s}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pimkpks_m', 'kspim_m')
hist_kspip_vs_kkpi = df_pipkmks_all_cuts.Histo2D(('kspip_vs_kkpi', 'M(#pi^{+}K_{s}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kspip_m')
hist_kspim_vs_kkpi = df_pimkpks_all_cuts.Histo2D(('kspip_vs_kkpi', 'M(#pi^{-}K^_+s) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max), 'pimkpks_m', 'kspim_m')
hist_pipkmks_before_kspip = df_pipkmks_all_cuts.Histo1D(('pipkmks_before_kspip', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_before_kspim = df_pimkpks_all_cuts.Histo1D(('pimkpks_before_kspim', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')
hist_pipkmks_after_kspip = df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Histo1D(('pipkmks_after_kspip', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m')
hist_pimkpks_after_kspim = df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Histo1D(('pimkpks_after_kspim', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m')

# #### Binned Distributions

hists_kspip = []
hists_kspim = []
hists_kspip_shaded = []
hists_kspim_shaded = []
hists_kspip_f1 = []
hists_kspim_f1 = []
hists_kspip_f1_shaded = []
hists_kspim_f1_shaded = []
hists_kspip_vs_kkpi_f1 = []
hists_kspim_vs_kkpi_f1 = []
hists_kspip_vs_kkpi = []
hists_kspim_vs_kkpi = []
hists_pipkmks_before_kspip = []
hists_pimkpks_before_kspim = []
hists_pipkmks_after_kspip = []
hists_pimkpks_after_kspim = []

for t in constants.ALLOWED_T_BINS:
    hists_kspip.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_t{t}', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m'))
    hists_kspim.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_t{t}', 'M(#pi^{-}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspim_m'))
    hists_kspip_shaded.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_t{t}_shaded', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m'))
    hists_kspim_shaded.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_t{t}_shaded', 'M(#pi^{-}K^_+s)', n_bins_kpi, kpi_min, kpi_max), 'kspim_m'))
    hists_kspip_f1.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_f1_t{t}', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m'))
    hists_kspim_f1.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_f1_t{t}', 'M(#pi^{-}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspim_m'))
    hists_kspip_f1_shaded.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_f1_f{t}_shaded', 'M(#pi^{+}K_{s})', n_bins_kpi, kpi_min, kpi_max), 'kspip_m'))
    hists_kspim_f1_shaded.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'kspip_f1_f{t}_shaded', 'M(#pi^{-}K^_+s)', n_bins_kpi, kpi_min, kpi_max), 'kspim_m'))
    hists_kspip_vs_kkpi_f1.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kspip_vs_kkpi_f1_t{t}', 'M(#pi^{+}K_{s}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kspip_m'))
    hists_kspim_vs_kkpi_f1.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kspip_vs_kkpi_f1_t{t}', 'M(#pi^{-}K_{s}) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_f1, kkpi_f1_min, kkpi_f1_max, n_bins_kpi, kpi_min, kpi_max,), 'pimkpks_m', 'kspim_m'))
    hists_kspip_vs_kkpi.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kspip_vs_kkpi_t{t}', 'M(#pi^{+}K_{s}) vs M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max,), 'pipkmks_m', 'kspip_m'))
    hists_kspim_vs_kkpi.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo2D((f'kspip_vs_kkpi_t{t}', 'M(#pi^{-}K^_+s) vs M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_no_cut, kkpi_no_cut_min, kkpi_no_cut_max, n_bins_kpi, kpi_min, kpi_max), 'pimkpks_m', 'kspim_m'))
    hists_pipkmks_before_kspip.append(df_pipkmks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_before_kspip_t{t}', 'M(#pi^{+}+K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_before_kspim.append(df_pimkpks_all_cuts.Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_before_kspim_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))
    hists_pipkmks_after_kspip.append(df_pipkmks_all_cuts.Filter(kcuts.KSTAR_PLUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pipkmks_after_kspip_t{t}', 'M(#pi^{+}K^{-}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pipkmks_m'))
    hists_pimkpks_after_kspim.append(df_pimkpks_all_cuts.Filter(kcuts.KSTAR_MINUS_CUT).Filter(kcuts.SELECT_T_BIN.format(t)).Histo1D((f'pimkpks_after_kspim_t{t}', 'M(#pi^{-}K^{+}K_{S})', n_bins_kkpi_kstar_cut, kkpi_kstar_cut_min, kkpi_kstar_cut_max), 'pimkpks_m'))


# # Write File 

df_pipkmks.Count().GetValue()
df_pimkpks.Count().GetValue()

df_pipkmks.Count().GetValue()
df_pimkpks.Count().GetValue()

df_pipkmks_kstar_cut.Count().GetValue()
df_pimkpks_kstar_cut.Count().GetValue()

df_pipkmks_all_cuts.Count().GetValue()
df_pimkpks_all_cuts.Count().GetValue()

df_pipkmks_all_cuts_kstar_cut.Count().GetValue()
df_pimkpks_all_cuts_kstar_cut.Count().GetValue()

hist_pipkmks.GetPtr().Write()
hist_pipkmks_kstar_cut.GetPtr().Write()
hist_pimkpks.GetPtr().Write()
hist_pimkpks_kstar_cut.GetPtr().Write()
hist_km_p.GetPtr().Write()
hist_kp_p.GetPtr().Write()
hist_km_theta.GetPtr().Write()
hist_kp_theta.GetPtr().Write()
hist_km_theta_vs_p.GetPtr().Write()
hist_kp_theta_vs_p.GetPtr().Write()
hist_km_p_vs_pipkmks.GetPtr().Write()
hist_kp_p_vs_pimkpks.GetPtr().Write()
hist_km_theta_vs_pipkmks.GetPtr().Write()
hist_kp_theta_vs_pimkpks.GetPtr().Write()
hist_pip1_p.GetPtr().Write()
hist_pim1_p.GetPtr().Write()
hist_pip1_theta.GetPtr().Write()
hist_pim1_theta.GetPtr().Write()
hist_pip1_theta_vs_p.GetPtr().Write()
hist_pim1_theta_vs_p.GetPtr().Write()
hist_pip1_p_vs_pipkmks.GetPtr().Write()
hist_pim1_p_vs_pimkpks.GetPtr().Write()
hist_pip1_theta_vs_pipkmks.GetPtr().Write()
hist_pim1_theta_vs_pimkpks.GetPtr().Write()
hist_ks_pipkmks_p.GetPtr().Write()
hist_ks_pimkpks_p.GetPtr().Write()
hist_ks_pipkmks_theta.GetPtr().Write()
hist_ks_pimkpks_theta.GetPtr().Write()
hist_ks_pipkmks_theta_vs_p.GetPtr().Write()
hist_ks_pimkpks_theta_vs_p.GetPtr().Write()
hist_ks_pipkmks_p_vs_pipkmks.GetPtr().Write()
hist_ks_pimkpks_p_vs_pimkpks.GetPtr().Write()
hist_ks_pipkmks_theta_vs_pipkmks.GetPtr().Write()
hist_ks_pimkpks_theta_vs_pimkpks.GetPtr().Write()
hist_pip2_p.GetPtr().Write()
hist_pip_p.GetPtr().Write()
hist_pip2_theta.GetPtr().Write()
hist_pip_theta.GetPtr().Write()
hist_pip2_theta_vs_p.GetPtr().Write()
hist_pip_theta_vs_p.GetPtr().Write()
hist_pip2_p_vs_pipkmks.GetPtr().Write()
hist_pip_p_vs_pimkpks.GetPtr().Write()
hist_pip2_theta_vs_pipkmks.GetPtr().Write()
hist_pip_theta_vs_pimkpks.GetPtr().Write()
hist_pim_p.GetPtr().Write()
hist_pim2_p.GetPtr().Write()
hist_pim_theta.GetPtr().Write()
hist_pim2_theta.GetPtr().Write()
hist_pim_theta_vs_p.GetPtr().Write()
hist_pim2_theta_vs_p.GetPtr().Write()
hist_pim_p_vs_pipkmks.GetPtr().Write()
hist_pim2_p_vs_pimkpks.GetPtr().Write()
hist_pim_theta_vs_pipkmks.GetPtr().Write()
hist_pim2_theta_vs_pimkpks.GetPtr().Write()
hist_ppip.GetPtr().Write()
hist_ppim.GetPtr().Write()
hist_ppip_shaded.GetPtr().Write()
hist_ppim_shaded.GetPtr().Write()
hist_ppip_f1.GetPtr().Write()
hist_ppim_f1.GetPtr().Write()
hist_ppip_f1_shaded.GetPtr().Write()
hist_ppim_f1_shaded.GetPtr().Write()
hist_ppip_vs_kkpi_f1.GetPtr().Write()
hist_ppim_vs_kkpi_f1.GetPtr().Write()
hist_ppip_vs_kkpi.GetPtr().Write()
hist_ppim_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_ppi.GetPtr().Write()
hist_pimkpks_before_ppi.GetPtr().Write()
hist_pipkmks_after_ppi.GetPtr().Write()
hist_pimkpks_after_ppi.GetPtr().Write()
hist_pkm.GetPtr().Write()
hist_pkp.GetPtr().Write()
hist_pkm_shaded.GetPtr().Write()
hist_pkp_shaded.GetPtr().Write()
hist_pkm_f1.GetPtr().Write()
hist_pkp_f1.GetPtr().Write()
hist_pkm_f1_shaded.GetPtr().Write()
hist_pkp_f1_shaded.GetPtr().Write()
hist_pkm_vs_kkpi_f1.GetPtr().Write()
hist_pkp_vs_kkpi_f1.GetPtr().Write()
hist_pkm_vs_kkpi.GetPtr().Write()
hist_pkp_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_pkm.GetPtr().Write()
hist_pimkpks_before_pkp.GetPtr().Write()
hist_pipkmks_after_pkm.GetPtr().Write()
hist_pimkpks_after_pkp.GetPtr().Write()
hist_pks_pipkmks.GetPtr().Write()
hist_pks_pimkpks.GetPtr().Write()
hist_pks_pipkmks_shaded.GetPtr().Write()
hist_pks_pimkpks_shaded.GetPtr().Write()
hist_pks_pipkmks_f1.GetPtr().Write()
hist_pks_pimkpks_f1.GetPtr().Write()
hist_pks_pipkmks_f1_shaded.GetPtr().Write()
hist_pks_pimkpks_f1_shaded.GetPtr().Write()
hist_pks_pipkmks_vs_kkpi_f1.GetPtr().Write()
hist_pks_pimkpks_vs_kkpi_f1.GetPtr().Write()
hist_pks_pipkmks_vs_kkpi.GetPtr().Write()
hist_pks_pimkpks_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_pks.GetPtr().Write()
hist_pimkpks_before_pks.GetPtr().Write()
hist_pipkmks_after_pks.GetPtr().Write()
hist_pimkpks_after_pks.GetPtr().Write()
hist_kskm.GetPtr().Write()
hist_kskp.GetPtr().Write()
hist_kskm_shaded.GetPtr().Write()
hist_kskp_shaded.GetPtr().Write()
hist_kskm_f1.GetPtr().Write()
hist_kskp_f1.GetPtr().Write()
hist_kskm_f1_shaded.GetPtr().Write()
hist_kskp_f1_shaded.GetPtr().Write()
hist_kskm_vs_kkpi_f1.GetPtr().Write()
hist_kskp_vs_kkpi_f1.GetPtr().Write()
hist_kskm_vs_kkpi.GetPtr().Write()
hist_kskp_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_kskm.GetPtr().Write()
hist_pimkpks_before_kskp.GetPtr().Write()
hist_pipkmks_after_kskm.GetPtr().Write()
hist_pimkpks_after_kskp.GetPtr().Write()
hist_kmpip.GetPtr().Write()
hist_kppim.GetPtr().Write()
hist_kmpip_shaded.GetPtr().Write()
hist_kppim_shaded.GetPtr().Write()
hist_kmpip_f1.GetPtr().Write()
hist_kppim_f1.GetPtr().Write()
hist_kmpip_f1_shaded.GetPtr().Write()
hist_kppim_f1_shaded.GetPtr().Write()
hist_kmpip_vs_kkpi_f1.GetPtr().Write()
hist_kppim_vs_kkpi_f1.GetPtr().Write()
hist_kmpip_vs_kkpi.GetPtr().Write()
hist_kppim_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_kmpip.GetPtr().Write()
hist_pimkpks_before_kppim.GetPtr().Write()
hist_pipkmks_after_kmpip.GetPtr().Write()
hist_pimkpks_after_kppim.GetPtr().Write()
hist_kspip.GetPtr().Write()
hist_kspim.GetPtr().Write()
hist_kspip_shaded.GetPtr().Write()
hist_kspim_shaded.GetPtr().Write()
hist_kspip_f1.GetPtr().Write()
hist_kspim_f1.GetPtr().Write()
hist_kspip_f1_shaded.GetPtr().Write()
hist_kspim_f1_shaded.GetPtr().Write()
hist_kspip_vs_kkpi_f1.GetPtr().Write()
hist_kspim_vs_kkpi_f1.GetPtr().Write()
hist_kspip_vs_kkpi.GetPtr().Write()
hist_kspim_vs_kkpi.GetPtr().Write()
hist_pipkmks_before_kspip.GetPtr().Write()
hist_pimkpks_before_kspim.GetPtr().Write()
hist_pipkmks_after_kspip.GetPtr().Write()
hist_pimkpks_after_kspim.GetPtr().Write()


binned_hist_list = [
pipkmks_hists, pimkpks_hists, pipkmks_kstar_cut_hists, pimkpks_kstar_cut_hists,
ks_pipkmks_p_hists, ks_pimkpks_p_hists, ks_pipkmks_theta_hists, ks_pimkpks_theta_hists, ks_pipkmks_theta_vs_p_hists, ks_pimkpks_theta_vs_p_hists, ks_pipkmks_p_vs_pipkmks_hists, ks_pimkpks_p_vs_pimkpks_hists, ks_pipkmks_theta_vs_pipkmks_hists, ks_pimkpks_theta_vs_pimkpks_hists,
pip1_p_hists, pim1_p_hists, pip1_theta_hists, pim1_theta_hists, pip1_theta_vs_p_hists, pim1_theta_vs_p_hists, pip1_p_vs_pipkmks_hists, pim1_p_vs_pimkpks_hists, pip1_theta_vs_pipkmks_hists, pim1_theta_vs_pimkpks_hists, 
ks_pipkmks_p_hists, ks_pimkpks_p_hists, ks_pipkmks_theta_hists, ks_pimkpks_theta_hists, ks_pipkmks_theta_vs_p_hists, ks_pimkpks_theta_vs_p_hists, ks_pipkmks_p_vs_pipkmks_hists, ks_pimkpks_p_vs_pimkpks_hists, ks_pipkmks_theta_vs_pipkmks_hists, ks_pimkpks_theta_vs_pimkpks_hists, 
pip2_p_hists, pip_p_hists, pip2_theta_hists, pip_theta_hists, pip2_theta_vs_p_hists, pip_theta_vs_p_hists, pip2_p_vs_pipkmks_hists, pip_p_vs_pimkpks_hists, pip2_theta_vs_pipkmks_hists, pip_theta_vs_pimkpks_hists, 
pim_p_hists, pim2_p_hists, pim_theta_hists, pim2_theta_hists, pim_theta_vs_p_hists, pim2_theta_vs_p_hists, pim_p_vs_pipkmks_hists, pim2_p_vs_pimkpks_hists, pim_theta_vs_pipkmks_hists, pim2_theta_vs_pimkpks_hists, 
hists_ppip, hists_ppim, hists_ppip_shaded, hists_ppim_shaded, hists_ppip_f1, hists_ppim_f1, hists_ppip_f1_shaded, hists_ppim_f1_shaded, hists_ppip_vs_kkpi_f1, hists_ppim_vs_kkpi_f1, hists_ppip_vs_kkpi, hists_ppim_vs_kkpi, hists_pipkmks_before_ppi, hists_pimkpks_before_ppi, hists_pipkmks_after_ppi, hists_pimkpks_after_ppi, 
hists_pkm, hists_pkp, hists_pkm_shaded, hists_pkp_shaded, hists_pkm_f1, hists_pkp_f1, hists_pkm_f1_shaded, hists_pkp_f1_shaded, hists_pkm_vs_kkpi_f1, hists_pkp_vs_kkpi_f1, hists_pkm_vs_kkpi, hists_pkp_vs_kkpi, hists_pipkmks_before_pkm, hists_pimkpks_before_pkp, hists_pipkmks_after_pkm, hists_pimkpks_after_pkp, 
hists_pks_pipkmks, hists_pks_pimkpks, hists_pks_pipkmks_shaded, hists_pks_pimkpks_shaded, hists_pks_pipkmks_f1, hists_pks_pimkpks_f1, hists_pks_pipkmks_f1_shaded, hists_pks_pimkpks_f1_shaded, hists_pks_pipkmks_vs_kkpi_f1, hists_pks_pimkpks_vs_kkpi_f1, hists_pks_pipkmks_vs_kkpi, hists_pks_pimkpks_vs_kkpi, hists_pipkmks_before_pks, hists_pimkpks_before_pks, hists_pipkmks_after_pks, hists_pimkpks_after_pks, 
hists_kskm, hists_kskp, hists_kskm_shaded, hists_kskp_shaded, hists_kskm_f1, hists_kskp_f1, hists_kskm_f1_shaded, hists_kskp_f1_shaded, hists_kskm_vs_kkpi_f1, hists_kskp_vs_kkpi_f1, hists_kskm_vs_kkpi, hists_kskp_vs_kkpi, hists_pipkmks_before_kskm, hists_pimkpks_before_kskp, hists_pipkmks_after_kskm, hists_pimkpks_after_kskp, 
hists_kmpip, hists_kppim, hists_kmpip_shaded, hists_kppim_shaded, hists_kmpip_f1, hists_kppim_f1, hists_kmpip_f1_shaded, hists_kppim_f1_shaded, hists_kmpip_vs_kkpi_f1, hists_kppim_vs_kkpi_f1, hists_kmpip_vs_kkpi, hists_kppim_vs_kkpi, hists_pipkmks_before_kmpip, hists_pimkpks_before_kppim, hists_pipkmks_after_kmpip, hists_pimkpks_after_kppim, hists_kspip, hists_kspim, hists_kspip_shaded, hists_kspim_shaded, hists_kspip_f1, hists_kspim_f1, hists_kspip_f1_shaded, hists_kspim_f1_shaded, hists_kspip_vs_kkpi_f1, hists_kspim_vs_kkpi_f1, hists_kspip_vs_kkpi, hists_kspim_vs_kkpi, hists_pipkmks_before_kspip, hists_pimkpks_before_kspim, hists_pipkmks_after_kspip, hists_pimkpks_after_kspim 
]

for l in binned_hist_list:
    for h in l:
        h.GetPtr().Write()

hist_file.Close()