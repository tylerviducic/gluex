# library for plotting in a notebook for my thesis

import ROOT
import my_library.common_analysis_tools as ct
import os
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

def get_dataframe(channel='pipkmks', run_period='spring', datatype='data'):
    file_and_tree = ct.get_flat_file_and_tree(channel, run_period, datatype, filtered=False)
    df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0])
    return ct.define_columns(df, channel)


def save_plot(canvas, filename):
    path_to_thesis_plots = '/work/halld/home/viducic/plots/thesis/'
    canvas.SaveAs(path_to_thesis_plots + filename + '.png')


def build_legend(histograms: list, x1=0.7, y1=0.7, x2=0.9, y2=0.9, labels: list=[]):
    if len(labels) != len(histograms):
        labels = [hist.GetTitle() for hist in histograms]
    print("building legend")
    legend = ROOT.TLegend(x1, y1, x2, y2)
    for hist in histograms:
        legend.AddEntry(hist, labels[histograms.index(hist)], 'l')
    return legend


def build_kkpi_title(channel, cut=None):
    validate_kstar_cut(channel, cut)
    if channel == 'pipkmks':
        title = "M(K^{-}K_{s}#pi^{+})"
    elif channel == 'pimkpks':
        title = "M(K^{+}K_{s}#pi^{-})"
    if not cut or cut == 'no':
        cut_info = ''
    else:
        cut_info = f" with " + ct.KSTAR_CUT_TITLE_DICT[cut]
    title += cut_info
    return title


def build_f1_1420_title(channel, kept_kstar):
    if channel == 'pipkmks':
        title = "M(K^{+}K^{-}#pi^{+}) with "
        if kept_kstar == 'charged':
            kept_charge_info = "K*^{+} Selected and K*^{0} Rejected"
        elif kept_kstar == 'neutral':
            kept_charge_info = "K*^{0} Selected and K*^{+} Rejected"
    elif channel == 'pimkpks':
        title = "M(K^{+}K^{-}#pi^{-}) with "
        if kept_kstar == 'charged':
            kept_charge_info = "K*^{-} Selected and K*^{0} Rejected"
        elif kept_kstar == 'neutral':
            kept_charge_info = "K*^{0} Selected and K*^{-} Rejected"
    title += kept_charge_info
    return title


def get_ks_before_after_cut(bin_low=0.3, bin_high=0.7, nbins=500):
    os.nice(18)
    ROOT.EnableImplicitMT()
    df = get_dataframe()
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
    df = get_dataframe()
    df.Filter(ct.MX2_PPIPKMKS_CUT)

    hist = df.Histo2D(('ks_m_vs_pathlength', 'ks_m_vs_pathlength', nbinsx, bin_lowx, bin_highx, nbinsy, bin_lowy, bin_highy), 'ks_m', 'pathlength_sig')
    hist.SetTitle("M(#pi^{+}#pi^{-}) vs. Pathlength Signifigance")
    hist.GetXaxis().SetTitle("M(#pi^{+}#pi^{-}) [GeV]")
    hist.GetYaxis().SetTitle("Pathlength Signifigance")
    hist.SetDirectory(0)
    return hist.GetValue()


def result_of_p_p_cut(nbins= 500, xlow=0.0, xhigh=2.0):
    df = get_dataframe()
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


def plot_delta(bin_low=1.0, bin_high=2.5, nbins=200):
    df = get_dataframe()
    df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    hist_delta = df.Histo1D(('ppip_m', 'M(p#pi^{+}) GeV', nbins, bin_low, bin_high), 'ppip_m')
    hist_delta.SetTitle("M(p#pi^{+}) GeV")
    hist_delta.GetXaxis().SetTitle("M(p#pi^{+}) GeV")
    hist_delta.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_delta.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_delta.SetDirectory(0)
    return hist_delta.GetValue()


def plot_nstar(bin_low=1.0, bin_high=2.5, nbins=200):
    df = get_dataframe(channel='pimkpks')
    df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    hist_nstar = df.Histo1D(('ppim_m', 'M(p#pi^{-}) GeV', nbins, bin_low, bin_high), 'ppim_m')
    hist_nstar.SetTitle("M(p#pi^{-}) GeV")
    hist_nstar.GetXaxis().SetTitle("M(p#pi^{-}) GeV")
    hist_nstar.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_nstar.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_nstar.SetDirectory(0)
    return hist_nstar.GetValue()


def plot_baryons():
    hist_delta = plot_delta()
    hist_nstar = plot_nstar()
    hist_nstar.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red']))
    hist_delta.SetDirectory(0)
    hist_nstar.SetDirectory(0)
    return hist_delta, hist_nstar


