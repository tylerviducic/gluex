# calculation of f1(1285) cross section using pyroot

import ROOT
import my_library.common_analysis_tools as ct
import pandas as pd
import math
from ctypes import c_double

def get_title_for_plots(channel, e, t):
    e_gamma = 'E_{#gamma}'
    if channel == 'pipkmks':
        title_kkpi = 'K^{-}K_{s}#pi^{+}'
    elif channel == 'pimkpks':
        title_kkpi = '#pi^{-}K^{+}K_{s}'
    else:
        return None
    line1 = f'Fit for {title_kkpi} for {e_gamma} = {e} GeV'
    line2 = f'{ct.T_CUT_DICT[t][0]} < t < {ct.T_CUT_DICT[t][1]} GeV^{2}'
    return '#splitline{' + line1 + '}{' + line2 + '}'


channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks' :
    v_mean = ct.F1_PIPKMKS_ACCETPANCE_CORRECTED_VOIGHT_WIDTH
    v_width = ct.F1_PIPKMKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA
elif channel == 'pimkpks' :
    v_mean = ct.F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_MEAN
    v_width = ct.F1_PIMKPKS_ACCEPTANCE_CORRECTED_VOIGHT_SIGMA

df = pd.read_csv(f'//work/halld/home/viducic/data/fit_params/{channel}/psac_binned_e_t_f1_mc_width.csv')

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
t_bin_list = []
t_bin_width_list = []
energy_bin_list = []

hist_range_low = 1.2
hist_range_high = 1.5

c = ROOT.TCanvas()
c.Divide(4, 2)

