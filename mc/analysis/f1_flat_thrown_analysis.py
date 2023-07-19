# script to run analysis of thrown data, both signal and phasespace

import ROOT
import time
import os
import my_library.common_analysis_tools as ct
import sys

"""
usage of this file is as follows:
python3 f1_flat_thrown_analysis.py <channel> <run_period> <data_type>
"""

os.nice(18)
ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
start_time = time.time()

channel = sys.argv[1]
run_period = sys.argv[2]
data_type = sys.argv[3]

ct.verify_thrown_args(channel, run_period, data_type)


file_and_tree = ct.get_flat_file_and_tree(channel, run_period, data_type, filtered=False, thrown=True)

histo_array = []

## LOAD IN DATA ##
df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

## DEFINE ALL NECESSARY COLUMNS ##

df = ct.define_columns(df, channel)

histo_array.append(df.Histo1D(('pipkmks', 'pipkmks', 150, 1.0, 2.5), 'pipkmks_m'))

n_e_bins = len(ct.ALLOWED_E_BINS)
n_t_bins = len(ct.ALLOWED_T_BINS)

def fill_histos(cut_df, histo_array, beam_index=0, t_index=0):
    hist_name = f'{channel}_'
    beam_name = 'beam_full_'
    t_name = 't_full'
    if beam_index > 0:
        beam_low = ct.BEAM_INDEX_DICT[beam_index][0]
        beam_high = ct.BEAM_INDEX_DICT[beam_index][1]
        beam_name = f'beam_{beam_low}_{beam_high}_'
    if t_index > 0:
        t_low = ct.T_CUT_DICT[t_index][0]
        t_high = ct.T_CUT_DICT[t_index][1]
        t_name = f't_{t_low}_{t_high}'
    hist_name += beam_name + t_name
    histo_array.append(cut_df.Histo1D((hist_name, hist_name, 150, 1.0, 2.5), f'{channel}_m'))


for energy_index in range(1, n_e_bins+1):
    e_cut_df = df.Filter(f'e_bin == {energy_index}')
    fill_histos(e_cut_df, histo_array, beam_index=energy_index)


    for t_index in range(1, n_t_bins+1):
        e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
        fill_histos(e_t_cut_df, histo_array, beam_index=energy_index, t_index=t_index)


for t_index in range(1, n_t_bins+1):
        t_cut_df = df.Filter(f't_bin == {t_index}')
        fill_histos(t_cut_df, histo_array, t_index=t_index)

print("histos done in {} seconds".format(time.time() - start_time))

## WRITE HISTOGRAMS TO FILE ##

output_path = ct.get_path_for_output_file(channel, run_period, data_type, thrown=True)

target_file = ROOT.TFile(f"{output_path}/mc_{channel}_thrown_{data_type}_flat_result_{ct.RUN_DICTt[run_period]}.root", 'RECREATE')
print('file created in {} seconds'.format(time.time() - start_time))

for histo in histo_array:
    histo.Write()


print("histos written in {} seconds".format(time.time() - start_time))
target_file.Close() 

ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/mc_{channel}_{data_type}_thrown_graph_{ct.RUN_DICT[run_period]}.dot")
