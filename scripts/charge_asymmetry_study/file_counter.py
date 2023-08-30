import glob

pipkmks_recon = {
    'spring': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_s18_100m_v16_rt_t29_3237/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root',
    'fall': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3238/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root',
    '2017': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3239/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root'
}

pipkmks_thrown = {
    'spring': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_s18_100m_v16_rt_t29_3237/root/thrown/*.root',
    'fall': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3238/root/thrown/*.root',
    '2017': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3239/root/thrown/*.root'
}

pimkpks_recon = {
    'spring': '/lustre19/expphy/volatile/halld/home/viducic/pimkpks_mc/signal/combined_runs/tree_pimkpks__ks_pippim__B4_M16_04*.root',
    'fall': '/lustre19/expphy/volatile/halld/home/viducic/pimkpks_mc/signal/combined_runs/tree_pimkpks__ks_pippim__B4_M16_05*.root',
    '2017': '/lustre19/expphy/volatile/halld/home/viducic/pimkpks_mc/signal/combined_runs/tree_pimkpks__ks_pippim__B4_M16_03*.root'
}

pimkpks_thrown = {
    'spring': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_s18_100m_v50_rt_t29_3249/root/thrown/*.root',
    'fall': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_f18_100m_v50_rt_t29_3250/root/thrown/*.root',
    '2017': '/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_s17_100m_v50_rt_t29_3248/root/thrown/*.root'
}

for run in ['spring', 'fall', '2017']:
    print(run)
    print('pipkmks_recon: ', len(glob.glob(pipkmks_recon[run])))
    print('pipkmks_thrown: ', len(glob.glob(pipkmks_thrown[run])))
    print('pimkpks_recon: ', len(glob.glob(pimkpks_recon[run])))
    print('pimkpks_thrown: ', len(glob.glob(pimkpks_thrown[run])))
    print()