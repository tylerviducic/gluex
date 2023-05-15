# script to test width of mx2_all distribution


"""
An effective resolution is computed as σ = f σ1 + (1 − f )σ2 where f is the fraction 
of the first Gaussian contribution.
"""

import ROOT

data_filename = '/work/halld/home/viducic/data/pipkmks/data/bestX2/pipkmks_flat_bestX2_2018_spring.root'
data_treename = 'pipkmks__B4_M16'

df = ROOT.RDataFrame(data_treename, data_filename)

df = df.Define('ks_px_measured', "pip2_px_measured + pim_px_measured")
df = df.Define('ks_py_measured', "pip2_py_measured + pim_py_measured")
df = df.Define('ks_pz_measured', "pip2_pz_measured + pim_pz_measured")
df = df.Define('ks_E_measured', "pip2_E_measured + pim_E_measured")
df = df.Define('ks_m_measured', "sqrt(ks_E_measured*ks_E_measured - ks_px_measured*ks_px_measured - ks_py_measured*ks_py_measured - ks_pz_measured*ks_pz_measured)")

df = df.Define('mxpx_ppipkmks', '-p_px_measured - pip1_px_measured - km_px_measured - ks_px_measured')
df = df.Define('mxpy_ppipkmks', '-p_py_measured - pip1_py_measured - km_py_measured - ks_py_measured')
df = df.Define('mxpz_ppipkmks', 'e_beam - p_pz_measured - pip1_pz_measured - km_pz_measured - ks_pz_measured')
df = df.Define('mxe_ppipkmks', 'e_beam + 0.938272088 - p_E_measured - pip1_E_measured - km_E_measured - ks_E_measured')
df = df.Define('mx2_ppipkmks', 'mxe_ppipkmks*mxe_ppipkmks - mxpx_ppipkmks*mxpx_ppipkmks - mxpy_ppipkmks*mxpy_ppipkmks - mxpz_ppipkmks*mxpz_ppipkmks')


data_hist = df.Histo1D(('mx2_ppipkmks', 'mx2_ppipkmks', 1000, -0.05, 0.05), 'mx2_ppipkmks').GetValue()


mx2_all = ROOT.RooRealVar("mx2_all", "mx2_all", -0.03, 0.03)
dh = ROOT.RooDataHist("dh", "dh", ROOT.RooArgList(mx2_all), data_hist)

# mx2_all.setRange("signal", 0.4, 0.6)

mx2_mean_1 = ROOT.RooRealVar("mean_1", "mean_1", 0.000, -0.01, 0.01)
mx2_sigma_1 = ROOT.RooRealVar("sigma_1", "sigma_1", 0.001, 0.0001, 0.02)

# ks_mean.setConstant(1)
# ks_sigma.setConstant(1)
gaus_1 = ROOT.RooGaussian("gaus_1", "gaus_1", mx2_all, mx2_mean_1, mx2_sigma_1)

mx2_mean_2 = ROOT.RooRealVar("mean_2", "mean_2", 0.000, -0.01, 0.01)
mx2_sigma_2 = ROOT.RooRealVar("sigma_2", "sigma_2", 0.001, 0.0001, 0.02)

gaus_2 = ROOT.RooGaussian("gaus_2", "gaus_2", mx2_all, mx2_mean_2, mx2_sigma_2)

gaus_frac = ROOT.RooRealVar("gaus_frac", "gaus_frac", 0.05, 0.0, 1.0)
double_gaus = ROOT.RooAddPdf("double_gaus", "double_gaus", ROOT.RooArgList(gaus_1, gaus_2), ROOT.RooArgList(gaus_frac))

# mx_mean_3 = ROOT.RooRealVar("mean_3", "mean_3", 0.000, -0.01, 0.01)
# mx_sigma_3 = ROOT.RooRealVar("sigma_3", "sigma_3", 0.001, 0.0001, 0.02)

# gaus_3 = ROOT.RooGaussian("gaus_3", "gaus_3", mx2_all, mx_mean_3, mx_sigma_3)

# gaus_frac_2 = ROOT.RooRealVar("gaus_frac_2", "gaus_frac_2", 0.05, 0.0, 1.0)
# triple_gaus = ROOT.RooAddPdf("triple_gaus", "triple_gaus", ROOT.RooArgList(gaus_1, gaus_2, gaus_3), ROOT.RooArgList(gaus_frac, gaus_frac_2))


## FIT IN DIFFERENT RANGE ##
# gaus.fitTo(dh, ROOT.RooFit.Range("signal"))
# gaus.fitTo(dh, ROOT.RooFit.SumCoefRange("signal"))

bkg_par1 = ROOT.RooRealVar("bkg_par1", "bkg_par1", 1.0, -100., 100.)
bkg_par2 = ROOT.RooRealVar("bkg_par2", "bkg_par2", 1.0, -100., 100.)
bkg = ROOT.RooPolynomial("bkg", "bkg", mx2_all, ROOT.RooArgList(bkg_par1))

sig_frac = ROOT.RooRealVar("sig_frac", "sig_frac", 0.5, 0.0, 1.0)

composite = ROOT.RooAddPdf("composite", "composite", ROOT.RooArgList(double_gaus, bkg), ROOT.RooArgList(sig_frac))
composite.chi2FitTo(dh)
# composite.fitTo(dh)
# triple_gaus.fitTo(dh)
# composite.fitTo(dh,ROOT.RooFit.SumCoefRange("signal"))

frame = mx2_all.frame()
dh.plotOn(frame)
composite.plotOn(frame)
composite.plotOn(frame, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(ROOT.kDashed))
composite.plotOn(frame, ROOT.RooFit.Components("double_gaus"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_1"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen))
composite.plotOn(frame, ROOT.RooFit.Components("gaus_2"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kBlue))
# triple_gaus.plotOn(frame)
# triple_gaus.plotOn(frame, ROOT.RooFit.Components("gaus_1"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen))
# triple_gaus.plotOn(frame, ROOT.RooFit.Components("gaus_2"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kBlue))
# triple_gaus.plotOn(frame, ROOT.RooFit.Components("gaus_3"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))

frame.Draw()

def get_composite_width(sig1, sig2, frac):
    return sig1 * frac + sig2 * (1.0 - frac)
    
composite_width = get_composite_width(mx2_sigma_1.getVal(), mx2_sigma_2.getVal(), gaus_frac.getVal())
print(f'Width of first gaussian is: {mx2_sigma_1.getVal()}')
print(f'Width of second gaussian is: {mx2_sigma_2.getVal()}')
print(f'Fraction of first gaussian is: {gaus_frac.getVal()}')
print(f'Width of double gaussian is: {composite_width}')
input("Press enter to exit")