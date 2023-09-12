"""
This script runs the dselectors for pi-K+ and pi+K- for recon signal and phasespace MC 
"""

import os

files = [
    '/work/halld/home/viducic/mc/analysis/pimkpks/run_dselector_all_gluex1_phasespace.py',
    '/work/halld/home/viducic/mc/analysis/pimkpks/run_dselector_all_gluex1_signal.py',
    '/work/halld/home/viducic/mc/analysis/pipkmks/run_dselector_all_gluex1_phasespace.py',
    '/work/halld/home/viducic/mc/analysis/pipkmks/run_dselector_all_gluex1_signal.py'
]

for file in files:
    command = f'python3 {file}'
    print(command)
    os.system(command)



