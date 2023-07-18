# script to execute pipkmks data analysis over all 3 run periods

import os

def run_recon_analysis(channel: str, run_period: str, data_type: str):
    analysis_file = '/work/halld/home/viducic/analysis/f1_flat_bx2_analysis.py'
    command = f'python3 {analysis_file} {channel} {run_period} {data_type}'
    print(f'Running over {data_type} for channel {channel} and run period {run_period}')
    print(f'Executing: {command}')
    os.system(command)

if __name__ == '__main__':
    channels = ['pipkmks', 'pimkpks']
    run_periods = ['spring', 'fall', '2017']
    recon_data_types = ['data', 'signal', 'phasespace']

    for channel in channels:
        for data_type in recon_data_types:
            for run_period in run_periods:
                run_recon_analysis(channel, run_period, data_type)
