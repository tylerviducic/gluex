# script for fitting ksk-pi+ distribution with a cut applied to one of the other K*

import ROOT

channel = 'pipkmks'
run_period = 'fall'
run_dict = {
    'fall': '2018_fall',
    'spring': '2018_spring',
    '2017': '2017'
}

beam = 9
kstar_cut = 'plus'
bin_width = 'medium'
t_bin = 3
beam_range = f'{beam - 0.5}_{beam+0.5}'

t_bin_dict = {1: '0.1-0.2', 2: '0.2-0.3', 3: '0.3-0.4',
              4: '0.4-0.65', 5: '0.65-0.9', 
              6: '0.9-1.4', 7: '1.4-1.9'}

filename = f'/work/halld/home/viducic/selector_output/f1_flat/{channel}_flat_result_{run_dict[run_period]}.root'
data_file = ROOT.TFile.Open(filename, 'READ')
data_hist_name = channel + '_beam_' + beam_range+ '_cut_kstar_' + kstar_cut + f'_cut_t_{t_bin_dict[t_bin]}_' + bin_width +';1'
data_hist = data_file.Get(data_hist_name)

data_hist.Draw()
input('Press enter to continue...')

x = ROOT.RooRealVar("x", "x", 1.0, 2.5)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)

# x.setRange("signal", 1.15, 2.0)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.01, 0.05)

relbw = ROOT.RelBreitWigner("relbw", "relbw", x, relbw_m, relbw_width)

