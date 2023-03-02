# draw yields of low-t bins 

#fit f1_1285 with relBW

import math
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

hbarc = 0.1973269631 # GeV fm   

proton = 0.93827
kaon = 0.49367
pion = 0.13957
k_short = 0.49765

def get_yield_error(dsigma, sigma, damp, amp):
    step_1 = (dsigma/sigma)**2 + (damp/amp)**2
    return math.sqrt(step_1)

def breakupMomentum(s, m1, m2):
    if(s < ((m1 + m2) ** 2)):
        return 0
    result = 0.5 * math.sqrt((s - ((m1 + m2) ** 2)) * (s - ((m1 - m2) ** 2)) / s)
    return result


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

    spin = 0

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)
    
    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    return par[0]*arg1*arg2/(arg3 + arg4)

def bw_1420(x, par):
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])

def bkg_func(x, par):
    return ROOT.TMath.Exp(par[0] + par[1] * x[0] + par[2] * x[0] * x[0]) 

def full_fit(x, par):
    q0 = breakupMomentum(par[1] * par[1], kaon, kaon)
    q = breakupMomentum(x[0] * x[0], kaon, kaon)

    spin = 1

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)

    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    bkg = ROOT.TMath.Exp(par[3] + par[4] * x[0] + par[5] * x[0] * x[0])

    # bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    # bw1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    return par[0]*arg1*arg2/(arg3 + arg4) + bkg

def get_fit_start(hist):
    first_pos_bin_index = hist.FindFirstBinAbove(1)
    return hist.GetXaxis().GetBinCenter(first_pos_bin_index)

beam_energy = 10

recon_filename = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_spring.root'
thrown_filename = f'/Users/tylerviducic/research/gluex/f1_mc/analysis/pipkmks_t_binned_thrown_0_2_{beam_energy}_spring.root'
data_filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_spring.root'
flux_filename = '/Users/tylerviducic/research/gluex/selector_output/flux_40856_42559.root'


hist_file_data = ROOT.TFile.Open(data_filename, "READ")
hist_file_recon = ROOT.TFile.Open(recon_filename, "READ")
hist_file_thrown = ROOT.TFile.Open(thrown_filename, "READ")


flux_file = ROOT.TFile.Open(flux_filename, "READ")
flux_hist = flux_file.Get("tagged_lumi")
flux = flux_hist.GetBinContent((int)(beam_energy -  6))


branching_ratio = 0.091


data_histogram_array = []
acceptance_list = []

bin_values = []

integral_values_1285 = []
error_values_1285 =[]
mean_1285 = []
gamma_1285 = [] 
rel_bw_list = []
bw_list = []

x2_per_ndf = []

background = []

param_dict = {
    7: [3.82588e+01, 1.29961, 8.50454e-02, -2.62452e+01, 3.01286e+01,  -7.69889],
    8: [3.82588e+01, 1.29961, 8.50454e-02, -2.62452e+01, 3.01286e+01,  -7.69889],
    9: [4.31990e+01, 1.28934, 6.01022e-02, -2.76107e+01, 3.17652e+01, -8.15195],
    10: [4.81463e+01, 1.27797, 4.52772e-02, -2.89764e+01, 3.34119e+01, -8.61501],
}

params = param_dict[beam_energy] #pipkmks

fit_start =  1.2
fit_end = 2.19

bin_width = []

energy_values_low = ['0.250', '0.300', '0.350', '0.400'] #'0.100', '0.150', '0.200',  
energy_values_med = ['0.500', '0.600', '0.700', '0.800', '0.900']
energy_values_high = ['1.100', '1.300']#, '1.500', '1.700', '1.900']

thrown_low =  ['0.25', '0.3', '0.35', '0.4'] # ['0.1', '0.15',
thrown_med = ['0.5', '0.6', '0.7', '0.8', '0.9']
thrown_high = ['1.1', '1.3']#,'1.5', '1.7', '1.9']

