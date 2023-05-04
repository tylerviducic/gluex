# fit flat trees

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


def full_fit_double(x, par):
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
    # bkg = par[6] + par[7] * x[0] + par[8] * x[0] * x[0]


    # bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    # bw1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    #print(x[0])
    return par[0]*arg1*arg2/(arg3 + arg4) + bw_1420 + bkg

def full_fit_single(x, par):
    q0 = breakupMomentum(par[1] * par[1], kaon, kaon)
    q = breakupMomentum(x[0] * x[0], kaon, kaon)

    spin = 1

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)

    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    bkg = ROOT.TMath.Exp(par[3] + par[4] * x[0] + par[5] * x[0] * x[0])
    # bkg = par[6] + par[7] * x[0] + par[8] * x[0] * x[0]


    # bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    # bw1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    #print(x[0])
    return par[0]*arg1*arg2/(arg3 + arg4) + bkg

def get_fit_start(hist):
    first_pos_bin_index = hist.FindFirstBinAbove(1)
    return hist.GetXaxis().GetBinCenter(first_pos_bin_index)\

def get_flux_and_weights(fall_file, spring_file, beam_energy):
    flux_file_fall = ROOT.TFile.Open(fall_file, "READ")
    flux_hist_fall = flux_file_fall.Get("tagged_lumi")
    flux_fall = flux_hist_fall.GetBinContent((int)(beam_energy -  6))
    flux_file_spring = ROOT.TFile.Open(spring_file, "READ")
    flux_hist_spring = flux_file_spring.Get("tagged_lumi")
    flux_spring = flux_hist_spring.GetBinContent((int)(beam_energy -  6))

    flux = flux_fall + flux_spring
    weight_fall = flux_fall / flux
    weight_spring = flux_spring / flux

    return(flux, weight_fall, weight_spring)  

def remove_zero_bins(hist):
    for i in range(1, hist.GetNbinsX() + 1):
        if hist.GetBinContent(i) < 0:
            print("Removing bin: ", i)
            hist.SetBinContent(i, 0)
            hist.SetBinError(i, 0)
    return hist

def bkg_func(x, par):
    return ROOT.TMath.Exp(par[0] + par[1] * x[0] + par[2] * x[0] * x[0]) 

beam_energy = 9
topology = 'pipkmks'

recon_filename_fall = f'/Users/tylerviducic/research/gluex/selector_output/mc_{topology}_flat_result_2018_fall.root'
recon_filename_spring = f'/Users/tylerviducic/research/gluex/selector_output/mc_{topology}_flat_result_2018_spring.root'
thrown_filename_fall = f'/Users/tylerviducic/research/gluex/selector_output/{topology}_t_binned_thrown_0_2_{beam_energy}_fall.root'
thrown_filename_spring = f'/Users/tylerviducic/research/gluex/selector_output/{topology}_t_binned_thrown_0_2_{beam_energy}_spring.root'
data_filename = f'/Users/tylerviducic/research/gluex/selector_output/{topology}_flat_result_2018_full.root'
flux_filename_fall = '/Users/tylerviducic/research/gluex/selector_output/flux_50685_51768.root'
flux_filename_spring = '/Users/tylerviducic/research/gluex/selector_output/flux_40856_42559.root'

hist_file_data = ROOT.TFile.Open(data_filename, "READ")
hist_file_recon_fall = ROOT.TFile.Open(recon_filename_fall, "READ")
hist_file_recon_spring = ROOT.TFile.Open(recon_filename_spring, "READ")
hist_file_thrown_fall = ROOT.TFile.Open(thrown_filename_fall, "READ")
hist_file_thrown_spring = ROOT.TFile.Open(thrown_filename_spring, "READ")

branching_ratio = 0.091
bin_size = (1.7 - 1)/50 #* 2

data_histogram_array = []
acceptance_list = []
acceptance_list_fall = []
acceptance_list_spring = []

bin_values = []

integral_values_1285 = []
raw_yield = []
raw_yield_1420 = []
raw_yield_bkg = []
error_values_1285 =[]
mean_1285 = []
gamma_1285 = [] 
rel_bw_list = []
bw_list = []

x2_per_ndf = []

background = []

cs_df = pd.DataFrame()

param_dict = {

    7: [27.5543, 1.285, 0.0227, 0.1, 0.1, 0.1],
    8: [62.5121, 1.285, 0.0227, 1, 1, 1],
    9: [55.6267, 1.285, 0.0227, 0.1, 0.1, 0.1],
    10: [48, 1.285, 0.0227, 1, 1, 1],
}
# param_dict = {

