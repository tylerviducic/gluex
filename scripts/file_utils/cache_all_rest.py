"""
Script used to cache all the MC files from tape
"""

import os
import glob

topdir = '/mss/halld/gluex_simulations/REQUESTED_MC/'
# channels = ['pipkmks', 'pimkpks']

project_ids = []
for i in range(3245, 3254):
    project_ids.append(i)
for i in range(3237, 3240):
    project_ids.append(i)

paths = [glob.glob(f'{topdir}/*{proj}')[0] for proj in project_ids]
    

for path in paths:
    print("+"*50)
    command = 'jcache get '
    for dir_path, dir_name, filename in os.walk(path):
        for name in dir_name:
            if name.endswith('hddm'):
                command += f'{dir_path}/{name}/*.hddm.tar '
    command += '-e viducic@jlab.org'
    print(command)
    os.system(command)