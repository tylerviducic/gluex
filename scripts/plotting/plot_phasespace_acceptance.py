# script to plot phasespace acceptance

import ROOT
from common_analysis_tools import *

channel = 'pipkmks'
cut = 'all'

hist_list = []
canvas_list = []
hist_7gev_list = []
hist_8gev_list = []

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

        lumi_spring = get_luminosity('spring', beam_low=e-0.5, beam_high=e+0.5)
        lumi_fall = get_luminosity('fall',beam_low=e-0.5, beam_high=e+0.5)
        lumi_2017 = get_luminosity('2017', beam_low=e-0.5, beam_high=e+0.5)

        total_lumi = lumi_spring + lumi_fall + lumi_2017

        acceptance_spring = phasespace_recon_hist_spring.Clone(f'acceptance_spring_{e}_{t}')
        acceptance_spring.Sumw2()
        acceptance_spring.Divide(phasespace_thrown_hist_spring)

        acceptance_fall = phasespace_recon_hist_fall.Clone(f'acceptance_fall_{e}_{t}')
        acceptance_fall.Sumw2()
        acceptance_fall.Divide(phasespace_thrown_hist_fall)

        acceptance_2017 = phasespace_recon_hist_2017.Clone(f'acceptance_2017_{e}_{t}')
        acceptance_2017.Sumw2()
        acceptance_2017.Divide(phasespace_thrown_hist_2017)

        if e == 7:
            hist_7gev_list.append((acceptance_spring, acceptance_fall, acceptance_2017))
        if e == 8:
            hist_8gev_list.append((acceptance_spring, acceptance_fall, acceptance_2017))


        acceptance = acceptance_spring.Clone(f'acceptance_{e}_{t}')
        acceptance.Scale(lumi_spring/total_lumi)
        acceptance.Add(acceptance_fall, lumi_fall/total_lumi)
        acceptance.Add(acceptance_2017, lumi_2017/total_lumi)

        acceptance.SetTitle(f'Acceptance for E(y) =  {e} GeV, t = {t_bin_dict[t]} GeV^2')
        acceptance.GetXaxis().SetTitle('M_{K^{+}K^{-}#pi^{+}} (GeV)')
        acceptance.GetYaxis().SetTitle('Acceptance')

        hist_list.append(acceptance)


        canvas_list[e-7].cd(t)
        hist_list[-1].Draw()
    
    canvas_list[e-7].Update()
    canvas_list[e-7].SaveAs(f'/work/halld/home/viducic/plots/cross_section/{channel}_phasespace_acceptance_{e}.png')

c1 = ROOT.TCanvas('c1', 'c1', 1200, 900)
c1.Divide(4, 2)
for k in range(1, 8):
    l = k-1
    c1.cd(k)
    hist_list[l+21].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['purple']))
    hist_list[l+21].Draw()
    hist_list[l].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
    hist_list[l].Draw('same')
    hist_list[l+7].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
    hist_list[l+7].Draw('same')
    hist_list[l+14].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
    hist_list[l+14].Draw('same')
c1.Update()

c2 = ROOT.TCanvas('c2', 'c2', 1200, 900)
c2.Divide(4, 2)
for m in range(1, 8):
    c2.cd(m)
    # hist_7gev_list[m-1][1].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
    # hist_7gev_list[m-1][1].Draw()
    # hist_7gev_list[m-1][2].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
    # hist_7gev_list[m-1][2].Draw('same')
    # hist_7gev_list[m-1][0].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
    # hist_7gev_list[m-1][0].Draw('same')
    hist_8gev_list[m-1][1].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['blue']))
    hist_8gev_list[m-1][1].Draw()
    hist_8gev_list[m-1][2].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['green']))
    hist_8gev_list[m-1][2].Draw('same')
    hist_8gev_list[m-1][0].SetLineColor(ROOT.TColor.GetColor(colorblind_hex_dict['red']))
    hist_8gev_list[m-1][0].Draw('same')


# leg_7gev = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
# leg_7gev.AddEntry(hist_7gev_list[0][0], 'Spring', 'l')
# leg_7gev.AddEntry(hist_7gev_list[0][1], 'Fall', 'l')
# leg_7gev.AddEntry(hist_7gev_list[0][2], '2017', 'l')
leg_8gev = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
leg_8gev.AddEntry(hist_8gev_list[0][0], 'Spring', 'l')
leg_8gev.AddEntry(hist_8gev_list[0][1], 'Fall', 'l')
leg_8gev.AddEntry(hist_8gev_list[0][2], '2017', 'l')
c2.cd(1)
# leg_7gev.Draw()
leg_8gev.Draw()
c2.cd(5)
# leg_7gev.Draw()
leg_8gev.Draw()
c2.Update()






input('Press any key to continue...')




