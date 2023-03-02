# for getting acceptance of f1_1285

import ROOT
import matplotlib.pyplot as plt

recon_filename_spring = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_spring.root'
thrown_filename_spring = '/Users/tylerviducic/research/gluex/f1_mc/analysis/pipkmks_t_binned_thrown_0_1_spring.root'
recon_filename_fall = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_fall.root'
thrown_filename_fall = '/Users/tylerviducic/research/gluex/f1_mc/analysis/pipkmks_t_binned_thrown_0_1_fall.root'
# data_filename = '/Users/tylerviducic/research/gluex/selector_output/pipkmks_2018_spring.root'

recon_file_spring = ROOT.TFile(recon_filename_spring, 'READ')
thrown_file_spring = ROOT.TFile(thrown_filename_spring, 'READ')
recon_file_fall = ROOT.TFile(recon_filename_fall, 'READ')
thrown_file_fall = ROOT.TFile(thrown_filename_fall, 'READ')
# data_file = ROOT.TFile(data_filename, 'READ')

bin_values = []
fall_acceptance = []
spring_acceptance = []
# corrected_histo_list = []

# thrown = 0.2 - 1.0
# recon = 0.200 - 1.000

# c1 = ROOT.TCanvas("c1")
# c1.Divide(5, 2)


for i in range(2, 18, 2):
    bin_values.append((i - 1)/10)
    
    recon_hist_name = f'Binnedf1_1285_{i/10:.3f}_fullbeam'
    thrown_hist_name = f'f1_t_{i/10:.1f}'
    # data_hist_name = f'Binnedf1_1285_{i/10:.3f}_fullbeam'
    # print(data_hist_name)
    
    recon_hist_fall = recon_file_fall.Get(recon_hist_name)
    thrown_hist_fall = thrown_file_fall.Get(thrown_hist_name)
    recon_hist_spring = recon_file_spring.Get(recon_hist_name)
    thrown_hist_spring = thrown_file_spring.Get(thrown_hist_name)
    # data_hist = data_file.Get(data_hist_name)

    acceptance_f = recon_hist_fall.GetEntries() / thrown_hist_fall.GetEntries()
    fall_acceptance.append(acceptance_f)
    acceptance_s = recon_hist_spring.GetEntries() / thrown_hist_spring.GetEntries()
    spring_acceptance.append(acceptance_s)
    # data_hist.Scale(acceptance)
    # corrected_histo_list.append(data_hist * (1 / acceptance))

fig = plt.figure()
ax1 = fig.add_subplot(111)
# ax1.errorbar(bin_values, fall_acceptance, xerr=0.1, color='blue', fmt='o', ls='none')
ax1.errorbar(bin_values, spring_acceptance, xerr=0.1, color='black', fmt='o', ls='none')
ax1.set_ylabel('num_recon/num_thrown')
ax1.set_xlabel('-t (GeV)^2')
ax1.set_title("Preliminary Acceptance for f1(1285) up to -t = 1.9 GeV^2")

plt.xlim([0, 1.75])
plt.ylim([0, 0.04])
plt.show()


# target_file = ROOT.TFile('acceptance_corrected_pipkmks_spring.root', 'RECREATE')

# for x in range(len(corrected_histo_list)):
#     c1.cd(x + 1)
#     corrected_histo_list[x].Draw()
#     corrected_histo_list[x].Write()

# c1.Update()