for energy in energy_values_low:
    bin_values.append(float(energy) - 0.025)
    bin_width.append(0.05)

    thrown_index = energy_values_low.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_low[thrown_index]}'
    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    # print(data_hist_name)


    data_hist = hist_file_data.Get(data_hist_name)
    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    data_hist.SetMinimum(0)
    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)
    data_histogram_array.append(data_hist)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)

for energy in energy_values_med:
    bin_values.append(float(energy) - 0.05)
    bin_width.append(0.1)

    thrown_index = energy_values_med.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_med[thrown_index]}'
    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    # print(data_hist_name)


    data_hist = hist_file_data.Get(data_hist_name)
    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    data_hist.SetMinimum(0)
    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)
    data_histogram_array.append(data_hist)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)

for energy in energy_values_high:
    bin_values.append(float(energy) - 0.1)
    bin_width.append(0.2)

    thrown_index = energy_values_high.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_high[thrown_index]}'
    data_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    # print(data_hist_name)


    data_hist = hist_file_data.Get(data_hist_name)
    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    data_hist.SetMinimum(0)
    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)
    data_histogram_array.append(data_hist)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)

c1 = ROOT.TCanvas("c1")
c1.Divide(6, 2)

print(acceptance_list)

ROOT.gStyle.SetOptStat(0)

# for y in range(len(data_histogram_array)):
#     c1.cd(y + 1)
#     data_histogram_array[y].Draw()
#     c1.Update()

for x in range(len(data_histogram_array)):
    c1.cd(x + 1)
    
    fit_start = get_fit_start(data_histogram_array[x])

    func = ROOT.TF1("func", full_fit, fit_start, fit_end, 6)
    # func.SetParameters(params[0], params[1], params[2], params[3], params[4], params[5])
    func.SetParameter(0, params[0])
    func.SetParameter(1, params[1])
    func.SetParameter(2, params[2])
    func.SetParameter(3, params[3])
    func.SetParameter(4, params[4])
    func.SetParameter(5, params[5])


    data_histogram_array[x].Fit(func, "WLRN")
    func.SetLineColor(2)

    rel_bw = ROOT.TF1("rel_bw", relBreitWigner, fit_start, fit_end, 3)
    rel_bw.SetParameters(func.GetParameter(0), func.GetParameter(1), func.GetParameter(2))
    rel_bw.SetParError(0, func.GetParError(0))
    rel_bw.SetParError(1, func.GetParError(1))
    rel_bw.SetParError(2, func.GetParError(2))
    rel_bw.SetLineColor(3)
    rel_bw_list.append(rel_bw)

    # bw = ROOT.TF1("bw", bw_1420, fit_start, fit_end, 3)
    # bw.SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    # bw.SetParError(0, func.GetParError(3))
    # bw.SetParError(1, func.GetParError(4))
    # bw.SetParError(2, func.GetParError(5))
    # bw.SetLineColor(1)
    # bw_list.append(bw)

    background.append(ROOT.TF1("background_1285", bkg_func, fit_start, fit_end, 3))
    background[x].SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    background[x].SetLineColor(4)

    integral_1285 = rel_bw.Integral(fit_start, fit_end)/bin_width[x]
    print(f"yield = {integral_1285} +/- {np.sqrt(integral_1285)}")
    dsig_1285, sig_1285 = func.GetParError(2), func.GetParameter(2)
    damp_1285, amp_1285 =func.GetParError(0), func.GetParameter(0)
    error_values_1285.append(math.sqrt(integral_1285)/ integral_1285)

    integral_values_1285.append(integral_1285 / acceptance_list[x])
    # integral_values_1285.append(integral_1285)
    # error_values_1285.append(integral_1285 * get_yield_error(dsig_1285, sig_1285, damp_1285, amp_1285))
    mean_1285.append(func.GetParameter(1))


    x2_per_ndf.append(func.GetChisquare()/func.GetNDF())


    for n in range(6):
        params[n] = func.GetParameter(n)

    # func.SetRange(1, 2.25)
    # func_1420.SetRange(1.25, 2.25)

    data_histogram_array[x].Draw()
    func.Draw("same")
    rel_bw_list[x].Draw("same")
    # # bw_list[x].Draw("same")
    # # # gaus_1285[x].Draw("same")
    background[x].Draw("same")

