import ROOT
import my_library.common_analysis_tools as ct
import my_library.constants as constants
import pandas as pd

# channel = 'pipkmks'
channel = 'pimkpks'
cut = 'all'

if channel == 'pipkmks' :
    v_mean = constants.F1_PIPKMKS_VOIGHT_MEAN
    v_width = constants.F1_PIPKMKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet
    f1_color = ROOT.kBlue
    # background_color = ROOT.kOrange
    background_color = total_fit_color
elif channel == 'pimkpks' :
    v_mean = constants.F1_PIMKPKS_VOIGHT_MEAN
    v_width = constants.F1_PIMKPKS_VOIGHT_WIDTH
    total_fit_color = ROOT.kViolet +9
    f1_color = ROOT.kRed
    # background_color = ROOT.kTeal-5
    background_color = total_fit_color

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

c = ROOT.TCanvas('c', 'c', 1000, 1000)

for e in range(8, 12):
    c.Clear()
    c.Divide(4, 2)
    luminosity = ct.get_luminosity_gluex_1(e-0.5, e+0.5)/1000
    hists=[]
    funcs = []
    bkgs = []
    voigts = []

    initial_guesses = {
        0: 10,
        1: v_mean, 
        3: v_width,
        4: -1000,
        5: 9000
    }
    
    for t in range(1, 8):
        c.cd(t)
        cor_hist = ct.get_binned_gluex1_kstar_corrected_data(channel, e, t)
        hist = ct.remove_zero_datapoints(cor_hist)
        hist.GetXaxis().SetRangeUser(1.2, 1.5)
        hist.GetYaxis().SetRangeUser(0, hist.GetMaximum()*1.2)
        hists.append(hist)


        func = ROOT.TF1(f'func_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3]) + pol1(4)', 1.2, 1.5)
        
        e_t_sigma = df.loc[(df['energy']==e) & (df['t_bin']==t)]['sigma'].values[0]

        func.SetParameter(0, initial_guesses[0])
        func.SetParLimits(0, 1, 1000)
        func.FixParameter(1, initial_guesses[1])
        # func.SetParLimits(1, 1.26, 1.3)
        func.FixParameter(2, e_t_sigma)
        func.FixParameter(3, initial_guesses[3])
        # func.SetParLimits(3, 0.005, 0.05)
        func.SetParameter(4, initial_guesses[4])
        func.SetParameter(5, initial_guesses[5])

        hist.Fit(func, 'RB')
        func.SetLineColor(total_fit_color)

        voight = ROOT.TF1(f'voight_{e}_{t}', '[0]*TMath::Voigt(x-[1], [2], [3])', 1.2, 1.5)
        voight.SetLineColor(ROOT.kBlack)
        voight.SetFillColor(f1_color)
        voight.SetFillStyle(1001)
        bkg = ROOT.TF1('bkg', 'pol1(0)', 1.2, 1.5)
        bkg.SetLineColor(background_color)
        bkg.SetLineStyle(2)

        initial_guesses[4] = func.GetParameter(4)
        initial_guesses[5] = func.GetParameter(5)

        voight.SetParameter(0, func.GetParameter(0))
        voight.SetParameter(1, func.GetParameter(1))
        voight.SetParameter(2, func.GetParameter(2))
        voight.SetParameter(3, func.GetParameter(3))
        bkg.SetParameter(0, func.GetParameter(4))
        bkg.SetParameter(1, func.GetParameter(5))

        funcs.append(func)
        voigts.append(voight)
        bkgs.append(bkg)

        hists[t-1].Draw()
        funcs[t-1].Draw('same')
        voigts[t-1].Draw('same')
        bkgs[t-1].Draw('same')

        c.Update()

    c.SaveAs(f'/work/halld/home/viducic/scripts/crosssection/plots/{channel}_e{e}_t{t}_fit.png')
