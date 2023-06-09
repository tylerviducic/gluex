# script to plot all gluex1 data just like the acceptance

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
        data_hist_spring = get_data_hist(channel, 'spring', cut, e, t)
        data_hist_spring.GetXaxis().SetRangeUser(1.2, 1.5)
        data_hist_fall = get_data_hist(channel, 'fall', cut, e, t)
        data_hist_fall.GetXaxis().SetRangeUser(1.2, 1.5)
        data_hist_2017 = get_data_hist(channel, '2017', cut, e, t)
        data_hist_2017.GetXaxis().SetRangeUser(1.2, 1.5)

        gluex1_hist = data_hist_spring.Clone(f'gluex1_data_{e}_{t}')
        gluex1_hist.Add(data_hist_fall)
        gluex1_hist.Add(data_hist_2017)

        gluex1_hist.SetTitle(f'Gluex-I Data for for E(y) =  {e} GeV, t = {t_bin_dict[t]} GeV^2')
        gluex1_hist.GetXaxis().SetTitle('M_{K^{+}K^{-}#pi^{+}} (GeV)')
        gluex1_hist.GetYaxis().SetTitle('counts/10 MeV')

        hist_list.append(gluex1_hist)


        canvas_list[e-7].cd(t)
        hist_list[-1].Draw()
    
    canvas_list[e-7].Update()
    canvas_list[e-7].SaveAs(f'/work/halld/home/viducic/plots/cross_section/{channel}_gluex1_data_{e}.png')

input('Press any key to continue...')