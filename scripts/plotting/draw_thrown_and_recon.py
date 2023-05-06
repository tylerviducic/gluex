# draw the thrown and recon plots on the same canvas

import ROOT
import matplotlib.pyplot as plt

beam_energy = 8
recon_filename = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_spring.root'
thrown_filename = f'/Users/tylerviducic/research/gluex/f1_mc/analysis/pipkmks_t_binned_thrown_0_2_{beam_energy}_spring.root'

hist_file_recon = ROOT.TFile(recon_filename, 'READ')
hist_file_thrown = ROOT.TFile(thrown_filename, 'READ')

thrown_list = []
recon_list = []
bin_values = []

energy_values_low = ['0.250', '0.300', '0.350', '0.400'] #'0.100', '0.150', '0.200',  
energy_values_med = ['0.500', '0.600', '0.700', '0.800', '0.900']
energy_values_high = ['1.100', '1.300']#, '1.500', '1.700', '1.900']

thrown_low =  ['0.25', '0.3', '0.35', '0.4']
thrown_med = ['0.5', '0.6', '0.7', '0.8', '0.9']
thrown_high = ['1.1', '1.3']#,'1.5', '1.7', '1.9']

acceptance_list = []

# thrown = 0.2 - 1.0
# recon = 0.200 - 1.000

# c1 = ROOT.TCanvas("c1")
# c1.Divide(5, 2)

ROOT.gStyle.SetOptStat(0)


for energy in energy_values_low:
    bin_values.append(float(energy) - 0.025)

    thrown_index = energy_values_low.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_low[thrown_index]}'



    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)

    recon_hist.SetLineColor(2)
    thrown_hist.SetLineColor(1)
    # recon_hist.Scale(100)

    thrown_list.append(thrown_hist)
    recon_list.append(recon_hist)

for energy in energy_values_med:
    bin_values.append(float(energy) - 0.05)

    thrown_index = energy_values_med.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_med[thrown_index]}'
    # print(data_hist_name)


    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)

    recon_hist.SetLineColor(2)
    thrown_hist.SetLineColor(1)
    # recon_hist.Scale(100)
    thrown_list.append(thrown_hist)
    recon_list.append(recon_hist)

for energy in energy_values_high:
    bin_values.append(float(energy) - 0.1)


    thrown_index = energy_values_high.index(energy)
    
    recon_hist_name = f'Binnedf1_1285_{energy}_beam_{beam_energy}'
    thrown_hist_name = f'f1_t_{thrown_high[thrown_index]}'
    # print(data_hist_name)


    recon_hist = hist_file_recon.Get(recon_hist_name)
    thrown_hist = hist_file_thrown.Get(thrown_hist_name)

    recon_hist.SetMinimum(0)
    thrown_hist.SetMinimum(0)
    # recon_hist.Scale(100)

    acceptance = recon_hist.GetEntries() / thrown_hist.GetEntries()
    if(acceptance > 0):
        acceptance_list.append(acceptance)
    else:
        acceptance_list.append(1.0)


    recon_hist.SetLineColor(2)
    thrown_hist.SetLineColor(1)

    thrown_list.append(thrown_hist)
    recon_list.append(recon_hist)




c1 = ROOT.TCanvas("c1")
c1.Divide(6, 2)
for x in range(len(thrown_hist)):
    c1.cd(x + 1)
    thrown_list[x].Draw()
    recon_list[x].Draw("same, h")
    c1.Update()

# fig = plt.figure()
# ax1 = fig.add_subplot(111) 
# ax1.errorbar(bin_values, thrown_list, xerr=0.1, fmt='o', ls='none', color='black')
# ax1.errorbar(bin_values, recon_list, xerr=0.1, fmt='o', ls='none', color='purple')
# ax1.set_ylabel("Acceptance")
# ax1.set_xlabel("-t (GeV)^2")
# ax1.set_title("Acceptance Corrected Yield vs -t (GeV^2)")

# plt.show()
