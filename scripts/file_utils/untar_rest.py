# file to untar rest files on /volatile

import os
import tarfile

# get list of files in the directory
topdir = '/lustre19/expphy/volatile/halld/home/viducic/REST/pimkpks_signal_2018_fall'
files = os.listdir(topdir)

# loop over files
for f in files:
    # check if file is a tar file
    if f.endswith('.tar'):
    # Create the full file path
        file_path = os.path.join(topdir, f)

        # Extract the .tar file
        with tarfile.open(file_path, 'r') as tar:
            tar.extractall(topdir)

        print(f"Extracted {f} successfully.")
