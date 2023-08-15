# file to untar rest files on /volatile

import os
import tarfile

# get list of files in the directory
topdir = '/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3239/hddm/'
target_dir = '/lustre19/expphy/volatile/halld/home/viducic/REST/pipkmks_signal_2017'
files = os.listdir(topdir)

# loop over files
for f in files:
    # check if file is a tar file
    if f.endswith('.tar'):
    # Create the full file path
        file_path = os.path.join(topdir, f)

        # Extract the .tar file
        with tarfile.open(file_path, 'r') as tar:
            tar.extractall(target_dir)

        print(f"Extracted {f} successfully.")