for e in range(7, 12):
    luminosity = ct.get_luminosity_gluex_1(e-0.5, e+0.5)
    for t in range(1, 8):
        c.cd(t)
        
        hist = ct.acceptance_correct_all_binned_gluex1_kkpi_data_with_phasespace(channel, cut, e, t)

        m_kkpi = ROOT.RooRealVar(f"m_kkpi_{e}_{t}", f"m_kkpi_{e}_{t}", hist_range_low, hist_range_high)
        dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(m_kkpi), hist)

        voight_mean = ROOT.RooRealVar(f"voight_mean_{e}_{t}", f"voight_mean_{e}_{t}", v_mean, 1.26, 1.3)
        voight_width = ROOT.RooRealVar(f"voight_width_{e}_{t}", f"voight_width_{e}_{t}", v_width, 0.01, 0.05)
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]
        voight_sigma = ROOT.RooRealVar(f"voight_sigma_{e}_{t}", f"voight_sigma_{e}_{t}", e_t_sigma, 0.001, 0.1)

        voight_sigma.setConstant(True)
        voight_width.setConstant(True)
        # voight_mean.setConstant(True)

        voight = ROOT.RooVoigtian(f"voight_{e}_{t}", f"voight_{e}_{t}", m_kkpi, voight_mean, voight_width, voight_sigma)

        ## CHEBYCHEV ##

        bkg_par1 = ROOT.RooRealVar(f"bkg_par1_{e}_{t}", f"bkg_par1_{e}_{t}", -2.0, 2.0)
        bkg_par2 = ROOT.RooRealVar(f"bkg_par2_{e}_{t}", f"bkg_par2_{e}_{t}", -2.0, 2.0)
        bkg_par3 = ROOT.RooRealVar(f"bkg_par3_{e}_{t}", f"bkg_par3_{e}_{t}", -2.0, 2.0)
        bkg_par4 = ROOT.RooRealVar(f"bkg_par4_{e}_{t}", f"bkg_par4_{e}_{t}", -2.0, 2.0)

        bkg = ROOT.RooChebychev(f"bkg_{e}_{t}", f"bkg_{e}_{t}", m_kkpi, ROOT.RooArgList(bkg_par1, bkg_par2, bkg_par3, bkg_par4)) 

        # sig_frac = ROOT.RooRealVar(f"sig_frac_{e}_{t}", f"sig_frac_{e}_{t}", 0.5, 0.0, 1.0)
        n_signal = ROOT.RooRealVar(f"n_signal_{e}_{t}", f"n_signal_{e}_{t}", 100000, 0, 10000000)
        n_bkg = ROOT.RooRealVar(f"n_bkg_{e}_{t}", f"n_bkg_{e}_{t}", 100000, 0, 10000000)

        combined_pdf = ROOT.RooAddPdf(f'combined_pdf_{e}_{t}', f'combined_pdf_{e}_{t}', ROOT.RooArgList(voight, bkg), ROOT.RooArgList(n_signal, n_bkg))
        chi2_var = combined_pdf.createChi2(dh)
        c2 = ROOT.RooChi2Var(f"c2_{e}_{t}", f"c2_{e}_{t}", combined_pdf, dh, ROOT.RooFit.Extended(True), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        minuit = ROOT.RooMinuit(c2)
        minuit.migrad()
        minuit.minos()
        # minuit.hesse()

        fit_result = minuit.save()

        hist_error = c_double(0.0)
        hist_integral = hist.IntegralAndError(hist.FindBin(hist_range_low), hist.FindBin(hist_range_high), hist_error)
        ac_yield = n_signal.getVal()
        ac_yield_error = n_signal.getError()
        cross_section = ct.calculate_crosssection_from_acceptance_corrected_yield(ac_yield, luminosity, ct.T_WIDTH_DICT[t], ct.F1_KKPI_BRANCHING_FRACTION)
        cross_section_error = ct.propogate_error_multiplication(cross_section, [ac_yield, luminosity, ct.F1_KKPI_BRANCHING_FRACTION], [ac_yield_error, math.sqrt(luminosity), ct.F1_KKPI_BRANCHING_FRACTION_ERROR])

        chi2_val = chi2_var.getVal()

        frame = m_kkpi.frame()

        frame = m_kkpi.frame()
        title = get_title_for_plots(channel, e, t)
        frame.SetTitle(title)
        frame.GetXaxis().SetTitle(title.split(" ")[0] + 'GeV')
        frame.GetYaxis().SetTitle(f'Event/10 MeV')

        n_bins = (hist_range_high-hist_range_low)*100
        ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
        chi2ndf = chi2_val / ndf

        dh.plotOn(frame)
        combined_pdf.plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['red'])))
        # pullHist = frame.pullHist()
        combined_pdf.plotOn(frame, ROOT.RooFit.Components(f"bkg_{e}_{t}"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['green'])), ROOT.RooFit.LineStyle(ROOT.kDashed))
        combined_pdf.plotOn(frame, ROOT.RooFit.Components(f"voight_{e}_{t}"), ROOT.RooFit.LineColor(ROOT.TColor.GetColor(ct.COLORBLIND_HEX_DICT['blue'])))

        ks_test_func = combined_pdf.createHistogram(f"ks_test_func_{e}_{t}", m_kkpi, ROOT.RooFit.Binning(1000))
        ks_test_data = dh.createHistogram(f"ks_test_data_{e}_{t}", m_kkpi, ROOT.RooFit.Binning(1000))

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
        t_bin_list.append((ct.T_CUT_DICT[t][0] + ct.T_CUT_DICT[t][1])/2.0)
        t_bin_width_list.append(ct.T_WIDTH_DICT[t]/2.0)
        energy_bin_list.append(e)
        
        frame.Draw()
        c.Update()

    c.SaveAs(f'/work/halld/home/viducic/plots/thesis/cross_section_fits/psac_{channel}_cross_section_fits_beam_{e}.png')
    

# make a pandas datframe out of the lists
value_df = pd.DataFrame({'mean': mean_list, 'mean_error': mean_error_list, 'width': width_list, 'width_error': width_error_list, 'chi2ndf': chi2ndf_list, 'ks_test': ks_test_list, 'yield': ac_yield_list, 'yield_error': yield_error_list, 'cross_section': cross_section_list, 'cross_section_error': cross_section_error_list, 't_bin_middle': t_bin_list, 't_bin_width': t_bin_width_list, 'beam_energy': energy_bin_list})
value_df.to_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/cross_section_values_psac.csv', index=False)

input('Press enter to exit')

