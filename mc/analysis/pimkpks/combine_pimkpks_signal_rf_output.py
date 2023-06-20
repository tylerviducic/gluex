# combine files from bggen

import os
import subprocess
import glob

print("Combining files for mxp reaction_filter..")

subdirs = []
topdir = '/lustre19/expphy/volatile/halld/home/viducic/pipkmks_pd/tree_pipkmks__ks_pippim__B4_M16'
for root, dirs, files in os.walk(topdir):
    for subdir in dirs:
        subdirs.append(subdir)

command = 'hadd /lustre19/expphy/volatile/halld/home/viducic/pipkmks_pd/combined_runs/tree_pipkmks__ks_pippim__B4_M16_{}.root {}/{}/*'

for subdir in subdirs:
    # print(command.format(subdir, subdir))
    subprocess.run(command.format(subdir, topdir, subdir), shell=True)
