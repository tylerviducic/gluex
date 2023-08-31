"""
This script:
1.) removes old workflow and makes new one
2.) loops over the all run periods for both charge conjugations and adds them to a workflow
3.) runs the workflow 
"""

import os
from venv import create

root_path = '/work/halld/home/viducic/mc/analysis/{}/analysis_launch'
path_to_configs = root_path + '/config_files'
launch_script = root_path + '/.launch_one_job_per_run.py'

file_suffix_dict = {
    'spring': 'spring_2018',
    'fall': 'fall_2018',
    '2017': '2017',
    '2019': '2019'
}

run_num_dict = {
    'spring': (40856, 42559),
    'fall': (50685, 51768),
    '2017': (30274, 31057),
    '2019': (71728, 72435)
}

channels = ['pipkmks', 'pimkpks']



for channel in channels:
# 1.) remove old workflow and make new one
    workflow = f'{channel}_ps_mc'
    cancel_command = f'swif2 cancel -workflow {workflow} -delete'
    print('Removing old workflow and making new one')
    print(cancel_command)
    os.system(cancel_command)
    create_command = f'swif2 create -workflow {workflow}'
    print(create_command)
    os.system(create_command)
# 2.) loop over all run periods for both charge conjugations and add them to a workflow
    for run in run_num_dict:
        add_job_command = f'{launch_script} + {path_to_configs.format(channel)}/jobs_correct_reactionfilter_{file_suffix_dict[run]}_ps.config {run_num_dict[run][0]} {run_num_dict[run][1]}'
        print(add_job_command)
        os.system(add_job_command)

# 3.) run the workflow
    run_workflow_command = f'swif2 run -workflow {workflow}'
    print(run_workflow_command)
    os.system(run_workflow_command)