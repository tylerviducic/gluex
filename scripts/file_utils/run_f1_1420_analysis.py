from my_library.flat_analysis import run_analysis

# TODO: re-run with updated output names 
charge_dict = {
    'pipkmks': ('plus', 'zero'),
    'pimkpks': ('minus', 'zero')
}

for channel in ['pipkmks', 'pimkpks']:
    for charge in charge_dict[channel]:
        print(f'running analysis for {channel} {charge}')
        run_analysis(channel, 'spring', 'f1_1420', kstar_charge=charge)


