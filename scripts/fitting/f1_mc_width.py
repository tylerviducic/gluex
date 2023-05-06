# get f1 width form f1 sample for use in yield extracton 

import ROOT

def bw(x, par):
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])

c1 = ROOT.TCanvas("c1", "c1", 800, 600)

mc_filename = '/Users/tylerviducic/research/gluex/selector_output/mc_pipkmks_recon_spring.root'

hist_name = 'IM_KsKmPip'
root_file = ROOT.TFile(mc_filename)
hist = root_file.Get(hist_name)
hist.Draw()

func = ROOT.TF1("func", bw, 1.15, 1.4, 3)
func.SetParameter(0, 7500)
func.SetParameter(1, 1.285)
func.SetParameter(2, 0.04)

hist.Fit(func, "WLRN")
func.Draw("same")
c1.Update()