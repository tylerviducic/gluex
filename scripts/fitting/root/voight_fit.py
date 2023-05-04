# script for fitting f1 peaks with voigt function

import ROOT
import math
# import numpy as np
# import matplotlib.pyplot as plt

def bw(x, par):
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])

def voigt(x, par):
    return par[0] * ROOT.TMath.Voigt(x[0] - par[1], par[2], par[3])

def bkg_func(x, par):
    return ROOT.TMath.Exp(par[0] + par[1] * x[0] + par[2] * x[0] * x[0]) 

def fit_voigt(x, par):
    threshold = 1.1
    bkg = (x[0] - threshold)**par[7] * (par[8] + par[9] * x[0] + par[10] * x[0] * x[0])
    bw_1420 = par[4] * ROOT.TMath.BreitWigner(x[0], par[5], par[6])

    return par[0] * ROOT.TMath.Voigt(x[0] - par[1], par[2], par[3]) + bw_1420 + bkg

def get_fit_start(hist):
    first_pos_bin_index = hist.FindFirstBinAbove(1)
    return hist.GetXaxis().GetBinCenter(first_pos_bin_index)

def remove_zero_bins(hist):
    for i in range(1, hist.GetNbinsX() + 1):
        if hist.GetBinContent(i) < 0:
            print("Removing bin: ", i)
            hist.SetBinContent(i, 0)
            hist.SetBinError(i, 0)
    return hist


##################################
####### start fitting here #######
##################################

# filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_full.root'
filename = '/work/halld/home/viducic/selector_output/f1/pipkmks_2018_full.root'

hist_file = ROOT.TFile.Open(filename)

bin_size = (1.7 - 1)/70

param_dict_voigt = {

    7: [27.5543, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1],
    8: [100, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 0.1, 0.1, 0.1, 0.1],
    9: [55.6267, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1],
    10: [48, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1]

}

beam_energy = 8 # GeV
params_voigt = param_dict_voigt[beam_energy]

energy_values_low = ['0.100', '0.200', '0.300', '0.400']
energy_values_med = ['0.650', '0.900']
energy_values_high = ['1.400', '1.900']

bin_values = []
bin_widths = []
data_histogram_array = []
voigt_list = []
bkg_voigt_list = []
bw_1420_voigt_list = []



for energy in energy_values_low:
    bin_values.append(float(energy) - 0.05)
    bin_widths.append(0.1)

    data_hist_name = 'Binnedf1_1285_{}_beam_{}'.format(energy, beam_energy)
    # print(data_hist_name)


    uncor_data_hist = hist_file.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

for energy in energy_values_med:
    bin_values.append(float(energy) - 0.125)
    bin_widths.append(0.25)

    data_hist_name = 'Binnedf1_1285_{}_beam_{}'.format(energy, beam_energy)
    # print(data_hist_name)


    uncor_data_hist = hist_file.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

for energy in energy_values_high:
    bin_values.append(float(energy) - 0.25)
    bin_widths.append(0.5)

    data_hist_name = 'Binnedf1_1285_{}_beam_{}'.format(energy, beam_energy)
    # print(data_hist_name)


    uncor_data_hist = hist_file.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
c1.Divide(3, 3)

ROOT.gStyle.SetOptStat(0)


for i in range(len(data_histogram_array)):
    c1.cd(i + 1)

    fit_start = get_fit_start(data_histogram_array[i])
    fit_end = 1.7

    func_voigt = ROOT.TF1("voight_{}".format(i), fit_voigt, fit_start, 1.7, 11)


    func_voigt.SetParameter(0, params_voigt[0])
    func_voigt.SetParameter(1, params_voigt[1])
    func_voigt.SetParameter(2, params_voigt[2])
    func_voigt.SetParameter(3, params_voigt[3])
    func_voigt.SetParameter(4, params_voigt[4])
    func_voigt.SetParameter(5, params_voigt[5])
    func_voigt.SetParameter(6, params_voigt[6])
    func_voigt.SetParameter(7, params_voigt[7])
    func_voigt.SetParameter(8, params_voigt[8])
    func_voigt.SetParameter(9, params_voigt[9])
    func_voigt.SetParameter(10, params_voigt[10])

    data_histogram_array[i].Fit(func_voigt, "LRN")

    func_voigt.SetLineColor(4)

    for m in range(11):
        param_dict_voigt[m] = func_voigt.GetParameter(m)

    data_histogram_array[i].Draw()
    func_voigt.Draw("same")

