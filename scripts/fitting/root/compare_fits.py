# script to compare different fit methods for the f1(1285) meson

import ROOT
import math
import numpy as np
import matplotlib.pyplot as plt


hbarc = 0.1973269631 # GeV fm   

proton = 0.93827
kaon = 0.49367
pion = 0.13957
k_short = 0.49765

def breakupMomentum(s, m1, m2):
    if(s < ((m1 + m2) ** 2)):
        return 0
    result = 0.5 * math.sqrt((s - ((m1 + m2) ** 2)) * (s - ((m1 - m2) ** 2)) / s)
    return result

def bw(x, par):
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])

def blattWeisskopf(L, p):
    z = (p/hbarc) ** 2 
    if L == 0:
        return 1
    elif L == 1:
        return math.sqrt(2 * z / (z + 1))
    elif L == 2:
        return math.sqrt(13*z*z/((z-3)**2 + 9*z))
    return 0

def relBreitWigner(x, par):
    intermediate_particle = kaon + pion
    q0 = breakupMomentum(par[1] * par[1], intermediate_particle, k_short)
    q = breakupMomentum(x[0] * x[0], intermediate_particle, k_short)

    spin = 1

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)
    
    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    return par[0]*arg1*arg2/(arg3 + arg4)

def voigt(x, par):
    return par[0] * ROOT.TMath.Voigt(x[0] - par[1], par[2], par[3])

def bkg_func(x, par):
    return ROOT.TMath.Exp(par[0] + par[1] * x[0] + par[2] * x[0] * x[0]) 

def fit_relbw(x, par):
    q0 = breakupMomentum(par[1] * par[1], kaon, kaon)
    q = breakupMomentum(x[0] * x[0], kaon, kaon)

    spin = 1

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)

    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    bw_1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])

    return par[0]*arg1*arg2/(arg3 + arg4) + bw_1420 + bkg

def fit_voigt(x, par, threshold):
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

filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_full.root'

hist_file = ROOT.TFile.Open(filename)

bin_size = (1.7 - 1)/70

