# file to keep mxp data on volatile 

import ROOT
import os

# get list of files in directory 
topdirs = [
    '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_mpx/combined_runs',
    '/lustre19/expphy/volatile/halld/home/viducic/mxp_study/pd_ks_constrained/combined_runs',
    '/lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/combined_runs',
    '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_pd/combined_runs'
]

files =[]

#loop over all the files in the top directory and add them to a list
for topdir in topdirs:
    for file in os.listdir(topdir):
        print(file)
        if file.endswith('.root'):
            files.append(topdir + "/" + file)


# open and close each file without performing any other operations
for file in files:
    print('Opening file: ' + file)
    f = ROOT.TFile.Open(file)
    f.Close()

print('Done!')