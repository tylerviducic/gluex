# get width of f1(1285) from my data in GlueX

import ROOT
import math

hbarc = 0.1973269631 # GeV fm   

proton = 0.93827
kaon = 0.49367
pion = 0.13957
k_short = 0.49765

def breakupMomentum(s, m1, m2):
    if(s < ((m1 + m2) ** 2)):
        return 0
    result = 0.5 * math.sqrt((s - ((m1 + m2) ** 2)) * (s - ((m1 - m2) ** 2)) / s)
    return result


def blattWeisskopf(L, p):
    z = (p/hbarc) ** 2 
    if L == 0:
        return 1
    elif L == 1:
        return math.sqrt(2 * z / (z + 1))
    elif L == 2:
        return math.sqrt(13*z*z/((z-3)**2 + 9*z))
    return 0

def relBreitWigner(x, par):
    intermediate_particle = kaon + pion
    q0 = breakupMomentum(par[1] * par[1], intermediate_particle, k_short)
    q = breakupMomentum(x[0] * x[0], intermediate_particle, k_short)

    spin = 0

    gamma = par[2] * par[1]/x[0] * q/q0 *  math.pow(blattWeisskopf(spin, q) / blattWeisskopf(spin, q0), 2)
    
    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma*gamma # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma*gamma)/(par[1]*par[1]))
    return par[0]*arg1*arg2/(arg3 + arg4)

def bw_1420(x, par):
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])

def full_fit(x, par):
    q0_1285 = breakupMomentum(par[1] * par[1], kaon, kaon)
    q_1285 = breakupMomentum(x[0] * x[0], kaon, kaon)

    q0_1420 = breakupMomentum(par[4] * par[4], kaon, kaon)
    q_1420 = breakupMomentum(x[0] * x[0], kaon, kaon)

    spin = 0

    gamma_1285 = par[2] * par[1]/x[0] * q_1285/q0_1285 *  math.pow(blattWeisskopf(spin, q_1285) / blattWeisskopf(spin, q0_1285), 2)
    gamma_1420 = par[5] * par[4]/x[0] * q_1420/q0_1420 *  math.pow(blattWeisskopf(spin, q_1420) / blattWeisskopf(spin, q0_1420), 2)

    arg1 = 14.0/22.0
    arg2 = par[1]*par[1]*gamma_1285*gamma_1285 # Gamma0=par[2]  M0=par[1]
    arg3 = ((x[0]*x[0]) - (par[1]*par[1]))*((x[0]*x[0]) - (par[1]*par[1]))
    arg4 = x[0]*x[0]*x[0]*x[0]*((gamma_1285*gamma_1285)/(par[1]*par[1]))

    arg5 = 14.0/22.0
    arg6 = par[4]*par[4]*gamma_1420*gamma_1420 # Gamma0=par[2]  M0=par[1]
    arg7 = ((x[0]*x[0]) - (par[4]*par[4]))*((x[0]*x[0]) - (par[4]*par[4]))
    arg8 = x[0]*x[0]*x[0]*x[0]*((gamma_1420*gamma_1420)/(par[4]*par[4]))


    # bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    bkg = par[6] + par[7] * x[0] + par[8] * x[0] * x[0] + par[9] * x[0] * x[0] * x[0] + par[10] * x[0] * x[0] * x[0] * x[0]
    # bkg = par[6] + par[7] * x[0]

    # bkg = ROOT.TMath.Exp(par[6] + par[7] * x[0] + par[8] * x[0] * x[0])
    bw1420 = par[3] * ROOT.TMath.BreitWigner(x[0], par[4], par[5])
    return par[0]*arg1*arg2/(arg3 + arg4) + par[3]*arg5*arg6/(arg7 + arg8) + bkg
    # return par[0]*arg1*arg2/(arg3 + arg4) + bw1420 + bkg

def bkg(x, par):
    # return par[0] + par[1] * x[0]
    # return ROOT.TMath.Exp(par[0] + par[1] * x[0] + par[2] * x[0] * x[0])
    return par[0] + par[1] * x[0] + par[2] * x[0] * x[0] + par[3] * x[0] * x[0] * x[0] + par[4] * x[0] * x[0] * x[0] * x[0]

c1 = ROOT.TCanvas("c1", "c1", 800, 600)

data_filename = '/Users/tylerviducic/research/gluex/selector_output/f1_width.root'

hist_name = 'IM_KsKmPip'
root_file = ROOT.TFile(data_filename)
hist = root_file.Get(hist_name)
hist.Draw()

func = ROOT.TF1("func", full_fit, 1.15, 1.6, 11)
func.SetParameter(0, 2000)
func.FixParameter(1, 1.285)
func.FixParameter(2, 0.023)
func.FixParameter(3, 5500)
func.FixParameter(4, 1.426)
func.FixParameter(5, 0.054)
func.SetParameter(6, 1000)
func.SetParameter(7, -200)
func.SetParameter(8, 4000)
func.SetParameter(9, -1000)
func.SetParameter(10, 350)


hist.Fit(func) # "WLRN"

f1_1285 = ROOT.TF1("f1_1285", relBreitWigner, 1.1, 2.0, 3)
f1_1285.SetParameters(func.GetParameter(0), func.GetParameter(1), func.GetParameter(2))
f1_1285.SetLineColor(1)

f1_1420 = ROOT.TF1("f1_1420", relBreitWigner, 1.1, 2.0, 3)
f1_1420.SetParameters(func.GetParameter(3), func.GetParameter(4), func.GetParameter(5))
f1_1420.SetLineColor(3)

background_func = ROOT.TF1("background_1285", bkg, 1.1, 2.0, 4)
background_func.SetParameters(func.GetParameter(6), func.GetParameter(7), func.GetParameter(8), func.GetParameter(9), func.GetParameter(10))
background_func.SetLineColor(4)

func.Draw("same")
f1_1285.Draw("same")
f1_1420.Draw("same")
background_func.Draw("same")


