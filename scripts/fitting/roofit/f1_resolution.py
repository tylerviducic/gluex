# script to get resolution of f1 to evaluate effectiveness of potential Ks constraint

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'

def get_acceptance_corrected_signal_mc(channel, run_period, n_bins):
    file_and_tree = get_flat_file_and_tree(channel, run_period, 'signal')
    signal_df = ROOT.RDataFrame(file_and_tree[1], file_and_tree[0]) 
    recon_phasespace_file_and_tree = get_flat_file_and_tree(channel, run_period, 'phasespace')
    thrown_phasespace_file_and_tree = get_flat_thrown_file_and_tree(channel, run_period, phasespace=True)
    recon_df = ROOT.RDataFrame(recon_phasespace_file_and_tree[1], recon_phasespace_file_and_tree[0])
    thrown_file = ROOT.TFile.Open(thrown_phasespace_file_and_tree[0], 'READ')
    print(thrown_phasespace_file_and_tree[0])

    signal_df = signal_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)
    # reduce signal_df to 10% of it's size
    signal_df = signal_df.Range(0, int(signal_df.Count().GetValue() / 250))
    recon_df = recon_df.Filter(KSTAR_ALL_CUT).Filter(T_RANGE).Filter(BEAM_RANGE)

    signal_hist = signal_df.Histo1D((f'data_hist_{run_period}', f'data_hist_{run_period}', n_bins, 1.2, 1.5), 'pipkmks_m').GetValue()
    recon_hist = recon_df.Histo1D((f'recon_hist_{run_period}', f'recon_hist_{run_period}', n_bins, 1.2, 1.5), 'pipkmks_m').GetValue()
    thrown_hist_name = channel + f'_f1_res_{n_bins};1'
    thrown_hist = thrown_file.Get(thrown_hist_name)

    signal_hist.Sumw2()
    recon_hist.Sumw2()
    thrown_hist.Sumw2()

    acceptance_hist = recon_hist.Clone()
    acceptance_hist.Divide(thrown_hist)
        
    ac_signal_hist = signal_hist.Clone()
    ac_signal_hist.Divide(acceptance_hist)

    ac_signal_hist.SetDirectory(0)

    # c = ROOT.TCanvas()
    # c.Divide(3, 1)
    # c.cd(1)
    # signal_hist.Draw()
    # # c.cd(2)
    # # recon_hist.Draw()
    # c.cd(2)
    # acceptance_hist.Draw()
    # c.cd(3)
    # ac_signal_hist.Draw()
    # c.Update()
    # input('press enter to continue')
    # c.Clear()
    return ac_signal_hist

n_bins = 30
ac_signal_hist_spring = get_acceptance_corrected_signal_mc(channel, 'spring', n_bins)
ac_signal_hist_fall = get_acceptance_corrected_signal_mc(channel, 'fall', n_bins)
ac_signal_hist_2017 = get_acceptance_corrected_signal_mc(channel, '2017', n_bins)

lumi_spring = get_luminosity('spring')
lumi_fall = get_luminosity('fall')
lumi_2017 = get_luminosity('2017')
lumi_total = lumi_spring + lumi_fall + lumi_2017

ac_signal_hist_total = ac_signal_hist_spring.Clone()
ac_signal_hist_total.Add(ac_signal_hist_fall, lumi_fall / lumi_spring)
ac_signal_hist_total.Add(ac_signal_hist_2017, lumi_2017 / lumi_spring)

for i in range(1, ac_signal_hist_total.GetNbinsX() + 1):
    my_error = propogate_error_addition([ac_signal_hist_spring.GetBinError(i), ac_signal_hist_fall.GetBinError(i), ac_signal_hist_2017.GetBinError(i)])
    sumw2_error = ac_signal_hist_total.GetBinError(i)
    print(f'bin {i}: my_error = {my_error}, sumw2_error = {sumw2_error}')

m_kkpi = ROOT.RooRealVar("m_kkpi", "m_kkpi", 1.2, 1.5)
range_min = 1.2
range_max = 1.4
m_kkpi.setRange("fit_range", range_min, range_max)
mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.2, 1.3)
width = ROOT.RooRealVar('width', 'width', 0.023, 0.001, 0.1)
sigma = ROOT.RooRealVar('sigma', 'sigma', 0.025, 0.001, 0.1)

width.setConstant(ROOT.kTRUE)
mean.setConstant(ROOT.kTRUE)


dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), ac_signal_hist_total)

func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
chi2_var = func.createChi2(dh)
fit_result = func.chi2FitTo(dh, ROOT.RooFit.Save(), ROOT.RooFit.Range("fit_range"))
# fit_result = func.chi2FitTo(dh, ROOT.RooFit.Save())

chi2_val = chi2_var.getVal()
n_bins = ac_signal_hist_total.GetNbinsX()
print("n_bins = " + str(n_bins))
ndf = n_bins - (fit_result.floatParsFinal().getSize() - fit_result.constPars().getSize())
chi2_per_ndf = chi2_val / ndf
print("chi2 = " + str(chi2_val))
print("ndf = " + str(ndf))
print("chi2/ndf = " + str(chi2_per_ndf))


frame = m_kkpi.frame()
dh.plotOn(frame)
func.plotOn(frame, ROOT.RooFit.Range("fit_range"))
# func.plotOn(frame)
pullHist = frame.pullHist()
npar = func.getParameters(dh).selectByAttrib("Constant", False).getSize()
chi2ndf = frame.chiSquare(npar)

frame.Draw()

input('press enter to continue')

pullDist = ROOT.TH1I("pullDist", "pullDist", 3, 0, 3)
for i in range(0, pullHist.GetN()):
    pullDist.Fill(pullHist.GetY()[i])

c = ROOT.TCanvas("c", "c", 800, 600)
c.Divide(1, 2)
c.cd(1)
pullHist.Draw("AP")

y = 0.0

line= ROOT.TLine(frame.GetXaxis().GetXmin(), y, frame.GetXaxis().GetXmax(), y)
line.SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw("same")
c.cd(2)
pullDist.Draw()
c.Update()

print(f'chi2ndf: {chi2ndf}')
input('press enter to continue')
