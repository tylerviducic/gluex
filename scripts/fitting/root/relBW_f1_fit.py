#fit f1_1285 with relBW

import math
import ROOT
import matplotlib.pyplot as plt
import numpy as np

hbarc = 0.1973269631 # GeV fm   

proton = 0.93827
kaon = 0.49367
pion = 0.13957
k_short = 0.49765

def get_yield_error(dsigma, sigma, damp, amp):
    step_1 = (dsigma/sigma)**2 +(damp/amp)**2
    return math.sqrt(step_1)

def breakupMomentum(s, m1, m2):
    if(s < ((m1 + m2) ** 2)):
        return 0
    result = 0.5 * math.sqrt((s - ((m1 + m2) ** 2)) * (s - ((m1 - m2) ** 2)) / s)
    return result

# double
# blattWeisskopf(int L, double p)
# {
#   double z = pow(p / hbarc, 2);  // 1fm interaction radius, VES uses 5.2 GeV^-1                                                                                                                                                              
#   double result;
#   switch (L) {
#   case 0:
#     result = 1; break;
#   case 1:
#     result = sqrt(2*z/(z+1)); break;
#   case 2:
#     result = sqrt(13*z*z/(pow(z-3, 2) + 9*z)); break;
#   case 3:
#     result = sqrt(277*z*z*z/(z*pow(z-15, 2) + 9*pow(2*z-5, 2))); break;
#   case 4:
#     result = sqrt(12746*pow(z,4)/(pow(z*z-45*z+105,2) + 25*z*pow(2*z-21,2))); break;
#   default:
#     result = 0; break;
#   }
#   return result;
# }

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

    spin = 2

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)
    
    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    # bkg = par[3] + par[4] * x[0] + par[5] * x[0] * x[0] 
    bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    bw1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    return par[0]*arg1*arg2/(arg3 + arg4) + bw1420 + bkg

def get_fit_start(hist):
    first_pos_bin_index = hist.FindFirstBinAbove(1)
    return hist.GetXaxis().GetBinCenter(first_pos_bin_index)


file_name1 = "/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_full.root"
file_name2 = "/Users/tylerviducic/research/gluex/selector_output/pimkpks_2018_full.root"

hist_file1 = ROOT.TFile.Open(file_name1, "READ")
hist_file2 = ROOT.TFile.Open(file_name2, "READ")

histogram_array = []

bin_values = []

integral_values_1285 = []
error_values_1285 =[]
mean_1285 = []
gamma_1285 = [] 
integral_values_1420 = []
error_values_1420 =[]
mean_1420 = []
gamma_1420 = []
rel_bw_list = []
bw_list = []

x2_per_ndf = []

background = []

# params = [500, 1.29, 0.04, 1542, -2.49601e+03, 1000]
params = [500, 1.285, 0.2, 700, 1.420, 0.055, -2.82823e+01, 3.72572e+01, -9.93123e+00] #pipkmks
#params = [300, 1.285, 0.2, 800, 1.420, 0.055, -7.53603e+01, 9.48413e+01, -2.73167e+01] #pimkpks

fit_start =  1.12
fit_end = 1.7

bin_width = 1.25 / 150

for i in range(200, 2200, 200):
    bin_values.append(float(i)/1000 - 0.1)
    histo_name = f'Binnedf1_{i/1000:.3f}_fullbeam_tprime'
    print(histo_name)


    hist_1 = hist_file1.Get(histo_name)
    hist_2 = hist_file2.Get(histo_name)

    hist_1.Add(hist_2)
    hist_1.SetMinimum(0)
    histogram_array.append(hist_1)

# c1 = ROOT.TCanvas("c1")
# c1.Divide(5, 2, 0.005, 0.005)

