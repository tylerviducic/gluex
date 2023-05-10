# barebones script for plotting things for things for thesis 
# each plotting snippet will become a function in thesis_plotter.py
# main at the bttom will be used to call the needed functions

import ROOT
from common_analysis_tools import *
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

def get_flat_data_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/data'
    treename = ''
    if not comboloop:
        file_path += f'/bestX2/{channel}_'
        if filtered:
            file_path += f'flat_bestX2_{run_dict[run_period]}.root'
            treename = f'{channel}_filetered_{run_dict[run_period]}'
        else:
            if hist:
                file_path += f'flat_result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{run_dict[run_period]}.root'
                treename = f'{channel}__B4_M16'
    else:
        file_path += f'/comboloop/{channel}_comboloop_flat_{run_dict[run_period]}.root'
        treename = f'{channel}__B4_M16'
    return (file_path, treename)

def get_flat_signal_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/mc/signal/mc_{channel}_'
    treename = ''
    if not comboloop:
        if filtered:
            file_path += f'filtered_{run_dict[run_period]}.root'
            treename = f'mc_{channel}_filtered_{run_dict[run_period]}'
        else:
            if hist:
                file_path += f'result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2{run_dict[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop signal mc file yet')
    return (file_path, treename)

def get_flat_phasespace_file_and_tree(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/mc/phasespace/mc_{channel}_phasespace_'
    if not comboloop:
        if filtered:
            file_path += f'filtered_{run_dict[run_period]}.root'
            treename = f'mc_{channel}_phasespace_filtered_{run_dict[run_period]}'
        else:
            if hist:
                file_path += f'result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2{run_dict[run_period]}.root'
                treename = f'{channel}__ks_pippim__B4_M16'
    else:
        print('no comboloop phasespace mc file yet')
    return (file_path, treename)

def get_flat_thrown_file_and_tree(channel, run_period):
    return f'/work/hall/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_flat_result_{run_dict[run_period]}.root'


def get_needed_flat_file_and_tree(channel, run_period, datatype, comboloop=False, filtered=True, hist=False):
    file_tuple = ()
    if datatype == 'data':
        file_tuple = get_flat_data_file_and_tree(channel, run_period, comboloop, filtered, hist)
    elif datatype == 'signal':
        file_tuple = get_flat_signal_file_and_tree(channel, run_period, comboloop, filtered, hist)
    elif datatype == 'phasespace':
        file_tuple = get_flat_phasespace_file_and_tree(channel, run_period, comboloop, filtered, hist)
    elif datatype == 'thrown':
        file_tuple = get_flat_thrown_file_and_tree(channel, run_period)
    else:
        print('invalid datatype')
        return
    print(f'filepath: {file_tuple[0]}')
    return file_tuple

#TODO write this function
def plot_data_kshort_no_cuts():
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2017.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)


if __name__ == "__main__":
    plot_data_kshort_no_cuts()