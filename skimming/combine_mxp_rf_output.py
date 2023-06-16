# combine files from bggen

import os
import subprocess
import glob

print("Combining files for mxp reaction_filter..")

subdirs = []
topdir = '/lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/tree_pipkmksmissprot__ks_pippim__B4'
for root, dirs, files in os.walk(topdir):
    for subdir in dirs:
        subdirs.append(subdir)

command = 'hadd /lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/combined_runs/tree_pipkmksmissprot__ks_pippim__B4_{}.root /lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/tree_pipkmksmissprot__ks_pippim__B4/{}/*'

for subdir in subdirs:
    # print(command.format(subdir, subdir))
    subprocess.run(command.format(subdir, subdir), shell=True)
