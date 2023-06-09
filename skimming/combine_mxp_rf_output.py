# combine files from bggen

import os
import subprocess
import glob

print("Combining files for mxp reaction_filter..")

subdirs = []
topdir = '/volatile/halld/home/viducic/pipkmks_mpx/tree_pipkmksmissprot__ks_pippim__B4_M16/'
for root, dirs, files in os.walk(topdir):
    for subdir in dirs:
        subdirs.append(subdir)

command = 'hadd /lustre19/expphy/volatile/halld/home/viducic/pipkmks_mpx/combined_runs/tree_pipkmksmissprot__ks_pippim__B4_M16_{}.root /lustre19/expphy/volatile/halld/home/viducic/pipkmks_mpx/tree_pipkmksmissprot__ks_pippim__B4_M16/{}/*'

for subdir in subdirs:
    # print(command.format(subdir, subdir))
    subprocess.run(command.format(subdir, subdir), shell=True)
