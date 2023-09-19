"""
runs dselector for pi-K+Ks over the Nstar mc files
"""

import os


common_path = '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/'
nstar_dirs = [
    'nstar_1440_pimkpks_3393',
    'nstar_1520_pimkpks_3394'
    #'nstar_1535_pimkpks_3395' ADD THE COMMA TO PROCEDING LINE WHEN UNCOMMENTING
]

ds_output_file = "/work/halld/home/viducic/data/pimkpks/mc/signal/imkpks_flat_bestX2.root" 
nstar_dir = "/work/halld/home/viducic/data/pimkpks/mc/nstar/"

for nstar_dir in nstar_dirs:
    path_to_files = f'{common_path}{nstar_dir}/root/trees/tree_pimkpks__ks_pippim__B4_M16_genr8/'
    run_command = f'root -l -b -q \'RunNstarMC_KsKpPim.C("{path_to_files}*.root")\''
    print(run_command)
    mv_command = f'mv {ds_output_file} {nstar_dir}/nstar_{nstar_dir.split("_")[1]}_flat_bestX2.root'
    print(mv_command)