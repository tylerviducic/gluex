# script to plot phasespace acceptance

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'
cut = 'all'

hist_list = []
canvas_list = []

for e in range(7, 11):
    c = ROOT.TCanvas(f'canvas_{e}', f'canvas_{e}', 1200, 900)
    c.Divide(4, 2)
    canvas_list.append(c)

    for t in range(1, 8):
        phasespace_recon_hist_spring = get_phasespace_recon_hist(channel, 'spring', cut, e, t)
        phasespace_recon_hist_spring.GetXaxis().SetRangeUser(1.2, 1.5)
        phasespace_recon_hist_fall = get_phasespace_recon_hist(channel, 'fall', cut, e, t)
        phasespace_recon_hist_fall.GetXaxis().SetRangeUser(1.2, 1.5)
        phasespace_recon_hist_2017 = get_phasespace_recon_hist(channel, '2017', cut, e, t)
        phasespace_recon_hist_2017.GetXaxis().SetRangeUser(1.2, 1.5)

        phasespace_thrown_hist_spring = get_phasespace_thrown_hist(channel, 'spring', e, t)
        phasespace_thrown_hist_spring.GetXaxis().SetRangeUser(1.2, 1.5)
        phasespace_thrown_hist_fall = get_phasespace_thrown_hist(channel, 'fall', e, t)
        phasespace_thrown_hist_fall.GetXaxis().SetRangeUser(1.2, 1.5)
        phasespace_thrown_hist_2017 = get_phasespace_thrown_hist(channel, '2017', e, t)
        phasespace_thrown_hist_2017.GetXaxis().SetRangeUser(1.2, 1.5)

        lumi_spring = get_luminosity('spring')
        lumi_fall = get_luminosity('fall')
        lumi_2017 = get_luminosity('2017')

        acceptance_spring = phasespace_recon_hist_spring.Clone(f'acceptance_spring_{e}_{t}')
        acceptance_spring.Divide(phasespace_thrown_hist_spring)

        acceptance_fall = phasespace_recon_hist_fall.Clone(f'acceptance_fall_{e}_{t}')
        acceptance_fall.Divide(phasespace_thrown_hist_fall)

        acceptance_2017 = phasespace_recon_hist_2017.Clone(f'acceptance_2017_{e}_{t}')
        acceptance_2017.Divide(phasespace_thrown_hist_2017)

        acceptance = acceptance_spring.Clone(f'acceptance_{e}_{t}')
        acceptance.Add(acceptance_fall, lumi_fall/lumi_spring)
        acceptance.Add(acceptance_2017, lumi_2017/lumi_spring)

        acceptance.SetTitle(f'Acceptance for E(y) =  {e} GeV, t = {t_bin_dict[t]} GeV^2')
        acceptance.GetXaxis().SetTitle('M_{K^{+}K^{-}#pi^{+}} (GeV)')
        acceptance.GetYaxis().SetTitle('Acceptance')

        hist_list.append(acceptance)


        canvas_list[e-7].cd(t)
        hist_list[-1].Draw()
    
    canvas_list[e-7].Update()
    canvas_list[e-7].SaveAs(f'/work/halld/home/viducic/plots/cross_section/{channel}_phasespace_acceptance_{e}.png')

input('Press any key to continue...')




