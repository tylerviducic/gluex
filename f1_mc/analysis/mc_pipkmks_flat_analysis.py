# script for making histograms from MONTE CARLO flat best chi2/ndf trees

import ROOT
import time
import os


os.nice(18)
ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

start_time = time.time()


run_period_dict = {
    'spring': '2018_spring',
    'fall': '2018_fall',
    '2017': '2017',
}

run_period = 'spring'
filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_flat_bestX2_{run_period_dict[run_period]}.root'
treename = 'pipkmks__ks_pippim__B4_M16'

histo_array = []

t_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
t_med = ['0.65', '0.9']
t_high = ['1.4', '1.9']#, '1.7', '1.9']

t_dict = {
    1: (0.0, 0.1), 2: (0.1, 0.2), 3: (0.2, 0.3), 4: (0.3, 0.4), 
    5: (0.4, 0.65), 6: (0.65, 0.9), 7: (0.9, 1.4), 8: (1.4, 1.9)
}

beam_dict = {
    1: (6.5, 7.5), 2: (7.5, 8.5), 3: (8.5, 9.5), 4: (9.5, 10.5)
}


## DEFINE CUTS ##
#TODO cuts to not be just-in-time compiled

ks_pathlength_cut = 'pathlength_sig > 5'
ks_cut1 = 'cos_colin > 0.99'
ks_cut2 = ' vertex_distance > 3'
ks_mass_cut = 'ks_m > 0.45 && ks_m < 0.55'
ppim_mass_cut = 'ppip_m > 1.4'
kmp_mass_cut = 'kmp_m > 1.95'
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'
beam_range = 'e_beam > 6.50000000000 && e_beam <= 10.5'
t_range = 'mand_t <= 1.9'

kstar_no_cut = 'kspip_m > 0.0'
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

