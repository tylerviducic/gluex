"""this script will be used to create workflows and config files such that 
jobs submitted are for a run number instead of just a single file. 30000 jobs
is far too many."""

import os

def create_config(run_number, out_dir):
    return 