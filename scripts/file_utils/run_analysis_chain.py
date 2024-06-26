# script to execute kkpi data analysis over all 3 run periods

import os
from my_library.flat_analysis import run_analysis
import time

#TODO:  STATUS BAR OR TIMER OR BOTH
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


if __name__ == '__main__':

    overall_start = time.time()
    channels = ['pipkmks', 'pimkpks']
    run_periods = ['spring', 'fall', '2017']
    # recon_data_types = ['data', 'signal', 'phasespace']
    recon_data_types = ['data', 'signal']
    # recon_data_types = ['data']
    # recon_data_types = ['signal', 'phasespace']
    thrown_data_types = ['signal']

    for channel in channels:
        for data_type in recon_data_types:
            for run_period in run_periods:
                print(f'running analysis for {channel} {data_type} {run_period}')
                start = time.time()
                run_analysis(channel, run_period, data_type)
                end = time.time()
                prGreen(f'Analysis for {channel} {data_type} {run_period} took {end-start} seconds')
                if data_type in thrown_data_types:
                    print(f'running thrown analysis for {channel} {data_type} {run_period}')
                    thrown_start = time.time()
                    run_analysis(channel, run_period, data_type, thrown=True)
                    thrown_end = time.time()
                    prGreen(f'Thrown analysis for {channel} {data_type} {run_period} took {thrown_end-thrown_start} seconds')
                print("", flush=True)

    overall_end = time.time()
    prGreen(f'Overall analysis took {(overall_end-overall_start)/60} minutes'.upper())
    print("")