def plot_ksp(channel, bin_low=1.4, bin_high=2.5, nbins=200):
    df = get_dataframe(channel)
    df = df.Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    if channel == 'pimkpks':
        df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.PPIM_MASS_CUT)
    elif channel == 'pipkmks':
        df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.PPIP_MASS_CUT)
    hist_ksp = df.Histo1D(('ksp_m', 'M(K_{s}p) GeV', nbins, bin_low, bin_high), 'ksp_m')
    hist_ksp.SetTitle("M(K_{s}p) GeV")
    hist_ksp.GetXaxis().SetTitle("M(K_{s}p) GeV")
    hist_ksp.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_ksp.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_ksp.SetDirectory(0)
    return hist_ksp.GetValue()


def plot_kmp(bin_low=1.4, bin_high=2.5, nbins=200):
    df = get_dataframe()
    df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT).Filter(ct.PPIP_MASS_CUT)
    hist_kmp = df.Histo1D(('kmp_m', 'M(K^{-}p) GeV', nbins, bin_low, bin_high), 'kmp_m')
    hist_kmp.SetTitle("M(K^{-}p) GeV")
    hist_kmp.GetXaxis().SetTitle("M(K^{-}p) GeV")
    hist_kmp.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_kmp.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_kmp.SetDirectory(0)
    return hist_kmp.GetValue()


def plot_kpp(bin_low=1.4, bin_high=2.5, nbins=200):
    df = get_dataframe('pimkpks')
    df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT).Filter(ct.PPIM_MASS_CUT)
    hist_kpp = df.Histo1D(('kpp_m', 'M(K^{+}p) GeV', nbins, bin_low, bin_high), 'kpp_m')
    hist_kpp.SetTitle("M(K^{+}p) GeV")
    hist_kpp.GetXaxis().SetTitle("M(K^{+}p) GeV")
    hist_kpp.GetYaxis().SetTitle(f"Counts/{1000*((bin_high-bin_low)/nbins):.2f} MeV")
    hist_kpp.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_kpp.SetDirectory(0)
    return hist_kpp.GetValue()


def plot_lambdas():
    hist_kmp = plot_kmp()
    hist_kpp = plot_kpp()
    hist_ksp_pipkmks = plot_ksp('pipkmks')
    hist_ksp_pimkpks = plot_ksp('pimkpks')
    return hist_kmp, hist_kpp, hist_ksp_pipkmks, hist_ksp_pimkpks
    

def plot_neutral_kstar(channel, nbins=200, xlow=0.5, xhigh=2.0):
    df = get_dataframe(channel)
    df = df.Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    if channel == 'pimkpks':
        df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.PPIM_MASS_CUT).Filter(ct.KSP_MASS_CUT)
        hist_neutral_kstar = df.Histo1D(('kstar_zero_m', 'M(K^{+}#pi^{-}) GeV', nbins, xlow, xhigh), 'kppim_m')
        hist_neutral_kstar.SetTitle("M(K^{+}#pi^{-}) GeV")
    elif channel == 'pipkmks':
        df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.PPIP_MASS_CUT).Filter(ct.KMP_MASS_CUT)
        hist_neutral_kstar = df.Histo1D(('kstar_zero)_m', 'M(K^{-}#pi^{+}) GeV', nbins, xlow, xhigh), 'kmpip_m')
        hist_neutral_kstar.SetTitle("M(K^{-}#pi^{+}) GeV")
    hist_neutral_kstar.GetXaxis().SetTitle(hist_neutral_kstar.GetTitle())
    hist_neutral_kstar.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/nbins):.2f} MeV")
    hist_neutral_kstar.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_neutral_kstar.SetDirectory(0)
    return hist_neutral_kstar.GetValue()


def plot_charged_kstar(channel, nbins=200, xlow=0.5, xhigh=2.0):
    df = get_dataframe(channel)
    df = df.Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    if channel == 'pimkpks':
        df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.PPIM_MASS_CUT).Filter(ct.KSP_MASS_CUT)
        hist_charged_kstar = df.Histo1D(('kstar_minus_m', 'M(K_{S}#pi^{-}) GeV', nbins, xlow, xhigh), 'kspim_m')
        hist_charged_kstar.SetTitle("M(K_{S}#pi^{+}) GeV")
    elif channel == 'pipkmks':
        df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.PPIP_MASS_CUT).Filter(ct.KMP_MASS_CUT)
        hist_charged_kstar = df.Histo1D(('kstar_plus_m', 'M(K_{S}#pi^{+}) GeV', nbins, xlow, xhigh), 'kspip_m')
        hist_charged_kstar.SetTitle("M(K_{S}#pi^{-}) GeV")
    hist_charged_kstar.GetXaxis().SetTitle(hist_charged_kstar.GetTitle())
    hist_charged_kstar.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/nbins):.2f} MeV")
    hist_charged_kstar.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_charged_kstar.SetDirectory(0)
    return hist_charged_kstar.GetValue()


