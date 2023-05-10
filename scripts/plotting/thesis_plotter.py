# barebones script for plotting things for things for thesis 
# each plotting snippet will become a function in thesis_plotter.py
# main at the bttom will be used to call the needed functions

import ROOT
from common_analysis_tools import *
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

#TODO add treename to these functions, return list or tuple

def get_flat_data_file(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/data'
    treename = ''
    if not comboloop:
        file_path += f'/bestX2/{channel}_'
        if filtered:
            file_path += f'flat_bestX2_{run_dict[run_period]}.root'
        else:
            if hist:
                file_path += f'flat_result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2_{run_dict[run_period]}.root'
    else:
        file_path += f'/comboloop/{channel}_comboloop_flat_{run_dict[run_period]}.root'
    return file_path

def get_flat_signal_file(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/mc/signal/mc_{channel}_'
    if not comboloop:
        if filtered:
            file_path += f'filtered_{run_dict[run_period]}.root'
        else:
            if hist:
                file_path += f'result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2{run_dict[run_period]}.root'
    else:
        print('no comboloop signal mc file yet')
    return file_path

def get_flat_phasespace_file(channel, run_period, comboloop=False, filtered=True, hist=False):
    file_path = f'/work/hall/home/viducic/data/{channel}/mc/phasespace/mc_{channel}_phasespace_'
    if not comboloop:
        if filtered:
            file_path += f'filtered_{run_dict[run_period]}.root'
        else:
            if hist:
                file_path += f'result_{run_dict[run_period]}.root'
            else:
                file_path += f'flat_bestX2{run_dict[run_period]}.root'
    else:
        print('no comboloop phasespace mc file yet')
    return file_path

def get_flat_thrown_file(channel, run_period):
    return f'/work/hall/home/viducic/data/{channel}/mc/thrown/mc_{channel}_thrown_flat_result_{run_dict[run_period]}.root'


def get_needed_flat_file(channel, run_period, datatype, comboloop=False, filtered=True, hist=False):
    if datatype == 'data':
        filepath = get_flat_data_file(channel, run_period, comboloop, filtered, hist)
        print(f'filepath: {filepath}')
    elif datatype == 'signal':
        filepath = get_flat_signal_file(channel, run_period, comboloop, filtered, hist)
    elif datatype == 'phasespace':
        filepath = get_flat_phasespace_file(channel, run_period, comboloop, filtered, hist)
    elif datatype == 'thrown':
        filepath = get_flat_thrown_file(channel, run_period)
    else:
        print('invalid datatype')
        return
    return filepath



def plot_data_kshort_no_cuts():
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2017.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)


if __name__ == "__main__":
    plot_data_kshort_no_cuts()