param_dict_relbw = {

    7: [27.5543, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
    8: [62.5121, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
    9: [55.6267, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
    10: [48, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1]

}

param_dict_voigt = {

    7: [27.5543, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1],
    8: [62.5121, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1],
    9: [55.6267, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1],
    10: [48, 1.285, 0.0227, 0.007, 100, 1.420, 0.0545, 1, 1, 1, 1]

}

beam_energy = 9 # GeV
params_relbw = param_dict_relbw[beam_energy]
params_voigt = param_dict_voigt[beam_energy]

energy_values_low = ['0.100', '0.200', '0.300', '0.400']
energy_values_med = ['0.650', '0.900']
energy_values_high = ['1.400', '1.900']

bin_values = []
bin_widths = []
data_histogram_array = []
rel_bw_list = []
bkg_rbw_list = []
bw_1420_rbw_list = []
voigt_list = []
bkg_voigt_list = []
bw_1420_voigt_list = []

for energy in energy_values_low:
    bin_values.append(float(energy) - 0.05)
    bin_widths.append(0.1)

    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    # print(data_hist_name)


    uncor_data_hist = hist_file.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

for energy in energy_values_med:
    bin_values.append(float(energy) - 0.125)
    bin_widths.append(0.25)

    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    # print(data_hist_name)


    uncor_data_hist = hist_file.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

for energy in energy_values_high:
    bin_values.append(float(energy) - 0.25)
    bin_widths.append(0.5)

    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
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
    
    func_relbw = ROOT.TF1(f"relbw_{i}", fit_relbw, fit_start, 1.7, 9)
    func_voigt = ROOT.TF1(f"voight_{i}", fit_voigt, fit_start, 1.7, 11)

    func_relbw.SetParameter(0, params_relbw[0])
    func_relbw.SetParameter(1, params_relbw[1])
    func_relbw.FixParameter(2, params_relbw[2])
    func_relbw.SetParameter(3, params_relbw[3])
    func_relbw.SetParameter(4, params_relbw[4])
    func_relbw.FixParameter(5, params_relbw[5])
    func_relbw.SetParameter(6, params_relbw[6])
    func_relbw.SetParameter(7, params_relbw[7])
    func_relbw.SetParameter(8, params_relbw[8])

    func_voigt.SetParameter(0, params_voigt[0])
    func_voigt.SetParameter(1, params_voigt[1])
    func_voigt.FixParameter(2, params_voigt[2])
    func_voigt.SetParameter(3, params_voigt[3])
    func_voigt.SetParameter(4, params_voigt[4])
    func_voigt.FixParameter(5, params_voigt[5])
    func_voigt.SetParameter(6, params_voigt[6])
    func_voigt.SetParameter(7, params_voigt[7])
    func_voigt.SetParameter(8, params_voigt[8])
    func_voigt.SetParameter(9, params_voigt[9])
    func_voigt.SetParameter(10, params_voigt[10])

    data_histogram_array[i].Fit(func_relbw, "LRN+")
    data_histogram_array[i].Fit(func_voigt, "LRN+")

    func_relbw.SetLineColor(2)
    func_voigt.SetLineColor(4)

    rel_bw = ROOT.TF1("rel_bw", relBreitWigner, fit_start, fit_end, 3)
    rel_bw.SetParameters(func_relbw.GetParameter(0), func_relbw.GetParameter(1), func_relbw.GetParameter(2))
    rel_bw.SetParError(0, func_relbw.GetParError(0))
    rel_bw.SetParError(1, func_relbw.GetParError(1))
    rel_bw.SetParError(2, func_relbw.GetParError(2))
    rel_bw.SetLineColor(3)
    rel_bw_list.append(rel_bw)

    voigt = ROOT.TF1("voigt", voigt, fit_start, fit_end, 4)
    voigt.SetParameters(func_voigt.GetParameter(0), func_voigt.GetParameter(1), func_voigt.GetParameter(2), func_voigt.GetParameter(3))
    voigt.SetParError(0, func_voigt.GetParError(0))
    voigt.SetParError(1, func_voigt.GetParError(1))
    voigt.SetParError(2, func_voigt.GetParError(2))
    voigt.SetParError(3, func_voigt.GetParError(3))
    voigt.SetLineColor(3)
    voigt_list.append(voigt)

    bw_1420_rbw = ROOT.TF1("bw_1420", bw, fit_start, fit_end, 3)
    bw_1420_rbw.SetParameters(func_relbw.GetParameter(3), func_relbw.GetParameter(4), func_relbw.GetParameter(5))
    bw_1420_rbw.SetParError(0, func_relbw.GetParError(3))
    bw_1420_rbw.SetParError(1, func_relbw.GetParError(4))
    bw_1420_rbw.SetParError(2, func_relbw.GetParError(5))
    bw_1420_rbw.SetLineColor(1)
    bw_1420_rbw_list.append(bw_1420_rbw)

    bkg_rbw_list.append(ROOT.TF1("background_1285", bkg_func, fit_start, fit_end, 3))
    bkg_rbw_list[i].SetParameters(func_relbw.GetParameter(6), func_relbw.GetParameter(7), func_relbw.GetParameter(8))
    bkg_rbw_list[i].SetLineColor(4)

    bw_1420_voigt = ROOT.TF1("bw_1420", bw, fit_start, fit_end, 3)
    bw_1420_voigt.SetParameters(func_voigt.GetParameter(4), func_voigt.GetParameter(5), func_voigt.GetParameter(6))
    bw_1420_voigt.SetParError(0, func_voigt.GetParError(4))
    bw_1420_voigt.SetParError(1, func_voigt.GetParError(5))
    bw_1420_voigt.SetParError(2, func_voigt.GetParError(6))
    bw_1420_voigt.SetLineColor(1)
    bw_1420_voigt_list.append(bw_1420_voigt)

    bkg_voigt_list.append(ROOT.TF1("background_1285", bkg_func, fit_start, fit_end, 4))
    bkg_voigt_list[i].SetParameters(func_voigt.GetParameter(7), func_voigt.GetParameter(8), func_voigt.GetParameter(9), func_voigt.GetParameter(10))
    bkg_voigt_list[i].SetLineColor(4)

    integral_relbw = rel_bw.Integral(fit_start, fit_end)/bin_size
    integral_1420_rbw = bw_1420_rbw.Integral(fit_start, fit_end)/bin_size
    integral_bkg_rbw = bkg_rbw_list[i].Integral(fit_start, fit_end)/bin_size
    integral_voigt = voigt.Integral(fit_start, fit_end)/bin_size
    integral_1420_voigt = bw_1420_voigt.Integral(fit_start, fit_end)/bin_size
    integral_bkg_voigt = bkg_voigt_list[i].Integral(fit_start, fit_end)/bin_size


    for n in range(9):
        param_dict_relbw[n] = func_relbw.GetParameter(n)

    for m in range(11):
        param_dict_voigt[m] = func_voigt.GetParameter(m)


    data_histogram_array[i].Draw()
    func_relbw.Draw("same")
    func_voigt.Draw("same")