#     7: [27.5543, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
#     8: [62.5121, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
#     9: [55.6267, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
#     10: [48, 1.285, 0.0227, 100, 1.420, 0.0545, 1, 1, 1],
# }

params = param_dict[beam_energy] #pipkmks

fit_start = 1.1
fit_end = 1.7


bin_width = []


energy_values_low = ['0.1', '0.2', '0.3', '0.4'] #'0.100', '0.150', '0.200',  
energy_values_med = ['0.65', '0.9']
energy_values_high = ['1.4', '1.9']#, '1.700', '1.900']

thrown_low =  ['0.1', '0.2', '0.3', '0.4'] # ['0.1', '0.15',
thrown_med = ['0.65', '0.9']
thrown_high = ['1.4', '1.9']#, '1.7', '1.9']

for energy in energy_values_low:
    bin_values.append(float(energy) - 0.05)
    bin_width.append(0.1)

    thrown_index = energy_values_low.index(energy)
    
    # recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    recon_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'
    thrown_hist_name = f'f1_t_{thrown_low[thrown_index]}'
    data_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'


    uncor_data_hist = hist_file_data.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)
    recon_hist_fall = hist_file_recon_fall.Get(recon_hist_name)
    thrown_hist_fall = hist_file_thrown_fall.Get(thrown_hist_name)
    recon_hist_spring = hist_file_recon_spring.Get(recon_hist_name)
    thrown_hist_spring = hist_file_thrown_spring.Get(thrown_hist_name)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)
    recon_hist_spring.SetMinimum(0)
    thrown_hist_spring.SetMinimum(0)
    recon_hist_fall.SetMinimum(0)
    thrown_hist_fall.SetMinimum(0)

    
    data_histogram_array.append(data_hist)

    acceptance_fall = recon_hist_fall.GetEntries() / thrown_hist_fall.GetEntries()
    acceptance_spring = recon_hist_spring.GetEntries() / thrown_hist_spring.GetEntries()

    flux, weight_fall, weight_spring = get_flux_and_weights(flux_filename_fall, flux_filename_spring, beam_energy)
    acceptance = weight_fall * acceptance_fall + weight_spring * acceptance_spring
    
    if(acceptance > 0):
        acceptance_list.append(acceptance)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)
    else:
        acceptance_list.append(1.0)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)

for energy in energy_values_med:
    bin_values.append(float(energy) - 0.125)
    bin_width.append(0.25)

    thrown_index = energy_values_med.index(energy)
    
    recon_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'
    thrown_hist_name = f'f1_t_{thrown_med[thrown_index]}'
    data_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'
    # print(data_hist_name)


    uncor_data_hist = hist_file_data.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)
    recon_hist_fall = hist_file_recon_fall.Get(recon_hist_name)
    thrown_hist_fall = hist_file_thrown_fall.Get(thrown_hist_name)
    recon_hist_spring = hist_file_recon_spring.Get(recon_hist_name)
    thrown_hist_spring = hist_file_thrown_spring.Get(thrown_hist_name)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)
    recon_hist_fall.SetMinimum(0)
    thrown_hist_fall.SetMinimum(0)
    recon_hist_spring.SetMinimum(0)
    thrown_hist_spring.SetMinimum(0)


    data_histogram_array.append(data_hist)

    acceptance_fall = recon_hist_fall.GetEntries() / thrown_hist_fall.GetEntries()
    acceptance_spring = recon_hist_spring.GetEntries() / thrown_hist_spring.GetEntries()

    flux, weight_fall, weight_spring = get_flux_and_weights(flux_filename_fall, flux_filename_spring, beam_energy)
    acceptance = weight_fall * acceptance_fall + weight_spring * acceptance_spring

    if(acceptance > 0):
        acceptance_list.append(acceptance)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)
    else:
        acceptance_list.append(1.0)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)

