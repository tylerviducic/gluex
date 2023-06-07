# calculation of f1(1285) cross section using pyroot

import ROOT
from common_analysis_tools import *
import pandas as pd
import math
from ctypes import c_double


channel = 'pipkmks'
cut = 'all'

df = pd.read_csv('/work/halld/home/viducic/data/fit_params/pipkmks/binned_e_t_f1_mc_width.csv')

mean_list = []
mean_error_list = []
width_list = []
width_error_list = []
chi2ndf_list = []
ks_test_list = []
ac_yield_list = []
yield_error_list = []
bin_width_list = []
cross_section_list = []
cross_section_error_list = []


# print(df)

canvas_dict = {}

fit_range_low = 1.2
fit_range_high = 1.5

for i in range(7, 11):
    canvas = ROOT.TCanvas(f'canvas_{i}', f'canvas_{i}', 1200, 900)
    canvas.Divide(4, 2)
    canvas_dict[i] = canvas

for e in range(7, 11):
    luminosity = get_luminosity_gluex_1(e-0.5, e+0.5)
    for t in range(1, 8):
        canvas_dict[e].cd(t)
        
        hist = acceptance_correct_all_gluex_1_kkpi_data(channel, cut, e, t)

        m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", fit_range_low, fit_range_high)
        dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), hist)

        voight_mean = ROOT.RooRealVar("voight_mean", "voight_mean", 1.281, 1.275, 1.2295)
        voight_width = ROOT.RooRealVar("voight_width", "voight_width", 0.022, 0.01, 0.05)
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]
        voight_sigma = ROOT.RooRealVar("voight_sigma", "voight_sigma", e_t_sigma, 0.001, 0.1)
        voight_sigma.setConstant(True)

        voight = ROOT.RooVoigtian("voight", "voight", m_kkpi, voight_mean, voight_width, voight_sigma)

        ## CHEBYCHEV ##

        bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", -1.0, 1.0)
        bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", -1.0, 1.0)
        bkg_par3 = ROOT.RooRealVar("bkg_par3", "bkg_par3", -1.0, 1.0)
        bkg_par4 = ROOT.RooRealVar("bkg_par4", "bkg_par4", -1.0, 1.0)

        bkg = ROOT.RooChebychev("bkg", "bkg", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3)) 

        sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)

        combined_pdf = ROOT.RooAddPdf('combined_pdf', 'combined_pdf', ROOT.RooArgList(voight, bkg), ROOT.RooArgList(sig_frac))
        chi2_var = combined_pdf.createChi2(dh)

        fit_result = combined_pdf.chi2FitTo(dh, ROOT.RooFit.Save())

        hist_error = c_double(0.0)
        hist_integral = hist.IntegralAndError(hist.FindBin(fit_range_low), hist.FindBin(fit_range_high), hist_error)
        ac_yield =  hist_integral * sig_frac.getVal()
        ac_yield_error = propogate_error_multiplication(ac_yield, [hist_integral, sig_frac.getVal()], [hist_error.value, sig_frac.getError()])
        cross_section = calculate_crosssection_from_acceptance_corrected_yield(ac_yield, luminosity, t_width_dict[t], F1_KKPI_BRANCHING_FRACTION)
        cross_section_error = propogate_error_multiplication(cross_section, [ac_yield, luminosity, F1_KKPI_BRANCHING_FRACTION], [ac_yield_error, math.sqrt(luminosity), F1_KKPI_BRANCHING_FRACTION_ERROR])

        chi2_val = chi2_var.getVal()

        frame = m_kkpi.frame()

        n_bins = hist.GetNbinsX()
        ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
        chi2ndf = chi2_val / ndf

        dh.plotOn(frame)
        combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red'])))
        # pullHist = frame.pullHist()
        combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green'])), ROOT.RooFit.LineStyle(ROOT.kDashed))
        combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue'])))

        ks_test_func = combined_pdf.createHistogram("ks_test_func", m_kkpi, ROOT.RooFit.Binning(1000))
        ks_test_data = dh.createHistogram("ks_test_data", m_kkpi, ROOT.RooFit.Binning(1000))

        kstest = ks_test_data.KolmogorovTest(ks_test_func)
        mean_list.append(voight_mean.getVal())
        mean_error_list.append(voight_mean.getError())
        width_list.append(voight_width.getVal())
        width_error_list.append(voight_width.getError())
        chi2ndf_list.append(chi2ndf)
        ks_test_list.append(kstest)
        ac_yield_list.append(ac_yield)
        yield_error_list.append(ac_yield_error)
        cross_section_list.append(cross_section)
        cross_section_error_list.append(cross_section_error)
        
        frame.Draw()

        canvas_dict[e].Update()

# make a pandas datframe out of the lists
value_df = pd.DataFrame({'mean': mean_list, 'mean_error': mean_error_list, 'width': width_list, 'width_error': width_error_list, 'chi2ndf': chi2ndf_list, 'ks_test': ks_test_list, 'yield': ac_yield_list, 'yield_error': yield_error_list, 'cross_section': cross_section_list, 'cross_section_error': cross_section_error_list})
value_df.to_csv('/work/halld/home/viducic/data/fit_params/pipkmks/cross_section_values.csv', index=False)

input('Press enter to exit')

