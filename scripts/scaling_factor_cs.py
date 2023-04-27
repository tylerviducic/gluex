# calculate the CS for scaling factor compairison with f1>etapipi

# eqn: S = L * sigma * BR(sub branches included) / N(generated)
# eqn for me: S = L * sigma * BR(f1->KKpi)/6 * BR(Ks->pipi)/N(generated)
# sigma = 6 * S * N(generated) / (L * BR(f1->KKpi) * BR(Ks->pipi))

import ROOT 

run_period = 'fall'
run_dict = {'fall': '2018_fall', 
            'spring': '2018_spring',
            '2017': '2017'}

flux_dict = {
    'fall': '50685_51768',
    'spring': '40856_42559'
}

kstar_no_cut = "no_cut"
kstar_plus_cut = 'kspip_m < 0.8 || kspip_m > 1.0'
kstar_zero_cut = 'kmpip_m < 0.8 || kmpip_m > 1.0'
kstar_all_cut = '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)'

kstar_cut_dict = {
    'no_cut': 'kstar_no_cut',
    'kspip_m < 0.8 || kspip_m > 1.0': 'kstar_plus_cut',
    'kmpip_m < 0.8 || kmpip_m > 1.0': 'kstar_zero_cut',
    '(kspip_m < 0.8 || kspip_m > 1.0) && (kmpip_m < 0.8 || kmpip_m > 1.0)': 'kstar_all_cut'
}

br_kkpi = 0.091
br_kspipi = 0.692

# scale_factor = 0.0215 # beam = 6.5-10.5 GeV, 0.5 < mand_t < 1.9 GeV^2
scale_factor = 0.019 # beam = 8-10 GeV, 0.5 < mand_t < 1.9 GeV^2


cut_data_filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_filtered_{run_dict[run_period]}.root'
cut_mc_filename = f'/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/mc_pipkmks_filtered_{run_dict[run_period]}.root'
flux_filename = f'/w/halld-scshelf2101/home/viducic/selector_output/flux/flux_{flux_dict[run_period]}.root'

flux_file = ROOT.TFile.Open(flux_filename, "READ")
lumi_hist = flux_file.Get('tagged_lumi')
lumi = lumi_hist.GetEntries()

data_df = ROOT.RDataFrame(f'pipkmks_filtered_{run_dict[run_period]}', cut_data_filename)
mc_df = ROOT.RDataFrame(f'mc_pipkmks_filtered_{run_dict[run_period]}', cut_mc_filename)

data_df = data_df.Filter('e_beam >= 8.0 && e_beam <= 10.0').Filter('mand_t >= 0.5 && mand_t <= 1.9').Filter(kstar_zero_cut)
mc_df = mc_df.Filter('e_beam >= 8.0 && e_beam <= 10.0').Filter('mand_t >= 0.5 && mand_t <= 1.9').Filter(kstar_zero_cut)

data_hist = data_df.Histo1D(('data_pipkmks_m', 'data_pipkmks_m', 100, 1.0, 1.7), 'pipkmks_m')
mc_hist = mc_df.Histo1D(('mc_pipkmks_m', 'mc_pipkmks_m', 100, 1.0, 1.7), 'pipkmks_m')
mc_hist.Scale(scale_factor)

data_hist.SetLineColor(ROOT.kBlue)
mc_hist.SetLineColor(ROOT.kRed)

n_generated = 51238104

sfcs = (scale_factor * 6 * n_generated) / (lumi * br_kkpi * br_kspipi)

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
data_hist.Draw()
mc_hist.Draw("HIST SAME")

c1.Update()

close_canvas = input('press enter to close canvas')

print('scaling factor cross section eqn: cs = [sf * 6 * N(gen)] / [L * BR(f1->KKpi) * BR(Ks->pipi)]')
print(f'calculation: cs = [{scale_factor} * 6 * {n_generated}] / [{lumi} * {br_kkpi} * {br_kspipi}]')
print(f'cs = {sfcs} pb (?)')