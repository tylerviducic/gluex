# script for fitting ksk-pi+ distribution with a cut applied to one of the other K*

import ROOT

#TODO fit acceptance corrected distributions because background is not smooth

channel = 'pipkmks'
run_period = 'fall'
selector_method = 'bestX2'
run_dict = {
    'fall': '2018_fall',
    'spring': '2018_spring',
    '2017': '2017'
}

beam = 9
kstar_cut = 'plus'
bin_width = 'narrow'
t_bin = 3
beam_range = f'{beam - 0.5}_{beam+0.5}'

t_bin_dict = {1: '0.1-0.2', 2: '0.2-0.3', 3: '0.3-0.4',
              4: '0.4-0.65', 5: '0.65-0.9', 
              6: '0.9-1.4', 7: '1.4-1.9'}

# filename = f'/work/halld/home/viducic/selector_output/f1_flat/{channel}_flat_result_{run_dict[run_period]}.root'
filename = f'/work/halld/home/viducic/data/{channel}/data/{selector_method}/{channel}_flat_result_{run_dict[run_period]}.root'
data_file = ROOT.TFile.Open(filename, 'READ')
data_hist_name = channel + '_beam_' + beam_range+ '_cut_kstar_' + kstar_cut + f'_cut_t_{t_bin_dict[t_bin]}_' + bin_width +';1'
data_hist = data_file.Get(data_hist_name)

# data_hist.Draw()
# input('Press enter to continue...')

x = ROOT.RooRealVar("x", "x", 1.125, 1.7)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)

# x.setRange("signal", 1.15, 2.0)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

relbw_m = ROOT.RooRealVar("relbw_m", "relbw_m", 1.285, 1.2, 1.3)
relbw_width = ROOT.RooRealVar("relbw_width", "relbw_width", 0.025, 0.01, 0.03)

relbw = ROOT.RelBreitWigner("relbw", "relbw", x, relbw_m, relbw_width)

bw_m = ROOT.RooRealVar("bw_m", "bw_m", 1.42, 1.35, 1.5)
bw_width = ROOT.RooRealVar("bw_width", "bw_width", 0.05, 0.01, 0.1)

bw = ROOT.RooBreitWigner("bw", "bw", x, bw_m, bw_width)

## BACKGROUND OPTIONS ##

## CHEBYCHEV ##

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

bkg = ROOT.RooChebychev("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

## BERSTEIN ##

# bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1, 0.0, 10.0)
# bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1, 0.0, 10.0)
# bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", 1, 0.0, 10.0)

# bkg = ROOT.RooBernstein("bkg", "bkg", x, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3))

## ARGUS ## 

# mass_offse_var = ROOT.RooRealVar("mass_offset_var", "mass_offset_var", -1.1, -1.7)
# arg_par_mass_offset = ROOT.RooFormulaVar("arg_par_mass_offset", "mass_offset_var + x", ROOT.RooArgSet(mass_offse_var, x))
# arg_par_m0 = ROOT.RooRealVar("arg_par_m0", "arg_par_m0", 3.7)
# arg_par_c = ROOT.RooRealVar("arg_par_c", "arg_par_c", 3.0, 0.0, 10.0)
# arg_par_p = ROOT.RooRealVar("arg_par_p", "arg_par_p", 0.5, 0.0, 2.0)

# bkg = ROOT.RooArgusBG("bkg", "bkg", arg_par_mass_offset, arg_par_m0, arg_par_c, arg_par_p)

## COMBINED PDF ##
bkg_frac = ROOT.RooRealVar("bkg_frac", "bkg_frac", 0.5, 0.1, 0.9)
bkg_pdf = ROOT.RooAddPdf("bkg_pdf", "bkg_pdf", ROOT.RooArgList(bkg, bw), ROOT.RooArgList(bkg_frac))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.1, 0.9)
combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(relbw, bkg_pdf), ROOT.RooArgList(sig_frac))

# combined_pdf.fitTo(dh, ROOT.RooFit.Range("signal"))
combined_pdf.fitTo(dh)

frame = x.frame()
dh.plotOn(frame)
combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kViolet))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("bw"), ROOT.RooFit.LineColor(ROOT.kGreen))
combined_pdf.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kBlue))

frame.Draw()

input('Press enter to continue...')