def plot_kstars():
    hist_charged_kstar_pipkmks = plot_charged_kstar('pipkmks')
    hist_charged_kstar_pimkpks = plot_charged_kstar('pimkpks')
    hist_neutral_kstar_pipkmks = plot_neutral_kstar('pipkmks')
    hist_neutral_kstar_pimkpks = plot_neutral_kstar('pimkpks')
    return hist_charged_kstar_pipkmks, hist_charged_kstar_pimkpks, hist_neutral_kstar_pipkmks, hist_neutral_kstar_pimkpks


def validate_kstar_cut(channel, cut):
    if channel == 'pipkmks':
        if cut not in ct.KSTAR_CUT_DICT_PIPKMKS.keys():
            raise ValueError("Invalid cut. Valid cuts are: " + str(ct.KSTAR_CUT_DICT_PIPKMKS.keys()))
    elif channel == 'pimkpks':
        if cut not in ct.KSTAR_CUT_DICT_PIMKPKS.keys():
            raise ValueError("Invalid cut. Valid cuts are: " + str(ct.KSTAR_CUT_DICT_PIMKPKS.keys()))
    return True


def plot_kkpi(channel, cut, nbins=150, xlow=1.0, xhigh=2.5):
    validate_kstar_cut(channel, cut)
    df = get_dataframe(channel)
    df = df.Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    if channel == 'pimkpks':
        df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.PPIM_MASS_CUT).Filter(ct.KSP_MASS_CUT).Filter(ct.KSTAR_CUT_DICT_PIMKPKS[cut])
    elif channel == 'pipkmks':
        df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.PPIP_MASS_CUT).Filter(ct.KMP_MASS_CUT).Filter(ct.KSTAR_CUT_DICT_PIPKMKS[cut])
    hist_kkpi = df.Histo1D(('kkpi_m', build_kkpi_title(channel, cut), nbins, xlow, xhigh), f'{channel}_m')
    hist_kkpi.GetXaxis().SetTitle(hist_kkpi.GetTitle().split(' ')[0])
    hist_kkpi.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/nbins):.2f} MeV")
    hist_kkpi.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_kkpi.SetDirectory(0)
    return hist_kkpi.GetValue()


def plot_f1_1420(channel, kept_kstar, n_bins=150, xlow=1.0, xhigh=2.5):
    df = get_dataframe(channel)
    df = df.Filter(ct.KS_PATHLENGTH_CUT).Filter(ct.KS_MASS_CUT).Filter(ct.P_P_CUT)
    if channel == 'pimkpks':
        df = df.Filter(ct.MX2_PPIMKPKS_CUT).Filter(ct.PPIM_MASS_CUT).Filter(ct.KSP_MASS_CUT)
        if kept_kstar == 'charged':
            df = df.Filter(ct.KEEP_CHARGED_REJECT_NEUTRAL_PIMKPKS)
        elif kept_kstar == 'neutral':
            df = df.Filter(ct.KEEP_NEUTRAL_REJECT_CHARGED_PIMKPKS)
    elif channel == 'pipkmks':
        df = df.Filter(ct.MX2_PPIPKMKS_CUT).Filter(ct.PPIP_MASS_CUT).Filter(ct.KMP_MASS_CUT)
        if kept_kstar == 'charged':
            df = df.Filter(ct.KEEP_CHARGED_REJECT_NEUTRAL_PIPKMKS)
        elif kept_kstar == 'neutral':
            df = df.Filter(ct.KEEP_NEUTRAL_REJECT_CHARGED_PIPKMKS)
    hist_f1_1420 = df.Histo1D(('pipkmks_1420', build_f1_1420_title(channel, kept_kstar), n_bins, xlow, xhigh), f'{channel}_m')
    hist_f1_1420.GetXaxis().SetTitle(hist_f1_1420.GetTitle().split(' ')[0] + ' GeV')
    hist_f1_1420.GetYaxis().SetTitle(f"Counts/{1000*((xhigh-xlow)/n_bins):.2f} MeV")
    hist_f1_1420.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    hist_f1_1420.SetDirectory(0)
    return hist_f1_1420.GetValue()


if __name__ == "__main__":
    ROOT.gStyle.SetOptStat(0)
    # get_ks_before_after_cut
    #()
    # result_of_p_p_cut()
    # plot_mx2_all()
    plot_pipkmks_phasespace_with_cuts()