for energy in energy_values_high:
    bin_values.append(float(energy) - 0.25)
    bin_width.append(0.5)

    thrown_index = energy_values_high.index(energy)
    
    recon_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'
    thrown_hist_name = f'f1_t_{thrown_high[thrown_index]}'
    data_hist_name = f'{topology}_beam_{beam_energy}_t_{energy}'
    # print(data_hist_name)

    uncor_data_hist = hist_file_data.Get(data_hist_name)
    data_hist = remove_zero_bins(uncor_data_hist)
    recon_hist_fall = hist_file_recon_fall.Get(recon_hist_name)
    thrown_hist_fall = hist_file_thrown_fall.Get(thrown_hist_name)
    recon_hist_spring = hist_file_recon_spring.Get(recon_hist_name)
    thrown_hist_spring = hist_file_thrown_spring.Get(thrown_hist_name)

    # data_hist.Rebin()

    data_hist.SetMinimum(0)
    recon_hist_spring.SetMinimum(0)
    thrown_hist_spring.SetMinimum(0)
    recon_hist_fall.SetMinimum(0)
    thrown_hist_fall.SetMinimum(0)

    data_histogram_array.append(data_hist)

    acceptance_fall = recon_hist_fall.GetEntries() / thrown_hist_fall.GetEntries()
    acceptance_spring = recon_hist_spring.GetEntries() / thrown_hist_spring.GetEntries()

    flux, weight_fall, weight_spring = get_flux_and_weights(flux_filename_fall, flux_filename_spring, beam_energy)
    acceptance = weight_fall * acceptance_fall + weight_spring * acceptance_spring

    if(acceptance > 0):
        acceptance_list.append(acceptance)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)
    else:
        acceptance_list.append(1.0)
        acceptance_list_spring.append(acceptance_spring)
        acceptance_list_fall.append(acceptance_fall)

c1 = ROOT.TCanvas("c1")
c1.Divide(4, 2)

print(acceptance_list)

ROOT.gStyle.SetOptStat(0)

# for y in range(len(data_histogram_array)):
#     c1.cd(y + 1)
#     data_histogram_array[y].Draw()
#     c1.Update()

for x in range(len(data_histogram_array)):
    c1.cd(x + 1)
    
    print(f"fitting histogram {x}")
    fit_start = get_fit_start(data_histogram_array[x])

    func = ROOT.TF1(f"func_{x}", full_fit_single, fit_start, fit_end, 6)
    # func.SetParameters(params[0], params[1], params[2], params[3], params[4], params[5])
    func.SetParameter(0, params[0])
    func.SetParameter(1, params[1])
    func.SetParameter(2, params[2])
    func.SetParameter(3, params[3])
    func.SetParameter(4, params[4])
    func.SetParameter(5, params[5])
    # func.SetParameter(6, params[6])
    # func.SetParameter(7, params[7])
    # func.SetParameter(8, params[8])


    data_histogram_array[x].Fit(func, "LRN") # rn 

    print(f"done fitting histogram {x}")
    func.SetLineColor(2)

    rel_bw = ROOT.TF1("rel_bw", relBreitWigner, fit_start, fit_end, 3)
    rel_bw.SetParameters(func.GetParameter(0), func.GetParameter(1), func.GetParameter(2))
    rel_bw.SetParError(0, func.GetParError(0))
    rel_bw.SetParError(1, func.GetParError(1))
    rel_bw.SetParError(2, func.GetParError(2))
    rel_bw.SetLineColor(3)
    rel_bw_list.append(rel_bw)

    # bw_1420 = ROOT.TF1("bw_1420", bw, fit_start, fit_end, 3)
    # bw_1420.SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    # bw_1420.SetParError(0, func.GetParError(3))
    # bw_1420.SetParError(1, func.GetParError(4))
    # bw_1420.SetParError(2, func.GetParError(5))
    # bw_1420.SetLineColor(1)
    # bw_list.append(bw_1420)

    background.append(ROOT.TF1("background_1285", bkg_func, fit_start, fit_end, 3))
    background[x].SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
    background[x].SetLineColor(4)

    # print(f"Intergral method returns: {rel_bw.Integral(fit_start, fit_end)}")

    integral_1285 = rel_bw.Integral(fit_start, fit_end)/bin_size
    # integral_1420 = bw_1420.Integral(fit_start, fit_end)/bin_size
    integral_bkg = background[x].Integral(fit_start, fit_end)/bin_size
    raw_yield.append(integral_1285)
    # raw_yield_1420.append(integral_1420)
    raw_yield_bkg.append(integral_bkg)
    # print(f"yield = {integral_1285} +/- {np.sqrt(integral_1285)}")
    dsig_1285, sig_1285 = func.GetParError(2), func.GetParameter(2)
    damp_1285, amp_1285 =func.GetParError(0), func.GetParameter(0)
    # error_values_1285.append(math.sqrt(integral_1285)/ integral_1285)
    error_values_1285.append(func.GetParError(0)/integral_1285)

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
    #bw_list[x].Draw("same")
    # # # gaus_1285[x].Draw("same")
    background[x].Draw("same")


