# file to keep mxp data on volatile 

import ROOT
import os

# get list of files in directory 
base_topdir = '/volatile/halld/home/viducic/'


# loop over the nested subdirectiories in the topdir and add the files at the bottom to a list
for subdir, dirs, files in os.walk(base_topdir):
    if 'PROOF' in subdir:
        continue
    # print('Adding files from: ' + subdir)
    for file in files:
        if file.endswith('.root'):
            print('Opening file: ' + subdir + '/' + file)
            try:
                f = ROOT.TFile.Open(subdir + '/' + file)
                f.Close()
            except:
                print('Error opening file: ' + subdir + '/' + file)
                continue


# open and close each file without performing any other operations
# for file in files:
#     print('Opening file: ' + file)
#     f = ROOT.TFile.Open(file)
#     f.Close()

print('Done!')