# script to execute pipkmks data analysis over all 3 run periods

import os
import time

#TODO STATUS BAR OR TIMER OR BOTH
#TODO options for smaller-scale running (maybe pass lists as arguments?)

def run_recon_analysis(channel: str, run_period: str, data_type: str):
    analysis_file = '/work/halld/home/viducic/analysis/f1_flat_bx2_analysis.py'
    command = f'python3 {analysis_file} {channel} {run_period} {data_type}'
    print(f'Running over {data_type} for channel {channel} and run period {run_period}')
    print(f'Executing: {command}')
    os.system(command)

def run_thrown_analysis(channel: str, run_period: str, data_type: str):
    analysis_file = '/work/halld/home/viducic/mc/analysis/f1_flat_thrown_analysis.py'
    command = f'python3 {analysis_file} {channel} {run_period} {data_type}'
    print(f'Running over thrown {data_type} for channel {channel} and run period {run_period}')
    print(f'Executing: {command}')
    os.system(command)

if __name__ == '__main__':
    total_start = time.time()
    channels = ['pipkmks', 'pimkpks']
    run_periods = ['spring', 'fall', '2017']
    recon_data_types = ['data', 'signal', 'phasespace']
    thrown_data_types = ['signal', 'phasespace']

    for channel in channels:
        for data_type in recon_data_types:
            for run_period in run_periods:
                print(f'Running over {data_type} for channel {channel} and run period {run_period}')
                start = time.time()
                run_recon_analysis(channel, run_period, data_type)
                end = time.time()
                print(f'Analysis of {data_type} for {channel} {run_period} completed in {end-start} seconds')
        for data_type in thrown_data_types:
            for run_period in run_periods:
                print(f'Running over thrown {data_type} for channel {channel} and run period {run_period}')
                start = time.time()
                run_thrown_analysis(channel, run_period, data_type)
                end = time.time()
                print(f'Analysis of thrown {data_type} for {channel} {run_period} completed in {end-start} seconds')
    total_end = time.time()
    print(f'Analysis chain completed in {total_end-total_start} seconds')
