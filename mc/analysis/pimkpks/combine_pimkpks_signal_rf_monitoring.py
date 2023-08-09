# combine files from bggen

import os
import subprocess
import glob

print("Combining files for pimkpks mc monitoring hists..")

subdirs = []
topdir = '/volatile/halld/home/viducic/pimkpks_mc/signal/hists/'
for root, dirs, files in os.walk(topdir):
    for subdir in dirs:
        subdirs.append(subdir)

command = 'hadd /lustre19/expphy/volatile/halld/home/viducic/pimkpks_mc/signal/combined_hists/hd_root_{}.root {}/{}/*'

for subdir in subdirs:
    # print(command.format(subdir, subdir))
    subprocess.run(command.format(subdir, topdir, subdir), shell=True)
