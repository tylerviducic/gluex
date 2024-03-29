# calculation of f1(1285) cross section using pyroot

import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd
import math
from ctypes import c_double
# import my_library.gluex_style as gxstyle

def get_title_for_plots(e, t):
    e_gamma = 'E_{#gamma}'
    tbin = f'{constants.T_CUT_DICT[t][0]} < t < {constants.T_CUT_DICT[t][1]} GeV^{2}'
    return f'{e_gamma} = {e} GeV, {tbin}'

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks' :
    v_mean = constants.F1_PIPKMKS_VOIGHT_MEAN
    v_width = constants.F1_PIPKMKS_VOIGHT_SIGMA
    total_fit_color = 860
    f1_color = 860-6
    gaus_color = 880
    background_color = 616
elif channel == 'pimkpks' :
    v_mean = constants.F1_PIMKPKS_VOIGHT_MEAN
    v_width = constants.F1_PIMKPKS_VOIGHT_SIGMA
    total_fit_color = 633
    f1_color = 634
    gaus_color = 887
    background_color = 618

df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv')

mean_list = []
mean_error_list = []
width_list = []
width_error_list = []
chi2ndf_list = []
ks_test_list = []
data_yield_list = []
yield_error_list = []
acceptance_list = []
acceptance_error_list = []
bin_width_list = []
cross_section_list = []
cross_section_error_list = []
t_bin_list = []
t_bin_width_list = []
energy_bin_list = []


hist_range_low = 1.15
hist_range_high = 1.5

c = ROOT.TCanvas()
c.Divide(4, 2)


