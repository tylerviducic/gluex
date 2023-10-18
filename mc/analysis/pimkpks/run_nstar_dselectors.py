"""
runs dselector for pi-K+Ks over the Nstar mc files
"""

import os

common_path = '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/'
nstar_dirs = [
    'pimkpks_nstar_1440_a0_3415',
    'pimkpks_nstar_1520_a0_3417',
    'pimkpks_nstar_1535_a0_3418',
    'pimkpks_nstar_1650_a2_3419',
    'pimkpks_nstar_1675_a3_3420',
    # 'pimkpks_nstar_1680_a2_3421',
    'pimkpks_nstar_1700_a2_3422',
    'pimkpks_nstar_1710_a2_3423',
    'pimkpks_nstar_1720_a2_3424'
]

ds_output_file = "/work/halld/home/viducic/data/pimkpks/mc/signal/pimkpks_flat_bestX2.root" 
nstar_output_dir = "/work/halld/home/viducic/data/pimkpks/mc/nstar/"

for nstar_dir in nstar_dirs:
    path_to_files = f'{common_path}{nstar_dir}/root/trees/tree_pimkpks__ks_pippim__B4_M16_genr8/'
    run_command = f'root -l -b -q \'RunNstarMC_KsKpPim.C("{path_to_files}*.root")\''
    print(run_command)
    os.system(run_command)
    mv_command = f'mv {ds_output_file} {nstar_output_dir}/nstar_{nstar_dir.split("_")[1]}_flat_bestX2.root'
    print(mv_command)
    os.system(mv_command)
