# thrown mc analysis with root dataframe for crossfeed contamination 
import ROOT
import time

start_time = time.time()

filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_flat_crossfeed_fall.root'
treename = 'pipkmks__ks_pippim__B4_M16'

df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

ks_pathlength_cut = 'pathlength_sig > 5'
ks_mass_cut = 'ks_m > 0.45 && ks_m < 0.55'



df = df.Filter(ks_pathlength_cut)#.Histo1D(('ks_pl', 'ks_pl', 100, 0.3, 0.7), 'ks_m')
# ks_no_pl = df.Filter(ks_cut2).Histo1D(('ks_no_pl', 'ks_no_pl', 100, 0.3, 0.7), 'ks_m')
# ks_all = df.Filter(ks_cut1).Filter(ks_cut2).Histo1D(('ks_all', 'ks_all', 100, 0.3, 0.7), 'ks_m')
# ks_none = df.Histo1D(('ks_none', 'ks_none', 100, 0.2, 0.8), 'ks_m')
print('cut 1 done in {} seconds'.format(time.time() - start_time))
# ks_pl.SetLineColor(2)
# ks_no_pl.SetLineColor(3)

# ks_pl.Draw()
# ks_no_pl.Draw('same')
# ks_all.Draw('same')
# ks_none.Draw('same')

df = df.Filter(ks_mass_cut)
print('cut 2 done in {} seconds'.format(time.time() - start_time))

df = df.Define('ppip_px', 'pip1_px + p_px')
df = df.Define('ppip_py', 'pip1_py + p_py')
df = df.Define('ppip_pz', 'pip1_pz + p_pz')
df = df.Define('ppip_E', 'pip1_E + p_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')

df = df.Filter('ppip_m > 1.4')
print("cut 3 done in {} seconds".format(time.time() - start_time))

df = df.Define('missing_px', '-p_px - pip1_px - ks_px - km_px')
df = df.Define('missing_py', '-p_py - pip1_py - ks_py - km_py')
df = df.Define('missing_pz', 'e_beam - p_pz - pip1_pz - ks_pz - km_pz')
df = df.Define('missing_E', 'e_beam + 0.938 - p_E - pip1_E - ks_E - km_E')

df = df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

# mx_all_hist = df.Histo1D(('mx_all', 'mx_all', 100, -0.5, 0.5), 'missing_m')
# mx_all_hist.Draw()

df = df.Define('kmp_px', 'p_px + km_px')
df = df.Define('kmp_py', 'p_py + km_py')
df = df.Define('kmp_pz', 'p_pz + km_pz')
df = df.Define('kmp_E', 'p_E + km_E')

df = df.Define('kmp_m', 'sqrt(kmp_E*kmp_E - kmp_px*kmp_px - kmp_py*kmp_py - kmp_pz*kmp_pz)')

df = df.Filter('kmp_m > 1.95')
print("cut 4 done in {} seconds".format(time.time() - start_time))

df = df.Define('kspip_px', 'pip1_px + ks_px')
df = df.Define('kspip_py', 'pip1_py + ks_py')
df = df.Define('kspip_pz', 'pip1_pz + ks_pz')
df = df.Define('kspip_E', 'pip1_E + ks_E')

df = df.Define('kspip_m', 'sqrt(kspip_E*kspip_E - kspip_px*kspip_px - kspip_py*kspip_py - kspip_pz*kspip_pz)')

df = df.Define('kmpip_px', 'pip1_px + km_px')
df = df.Define('kmpip_py', 'pip1_py + km_py')
df = df.Define('kmpip_pz', 'pip1_pz + km_pz')
df = df.Define('kmpip_E', 'pip1_E + km_E')

df = df.Define('kmpip_m', 'sqrt(kmpip_E*kmpip_E - kmpip_px*kmpip_px - kmpip_py*kmpip_py - kmpip_pz*kmpip_pz)')

df = df.Define('pipkmks_px', 'pip1_px + km_px + ks_px')
df = df.Define('pipkmks_py', 'pip1_py + km_py + ks_py')
df = df.Define('pipkmks_pz', 'pip1_pz + km_pz + ks_pz')
df = df.Define('pipkmks_E', 'pip1_E + km_E + ks_E')

df = df.Define('pipkmks_m', 'sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)')

kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

f1_nocut = df.Histo1D(('f1_nocut', 'f1_nocut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut', 'f1_kstar_plus_cut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut', 'f1_kstar_zero_cut', 50, 1.0, 1.7), 'pipkmks_m')
f1_kstar_all_cut = df.Filter(kstar_all_cut).Histo1D(('f1_kstar_all_cut', 'f1_kstar_all_cut', 50, 1.0, 1.7), 'pipkmks_m')

f1_nocut.SetLineColor(1)
f1_kstar_plus_cut.SetLineColor(2)
f1_kstar_zero_cut.SetLineColor(6)
f1_kstar_all_cut.SetLineColor(8)

df = df.Filter(kstar_all_cut)

# beam_df_array = []

# for beam_value in range(5, 11):
#     beam_low = beam_value - 0.5
#     beam_high = beam_value + 0.5
#     beam_df_array.append(df.Filter('e_beam > {} && e_beam <= {}'.format(beam_low, beam_high)))

# # df_beam_5 = df.Filter('e_beam > 4.5 && e_beam <= 5.5')
# # df_beam_6 = df.Filter('e_beam > 5.5 && e_beam <= 6.5')
# # df_beam_7 = df.Filter('e_beam > 6.5 && e_beam <= 7.5')
# # df_beam_8 = df.Filter('e_beam > 7.5 && e_beam <= 8.5')
# # df_beam_9 = df.Filter('e_beam > 8.5 && e_beam <= 9.5')
# # df_beam_10 = df.Filter('e_beam > 9.5 && e_beam <= 10.5')

# print("beam cuts done in {} seconds".format(time.time() - start_time))


# histo_array_low = []
# histo_array_med = []
# histo_array_high = []
histo_array = []

t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']



for t in t_low:
    histo_array.append(df.Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmk_t_{}'.format(t), 'pipkmks_t_{}'.format(t), 50, 1.0, 1.7), 'pipkmks_m'))
for t in t_med:
    histo_array.append(df.Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_t_{}'.format(t), 'pipkmks_t_{}'.format(t), 50, 1.0, 1.7), 'pipkmks_m'))
for t in t_high:
    histo_array.append(df.Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pipkmks_t_{}'.format(t), 'pipkmks_t_{}'.format(t), 50, 1.0, 1.7), 'pipkmks_m'))

# print(len(histo_array_low))
print("histos done in {} seconds".format(time.time() - start_time))

target_file = ROOT.TFile("/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_flat_crossfeed.root", 'RECREATE')
for histo in histo_array:
    histo.Write()


target_file.Close()
    