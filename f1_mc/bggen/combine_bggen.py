# combine files from bggen

import os
import subprocess
import glob

print("Combining files from bggen...")

subdirs = []
bggen_topdir = '/volatile/halld/home/viducic/bggen_batch_02/tree_pipkmks__ks_pippim__B4_M16/'
for root, dirs, files in os.walk(bggen_topdir):
    for subdir in dirs:
        subdirs.append(subdir)

command = 'hadd /volatile/halld/home/viducic/combined_bggen/batch_04/bggen_combined_{}.root /volatile/halld/home/viducic/bggen_batch_04/tree_pipkmks__ks_pippim__B4_M16/{}/*'

for subdir in subdirs:
    #print(command.format(subdir, subdir))
    subprocess.run(command.format(subdir, subdir), shell=True)
