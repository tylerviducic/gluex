# barebones script for plotting things for things for thesis 
# each plotting snippet will become a function in thesis_plotter.py
# main at the bttom will be used to call the needed functions

import ROOT
from common_analysis_tools import *
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt


#TODO write this function
def plot_data_kshort_no_cuts():
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2017.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)


if __name__ == "__main__":
    plot_data_kshort_no_cuts()