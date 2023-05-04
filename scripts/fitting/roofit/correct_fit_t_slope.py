# script to acceptance correct and fit integrated tslope of pipkmkms and pimkpks so generate better signal

import ROOT
import math

run_period = 'fall'
run_dict = {'fall': '2018_fall',
            'spring': '2018_spring',
            '2017': '2017'}

data_filename = f'/work/halld/home/viducic/selector_output/f1_flat/pipkmks_filtered_{run_dict[run_period]}.root'
mc_filename = f'/work/halld/home/viducic/selector_output/f1_flat/mc_pipkmks_filtered_{run_dict[run_period]}.root'
thrown_filename = f'/work/halld/home/viducic/selector_output/f1_flat/mc_pipkmks_thrown_flat_result_{run_dict[run_period]}.root'

data_treename = 'pipkmks_filtered_2018_fall'
mc_treename = 'mc_pipkmks_filtered_2018_fall'

# define filters
beam_range = 'e_beam > 6.50000000000 && e_beam <= 10.5'
t_range = 'mand_t >= 0.2 && mand_t <= 1.9'
f1_region = 'pipkmks_m > 1.255 && pipkmks_m < 1.311'

thrown_file = ROOT.TFile(thrown_filename, 'READ')


# tslope hist name for thrown is called tslope
# hist goes 0.0-2.0 w/ 100 bins
# beam range is beam > 6.5 && beam < 10.5
# t range is t < 1.9
# data and recon MC is not filtered for t or beam energy. 
# fit from 0.2-1.9
# must cut on signal region


#TODO add t and beam energy cuts to data and recon MC wrt inclusivity 

data_rdf = ROOT.RDataFrame(data_treename, data_filename)
mc_rdf = ROOT.RDataFrame(mc_treename, mc_filename)

mc_hist = mc_rdf.Filter(beam_range).Filter(t_range).Filter(f1_region).Histo1D(('mc_t', 'mc_t', 100, 0.0, 2.0), 'mand_t')
data_hist = data_rdf.Filter(beam_range).Filter(t_range).Filter(f1_region).Histo1D(('data_t', 'data_t', 100, 0.0, 2.0), 'mand_t')
thrown_hist = thrown_file.Get('tslope')

acceptance_hist = mc_hist.Clone()
acceptance_hist.Divide(thrown_hist)

data_hist.Divide(acceptance_hist)
# data_hist.Draw()
# print(data_hist)
# input('press enter to continue')
corrected_data = data_hist.Clone()
corrected_data.Sumw2()


t = ROOT.RooRealVar('t', 't', 0.2, 1.8)
b = ROOT.RooRealVar('b', 'b', -3.0, -4.0, -1.0)
# b.setConstant(True)

data_rdh = ROOT.RooDataHist("data_rdh", "data_rdh", ROOT.RooArgList(t), corrected_data)

func = ROOT.RooExponential('func', 'func', t, b)
func.fitTo(data_rdh, ROOT.RooFit.SumW2Error(True))

frame = t.frame()
data_rdh.plotOn(frame)
func.plotOn(frame)

frame.Draw()
input('press enter to continue')


