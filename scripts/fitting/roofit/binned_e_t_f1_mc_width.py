# fit KKPi in E and t bins for cross section to get the width used in the fits to data

import ROOT 
from common_analysis_tools import *

channel = 'pipkmks'
cut = 'all'

beam_energy = 9

chi2_ndf_list = []

c = ROOT.TCanvas()
c.Divide(3, 3)

for i in range(1, 8):
    c.cd(i)
    ac_signal_hist_total = accepptance_correct_all_gluex1_kkpi_signal(channel, cut, beam_energy, i)

    m_kkpi = ROOT.RooRealVar('m_kkpi', 'm_kkpi', 1.2, 1.5)
    mean = ROOT.RooRealVar('mean', 'mean', 1.285, 1.2, 1.3)
    width = ROOT.RooRealVar('width', 'width', 0.023, 0.001, 0.1)
    sigma = ROOT.RooRealVar('sigma', 'sigma', 0.025, 0.001, 0.1)

    width.setConstant(ROOT.kTRUE)
    mean.setConstant(ROOT.kTRUE)

    dh = ROOT.RooDataHist('dh', 'dh', ROOT.RooArgList(m_kkpi), ac_signal_hist_total)

    func = ROOT.RooVoigtian('func', 'func', m_kkpi, mean, width, sigma)
    chi2_var = func.createChi2(dh)
    fit_result = func.chi2FitTo(dh, ROOT.RooFit.Save())

    frame = m_kkpi.frame()
    dh.plotOn(frame)
    func.plotOn(frame)
    npar = func.getParameters(dh).selectByAttrib("Constant", False).getSize()
    chi2ndf = frame.chiSquare(npar)
    chi2_ndf_list.append(chi2ndf)

    frame.Draw()

for j in range(len(chi2_ndf_list)):
    print(f'chi2/ndf for bin {j+1}: {chi2_ndf_list[j]}')

input('Press enter to continue...')


    
