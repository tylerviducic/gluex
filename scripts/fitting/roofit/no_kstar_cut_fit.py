# script to fit m(kkpi) without cut on K* 

import ROOT

data_filename = "/w/halld-scshelf2101/home/viducic/selector_output/f1_flat/pipkmks_flat_result_2018_spring.root"

data_file = ROOT.TFile(data_filename, 'READ')


mass_range = 'wide'
data_hist = data_file.Get(f"f1_nocut_{mass_range}")
# data_hist = data_file.Get(f"pipkmks_beam_8_t_0.4_kstar_no_cut_narrow")

mass_range_end_values = {
    'narrow': 1.7,
    'medium': 2.5,
    'wide': 3.8
}

x = ROOT.RooRealVar("x", "x", 1.0, mass_range_end_values[mass_range])
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(x), data_hist)

ROOT.gROOT.ProcessLineSync(".x /w/halld-scshelf2101/home/viducic/roofunctions/RelBreitWigner.cxx+")

m_relbw = ROOT.RooRealVar("m", "m", 1.285, 1.2, 1.325)
width_relbw = ROOT.RooRealVar("width", "width", 0.026, 0.01, 0.1)
# amplitude_relbw = ROOT.RooRealVar("amplitude", "amplitude", 0.0, 10000.0)

relbw = ROOT.RelBreitWigner("relbw", "relbw", x, m_relbw, width_relbw)

m_bw = ROOT.RooRealVar("m_bw", "m_bw", 1.420, 1.375, 1.5)
width_bw = ROOT.RooRealVar("width_bw", "width_bw", 0.052, 0.01, 0.15)
# amplitude_bw = ROOT.RooRealVar("amplitude_bw", "amplitude_bw", 0.0, 10000.0)

bw = ROOT.RooBreitWigner("bw", "bw", x, m_bw, width_bw)

# ARGUS BACKGROUND
mass_offse_var = ROOT.RooRealVar("mass_offset_var", "mass_offset_var", -1.1, -1.2)
arg_par_mass_offset = ROOT.RooFormulaVar("arg_par_mass_offset", "mass_offset_var + x", ROOT.RooArgSet(mass_offse_var, x))
arg_par_m0 = ROOT.RooRealVar("arg_par_m0", "arg_par_m0", 3.7)
arg_par_c = ROOT.RooRealVar("arg_par_c", "arg_par_c", 3.0, 0.0, 10.0)
arg_par_p = ROOT.RooRealVar("arg_par_p", "arg_par_p", 0.5, 0.0, 2.0)

bkg = ROOT.RooArgusBG("bkg", "bkg", arg_par_mass_offset, arg_par_m0, arg_par_c, arg_par_p)

# COMBINE MODELS
frac_bkg = ROOT.RooRealVar("frac_bkg", "frac_bkg", 0.01, 0.9)
composite_bkg = ROOT.RooAddPdf("composite_bkg", "composite_bkg", ROOT.RooArgList(bw, bkg), ROOT.RooArgList(frac_bkg))

frac_relbw = ROOT.RooRealVar("frac_relbw", "frac_relbw", 0.001, 0.9)
composite_model = ROOT.RooAddPdf("composite_model", "composite_model", ROOT.RooArgList(relbw, composite_bkg), ROOT.RooArgList(frac_relbw))

composite_model.fitTo(dh)


frame = x.frame()
dh.plotOn(frame)
composite_model.plotOn(frame)
composite_model.plotOn(frame, ROOT.RooFit.Components("composite_bkg"), ROOT.RooFit.LineColor(ROOT.kRed))
composite_model.plotOn(frame, ROOT.RooFit.Components("relbw"), ROOT.RooFit.LineColor(ROOT.kGreen))

frame.Draw()

