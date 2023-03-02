# script for making histograms from flat best chi2/ndf trees

import ROOT
import time

start_time = time.time()

filename = '/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pimkpks_flat_bestX2_2018_fall.root'
treename = 'pimkpks__B4_M16'

df = ROOT.RDataFrame(treename, filename)

# print(df.GetColumnNames())

df = df.Define('ks_px', "pim2_px + pip_px")
df = df.Define('ks_py', "pim2_py + pip_py")
df = df.Define('ks_pz', "pim2_pz + pip_pz")
df = df.Define('ks_E', "pim2_E + pip_E")
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

df = df.Define('ppim_px', 'pim1_px + p_px')
df = df.Define('ppim_py', 'pim1_py + p_py')
df = df.Define('ppim_pz', 'pim1_pz + p_pz')
df = df.Define('ppim_E', 'pim1_E + p_E')
df = df.Define('ppim_m', 'sqrt(ppim_E*ppim_E - ppim_px*ppim_px - ppim_py*ppim_py - ppim_pz*ppim_pz)')

df = df.Filter('ppim_m > 1.4')
print("cut 3 done in {} seconds".format(time.time() - start_time))

df = df.Define('missing_px', '-p_px - pim1_px - ks_px - kp_px')
df = df.Define('missing_py', '-p_py - pim1_py - ks_py - kp_py')
df = df.Define('missing_pz', 'e_beam - p_pz - pim1_pz - ks_pz - kp_pz')
df = df.Define('missing_E', 'e_beam + 0.938 - p_E - pim1_E - ks_E - kp_E')

df = df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

# mx_all_hist = df.Histo1D(('mx_all', 'mx_all', 100, -0.5, 0.5), 'missing_m')
# mx_all_hist.Draw()

df = df.Define('kpp_px', 'p_px + kp_px')
df = df.Define('kpp_py', 'p_py + kp_py')
df = df.Define('kpp_pz', 'p_pz + kp_pz')
df = df.Define('kpp_E', 'p_E + kp_E')

df = df.Define('kpp_m', 'sqrt(kpp_E*kpp_E - kpp_px*kpp_px - kpp_py*kpp_py - kpp_pz*kpp_pz)')

df = df.Filter('kpp_m > 1.95')
print("cut 4 done in {} seconds".format(time.time() - start_time))

df = df.Define('kspim_px', 'pim1_px + ks_px')
df = df.Define('kspim_py', 'pim1_py + ks_py')
df = df.Define('kspim_pz', 'pim1_pz + ks_pz')
df = df.Define('kspim_E', 'pim1_E + ks_E')

df = df.Define('kspim_m', 'sqrt(kspim_E*kspim_E - kspim_px*kspim_px - kspim_py*kspim_py - kspim_pz*kspim_pz)')

df = df.Define('kppim_px', 'pim1_px + kp_px')
df = df.Define('kppim_py', 'pim1_py + kp_py')
df = df.Define('kppim_pz', 'pim1_pz + kp_pz')
df = df.Define('kppim_E', 'pim1_E + kp_E')

df = df.Define('kppim_m', 'sqrt(kppim_E*kppim_E - kppim_px*kppim_px - kppim_py*kppim_py - kppim_pz*kppim_pz)')

df = df.Define('pimkpks_px', 'pim1_px + kp_px + ks_px')
df = df.Define('pimkpks_py', 'pim1_py + kp_py + ks_py')
df = df.Define('pimkpks_pz', 'pim1_pz + kp_pz + ks_pz')
df = df.Define('pimkpks_E', 'pim1_E + kp_E + ks_E')

df = df.Define('pimkpks_m', 'sqrt(pimkpks_E*pimkpks_E - pimkpks_px*pimkpks_px - pimkpks_py*pimkpks_py - pimkpks_pz*pimkpks_pz)')

kstar_plus_cut = 'kspim_m < 0.8 || kspim_m > 1.0'
kstar_zero_cut = 'kppim_m < 0.8 || kppim_m > 1.0'
kstar_all_cut = '(kspim_m < 0.8 || kspim_m > 1.0) && (kppim_m < 0.8 || kppim_m > 1.0)'

f1_nocut = df.Histo1D(('f1_nocut', 'f1_nocut', 50, 1.0, 1.7), 'pimkpks_m')
f1_kstar_plus_cut = df.Filter(kstar_plus_cut).Histo1D(('f1_kstar_plus_cut', 'f1_kstar_plus_cut', 50, 1.0, 1.7), 'pimkpks_m')
f1_kstar_zero_cut = df.Filter(kstar_zero_cut).Histo1D(('f1_kstar_zero_cut', 'f1_kstar_zero_cut', 50, 1.0, 1.7), 'pimkpks_m')
f1_kstar_all_cut = df.Filter(kstar_all_cut).Histo1D(('f1_kstar_all_cut', 'f1_kstar_all_cut', 50, 1.0, 1.7), 'pimkpks_m')

f1_nocut.SetLineColor(1)
f1_kstar_plus_cut.SetLineColor(2)
f1_kstar_zero_cut.SetLineColor(6)
f1_kstar_all_cut.SetLineColor(8)

df = df.Filter(kstar_all_cut)

beam_df_array = []

for beam_value in range(5, 11):
    beam_low = beam_value - 0.5
    beam_high = beam_value + 0.5
    beam_df_array.append(df.Filter('e_beam > {} && e_beam <= {}'.format(beam_low, beam_high)))

# df_beam_5 = df.Filter('e_beam > 4.5 && e_beam <= 5.5')
# df_beam_6 = df.Filter('e_beam > 5.5 && e_beam <= 6.5')
# df_beam_7 = df.Filter('e_beam > 6.5 && e_beam <= 7.5')
# df_beam_8 = df.Filter('e_beam > 7.5 && e_beam <= 8.5')
# df_beam_9 = df.Filter('e_beam > 8.5 && e_beam <= 9.5')
# df_beam_10 = df.Filter('e_beam > 9.5 && e_beam <= 10.5')

print("beam cuts done in {} seconds".format(time.time() - start_time))


histo_array_low = []
histo_array_med = []
histo_array_high = []

t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']

for i in range(len(beam_df_array)):
    beam = i + 5
    for t in t_low:
        histo_array_low.append(beam_df_array[i].Filter('mand_t > ({} - 0.1) && mand_t <= {}'.format(t, t)).Histo1D(('pimkpks_beam_{}_t_{}'.format(beam, t), 'pimkpks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pimkpks_m'))
    for t in t_med:
        histo_array_med.append(beam_df_array[i].Filter('mand_t > ({} - 0.25) && mand_t <= {}'.format(t, t)).Histo1D(('pimkpks_beam_{}_t_{}'.format(beam, t), 'pimkpks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pimkpks_m'))
    for t in t_high:
        histo_array_high.append(beam_df_array[i].Filter('mand_t > ({} - 0.5) && mand_t <= {}'.format(t, t)).Histo1D(('pimkpks_beam_{}_t_{}'.format(beam, t), 'pimkpks_beam_{}_t_{}'.format(beam, t), 50, 1.0, 1.7), 'pimkpks_m'))

# print(len(histo_array_low))
print("histos done in {} seconds".format(time.time() - start_time))

target_file = ROOT.TFile("/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pimkpks_flat_result_2018_fall.root", 'RECREATE')
for histo in histo_array_low:
    histo.Write()
for histo in histo_array_med:
    histo.Write()
for histo in histo_array_high:
    histo.Write()

target_file.Close()