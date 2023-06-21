# file to keep mxp data on volatile 

import ROOT
import os

# get list of files in directory 
topdir = '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_mpx/combined_runs'
files = os.listdir(topdir)

# open and close each file without performing any other operations
for file in files:
    f = ROOT.TFile.Open(topdir + '/' + file)
    f.Close()

print('Done!')