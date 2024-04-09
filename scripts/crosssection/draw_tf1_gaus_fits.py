import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd
import my_library.gluex_style

# ROOT.Math.IntegratorOneDimOptions.SetDefaultAbsTolerance(1.E-3)
# ROOT.Math.IntegratorOneDimOptions.SetDefaultRelTolerance(1.E-3)

channel = 'pipkmks'
# channel = 'pimkpks'
cut = 'all'

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetLineStyleString(7,"24 8")
ROOT.gStyle.SetLineStyleString(8,"8 24")

if channel == 'pipkmks' :
    v_mean = constants.F1_PIPKMKS_VOIGHT_MEAN
    v_width = constants.F1_PIPKMKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet
    f1_color = ROOT.kBlue
    # background_color = ROOT.kOrange
    background_color = total_fit_color
    hist_title = 'K^{-}K_{s}#pi^{+}'
    gaus_mean = constants.F1_PIPKMKS_GAUS_MEAN
    gaus_width = constants.F1_PIPKMKS_GAUS_WIDTH
elif channel == 'pimkpks' :
    v_mean = constants.F1_PIMKPKS_VOIGHT_MEAN
    v_width = constants.F1_PIMKPKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet +9
    f1_color = ROOT.kRed
    # background_color = ROOT.kTeal-5
    background_color = total_fit_color
    hist_title = 'K^{+}K_{s}#pi^{-}'
    gaus_mean = constants.F1_PIMKPKS_GAUS_MEAN
    gaus_width = constants.F1_PIMKPKS_GAUS_WIDTH

df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/binned_e_t_f1_mc_width.csv') 
yield_df = pd.read_csv(f'/work/halld/home/viducic/data/fit_params/{channel}/tf1_gaus_yield_values.csv')


parameter_names = ['voight amplitude', 'voight mean', 'voight sigma', 'voight width', 'gaus amplitude', 'gaus mean', 'gaus width', 'bkg par1', 'bkg par2', 'bkg par3']

fit_low, fit_high = 1.16, 1.63

c = ROOT.TCanvas('c', 'c', 1000, 1000)

