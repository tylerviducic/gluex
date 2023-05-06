# compare slope of data to prediction

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
    step_1 = (dsigma/sigma)**2 +(damp/amp)**2
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

    spin = 2

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)

    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    bkg = ROOT.TMath.Exp(par[3] + par[4] * x[0] + par[5] * x[0] * x[0])

    return par[0]*arg1*arg2/(arg3 + arg4) + bkg

def get_fit_start(hist):
    first_pos_bin_index = hist.FindFirstBinAbove(1)
    return hist.GetXaxis().GetBinCenter(first_pos_bin_index)


recon_filename = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_spring.root'
thrown_filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_t_binned_thrown_0_2_b10_spring.root'
data_filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_spring.root'


hist_file_data = ROOT.TFile.Open(data_filename, "READ")
hist_file_recon = ROOT.TFile.Open(recon_filename, "READ")
hist_file_thrown = ROOT.TFile.Open(thrown_filename, "READ")


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

# params = [500, 1.29, 0.04, 1542, -2.49601e+03, 1000]
params = [500, 1.285, 0.2, -7.53603e+01, 9.48413e+01, -2.73167e+01] #pipkmks
# params = [300, 1.285, 0.2, 800, 1.420, 0.055, -7.53603e+01, 9.48413e+01, -2.73167e+01] #pimkpks

fit_start =  1.2
fit_end = 1.9

bin_width = 1.25 / 150

for i in range(2, 16, 2):
    bin_values.append((i - 1)/10)
    
    recon_hist_name = f'Binnedf1_1285_{i/10:.3f}_beam_10'
    thrown_hist_name = f'f1_t_{i/10:.1f}'
    data_hist_name = f'Binnedf1_1285_{i/10:.3f}_beam_10'


    data_hist = hist_file_data.Get(data_hist_name)
    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    data_hist.SetMinimum(0)
    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)
    data_histogram_array.append(data_hist)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    acceptance_list.append(acceptance)

# c1 = ROOT.TCanvas("c1")
# c1.Divide(4,2)
norm_factor = 13.282347
for x in range(len(data_histogram_array)):
    # c1.cd(x+1)
    
    fit_start = get_fit_start(data_histogram_array[x])

    func = ROOT.TF1("func", full_fit, fit_start, fit_end, 6)
    func.SetParameter(0, params[0])
    func.SetParameter(1, params[1])
    func.SetParameter(2, params[2])
    func.SetParameter(3, params[3])
    func.SetParameter(4, params[4])
    func.SetParameter(5, params[5])

    data_histogram_array[x].Fit(func, "N R")
    func.SetLineColor(2)
    
    rel_bw = ROOT.TF1("rel_bw", relBreitWigner, fit_start, fit_end, 3)
    rel_bw.SetParameters(func.GetParameter(0), func.GetParameter(1), func.GetParameter(2))
    rel_bw.SetParError(0, func.GetParError(0))
    rel_bw.SetParError(1, func.GetParError(1))
    rel_bw.SetParError(2, func.GetParError(2))
    rel_bw.SetLineColor(3)
    rel_bw_list.append(rel_bw)

    background.append(ROOT.TF1("background_1285", bkg_func, 1, fit_end, 3))
    background[x].SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    background[x].SetLineColor(4)

    integral_1285 = rel_bw.Integral(fit_start, fit_end)/bin_width
    dsig_1285, sig_1285 = func.GetParError(2), func.GetParameter(2)
    damp_1285, amp_1285 =func.GetParError(0), func.GetParameter(0)
    integral_values_1285.append(integral_1285 / acceptance_list[x])
    # integral_values_1285.append(integral_1285)
    # error_values_1285.append(get_yield_error(dsig_1285, sig_1285, damp_1285, amp_1285))
    error_values_1285.append(integral_values_1285[x] * np.sqrt(integral_1285)/ integral_1285)
    # error_values_1285.append(np.sqrt(integral_values_1285[x]))
    mean_1285.append(func.GetParameter(1))

    x2_per_ndf.append(func.GetChisquare()/func.GetNDF())

    for n in range(6):
        params[n] = func.GetParameter(n)

    # data_histogram_array[x].Draw()
    # func.Draw("same")
    # rel_bw_list[x].Draw("same")
    # background[x].Draw("same")

# filename7 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-7GeVnew.dat'
# filename8 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-8GeVnew.dat'
# filename9 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-9GeVnew.dat'
filename10 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-10GeVnew.dat'
# filename11 = '/Users/tylerviducic/research/gluex/theory_predictions/t-slope-11GeVnew.dat'

# df7 = pd.read_csv(filename7, delim_whitespace=True)
# df8 = pd.read_csv(filename8, delim_whitespace=True)
# df9 = pd.read_csv(filename9, delim_whitespace=True)
df10 = pd.read_csv(filename10, delim_whitespace=True)
# df11 = pd.read_csv(filename11, delim_whitespace=True)
# df7.columns = ['minus_t', 'diff_cs']
# df8.columns = ['minus_t', 'diff_cs']
# df9.columns = ['minus_t', 'diff_cs']
df10.columns = ['minus_t', 'diff_cs']
# df11.columns = ['minus_t', 'diff_cs']
normalized_yield = [entry / norm_factor for entry in integral_values_1285]
# print(normalized_yield)

for entry, error in zip(integral_values_1285, error_values_1285):
    print(f"yield = {entry} +/- {error}")
print(integral_values_1285[2] / df10[df10["minus_t"] == 0.5]["diff_cs"])
fig = plt.figure()
ax1 = fig.add_subplot(111) 
ax1.errorbar(bin_values, integral_values_1285, yerr=error_values_1285, xerr=0.1,fmt='o', ls='none', color='black')
ax1.set_ylabel("Acceptance Corrected Yield")
ax1.set_xlabel("-t (GeV)^2")
ax1.set_title("Acceptance Corrected Yield (normalized to theory) vs -t (GeV^2)")

# ax2 = ax1.twinx()
# ax2.scatter(df9['minus_t'], df9['diff_cs'] * norm_factor,marker = 'P', color='blue', s=3)
# for t1 in ax2.get_yticklabels():
#     t1.set_color('blue')
ax1.scatter(df10['minus_t'], df10['diff_cs'] * norm_factor, marker='o' ,color='blue', s=3)
# ax1.scatter(df8['minus_t'], df8['diff_cs'], marker='o' ,color='black', s=3)
# ax1.scatter(df9['minus_t'], df9['diff_cs'],marker = 'P', color='red', s=3)
# ax1.scatter(df10['minus_t'], df10['diff_cs'],marker = 's', color='blue', s=3)
# ax1.scatter(df11['minus_t'], df11['diff_cs'],marker = '*', color='purple', s=3)
# ax2.plot(df8['minus_t'], df8['diff_cs'], color='black')
plt.xlim([0, 1.7])
ax1.set_yscale('log')
# ax2.set_yscale('log')


plt.show()
# c1.Update()
# input("Press any key to exit")
plt.close() 