kstar_cut_dict = {
    'kspip_m > 0.0': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

f1_cut_list = [kstar_no_cut, kstar_plus_cut, kstar_zero_cut, kstar_all_cut]

t_bin_filter = """
int get_t_bin_index(double t) {
    if (t <= 0.4) {
        return static_cast<int>(t/0.1)+1;
    }
    else if (t > 0.4 && t <= 0.9) {
        return static_cast<int>((t-0.4)/0.25)+5;
    }
    else if (t > 0.9 && t <= 1.9) {
        return static_cast<int>((t-0.9)/0.5)+7;
    }
    else {
        return -1;
    }
}
"""

ROOT.gInterpreter.Declare(t_bin_filter)

## LOAD IN DATA ##

df = ROOT.RDataFrame(treename, filename)


## DEFINE ALL NECESSARY COLUMNS ##

df = df.Define('ks_px', "pip2_px + pim_px")
df = df.Define('ks_py', "pip2_py + pim_py")
df = df.Define('ks_pz', "pip2_pz + pim_pz")
df = df.Define('ks_E', "pip2_E + pim_E")
df = df.Define('ks_m', "sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)")

df = df.Define('ppip_px', 'pip1_px + p_px')
df = df.Define('ppip_py', 'pip1_py + p_py')
df = df.Define('ppip_pz', 'pip1_pz + p_pz')
df = df.Define('ppip_E', 'pip1_E + p_E')
df = df.Define('ppip_m', 'sqrt(ppip_E*ppip_E - ppip_px*ppip_px - ppip_py*ppip_py - ppip_pz*ppip_pz)')


df = df.Define('missing_px', '-p_px - pip1_px - ks_px - km_px')
df = df.Define('missing_py', '-p_py - pip1_py - ks_py - km_py')
df = df.Define('missing_pz', 'e_beam - p_pz - pip1_pz - ks_pz - km_pz')
df = df.Define('missing_E', 'e_beam + 0.938 - p_E - pip1_E - ks_E - km_E')

df = df.Define('kmp_px', 'p_px + km_px')
df = df.Define('kmp_py', 'p_py + km_py')
df = df.Define('kmp_pz', 'p_pz + km_pz')
df = df.Define('kmp_E', 'p_E + km_E')

df = df.Define('kmp_m', 'sqrt(kmp_E*kmp_E - kmp_px*kmp_px - kmp_py*kmp_py - kmp_pz*kmp_pz)')

df = df.Define('missing_m', 'sqrt(missing_E*missing_E - missing_px*missing_px - missing_py*missing_py - missing_pz*missing_pz)')

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

df = df.Define('kmks_px', 'km_px + ks_px')
df = df.Define('kmks_py', 'km_py + ks_py')
df = df.Define('kmks_pz', 'km_pz + ks_pz')
df = df.Define('kmks_E', 'km_E + ks_E')
df = df.Define('kmks_m', 'sqrt(kmks_E*kmks_E - kmks_px*kmks_px - kmks_py*kmks_py - kmks_pz*kmks_pz)')

df = df.Define('e_bin', 'int(e_beam-6.5) +1')
df = df.Define('t_bin', 'get_t_bin_index(mand_t)')

## FILTER DATAFRAME AFTER DATA IS DEFINED ##

df = df.Filter(ks_pathlength_cut)
print('cut 1 done in {} seconds'.format(time.time() - start_time))
df = df.Filter(ks_mass_cut)
print('cut 2 done in {} seconds'.format(time.time() - start_time))
df = df.Filter(ppim_mass_cut)
print("cut 3 done in {} seconds".format(time.time() - start_time))
df = df.Filter(kmp_mass_cut)
print("cut 4 done in {} seconds".format(time.time() - start_time))

## MAKE HISTOGRAMS ##

ks_m = df.Histo1D(('ks_m', 'ks_m', 100, 0.3, 0.7), 'ks_m')

## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
df.Snapshot(f'mc_pipkmks_filtered_{run_period_dict[run_period]}', f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_filtered_{run_period_dict[run_period]}.root')

## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
df = df.Filter(beam_range).Filter(t_range)

print('cut file written in {} seconds'.format(time.time() - start_time))

## DEFINE FUNCTION TO LOOP OVER ENERGY AND T BINS ##

def fill_and_store_histograms(hlist, filtered_df, n_e_bins, n_t_bins, cut):
        cut_name = kstar_cut_dict[cut]
        
        hlist.append(filtered_df.Histo1D(('tslope_{}'.format(kstar_cut_dict[cut]), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))

        for energy_index in range(1, n_e_bins+1):
            beam_low = beam_dict[energy_index][0]
            beam_high = beam_dict[energy_index][1]
            hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('tslope_{}_beam_{}-{}'.format(kstar_cut_dict[cut], beam_low, beam_high), 'tslope_{}'.format(kstar_cut_dict[cut]), 100, 0.0, 2.0), 'mand_t'))
            hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_narrow'.format(beam_low, beam_high, cut_name), 50, 1.0, 1.7), 'pipkmks_m'))
            hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_medium'.format(beam_low, beam_high, cut_name), 100, 1.0, 2.5), 'pipkmks_m'))
            hlist.append(filtered_df.Filter(f'e_bin == {energy_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 'pipkmks_beam_{}-{}_cut_{}_full_t_wide'.format(beam_low, beam_high, cut_name), 200, 1.0, 3.8), 'pipkmks_m'))


            for t_index in range(1, n_t_bins+1):
                t_low = t_dict[t_index][0]
                t_high = t_dict[t_index][1]
                histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_narrow'.format(beam_low, beam_high, cut_name, t_low, t_high), 50, 1.0, 1.7), 'pipkmks_m'))
                histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_medium'.format(beam_low, beam_high, cut_name, t_low, t_high), 100, 1.0, 2.5), 'pipkmks_m'))
                histo_array.append(filtered_df.Filter(f'e_bin == {energy_index}').Filter(f't_bin == {t_index}').Histo1D(('pipkmks_beam_{}_{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 'pipkmks_beam_{}-{}_cut_{}_t_{}-{}_wide'.format(beam_low, beam_high, cut_name, t_low, t_high), 200, 1.0, 3.8), 'pipkmks_m'))

        return hlist

## LOOP OVER K* CUTS AND EXECUTE HISTO FILLING FUNCTION ##

for cut in f1_cut_list:
    histo_array = fill_and_store_histograms(histo_array, df.Filter(cut), 4, 8, cut=cut)

print("histos done in {} seconds".format(time.time() - start_time))

## WRITE HISTOGRAMS TO FILE ##

target_file = ROOT.TFile(f"/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/MC_pipkmks_flat_result_{run_period_dict[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))

ks_m.Write()

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close() 

