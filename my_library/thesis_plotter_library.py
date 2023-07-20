# library for plotting in a notebook for my thesis

import ROOT
import my_library.common_analysis_tools as ct
import os
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

def save_plot(canvas, filename):
    path_to_thesis_plots = '/work/halld/home/viducic/plots/thesis/'
    canvas.SaveAs(path_to_thesis_plots + filename + '.png')

def build_legend(histograms: list, x1=0.7, y1=0.7, x2=0.9, y2=0.9):
    print("building legend")
    legend = ROOT.TLegend(x1, y1, x2, y2)
    for hist in histograms:
        legend.AddEntry(hist, hist.GetTitle(), 'l')
    return legend

def get_ks_before_after_cut(bin_low=0.3, bin_high=0.7, nbins=500):
    os.nice(18)
    ROOT.EnableImplicitMT()
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = ct.define_columns(df, 'pipkmks')

    df.Filter(ct.MX2_PPIPKMKS_CUT)

    hist_no_cut = df.Histo1D(('ks_m', 'ks_m', nbins, bin_low, bin_high), 'ks_m')
    hist_no_cut.SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist_no_cut.GetXaxis().SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist_no_cut.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_cut = df.Filter(ct.KS_PATHLENGTH_CUT).Histo1D(('ks_m', 'ks_m', nbins, bin_low, bin_high), 'ks_m')
    hist_cut.SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist_cut.GetXaxis().SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist_cut.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_no_cut.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_cut.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red']))
    hist_cut.SetDirectory(0)
    hist_no_cut.SetDirectory(0)
    return hist_no_cut.GetValue(), hist_cut.GetValue()

def get_mpipi_vs_pathlength_sig(bin_lowx=0.3, bin_highx=0.7, bin_lowy=0, bin_highy=10, nbinsx=200, nbinsy=200):
    os.nice(18)
    ROOT.EnableImplicitMT()
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = ct.define_columns(df, 'pipkmks')
    df.Filter(ct.MX2_PPIPKMKS_CUT)

    hist = df.Histo2D(('ks_m_vs_pathlength', 'ks_m_vs_pathlength', nbinsx, bin_lowx, bin_highx, nbinsy, bin_lowy, bin_highy), 'ks_m', 'pathlength_sig')
    hist.SetTitle("M(#pi^{+}#pi^{-}) vs. Pathlength Signifigance")
    hist.GetXaxis().SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist.GetYaxis().SetTitle("Pathlength Signifigance")
    hist.SetDirectory(0)
    return hist.GetValue()

def result_of_p_p_cut(nbins= 500, xlow=0.0, xhigh=2.0):
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = ct.define_columns(df, 'pipkmks')
    df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT)
    hist_t_mand = df.Histo1D(('mand_t', 'mand_t', nbins, xlow, xhigh), 'mand_t')
    hist_t_mand.SetTitle("-t = M^{2}(p - p^{\\prime}) GeV^{2}")
    hist_t_mand.GetXaxis().SetTitle("M^{2}(p - p^{\\prime}) GeV^{2}")
    hist_t_mand.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/nbins):.2f} MeV")
    hist_t_mand.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_cut_tmand = df.Filter(ct.P_P_CUT).Histo1D(('mand_t_cut', 'mand_t_cut', nbins, xlow, xhigh), 'mand_t')
    hist_cut_tmand.SetTitle("-t = M^{2}(p - p^{\\prime}) GeV^{2}")
    hist_cut_tmand.GetXaxis().SetTitle("M^{2}(p - p^{\\prime}) GeV^{2}")
    hist_cut_tmand.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/nbins):.2f} MeV")
    hist_cut_tmand.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red']))
    hist_cut_tmand.SetDirectory(0)
    hist_t_mand.SetDirectory(0)
    return hist_t_mand.GetValue(), hist_cut_tmand.GetValue()

def plot_mx2_all(bin_low=-0.05, bin_high=0.05, nbins=500):
    data_file = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
    file_treename = 'pipkmks__B4_M16'

    df = ROOT.RDataFrame(file_treename, data_file)
    df = ct.define_columns(df, 'pipkmks')
     
    hist = df.Histo1D(('mx2_ppipkmks', 'mx2_ppipkmks', nbins, bin_low, bin_high), 'mx2_ppipkmks')
    hist.SetTitle("MX^{2}(p#pi^{+}K^{-}K_{S}) [GeV]")
    hist.GetXaxis().SetTitle("MX^{2}(p#pi^{+}K^{-}K_{S}) [GeV]")
    hist.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist.SetDirectory(0)
    return hist 

def plot_pipkmks_phasespace_with_cuts():
    file_and_tree = ct.get_flat_phasespace_file_and_tree('pipkmks', 'spring')

    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])

    c = ROOT.TCanvas()
    hist_cut = df.Filter(ct.KSTAR_ALL_CUT_PIPKMKS).Histo1D(('pipkmks', 'pipkmks', 100, 1.1, 2.0), 'pipkmks_m')
    hist = df.Histo1D(('pipkmks', 'pipkmks', 100, 1.1, 2.0), 'pipkmks_m')
    hist.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_cut.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red']))
    hist.Draw()
    hist_cut.Draw("SAME")
    c.Update()
    input("Press Enter to continue...")
    

if __name__ == "__main__":
    ROOT.gStyle.SetOptStat(0)
    # get_ks_before_after_cut
    #()
    # result_of_p_p_cut()
    # plot_mx2_all()
    plot_pipkmks_phasespace_with_cuts()