"""
runs dselector for pi-K+Ks over the Nstar mc files
"""

import os

common_path = '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/'
f1_dirs = [
    'pimkpks_f1_1420_kkstar_minus_3425',
    'pimkpks_f1_1420_kkstar_zero_3427',
    'pipkmks_f1_1420_kkstar_zero_3428',
    'pipkmks_f1_1420_kkstar_plus_3429',
]

ds_output_file = "/work/halld/home/viducic/data/{0}/mc/signal/{0}_flat_bestX2.root" 
f1_output_dir = "/work/halld/home/viducic/data/{}/mc/f1_1420/"

for f1_dir in f1_dirs:
    channel = f1_dir.split("_")[0]
    charge = f1_dir.split("_")[4]
    if channel == "pimkpks":
        run_file = '/work/halld/home/viducic/mc/analysis/pimkpks/RunF1MC_KsKpPim_CorrectRF.C'
    elif channel == "pipkmks":
        run_file = '/work/halld/home/viducic/mc/analysis/pipkmks/RunF1MC_KsKmPip.C'
    else:
        print("Error: channel not recognized")
        exit(1) 

    path_to_files = f'{common_path}{f1_dir}/root/trees/tree_{channel}__ks_pippim__B4_M16_genr8/'
    run_command = f'root -l -b -q \'{run_file}("{path_to_files}*.root")\''
    print(run_command)
    os.system(run_command)
    mv_command = f'mv {ds_output_file.format(channel)} {f1_output_dir.format(channel)}/f1_1420_kstar_{charge}_flat_bestX2.root'
    print(mv_command)
    os.system(mv_command)