theory_filename = f'/Users/tylerviducic/research/gluex/theory_predictions/t-slope-{beam_energy}GeVnew.dat'

theory_df = pd.read_csv(theory_filename, delim_whitespace=True)

theory_df.columns = ['minus_t', 'diff_cs']
theory_df = theory_df[theory_df['minus_t'] > 0.29]
theory_df['diff_cs'] = theory_df['diff_cs'] * 1000

bin_corrected_yield = [i/j for i, j in zip(integral_values_1285, bin_width)]
for i, j in zip(integral_values_1285, bin_width):
    print(j)
bin_corrected_raw_yield_1285 = [i/j for i, j in zip(raw_yield, bin_width)]
#bin_corrected_raw_yield_1420 = [i/j for i, j in zip(raw_yield_1420, bin_width)]
bin_corrected_raw_yield_bkg = [i/j for i, j in zip(raw_yield_bkg, bin_width)]


diff_cs = [entry / (flux * branching_ratio /6) for entry in bin_corrected_yield] #/6
diff_cs_error = [error * cs for error, cs in zip(error_values_1285, diff_cs)]


# for t_point, cs_point in zip(bin_values, diff_cs):
    # print(f"t = {t_point} -- cs = {cs_point} +/- {diff_cs_error[bin_values.index(t_point)]}\n Flux = {flux}, efficiency = {acceptance_list[bin_values.index(t_point)]}\n yield = ")
    # print(f"t = {t_point} | yield = {integral_values_1285}binwidth = {bin_width[bin_values.index(t_point)]} cs = {cs_point} +/- {diff_cs_error[bin_values.index(t_point)]} | Flux = {flux} | efficiency = {acceptance_list[bin_values.index(t_point)]}")


cs_df['t'] = bin_values
cs_df['bin_width'] = bin_width
cs_df['yield'] = raw_yield
cs_df['yield_percent_error'] = [x * 100 for x in error_values_1285]
cs_df['acceptance'] = acceptance_list
cs_df['cs'] = diff_cs

print(cs_df)

csv_filename = f'/Users/tylerviducic/research/gluex/fit_csv/cs_dataframe_{beam_energy}_{topology}.csv'
cs_df.to_csv(csv_filename, index=False)

fig = plt.figure()
ax1 = fig.add_subplot(111) 
ax1.errorbar(bin_values, diff_cs, yerr=diff_cs_error, xerr=[x/2 for x in bin_width], fmt='o', ls='none', color='red')
# ax1.errorbar(bin_values, integral_values_1420, yerr=error_values_1420,fmt='o', ls='none', color='black')
#ax1.errorbar(bin_values, integral_values_1285, fmt='o', ls='none', color='red')
ax1.scatter(theory_df['minus_t'], theory_df['diff_cs'], marker='o' ,color='blue', s=3)
ax1.set_ylabel("differential cross section [pb/GeV]")
ax1.set_xlabel("-t (GeV)^2")
# ax1.set_title("N(f1(1285)) vs W (GeV)")
ax1.set_title("differential cross-section [pb]/GeV vs -t (GeV^2)")
ax1.set_yscale('log')
ax1.set_xlim([0.0, 2.0])
ax1.set_ylim([1000, 1e6])


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

print(acceptance_fall)
print(bin_values)

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.scatter(bin_values, acceptance_list, color='black')
ax4.scatter(bin_values, acceptance_list_fall, color='red')
ax4.scatter(bin_values, acceptance_list_spring, color='blue')
ax4.set_ylabel("acceptance")
ax4.set_xlabel("-t (GeV)^2")
ax4.set_title("acceptance vs -t")
ax4.set_xlim([0.0, 2.0])
# ax4.set_ylim([0.03, 0.05])

# fig5 = plt.figure()
# ax5 = fig5.add_subplot(111)
# ax5.scatter(bin_values, bin_corrected_raw_yield_1285, color='black')
#ax5.scatter(bin_values, bin_corrected_raw_yield_1420, color='red')
# ax5.scatter(bin_values, bin_corrected_raw_yield_bkg, color='blue')
# ax5.scatter(bin_values, bin_corrected_yield, color='green')


plt.show()

c1.Update()
input("Press any key to exit")
c1.Close()
plt.close()