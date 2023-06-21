# file to keep mxp data on volatile 

import ROOT
import os

# get list of files in directory 
topdirs = [
    '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_mpx/combined_runs'
    '/lustre19/expphy/volatile/halld/home/viducic/mxp_study/pd_ks_constrained/combined_runs'
    '/lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/combined_runs'
    '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_pd/combined_runs'
]

for topdir in topdirs:
    files = os.listdir(topdir)

    # open and close each file without performing any other operations
    for file in files:
        f = ROOT.TFile.Open(topdir + '/' + file)
        f.Close()

print('Done!')