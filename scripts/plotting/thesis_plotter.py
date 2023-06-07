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
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = df.Define("ks_px", 'pip2_px + pim_px')
    df = df.Define("ks_py", 'pip2_py + pim_py')
    df = df.Define("ks_pz", 'pip2_pz + pim_pz')
    df = df.Define("ks_E", 'pip2_E + pim_E')
    df = df.Define("ks_m", 'sqrt(ks_E*ks_E - ks_px*ks_px - ks_py*ks_py - ks_pz*ks_pz)')
    hist_no_cut = df.Histo1D(('ks_m', 'ks_m', 500, 0.35, 0.65), 'ks_m')
    hist_cut = df.Filter(KS_PATHLENGTH_CUT).Histo1D(('ks_m', 'ks_m', 500, 0.35, 0.65), 'ks_m')
    hist_cut.SetLineColor(ROOT.kRed)
    c = ROOT.TCanvas()
    hist_no_cut.Draw()
    hist_cut.Draw("SAME")
    c.Update()
    input("Press Enter to continue...")

def result_of_p_p_cut():
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = df.Define('p_p', 'sqrt(p_px*p_px + p_py*p_py + p_pz*p_pz)')
    hist_t_mand = df.Histo1D(('mand_t', 'mand_t', 500, 0.0, 1.0), 'mand_t')
    hist_cut_tmand = df.Filter('p_p > 0.4').Histo1D(('mand_t_cut', 'mand_t_cut', 500, 0.0, 1.0), 'mand_t')
    hist_cut_tmand.SetLineColor(ROOT.kRed)
    c = ROOT.TCanvas()
    hist_t_mand.Draw()
    hist_cut_tmand.Draw("SAME")
    c.Update()
    input("Press Enter to continue...")

def plot_mx2_all():
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)


    df = df.Define('ks_px_measured', "pip2_px_measured + pim_px_measured")
    df = df.Define('ks_py_measured', "pip2_py_measured + pim_py_measured")
    df = df.Define('ks_pz_measured', "pip2_pz_measured + pim_pz_measured")
    df = df.Define('ks_E_measured', "pip2_E_measured + pim_E_measured")
    df = df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

    df = df.Define('mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
    df = df.Define('mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
    df = df.Define('mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
    df = df.Define('mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
    df = df.Define('mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')
     
    # c = ROOT.TCanvas()
    hist = df.Histo1D(('mx2_ppipkmks', 'mx2_ppipkmks', 500, -0.05, 0.05), 'mx2_ppipkmks')
    hist.Draw()
    input("Press Enter to continue...")

def plot_pipkmks_phasespace_with_cuts():
    file_and_tree = get_flat_phasespace_file_and_tree('pipkmks', 'spring')

    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

    c = ROOT.TCanvas()
    hist_cut = df.Filter(KSTAR_ALL_CUT).Histo1D(('pipkmks', 'pipkmks', 100, 1.1, 2.0), 'pipkmks_m')
    hist = df.Histo1D(('pipkmks', 'pipkmks', 100, 1.1, 2.0), 'pipkmks_m')
    hist.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
    hist_cut.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
    hist.Draw()
    hist_cut.Draw("SAME")
    c.Update()
    input("Press Enter to continue...")
    

if __name__ == "__main__":
    ROOT.gStyle.SetOptStat(0)
    # plot_data_kshort_no_cuts()
    # result_of_p_p_cut()
    # plot_mx2_all()
    plot_pipkmks_phasespace_with_cuts()