theory_filename = f'/Users/tylerviducic/research/gluex/theory_predictions/t-slope-{beam_energy}GeVnew.dat'

theory_df = pd.read_csv(theory_filename, delim_whitespace=True)

theory_df.columns = ['minus_t', 'diff_cs']
theory_df = theory_df[theory_df['minus_t'] > 0.29]
theory_df['diff_cs'] = theory_df['diff_cs'] * 1000

bin_corrected_yield = [i/j for i, j in zip(integral_values_1285, bin_width)]
# bin_corrected_error = [i/j for i, j in zip(error_values_1285, bin_width)]

print(error_values_1285)

diff_cs = [entry / (flux * branching_ratio / 6) for entry in bin_corrected_yield]
diff_cs_error = [error * cs for error, cs in zip(error_values_1285, diff_cs)]
# print(normalized_yield)

# for entry, error in zip(diff_cs, error_values_1285):
#     print(f"yield = {entry} +/- {error}")

for t_point, cs_point in zip(bin_values, diff_cs):
    print(f"t = {t_point} -- cs = {cs_point} +/- {diff_cs_error[bin_values.index(t_point)]}\n Flux = {flux}, efficiency = {acceptance_list[bin_values.index(t_point)]}\n yield = ")


fig = plt.figure()
ax1 = fig.add_subplot(111) 
ax1.errorbar(bin_values, diff_cs, yerr=diff_cs_error, xerr=[x/2 for x in bin_width], fmt='o', ls='none', color='green')
# ax1.errorbar(bin_values, integral_values_1420, yerr=error_values_1420,fmt='o', ls='none', color='black')
#ax1.errorbar(bin_values, integral_values_1285, fmt='o', ls='none', color='red')
ax1.scatter(theory_df['minus_t'], theory_df['diff_cs'], marker='o' ,color='blue', s=3)
ax1.set_ylabel("differential cross section")
ax1.set_xlabel("-t (GeV)^2")
# ax1.set_title("N(f1(1285)) vs W (GeV)")
ax1.set_title("differential cross-section vs -t (GeV^2)")
ax1.set_yscale('log')
ax1.set_xlim([0.25, 0.8])


fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(bin_values, x2_per_ndf, color='red')
ax2.set_ylabel("X2/NDF")
ax2.set_xlabel("-t (GeV)^2")
ax2.set_title("X2/NDF vs -t")

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter(bin_values, mean_1285, color='blue')
ax3.set_ylabel("fit mean")
ax3.set_xlabel("-t (GeV)^2")
ax3.set_title("Breit-Wigner mean vs -t")

# fig4 = plt.figure()
# ax4 = fig4.add_subplot(111)
# ax4.scatter(bin_values, acceptance_list, color='black')
# ax4.set_ylabel("acceptance")
# ax4.set_xlabel("-t (GeV)^2")
# ax4.set_title("acceptance vs -t")
# ax4.set_xlim([0, 1.7])
# ax4.set_ylim([0, 0.01])

# fig4 = plt.figure()
# ax4 = fig4.add_subplot(111) 
# ax4.errorbar(bin_values, integral_values_1420, yerr=error_values_1420,fmt='o', ls='none', color='black')
# #ax1.errorbar(bin_values, integral_values_1285, fmt='o', ls='none', color='red')
# ax4.set_ylabel("Count")
# ax4.set_xlabel("-t (GeV)^2")
# # ax1.set_title("N(f1(1285)) vs W (GeV)")
# ax4.set_title("N(f1(1420)) vs -t (GeV)")

plt.show()

c1.Update()
input("Press any key to exit")
c1.Close()
plt.close()