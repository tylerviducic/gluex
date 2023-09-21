# script for making histograms from flat best chi2/ndf trees for any datatype
import ROOT
import time
import os
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import my_library.kinematic_cuts as kcuts
import sys

def run_analysis(channel, run_period, data_type, thrown=False):
    """
    Function to run analysis over a given channel, run period, and data type.
    """

    os.nice(18)
    ROOT.EnableImplicitMT()
    ROOT.gStyle.SetOptStat(0)
    start_time = time.time()

    ct.verify_args(channel, run_period, data_type)

    df = ct.get_dataframe(channel, run_period, data_type, filtered=False, thrown=thrown)

    output_path = ct.get_path_for_output_file(channel, data_type, thrown=thrown)
    result_filename = ct.get_filename_for_output_file(channel, run_period, data_type, thrown=thrown)



    # if run_period == '2019_unconstrained':
    #     treename = 'pimkpks__T1_S2_M16'
    # elif run_period == '2019_constrained':
    #     treename = 'pimkpks__T1_S2'

    histo_array = []

    ## FILTER DATAFRAME AFTER DATA IS DEFINED ##
    if not thrown:
        df = ct.filter_dataframe(df, channel)
        print('cuts done in {} seconds'.format(time.time() - start_time))

        ## SAVE FILTERED DATA FOR USE ELSEWHERE IF NEEDED ##
        ## COMMENT/UNCOMMENT AS NEEDED WHEN CHANGING THINGS ABOVE THIS LINE ##
        df.Snapshot(f'{channel}_filtered_{constants.RUN_DICT[run_period]}', f'{output_path}/{channel}_filtered_{constants.RUN_DICT[run_period]}.root')

        # ## FILTER BEAM AND T RANGE TO FIT WITHIN THE INDEX SET EARLIER ##
        df = df.Filter(kcuts.BEAM_RANGE).Filter(kcuts.T_RANGE)

        if channel == 'pipkmks':
            cut_dict = kcuts.KSTAR_CUT_DICT_PIPKMKS
        elif channel == 'pimkpks':
            cut_dict = kcuts.KSTAR_CUT_DICT_PIMKPKS

    print('cut file written in {} seconds'.format(time.time() - start_time))

    ## LOOP OVER K* CUTS AND EXECUTE HISTO FILLING FUNCTION ##

    n_e_bins = len(constants.ALLOWED_E_BINS)
    n_t_bins = len(constants.ALLOWED_T_BINS)

    if not thrown:
        for cut in cut_dict:
            cut_df = df.Filter(cut_dict[cut])
            ct.fill_histos(cut_df, histo_array, channel, cut, beam_index=0, t_index=0)
                
            for energy_index in range(1, n_e_bins+1):
                e_cut_df = cut_df.Filter(kcuts.SELECT_BEAM_BIN.format(energy_index))
                ct.fill_histos(e_cut_df, histo_array, channel, cut=cut, beam_index=energy_index)

                for t_index in range(1, n_t_bins+1):
                    e_t_cut_df = e_cut_df.Filter(kcuts.SELECT_T_BIN.format(t_index))
                    ct.fill_histos(e_t_cut_df, histo_array, channel, cut=cut, beam_index=energy_index, t_index=t_index)
                
            for t_index in range(1, n_t_bins+1):
                t_cut_df = cut_df.Filter(kcuts.SELECT_T_BIN.format(t_index))
                ct.fill_histos(t_cut_df, histo_array, channel, cut=cut, t_index=t_index)
    else:
        for energy_index in range(1, n_e_bins+1):
            e_cut_df = df.Filter(f'e_bin == {energy_index}')
            ct.fill_histos(e_cut_df, histo_array, channel, beam_index=energy_index)


            for t_index in range(1, n_t_bins+1):
                e_t_cut_df = e_cut_df.Filter(f't_bin == {t_index}')
                ct.fill_histos(e_t_cut_df, histo_array, channel, beam_index=energy_index, t_index=t_index)


        for t_index in range(1, n_t_bins+1):
                t_cut_df = df.Filter(f't_bin == {t_index}')
                ct.fill_histos(t_cut_df, histo_array, channel, t_index=t_index)

    print("histos done in {} seconds".format(time.time() - start_time))

    ## WRITE HISTOGRAMS TO FILE ##

    target_file = ROOT.TFile(f"{output_path}/{result_filename}", 'RECREATE')
    print('file created in {} seconds'.format(time.time() - start_time))

    for histo in histo_array:
        histo.Write()


    print("histos written in {} seconds".format(time.time() - start_time))
    target_file.Close()

    if not thrown:
        ROOT.RDF.SaveGraph(df, f"/work/halld/home/viducic/plots/analysis_graphs/{channel}_{data_type}_graph_{constants.RUN_DICT[run_period]}.dot")