for e in range(8, 12):
    hist_uncor_list = []
    hist_cor_list = []
    luminosity = ct.get_luminosity_gluex_1(e-0.5, e+0.5)
    for t in range(1, 8):
        c.cd(t)
        
        hist_uncor_list.append(ct.get_gluex1_binned_kkpi_data(channel, cut, e, t))
        hist = ct.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist_cor_list.append(hist)

        m_kkpi = ROOT.RooRealVar(f"m_kkpi_{e}_{t}", f"m_kkpi_{e}_{t}", hist_range_low, hist_range_high)
        range_min = 1.15
        range_max = 1.5
        m_kkpi.setRange("fit_range", range_min, range_max)
        dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), hist)

        voight_mean = ROOT.RooRealVar(f"voight_mean_{e}_{t}", f"voight_mean_{e}_{t}", v_mean, 1.26, 1.3)
        voight_width = ROOT.RooRealVar(f"voight_width_{e}_{t}", f"voight_width_{e}_{t}", v_width, 0.01, 0.05)
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]
        voight_sigma = ROOT.RooRealVar(f"voight_sigma_{e}_{t}", f"voight_sigma_{e}_{t}", e_t_sigma, 0.001, 0.1)

        voight_sigma.setConstant(True)
        voight_width.setConstant(True)
        voight_mean.setConstant(True)

        voight = ROOT.RooVoigtian(f"voight_{e}_{t}", f"voight_{e}_{t}", m_kkpi, voight_mean, voight_width, voight_sigma)

        gaus_m = ROOT.RooRealVar("gaus_m", "gaus_m", 1.37, 1.3, 1.5)
        gaus_width = ROOT.RooRealVar("gaus_width", "gaus_width", 0.037, 0.02, 0.075)
        gaus = ROOT.RooGaussian("gaus", "gaus", m_kkpi, gaus_m, gaus_width)
        # gaus_m.setConstant(True)
        # gaus_width.setConstant(True)

        ## CHEBYCHEV ##

        bkg_par1 = ROOT.RooRealVar(f"bkg_par1_{e}_{t}", f"bkg_par1_{e}_{t}", 0.0, 2.0)
        bkg_par2 = ROOT.RooRealVar(f"bkg_par2_{e}_{t}", f"bkg_par2_{e}_{t}", 0.0, 2.0)
        bkg_par3 = ROOT.RooRealVar(f"bkg_par3_{e}_{t}", f"bkg_par3_{e}_{t}", 0.0, 2.0)
        bkg_par4 = ROOT.RooRealVar(f"bkg_par4_{e}_{t}", f"bkg_par4_{e}_{t}", 0.0, 2.0)

        bkg = ROOT.RooChebychev(f"bkg_{e}_{t}", f"bkg_{e}_{t}", m_kkpi, ROOT.RooArgList(bkg_par1) )

        # sig_frac = ROOT.RooRealVar(f"sig_frac_{e}_{t}", f"sig_frac_{e}_{t}", 0.5, 0.0, 1.0)
        n_signal = ROOT.RooRealVar(f"n_signal_{e}_{t}", f"n_signal_{e}_{t}", 100000, 0, 10000000)
        n_gaus = ROOT.RooRealVar(f"n_gaus_{e}_{t}", f"n_gaus_{e}_{t}", 100000, 0, 10000000)
        n_bkg = ROOT.RooRealVar(f"n_bkg_{e}_{t}", f"n_bkg_{e}_{t}", 100000, 0, 10000000)

        combined_pdf = ROOT.RooAddPdf(f'combined_pdf_{e}_{t}', f'combined_pdf_{e}_{t}', ROOT.RooArgList(voight, gaus, bkg), ROOT.RooArgList(n_signal, n_gaus, n_bkg))
        chi2_var = combined_pdf.createChi2(dh)
        c2 = ROOT.RooChi2Var(f"c2_{e}_{t}", f"c2_{e}_{t}", combined_pdf, dh, ROOT.RooFit.Extended(True), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Range("fit_range"))
        minuit = ROOT.RooMinuit(c2)
        minuit.migrad()
        # minuit.minos()
        minuit.hesse()
        fit_result = minuit.save()

        bkg_par1_guess = bkg_par1.getVal()
        bkg_par2_guess = bkg_par2.getVal()
        bkg_par3_guess = bkg_par3.getVal()
        bkg_par4_guess = bkg_par4.getVal()

        data_yield = n_signal.getVal()
        data_yield_error = n_signal.getError()
        acceptance, acceptance_error = ct.get_binned_gluex1_signal_acceptance(channel, e, t)

        cross_section = ct.calculate_crosssection(data_yield, acceptance, luminosity, constants.T_WIDTH_DICT[t], constants.F1_KKPI_BRANCHING_FRACTION)
        cross_section_error = ct.propogate_error_multiplication(cross_section, [data_yield, acceptance, luminosity, constants.F1_KKPI_BRANCHING_FRACTION], [data_yield_error, acceptance_error, luminosity * 0.05, constants.F1_KKPI_BRANCHING_FRACTION_ERROR])

        chi2_val = c2.getVal()

        frame = m_kkpi.frame()
        # title = get_title_for_plots(channel, e, t)
        title = get_title_for_plots(e, t)
        frame.SetTitle(title)
        frame.GetXaxis().SetTitle(title.split(" ")[0] + 'GeV')
        frame.GetYaxis().SetTitle(f'Event/10 MeV')

        n_bins = (hist_range_high-hist_range_low)*100
        ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
        chi2ndf = chi2_val / ndf

        dh.plotOn(frame)
        combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(total_fit_color), ROOT.RooFit.Name("full_fit"))
        combined_pdf.plotOn(frame, ROOT.RooFit.Components("voight"), ROOT.RooFit.LineColor(f1_color), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(f1_color), ROOT.RooFit.LineWidth(5), ROOT.RooFit.Name("f1_signal"))
        combined_pdf.plotOn(frame, ROOT.RooFit.Components("gaus"), ROOT.RooFit.LineColor(gaus_color), ROOT.RooFit.LineWidth(4), ROOT.RooFit.Name("1420_tail"))
        combined_pdf.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(background_color), ROOT.RooFit.MarkerColor(background_color), ROOT.RooFit.LineWidth(4), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name("bkg"))

        ks_test_func = combined_pdf.createHistogram(f"ks_test_func_{e}_{t}", m_kkpi, ROOT.RooFit.Binning(1000))
        ks_test_data = dh.createHistogram(f"ks_test_data_{e}_{t}", m_kkpi, ROOT.RooFit.Binning(1000))

        kstest = ks_test_data.KolmogorovTest(ks_test_func)
        mean_list.append(voight_mean.getVal())
        mean_error_list.append(voight_mean.getError())
        width_list.append(voight_width.getVal())
        width_error_list.append(voight_width.getError())
        chi2ndf_list.append(chi2ndf)
        ks_test_list.append(kstest)
        data_yield_list.append(data_yield)
        yield_error_list.append(data_yield_error)
        acceptance_list.append(acceptance)
        acceptance_error_list.append(acceptance_error)
        cross_section_list.append(cross_section)
        cross_section_error_list.append(cross_section_error)
        t_bin_list.append((constants.T_CUT_DICT[t][0] + constants.T_CUT_DICT[t][1])/2.0)
        t_bin_width_list.append(constants.T_WIDTH_DICT[t]/2.0)
        energy_bin_list.append(e)
        
        frame.Draw()
        c.Update()

    c.SaveAs(f'/work/halld/home/viducic/plots/thesis/cross_section_fits/{channel}_cross_section_fits_beam_{e}.png')
    c.SaveAs(f'/work/halld/home/viducic/scripts/plotting/dnp_maui/plots/{channel}_cross_section_fits_beam_{e}.png')
    # c1 = ROOT.TCanvas()
    # c1.Divide(4, 2)
    # index = 1
    # for hist_uncor, hist_cor in zip(hist_uncor_list, hist_cor_list):
    #     c1.cd(index)
    #     index += 1
    #     hist_uncor.GetXaxis().SetRangeUser(hist_range_low, hist_range_high)
    #     hist_cor.GetXaxis().SetRangeUser(hist_range_low, hist_range_high)
    #     hist_cor.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red']))
    #     hist_uncor.SetLineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue']))
    #     hist_uncor.Draw()
    #     hist_cor.Draw('same')
    #     c1.Update()
    # c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/cross_section_fits/{channel}_data_hist_correction_comparison_{e}.png')




# c1.SaveAs(f'/work/halld/home/viducic/plots/thesis/cross_section_fits/{channel}_uncorrected_data_hist_beam_{e}.png')
# make a pandas datframe out of the lists
value_df = pd.DataFrame({'mean': mean_list, 'mean_error': mean_error_list, 'width': width_list, 'width_error': width_error_list, 'chi2ndf': chi2ndf_list, 'ks_test': ks_test_list, 'yield': data_yield_list, 'yield_error': yield_error_list, 'acceptance': acceptance_list, 'acceptance_error': acceptance_error_list,'cross_section': cross_section_list, 'cross_section_error': cross_section_error_list, 't_bin_middle': t_bin_list, 't_bin_width': t_bin_width_list, 'beam_energy': energy_bin_list})
value_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values.csv', index=False)


input('Press enter to exit')

