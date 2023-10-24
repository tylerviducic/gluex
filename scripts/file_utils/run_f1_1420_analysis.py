from my_library.flat_analysis import run_analysis

# files = [
#     '/work/halld/home/viducic/data/pimkpks/mc/f1_1420/f1_1420_kstar_minus_flat_bestX2.root',
#     '/work/halld/home/viducic/data/pimkpks/mc/f1_1420/f1_1420_kstar_zero_flat_bestX2.root',
#     '/work/halld/home/viducic/data/pipkmks/mc/f1_1420/f1_1420_kstar_plus_flat_bestX2.root',
#     '/work/halld/home/viducic/data/pipkmks/mc/f1_1420/f1_1420_kstar_zero_flat_bestX2.root'
# ]

file_path = '/work/halld/home/viducic/data/{}/mc/f1_1420/f1_1420_kstar_{}_flat_bestX2.root'

charge_dict = {
    'pipkmks': ('plus', 'zero'),
    'pimkpks': ('minus', 'zero')
}

for channel in ['pipkmks', 'pimkpks']:
    for charge in charge_dict[channel]:
        print(f'running analysis for {channel} {charge}')
        run_analysis(channel, 'spring', 'f1_1420', kstar_charge=charge)