for x in range(len(histogram_array)):
    #c1.cd(x + 1)
    
    fit_start = get_fit_start(histogram_array[x])

    func = ROOT.TF1("func", full_fit, fit_start, fit_end, 9)
    # func.SetParameters(params[0], params[1], params[2], params[3], params[4], params[5])
    func.SetParameter(0, params[0])
    func.SetParameter(1, params[1])
    func.SetParameter(2, params[2])
    func.SetParameter(3, params[3])
    func.SetParameter(4, params[4])
    func.SetParameter(5, params[5])
    func.SetParameter(6, params[6])
    func.SetParameter(7, params[7])
    func.SetParameter(8, params[8])

    histogram_array[x].Fit(func, "R")
    func.SetLineColor(2)
    
    rel_bw = ROOT.TF1("rel_bw", relBreitWigner, fit_start, fit_end, 3)
    rel_bw.SetParameters(func.GetParameter(0), func.GetParameter(1), func.GetParameter(2))
    rel_bw.SetParError(0, func.GetParError(0))
    rel_bw.SetParError(1, func.GetParError(1))
    rel_bw.SetParError(2, func.GetParError(2))
    rel_bw.SetLineColor(3)
    rel_bw_list.append(rel_bw)

    bw = ROOT.TF1("bw", bw_1420, fit_start, fit_end, 3)
    bw.SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    bw.SetParError(0, func.GetParError(3))
    bw.SetParError(1, func.GetParError(4))
    bw.SetParError(2, func.GetParError(5))
    bw.SetLineColor(1)
    bw_list.append(bw)

    background.append(ROOT.TF1("background_1285", bkg_func, 1, fit_end, 3))
    background[x].SetParameters(func.GetParameter(6), func.GetParameter(7), func.GetParameter(8))
    background[x].SetLineColor(4)

    integral_1285 = rel_bw.Integral(fit_start, fit_end)/bin_width
    integral_1420 = bw.Integral(fit_start, fit_end)/bin_width
    #integral_1285 = bw.GetParameter(0)/bin_width
    dsig_1285, sig_1285 = func.GetParError(2), func.GetParameter(2)
    damp_1285, amp_1285 =func.GetParError(0), func.GetParameter(0)
    dsig_1420, sig_1420 = func.GetParError(5), func.GetParameter(5)
    damp_1420, amp_1420 =func.GetParError(3), func.GetParameter(3)
    integral_values_1285.append(integral_1285)
    integral_values_1420.append(integral_1420)
    error_values_1285.append(integral_1285 * get_yield_error(dsig_1285, sig_1285, damp_1285, amp_1285))
    error_values_1420.append(integral_1420 * get_yield_error(dsig_1420, sig_1420, damp_1420, amp_1420))
    mean_1285.append(func.GetParameter(1))
    mean_1420.append(func.GetParameter(4))


    x2_per_ndf.append(func.GetChisquare()/func.GetNDF())

    for n in range(9):
        params[n] = func.GetParameter(n)
        # params_1420[n] = func_1420.GetParameter(n)

    # func.SetRange(1, 2.25)
    # func_1420.SetRange(1.25, 2.25)

    # histogram_array[x].Draw()
    # func.Draw("same")
    # rel_bw_list[x].Draw("same")
    # bw_list[x].Draw("same")
    # # gaus_1285[x].Draw("same")
    # background[x].Draw("same")

fig = plt.figure()
ax1 = fig.add_subplot(111) 
ax1.errorbar(bin_values, integral_values_1285, yerr=error_values_1285,fmt='o', ls='none', color='green')
ax1.errorbar(bin_values, integral_values_1420, yerr=error_values_1420,fmt='o', ls='none', color='black')
#ax1.errorbar(bin_values, integral_values_1285, fmt='o', ls='none', color='red')
ax1.set_ylabel("Count")
ax1.set_xlabel("-t' (GeV)^2")
# ax1.set_title("N(f1(1285)) vs W (GeV)")
ax1.set_title("Yield vs -t' (GeV^2)")

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(bin_values, x2_per_ndf, color='red')
ax2.set_ylabel("X2/NDF")
ax2.set_xlabel("-t (GeV)^2")
ax2.set_title("X2/NDF vs -t")

# fig3 = plt.figure()
# ax3 = fig3.add_subplot(111)
# ax3.scatter(bin_values, mean_1285, color='blue')
# ax3.set_ylabel("fit mean")
# ax3.set_xlabel("-t (GeV)^2")
# ax3.set_title("Breit-Wigner mean vs -t")

# fig4 = plt.figure()
# ax4 = fig4.add_subplot(111) 
# ax4.errorbar(bin_values, integral_values_1420, yerr=error_values_1420,fmt='o', ls='none', color='black')
# #ax1.errorbar(bin_values, integral_values_1285, fmt='o', ls='none', color='red')
# ax4.set_ylabel("Count")
# ax4.set_xlabel("-t (GeV)^2")
# # ax1.set_title("N(f1(1285)) vs W (GeV)")
# ax4.set_title("N(f1(1420)) vs -t (GeV)")

plt.show()

# c1.Update()
input("Press any key to exit")
# c1.Close()
