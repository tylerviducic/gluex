"""
This script:
1.) removes old workflow and makes new one
2.) loops over the all run periods for both charge conjugations and adds them to a workflow
3.) runs the workflow 
"""

import os

path_to_configs = '/work/halld/home/viducic/mc/analysis/dselector_jobs/f1_flat/config_files'

file_suffix_dict = {
    'spring': 'spring_2018',
    'fall': 'fall_2018',
    '2017': '2017',
}

run_num_dict = {
    'spring': (40856, 42559),
    'fall': (50685, 51768),
    '2017': (30274, 31057),
}


channels = ['pipkmks', 'pimkpks']

# 1.) remove old workflow and make new one
cancel_command = 'swif2 cancel -workflow f1_new_mc -delete'
create_command = 'swif2 create -workflow f1_new_mc'

print('Removing old workflow and making new one')
print(cancel_command)
os.system(cancel_command)
print(create_command)
os.system(create_command)

# 2.) loop over all run periods for both charge conjugations and add them to a workflow
for channel in channels:
    for run in run_num_dict:
        add_job_command = f'./launch.py {path_to_configs}/{channel}/jobs_root_analysis_{file_suffix_dict[run]}.config {run_num_dict[run][0]} {run_num_dict[run][1]}'
        print(add_job_command)
        os.system(add_job_command)

# 3.) run the workflow
run_workflow_command = 'swif2 run -workflow f1_new_mc'
print(run_workflow_command)
os.system(run_workflow_command)