for e in range(8, 12):
    c.Clear()
    c.Divide(4, 2)
    hists=[]
    funcs = []
    bkgs = []
    voigts = []
    gauses = []

    initial_guesses = {
        0: 5, # voight amplitude
        1: v_mean, # voight mean
        3: v_width, # voight width
        4: 15, # gaus amplitude
        5: gaus_mean, # gaus mean
        6: gaus_width, # gaus width
        7: -100, # bkg par1
        8: 100, # bkg par2
        9: 1 # bkg par3
    }
    
    for t in range(1, 8):
        cor_hist = ct.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist = ct.remove_zero_datapoints(cor_hist)

        hist.GetXaxis().SetRangeUser(1.1, 1.65)
        hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)

        hist.GetXaxis().SetTitle(f'M({hist_title}) [GeV]')
        # hist.GetXaxis().SetTitleSize(0.055)
        hist.GetYaxis().SetTitle('Counts/10 MeV')
        # hist.SetTitleSize(0.055)
        hist.SetTitle("")
        hist.SetMarkerStyle(20)
        hist.SetLineColor(ROOT.kBlack)


        hists.append(hist)


        func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + gaus(4) + pol2(7)', fit_low, fit_high)        
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]

        func.SetParameter(0, initial_guesses[0]) # voight amplitude
        func.SetParLimits(0, 0., 100000)
        func.FixParameter(1, initial_guesses[1]) # voight mean
        func.FixParameter(2, e_t_sigma)
        func.FixParameter(3, initial_guesses[3]) # voight width
        func.SetParameter(4, initial_guesses[4]) # gaus amplitude
        func.SetParLimits(4, 0., 100000)
        func.FixParameter(5, initial_guesses[5]) # gaus mean 
        func.FixParameter(6, initial_guesses[6]) # gaus width

        func.SetParameter(7, initial_guesses[7]) # bkg par1
        func.SetParameter(8, initial_guesses[8]) # bkg par2
        func.SetParameter(9, initial_guesses[9]) # bkg par3


        func.SetParNames(parameter_names[0], parameter_names[1], parameter_names[2], parameter_names[3], parameter_names[4], parameter_names[5], parameter_names[6], parameter_names[7], parameter_names[8], parameter_names[9])

        result = hist.Fit(func, 'SRBNQ')
        
        func.SetLineColor(f1_color)

        voight = ROOT.TF1(f'voight_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', fit_low, fit_high)
        voight.SetLineColor(ROOT.kBlack)
        voight.SetFillColor(f1_color)
        voight.SetFillStyle(1001)
        gaus = ROOT.TF1('gaus', 'gaus(0)', fit_low, fit_high)
        gaus.SetLineColor(background_color)
        gaus.SetLineStyle(7)
        bkg = ROOT.TF1('bkg', 'pol2(0)', fit_low, fit_high)
        # bkg = ROOT.TF1('bkg', '[0] + [1]*(x+1.15) + [2]*(x-1.15)*(x-1.15)', fit_low, fit_high)
        bkg.SetLineColor(background_color)
        bkg.SetLineStyle(8)

        initial_guesses[0] = func.GetParameter(0)
        initial_guesses[4] = func.GetParameter(4)
        initial_guesses[5] = func.GetParameter(5)
        initial_guesses[6] = func.GetParameter(6)
        initial_guesses[7] = func.GetParameter(7)
        initial_guesses[8] = func.GetParameter(8)
        initial_guesses[9] = func.GetParameter(9)


        voight.SetParameter(0, func.GetParameter(0))
        voight.SetParError(0, func.GetParError(0))
        voight.SetParameter(1, func.GetParameter(1))
        voight.SetParameter(2, func.GetParameter(2))
        voight.SetParameter(3, func.GetParameter(3))
        gaus.SetParameter(0, func.GetParameter(4))
        gaus.SetParameter(1, func.GetParameter(5))
        gaus.SetParameter(2, func.GetParameter(6))
        bkg.SetParameter(0, func.GetParameter(7))
        bkg.SetParameter(1, func.GetParameter(8))
        bkg.SetParameter(2, func.GetParameter(9))

        chi2_per_ndf = func.GetChisquare()/func.GetNDF()

        funcs.append(func)
        voigts.append(voight)
        gauses.append(gaus)
        bkgs.append(bkg)

        hists[t-1].Draw("E1")
        funcs[t-1].Draw('same')
        voigts[t-1].Draw('same')
        bkgs[t-1].Draw('same')
        gauses[t-1].Draw('same')

        legend = ROOT.TLegend(0.13, 0.525, 0.3, 0.7)
        legend.AddEntry(func, "Total Fit", "l")
        legend.AddEntry(voight, "f_{1}(1285) Signal", "lf")
        legend.AddEntry(gaus, "f_{1}(1420) Tail", "l")
        legend.AddEntry(bkg, "Background", "l")
        legend.Draw()

        et_row = yield_df.loc[(yield_df['e']==e) & (yield_df['t']==t)]
        f1_yield = et_row['yield'].values[0]
        f1_yield_err = et_row['yield_err'].values[0]

        t_middle = constants.T_CUT_DICT[t][0] + constants.T_WIDTH_DICT[t]/2

        fit_params = ROOT.TLatex()
        fit_params.SetTextSize(0.04)
        fit_params.DrawLatexNDC(0.15, 0.9, "E_{#gamma} = " + str(e) + " GeV")
        fit_params.DrawLatexNDC(0.15, 0.85, f"|t| = {t_middle:0.3f}" + " GeV^{2}")
        fit_params.DrawLatexNDC(0.15, 0.8, "Yield = " + '{:.2f}'.format(f1_yield) + " #pm " + '{:.2f}'.format(f1_yield_err) + " Events")
        fit_params.DrawLatexNDC(0.15, 0.75, "#chi^{2}/ndf = " + '{:.2f}'.format(chi2_per_ndf))

        c.SaveAs(f'/work/halld/home/viducic/scripts/crosssection/plots/pol2_gaus_{channel}_e{e}_t{t}_fit.png')
